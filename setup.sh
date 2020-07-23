#!/bin/bash

# Edit this as needed -- Do not include trailing slash '/'
EXECUTABLE_DIRECTORY=/usr/local/bin

# If not executable, make executable
if [[ ! -x mask.py ]];then
  chmod +x mask.py
fi

# You will most likely need the sudo command to copy to $EXECUTABLE_DIRECTORY
sudo cp mask.py ${EXECUTABLE_DIRECTORY}/mask
