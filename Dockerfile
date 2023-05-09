FROM bitnami/pytorch

ENV PORT=8000

WORKDIR /code

COPY . /code

RUN apt-get update && \
    apt-get install -y ffmpeg libsm6 libxext6 && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

EXPOSE $PORT

CMD uvicorn main:app --host 0.0.0.0 --port $PORT