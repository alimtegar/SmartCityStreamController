import time
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from starlette.background import BackgroundTask


from .streaming import StreamingThread
from .dependencies import streamings


router = APIRouter(prefix='/streams')

# @router.get('/')
# def show(fps: int = 15):
#     return ", ".join(list(streamings.keys()))


@router.get('/{camera_id}/stream')
def get_stream(camera_id: str, fps: int = 15):
    stream: StreamingThread = streamings.get(camera_id)
    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")

    return StreamingResponse(
        content=stream_generator(stream, fps),
        media_type='multipart/x-mixed-replace; boundary=frame',
        background=BackgroundTask(stream.stop_frame)
    )

@router.get('/{camera_id}')
def show_stream(camera_id: str, fps: int = 15):
    html = f"""
    <!DOCTYPE html>
    <html>
        <head><title>Streaming</title></head>
        <body>
            <img width="1024" src="/streams/{camera_id}/stream?fps={fps}" />
        </body>
    </html>
    """
    return HTMLResponse(content=html, status_code=200)


def stream_generator(stream: StreamingThread, fps: int):
    fps_sleep = 1/fps
    for frame in stream.stream_frame():
            time.sleep(fps_sleep)
            yield (b'--frame\r\n'
                   b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')
