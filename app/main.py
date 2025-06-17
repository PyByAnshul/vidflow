from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routes import video_routes

app = FastAPI(title="VidFlow API")

app.include_router(video_routes.router, prefix="/api")

@app.get("/")
async def read_root():
    return FileResponse("app/templates/index.html")

@app.get("/thumbnails/{filename}")
async def get_thumbnail(filename: str):
    return FileResponse(f"thumbnails/{filename}")

@app.get("/videos/{filename}")
async def get_video(filename: str):
    return FileResponse(f"videos/{filename}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 