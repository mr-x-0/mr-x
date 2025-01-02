FROM nikolaik/python-nodejs:python3.10-nodejs19

 WORKDIR /app

 COPY requirements.txt requirements.txt
 RUN pip3 install -r requirements.txt

 COPY . .

 CMD [ "python3", "main.py"]
