# Live Streaming Camera API

Camera Routes (`/camera`) are to manage camera data,
while Streaming


## How to run
1. Install dependency
```
pip install -r requirements.txt
```

2. Start Server
```
uvicorn app.main:app
```

3. Open API Docs (Swaggger) on http://localhost:3000/docs

## Demo
1. First, open the API Docs (Swaggger) by visiting to http://localhost:3000/docs
2. Next, go to section **/camera/video (POST)** to upload the video that you want to stream and specify the parameters for the streamed video. You will need to include the following parameters in your request:

- **video**: the video file you want to stream
- **name**: a name for the stream
- **res**: the desired resolution for the video
- **loop**: whether or not the video should loop
- **counter_line_str**: an array of coordinate pairs to specify a counter line in the video

If the request is successful, the response will be as follows:

```
{
  "data": {
    "id": 1,
    "name": "demo",
    "source": "./uploads/videos/demo-1234567890.mp4",
    "res": 720,
    "loop": true,
    "counter_line": [
      [
        100,
        300
      ],
      [
        700,
        300
      ]
    ]
  }
}
```
3. Finally, use the **id** value (**1** in this example) to stream the video by visiting  http://localhost:3000/streams/camera-{id}

<!-- ### Docker
1. Build image
```
docker build -t streaming .
```

1. Start container
```
docker run -p 3000:3000 streaming
``` -->
