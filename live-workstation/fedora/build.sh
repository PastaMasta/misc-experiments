#! /bin/bash

set -x

kss="${*:-./fedora-workstation.ks}"

for ks in $kss ; do
  livecd-creator --config=${ks} --verbose --fslabel="myimage" 2>&1 | tee ./build.out
done

#iso="/tmp/Fedora-Workstation-Live-x86_64-29-1.2.iso"
#livemedia-creator --make-iso --ks ${ks} --iso ${iso} --keep-image
