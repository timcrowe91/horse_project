

FROM python:3.8.6-buster




COPY data_model /data_model
COPY api /api
COPY requirements.txt /requirements.txt
COPY horse_project /horse_project

RUN pip install --upgrade pip
RUN pip install -r requirements.txt



CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT