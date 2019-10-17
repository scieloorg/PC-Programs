FROM ubuntu:18.04
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    build-essential \
    ca-certificates \
    gcc \
    git \
    libpq-dev \
    make \
    python-pip \
    python2.7 \
    python2.7-dev \
    ssh \
    lib32z1 \
    lib32z1-dev \
    && apt-get autoremove \
    && apt-get clean

COPY ./requirements.txt /app/requirements.txt

RUN pip --no-cache-dir install -r /app/requirements.txt
RUN chown -R nobody:nogroup /app

RUN wget https://github.com/bireme/cisis/releases/download/32bits-5.7e-1660/cisis-32bits-5.7e-1660.tar.gz

RUN mkdir cisis

RUN tar vxzf cisis-32bits-5.7e-1660.tar.gz -C cisis \
    && chmod +x cisis \
    && chown nobody cisis \
    && mv cisis/* /bin

USER nobody

WORKDIR /app

