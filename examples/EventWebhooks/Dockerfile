FROM python:3.8-slim
ARG basedir
RUN apt update && apt install -y curl

WORKDIR /usr/src/app
COPY ${basedir}requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

ENV PYTHONPATH="/usr/src/app/:/usr/src/lib/"
ENV PYTHONUNBUFFERED=1

COPY ${basedir}/src/* /usr/src/app
