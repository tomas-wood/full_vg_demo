FROM ubuntu:xenial

# MAINTAINER "thomas@synpon.com"

RUN mkdir /app

COPY ./frontend.py /app/frontend.py

COPY ./app /app/app

COPY ./requirements.txt /app/requirements.txt

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

VOLUME ["/app/visual_genome"]

WORKDIR "/app"

ENTRYPOINT ["python"]

CMD ["./frontend.py"]
