# Real-time Pose Estimation Enabler

A real-time pose estimation enabler which can use IP camera ,local video or local image as input, and save the output data in .josn format. 

The structure of the project relies on HRNet project.

## Models

This enabler combines three models to achieve the final task. 

​	The first model is **Yolov5 model**, which is used for person detection. The Yolov5 model will detect the people in the video and pass their location information to the second model.

​	The second model is **HRNet**. It is the bone of the project. According to the information that gets from the Yolov5, HRNet will strip the person from the video for **skeleton** recognition.

​	Between the second model and last model, there is a transfer layer. It will change the skeleton location information to skeleton image. And combine a series of images to a skeleton flow diagram.

​	The last model is basic on **3D-CNN**. It's input is the skeleton flow diagram and it will classify the pose of the people.

## Dataset

The Yolov5 and HRNet in our model has been pre-trained. For the 3D-CNN model, we recorded dozens of videos as training datasets. The making of the training set is divided into the following steps:

​	Firstly, slice the video into single image.

​	Secondly, extract the skeleton information from each image.

​	Thirdly, reconstruct the skeleton information into skeleton picture.

​	Finally, combine these picture into gif.

## Quick start

If you are not in the Intel machine one or you have not install the environment of the project. You should follow these steps to start.

1. Install pytorch == v1.6.0 following [official instruction](https://pytorch.org/).
   **Note that if you use pytorch's version is not v1.6.0, you should following the instruction at <https://github.com/Microsoft/human-pose-estimation.pytorch> to disable cudnn's implementations of BatchNorm layer**

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Then we can cd to the demo file to use the pose detection function.

```bash
cd /demo
# to use local video, you can use this statement.
python3 pose_detection.py --video {your_videos} --write
# to use IP camera, you can use this statement.
python3 pose_detection.py --webcam {your_webcam} --write
```

## Docker

(This part is going to be finished soon.)



## Model Train

This part will be detailedly introduce in the **automatic generation datasets** section.

