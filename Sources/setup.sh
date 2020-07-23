#!/bin/bash

echo "------------------------"
echo "Setting up Packages..."
echo "------------------------"
apt-get install opencv*


echo "------------------------"
echo "Installing Extcolors..."
echo "------------------------"
pip3 install extcolors


echo "------------------------"
echo "Installing OpenCV"
echo "------------------------"
pip3 install opencv-python


echo "------------------------"
echo "Installing HexDump"
echo "------------------------"
pip3 install hexdump


echo "------------------------"
echo "Finishing setup Gracefully..."
