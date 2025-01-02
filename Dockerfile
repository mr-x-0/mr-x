FROM nikolaik/python-nodejs:python3.10-nodejs19

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

 COPY . /app/

 WORKDIR /app

 COPY requirements.txt requirements.txt
 RUN pip3 install -r requirements.txt

 COPY . .

 CMD [ "python3", "main.py"]
