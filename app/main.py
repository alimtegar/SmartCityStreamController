from fastapi import FastAPI

import app.streams.module as streams
import app.camera.module as camera
import app.vehicle.module as vehicle


app = FastAPI()

streams.register_module(app)
camera.register_module(app)
vehicle.register_module(app)