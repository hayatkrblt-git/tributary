FROM python:3.11
COPY ./requirements.txt .
CMD python entrypoint.py
COPY ./entrypoint.py .