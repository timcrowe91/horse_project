

FROM python:3.8.6-buster




COPY data.py /data.py

COPY requirements.txt /requirements.txt
COPY horse_project /horse_project
COPY home/rexelardo/code/Lewagon_GCP_Credentials.json /credentials.json

RUN pip install --upgrade pip
RUN pip install -r requirements.txt



CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT