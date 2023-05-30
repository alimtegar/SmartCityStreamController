# Smart City

## Requirements
- [Docker](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/downloads) (Optional, only if you want to clone this repository)

## How to Set Up

1. Download this repository or clone it with Git:
```
git clone https://github.com/widya-robotics-ai-intern-2023/smart_city.git
```
2. Open the repository folder.
3. Download the model weights [here](https://drive.google.com/drive/folders/1gVZqc17D76PemjNEqF6qz4VILmhFCFRJ?usp=share_link) and move them to the **./model_weights/** folder.

## How to Stream Video (with Webcam)
<details>
<summary>Linux</summary>

### Linux
1. First, open the terminal and change the directory to the application folder. Then, run the application by entering following command:
```
docker-compose up
```
2. Open the API Docs (Swagger UI) by visiting to http://localhost:8000/docs.
3. To add the webcam for video streaming, go to section **/camera (POST)** and send a request with the following parameters:
- **source**: the source of the webcam
- **res**: the desired resolution for the video
- **counter_line**: an array of coordinate pairs to specify a counter line in the video

Upon a successful request, the response will be as follows:

```
{
  "data": {
    "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "source": 0,
    "res": 1280,
    "loop": true,
    "counter_line": [
      [
        100,
        720
      ],
      [
        1280,
        400
      ]
    ]
  }
}
```
4. To stream the video, use the **id** value returned in the successful response from step 3 as part of the URL: http://localhost:8000/streams/{id}.

</details>
<details>
<summary>Windows and macOS</summary>

### Windows and macOS

1. First, start your MySQL server.
2. Create the **.env** file by copying the **.env.example** file and renaming it to **.env**. Provide the required information about your MySQL server in the **.env** file. This step will enable the application to establish a connection with the MySQL server.
3. Open the terminal and change the directory to the application folder. Then, run the application by simply entering following commands:
```
pip install -r requirements.txt
uvicorn app.main:app
```
4. Open the API Docs (Swagger UI) by visiting to http://localhost:8000/docs.
5. To add the webcam for video streaming, go to section **/camera (POST)** and send a request with the following parameters:
- **source**: the source of the webcam
- **res**: the desired resolution for the video
- **counter_line**: an array of coordinate pairs to specify a counter line in the video

Upon a successful request, the response will be as follows:

```
{
  "data": {
    "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "source": 0,
    "res": 1280,
    "loop": true,
    "counter_line": [
      [
        100,
        720
      ],
      [
        1280,
        400
      ]
    ]
  }
}
```
6. To stream the video, use the **id** value returned in the successful response from step 5 as part of the URL: http://localhost:8000/streams/{id}.
</details>

## How to Stream Video (with Video File)
<details>
<summary>All OS</summary>

### All OS

1. First, open the terminal and change the directory to the application folder. Then, run the application by entering following command:
```
docker-compose up
```
1. Open the API Docs (Swagger) by visiting to http://localhost:8000/docs.
2. To upload the video that you want to stream, go to section **/camera/video (POST)**  and send a request with following parameters:

- **video**: the video file that you want to stream
- **res**: the desired resolution for the video
- **loop**: whether or not the video should loop
- **counter_line_str**: an array of coordinate pairs to specify a counter line in the video

Upon a successful request, the response will be as follows:

```
{
  "data": {
    "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "source": "./uploads/videos/video-1234567890.mp4",
    "res": 1280,
    "loop": true,
    "counter_line": [
      [
        100,
        720
      ],
      [
        1280,
        400
      ]
    ]
  }
}
```
4. To stream the video, use the **id** value returned in the successful response from step 3 as part of the URL: http://localhost:8000/streams/{id}.
</details>
