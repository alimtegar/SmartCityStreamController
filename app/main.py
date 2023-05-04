from fastapi import FastAPI

import app.stream.module as stream
import app.camera.module as camera
import app.vehicle.module as vehicle


app = FastAPI()

stream.register_module(app)
camera.register_module(app)
vehicle.register_module(app)