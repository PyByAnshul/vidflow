import os
import subprocess
from celery import Celery
from app.services.video_service import videos_collection

celery_app = Celery('vidflow', broker=os.getenv("REDIS_URI", "redis://localhost:6379/0"))

@celery_app.task
def process_video(video_id):
    video = videos_collection.find_one({"video_id": video_id})
    if not video:
        return

    file_path = os.path.join("videos", f"{video_id}_{video['filename']}")
    
    duration_cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    
    try:
        duration_output = subprocess.check_output(duration_cmd).decode().strip()
        print(f"Duration output: {duration_output}")
        
        try:
            duration = float(duration_output)
        except ValueError:
            print(f"Invalid duration output: {duration_output}")
            return

        
        thumbnail_time = duration * 0.1
        thumbnail_path = os.path.join("thumbnails", f"{video_id}.jpg")
        
        
        thumbnail_cmd = [
            "ffmpeg",
            "-y",  
            "-ss", str(thumbnail_time),
            "-i", file_path,
            "-vframes", "1",
            "-q:v", "2",  
            "-vf", "scale=320:-1",  
            thumbnail_path
        ]
        
        subprocess.run(thumbnail_cmd, check=True)

        
        videos_collection.update_one(
            {"video_id": video_id},
            {
                "$set": {
                    "duration": duration,
                    "thumbnail_url": f"http://localhost:8000/thumbnails/{video_id}.jpg",
                    "status": "done"
                }
            }
        )
        
    except subprocess.CalledProcessError as e:
        print(f"Error processing video: {str(e)}")
        videos_collection.update_one(
            {"video_id": video_id},
            {"$set": {"status": "error"}}
        )
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        videos_collection.update_one(
            {"video_id": video_id},
            {"$set": {"status": "error"}}
        ) 