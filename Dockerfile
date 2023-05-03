FROM python:3.10.11

WORKDIR /src
COPY matdn.py matdn.py 
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt