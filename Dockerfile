FROM ubuntu:latest


RUN apt update && apt install python3 python3-pip python3-dev -y
RUN mkdir /usr/local/app
WORKDIR /usr/local/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

ADD biosimulations_dispatch ./biosimulations_dispatch

ENTRYPOINT ["flask", "run", "--port=5000", "--host=0.0.0.0"]