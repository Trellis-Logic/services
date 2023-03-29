FROM python:3.8
ARG basedir
RUN apt update && apt install -y curl
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && /usr/bin/python3 get-pip.py

WORKDIR /usr/src/app
COPY ${basedir}requirements.txt /usr/src/app/
RUN /usr/bin/python3 -m pip install -r requirements.txt

ENV PYTHONPATH="/usr/src/app/:/usr/src/lib/"
ENV PYTHONUNBUFFERED=1

COPY ${basedir}/src/* /usr/src/app
