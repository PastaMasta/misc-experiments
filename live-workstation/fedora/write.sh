#! /bin/bash

function usage {
  echo "Not enough args!"
  echo $* image.iso /dev/somedevice [ /dev/... ]
  exit 1
}
[[ $# -lt 2 ]] && usage $0

image=$1
shift
devs=$*

for dev in devs ; do
  livecd-iso-to-disk --format --efi --timeout 60 ${image} ${dev}
done
