FROM ubuntu:xenial

# MAINTAINER "thomas@synpon.com"

RUN mkdir /app

COPY . /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    nano \
    wget \
    python-dev \
    python-pip \
    python-tk \
    unzip

RUN pip install setuptools wheel futures

RUN cd /app && \
    pip install -r requirements.txt

#WORKDIR "/app"

#ENTRYPOINT ["python"]

#CMD ["frontend.py"]
