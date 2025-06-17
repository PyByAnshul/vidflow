import os
from datetime import datetime
from pymongo import MongoClient
from fastapi import UploadFile
from bson import ObjectId

client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017/"))
db = client.vidflow
videos_collection = db.videos

async def save_video(file: UploadFile):
    video_id = str(datetime.now().timestamp())
    file_path = os.path.join("videos", f"{video_id}_{file.filename}")
    with open(file_path, "wb") as f:
        f.write(await file.read())
    videos_collection.insert_one({
        "video_id": video_id,
        "filename": file.filename,
        "upload_time": datetime.now(),
        "status": "pending",
        "video_url": f"/videos/{video_id}_{file.filename}"
    })
    return video_id

async def get_video_status(video_id: str):
    video = videos_collection.find_one({"video_id": video_id})
    return video["status"] if video else None

async def get_video_metadata(video_id: str):
    video = videos_collection.find_one({"video_id": video_id})
    if video:
        video['_id'] = str(video['_id'])  
    return video

async def get_all_videos():
    videos = list(videos_collection.find())
    for video in videos:
        video['_id'] = str(video['_id'])  
        if 'video_url' not in video:
            video['video_url'] = f"/videos/{video['video_id']}_{video['filename']}"
    return videos 