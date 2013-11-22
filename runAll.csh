#!/bin/tcsh          

nohup python simpleAccessReco.py -b --nPU=20 --nBx=50 --nEv=1000 --index=0 &
nohup python simpleAccessReco.py -b --nPU=50 --nBx=50 --nEv=1000 --index=0 &
nohup python simpleAccessReco.py -b --nPU=50 --nBx=25 --nEv=1000 --index=0 &
nohup python simpleAccessReco.py -b --nPU=70 --nBx=25 --nEv=1000 --index=0 &
nohup python simpleAccessReco.py -b --nPU=140 --nBx=25 --nEv=1000 --index=0 &

