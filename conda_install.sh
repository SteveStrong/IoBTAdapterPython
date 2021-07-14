#!/bin/bash

conda create -name iobt-adapter python=3.8
conda install -c conda-forge opencv
conda install -c conda-forge paho-mqtt
conda install -c conda-forge numpy
# conda install -c conda-forge pysimplegui
conda install -c conda-forge imutils

conda install -c conda-forge r-signal

conda install -c anaconda pandas

# conda install -c conda-forge moviepy
# conda install -c pytorch pytorchy
# conda install -c pytorch torchvisiony
# conda install -c conda-forge cupy

# conda install -c conda-forge onnx
# conda install -c conda-forge onnxruntime


# to integrate bash with conda
# conda init bash  