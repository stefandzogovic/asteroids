FROM ubuntu:18.04

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/requirements.txt

RUN apt-get update -y
RUN apt install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt -y install python3.8
RUN apt install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN apt-get -y install libfontconfig \
&& apt install libgl1-mesa-glx -y \
&& apt-get install libxcb-icccm4 -y  \
&& apt-get -y install libxcb-image0 \
&& apt-get install libxcb-keysyms1 -y \
&& apt-get install libxcb-randr0 -y \
&& apt-get install -y libxcb-render-util0 \
&& apt-get install libxcb-shape0 -y \
&& apt-get install libxcb-xfixes0 -y \  
&& apt-get install libxcb-xinerama0 -y \
&& apt-get install libxcb-xkb1 -y \
&& apt-get install libxkbcommon-x11-0 -y \
&& apt-get install libnvidia-gl-440 -y \
&& apt-get update

COPY . /usr/src/app

CMD ["python3", "-m", "MultiPlayer.servermultiplayer"]