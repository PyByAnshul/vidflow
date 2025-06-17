from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.video_service import save_video, get_video_status, get_video_metadata, get_all_videos
from app.tasks.video_tasks import process_video

router = APIRouter()

@router.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    video_id = await save_video(file)
    process_video.delay(video_id)
    return {"video_id": video_id}

@router.get("/video-status/{video_id}")
async def video_status(video_id: str):
    status = await get_video_status(video_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return {"status": status}

@router.get("/video-metadata/{video_id}")
async def video_metadata(video_id: str):
    metadata = await get_video_metadata(video_id)
    if metadata is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return metadata

@router.get("/videos")
async def list_videos():
    videos = await get_all_videos()
    return videos 