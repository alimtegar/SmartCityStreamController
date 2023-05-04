import os
import time
import json
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse

from app.camera.repository import CameraRepository
from .schemas import CreateCamera, EditCamera
from .dependencies import get_camera_repository

router = APIRouter(prefix="/cameras")

@router.post("/")
def add_camera(camera: CreateCamera, camera_repository: CameraRepository = Depends(get_camera_repository)):
    new_camera = camera_repository.add(camera)
    return JSONResponse(status_code=201, content={
        "data": new_camera.dict(),
    })


@router.post("/video")
def add_camera_with_uploaded_video(
    file: UploadFile = File(...), 
    # name: str = Form(...),
    res: Optional[int] = Form(720),
    loop: Optional[bool] = Form(True),
    counter_line_str: Optional[str] = Form('[[0,300], [720, 300]]'),
    camera_repository: CameraRepository = Depends(get_camera_repository)
):
    try:
        contents = file.file.read()
        
        file_name, file_ext = os.path.splitext(file.filename)
        file_name += f'-{int(time.time())}'
        file_path = f'./uploads/videos/{file_name}{file_ext}'
        
        with open(file_path, 'wb') as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        file.file.close()
    
    camera = CreateCamera(
        # name=name,
        source=file_path, 
        res=res,
        loop=loop,
        counter_line=json.loads(counter_line_str),
    )
    new_camera = camera_repository.add(camera)
    return JSONResponse(status_code=201, content={
        "data": new_camera.dict(),
    })


@router.get("/")
def get_cameras(camera_repository: CameraRepository = Depends(get_camera_repository)):
    cameras = camera_repository.get_all()
    return {
        "data": [camera.dict() for camera in cameras]
    }


@router.get("/{id}")
def get_camera(id: int, camera_repository: CameraRepository = Depends(get_camera_repository)):
    camera = camera_repository.find(id)
    return {
        "data": camera.dict(),
    }


@router.put("/{id}")
def edit_camera(id: int, camera: EditCamera, camera_repository: CameraRepository = Depends(get_camera_repository)):
    camera = camera_repository.edit(id, camera)
    return {"data": camera.dict()}


@router.delete("/{id}")
def delete_camera(id: int, camera_repository: CameraRepository = Depends(get_camera_repository)):
    camera_repository.delete(id)
    return JSONResponse(status_code=204)
