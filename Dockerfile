FROM continuumio/miniconda3:4.3.27

RUN apt-get update

RUN mkdir /neutral-info
COPY . /neutral-info/
WORKDIR /neutral-info/

# install package
RUN pip install pipenv && \
    pipenv sync

# env
RUN VERSION=DEPLOY python genenv.py

# time
RUN echo "Asia/Taipei" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

CMD ["/bin/bash"]
