docker run --rm -it --net=host --privileged=true --device=/dev/snd:/dev/snd \
       --device=/dev/dri:/dev/dri -e DISPLAY -v \
       /tmp/.X11-unix/:/tmp/.X11-unix/ game