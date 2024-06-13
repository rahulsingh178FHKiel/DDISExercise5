# syntax=docker/dockerfile:1

FROM python:3.9-slim

ENV HOST 0.0.0.0

ENV PORT 5000

EXPOSE 5000	

WORKDIR /python-docker

COPY requirements.txt requirements.txt

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD [ "python", "basicAPI.py"]
