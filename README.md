# freeradius-k8s

## Commands
Create docker image in microk8s
```
cd freeradius/freeradiuspy
sudo docker build . -t freeradiuspy
sudo docker save freeradiuspy > freeradiuspy.tar
microk8s ctr image import freeradiuspy.tar
```