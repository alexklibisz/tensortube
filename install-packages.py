#!/bin/sh

export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.11.0rc0-cp27-none-linux_x86_64.whl
pip2.7 install --user $TF_BINARY_URL
pip2.7 install --user pytube
# pip2.7 install --user opencv-python
pip2.7 install --user flask
pip2.7 install --user imageio
