# Pose_enabler
First of all, we should follow the requirement.txt to install all the libraries：

```shell
source activate 'your env environment name'
cd ./demo
pip install -r requirement.txt
```

Then you should down load two `.pth` file to the path:
```shell
./demo/pose_hrnet_w48_384x288.pth
./demo/mobile_epoch2.pth
```

Finally run the following command:

```shell
python3 pose_detection_2.py --video 'your video path' --write
```

