FROM tpdock/freeradius

RUN apt update && apt install -y software-properties-common

RUN add-apt-repository -y ppa:deadsnakes/ppa

RUN apt update && apt install -y python3.8

RUN rm /usr/bin/python3 && ln -s /usr/bin/python3.8 /usr/bin/python3