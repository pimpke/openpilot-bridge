FROM ghcr.io/commaai/openpilot-sim:latest

RUN apt purge libzmq* -y

RUN git clone https://github.com/zeromq/libzmq.git /libzmq && \
	cd /libzmq && \
	./autogen.sh && \
	./configure && \
	make && \
	make install && \
	ldconfig

RUN pip install pydevd-pycharm==221.6008.17

RUN apt-get update \
    && apt-get install -y gdb libgsl-dev \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH ${PYTHONPATH:+${PYTHONPATH}:}/openpilot:/openpilot-bridge
