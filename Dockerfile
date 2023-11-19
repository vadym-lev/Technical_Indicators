FROM ubuntu:22.04
RUN apt-get update
RUN apt-get install -y python3.11 python3-pip python3.11-dev
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
RUN update-alternatives --config python3

WORKDIR /app/
COPY requirements.txt .
RUN pip install --upgrade -r requirements.txt