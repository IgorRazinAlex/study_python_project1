FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python3-pip
RUN apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6
RUN apt-get install -y alsa-utils apulse
RUN apt-get install -y libsndfile1-dev
RUN apt-get install -y pulseaudio libpulse-dev
RUN apt-get install -y libpulse0 libasound2 libasound2-plugins
RUN apt-get clean
RUN pip install --upgrade pip

ENV DISPLAY=:0

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8878

RUN chmod +x run.sh

CMD ./run.sh