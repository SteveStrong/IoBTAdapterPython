#!/bin/bash
export PATH=~/miniconda/bin:$PATH
conda create -y --name iobt-adapter python=3.8
conda install -c conda-forge opencv
conda install -c conda-forge paho-mqtt
conda install -c conda-forge numpy
conda install -c conda-forge imuteils
conda install -c anaconda pandas
conda install -c conda-forge wxpython
conda install -c conda-forge rx
pip install SoundCard
pip install signalrcore