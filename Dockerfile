FROM python:3.8-buster

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

COPY . /usr/src/app

CMD ["python", "/usr/src/app/MultiPlayer/servermultiplayer.py"]