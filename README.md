# VidFlow

A Python backend application for video processing using FastAPI, MongoDB, Celery, and FFmpeg.

## Setup


 docker-compose up --build

## API Usage

### Upload Video
- **POST /api/upload-video/**
  - Upload a video file using form data.

### Check Video Status
- **GET /api/video-status/{video_id}**
  - Get the current status of a video processing job.

### Get Video Metadata
- **GET /api/video-metadata/{video_id}**
  - Retrieve metadata including duration and thumbnail URL.

