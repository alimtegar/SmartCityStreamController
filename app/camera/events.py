from app.events import AppEvent, EventsEmitter
from app.stream.dependencies import add_stream, remove_stream, reset_stream
from .model import Camera


class CameraEventPayload(AppEvent):
    def __init__(self, camera: Camera) -> None:
        self.camera = camera

class CameraCreated(CameraEventPayload):
    event = "camera:created"

class CameraUpdated(CameraEventPayload):
    event = "camera:updated"

class CameraDeleted(CameraEventPayload):
    event = "camera:deleted"


def setup_event_listeners(events_emitter: EventsEmitter):
    def on_camera_created(event: CameraCreated):
        # stream_name = f"camera-{event.camera.id}"
        stream_name = event.camera.id
        add_stream(
            name=stream_name,
            source=event.camera.source,
            res=event.camera.res,
            loop=event.camera.loop,
            counter_line=event.camera.counter_line,
        )


    def on_camera_deleted(event: CameraDeleted):
        # stream_name = f"camera-{event.camera.id}"
        stream_name = event.camera.id
        remove_stream(name=stream_name)


    def on_camera_updated(event: CameraUpdated):
        # stream_name = f"camera-{event.camera.id}"
        stream_name = event.camera.id
        reset_stream(
            name=stream_name,
            source=event.camera.source,
            res=event.camera.res,
            loop=event.camera.loop,
            counter_line=event.camera.counter_line,
        )


    events_emitter.on(CameraCreated.event, on_camera_created)
    events_emitter.on(CameraDeleted.event, on_camera_deleted)
    events_emitter.on(CameraUpdated.event, on_camera_updated)
