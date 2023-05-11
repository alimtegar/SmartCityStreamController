# Smart City

<!-- Camera Routes (`/camera`) are to manage camera data, -->
<!-- while Streaming -->

## Requirements
- Docker

## How to Run
1. To run the application, simply enter the following command in your terminal:
```
docker-compose up
```
2. Open API Docs (Swagger) by visiting to http://localhost:3000/docs

## Demo
1. First, open the API Docs (Swagger) by visiting to http://localhost:3000/docs
2. Next, go to section **/camera/video (POST)** to upload the video that you want to stream and specify the parameters for the streamed video. You will need to include the following parameters in your request:

- **video**: the video file you want to stream
- **res**: the desired resolution for the video
- **loop**: whether or not the video should loop
- **counter_line_str**: an array of coordinate pairs to specify a counter line in the video

If the request is successful, the response will be as follows:

```
{
  "data": {
    "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "source": "./uploads/videos/video-1234567890.mp4",
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
3. Finally, use the **id** value to stream the video by visiting  http://localhost:3000/streams/{id}

<!-- ### Docker
1. Build image
```
docker build -t streaming .
```

1. Start container
```
docker run -p 3000:3000 streaming
``` -->
