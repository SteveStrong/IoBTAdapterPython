#!/bin/bash

conda create --name iobt-adapter python=3.8
conda install -c conda-forge opencv
conda install -c conda-forge paho-mqtt
conda install -c conda-forge numpy
# conda install -c conda-forge pysimplegui
conda install -c conda-forge imuteils

conda install -c anaconda pandas

conda install -c conda-forge wxpython
conda install -c conda-forge rx

# conda install -c conda-forge moviepy
# conda install -c pytorch pytorchy
# conda install -c pytorch torchvisiony
# conda install -c conda-forge cupy

# conda install -c conda-forge onnx
# conda install -c conda-forge onnxruntime

# to integrate bash with conda
# conda init bash  

conda activate iobt-adapter
pip install SoundCard
pip install signalrcore