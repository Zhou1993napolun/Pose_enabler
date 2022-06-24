# Pose_enabler
First of all, we should follow the requirement.txt to install all the libraries：

```shell
source activate 'your env environment name'
cd ./demo
pip install -r requirement.txt
```

And we need another weight file:

`mobile_epoch2.pth` : The Link is : https://drive.google.com/file/d/1IqiE7hQGc7qKRtNzqzraejVKjzpCvoOG/view?usp=sharing

`pose_hrnet_w48_384x288.pth` ： The Link is : https://drive.google.com/file/d/1p-aDyEba3M4HHOjL_fCjPhUxraSVKZJi/view?usp=sharing


Then we should down load two `.pth` file to the path:
```shell
./demo/pose_hrnet_w48_384x288.pth
./demo/mobile_epoch2.pth
```

Finally run the following command:

```shell
python3 pose_detection_2.py --video 'your video path' --write
```

