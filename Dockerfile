FROM python:3.11-bullseye

WORKDIR /code

COPY ./connector/Include/*.* .
COPY ./connector/Include/init_scripts/*.* ./init_scripts/*.*

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -r requirements.txt

COPY . .