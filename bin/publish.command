#!/bin/bash

# copy to local esp32 git repo
# -n to simulate
rsync -avzh --delete --exclude ".*" \
    --exclude "L*" \
    ~/Dropbox/Files/Class/49/python/esp32/ \
    ~/Dropbox/Files/Class/49/github/esp32
