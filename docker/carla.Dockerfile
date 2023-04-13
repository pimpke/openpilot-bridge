FROM carlasim/carla:0.9.13

USER root

# Update nvidia GPG key
RUN \
    rm /etc/apt/sources.list.d/cuda.list && \
    rm /etc/apt/sources.list.d/nvidia-ml.list && \
    apt-key del 7fa2af80 && \
    apt-get update && apt-get install -y --no-install-recommends wget && \
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-keyring_1.0-1_all.deb && \
    dpkg -i cuda-keyring_1.0-1_all.deb && \
    apt-get update

RUN apt-get update && apt-get -y install sudo
RUN apt-get install -y libvulkan1 vulkan-utils
RUN apt-get install -y xserver-xorg mesa-utils
RUN apt-get install -y mesa-vulkan-drivers 
RUN apt-get install -y tmux 

USER carla

CMD /bin/bash
