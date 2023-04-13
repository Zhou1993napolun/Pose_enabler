# 从 git 复现 reid - pose 部分
_本文件为在 Intel NUC 1 上部署 Pose Enabler 的实际操作步骤。部署过程在 Reid Person 之后，使用了其中建立的环境，如果在新环境中运行出现依赖问题，可查阅 person 复现文档。以下步骤参照 README 文件执行，可作为其补充。_

## 1. 安装所需环境
README 中的步骤为先进入 demo 目录后安装环境，但是实际上 requirements.txt 文件仅存在于根目录下，可通过 `find` 命令确认：
```sh
find . -name 'requirement*'
```
所以所用命令简化为：
```sh
conda activate reid0406
pip install -r requirements.txt
```
这个过程中发现其要求的 torch 等包的版本均为给定版本号，如 `torch==1.6.0`，而之前的 Person 部分要求版本为大于某个版本号，如 `torch>=1.6.0`，所以在 Person 部分安装的环境基础上，很多包都需要重新下载。 为了尽可能简化步骤节省时间，尝试修改requirements 文件，将版本要求改为最低值而非固定版本号。  
>_本修改在新建的 git 分支中操作，也保留有原版本，**之后在确定第三部分 clothes 的要求后会尝试以完全给定的版本再次测试。** git 操作在此不作赘述。_

> 小插曲：刚刚因为强制结束了torch下载，或是因为误触到了什么组合键，就遇到了光标消失的问题，解决方式如下：
```sh
echo -e "\033[?25h"
```

将 `requirements.txt` 中所有的相等约束均替换为不等约束后重复安装步骤，成功完成安装过程。

## 2. 从百度云下载权重文件
>地址1：https://pan.baidu.com/s/1KspL5ORu-jCL8hXWzi4ESg  
地址2：https://pan.baidu.com/s/1zZQV1EruG9iU0CoTXu-rCQ  
提取码：1234

从地址 1 和地址 2 使用相同的的提取码分别下载文件 `mobile_epoch2.pth` 和 `pose_hrnet_w48_384x288.pth`，上传至 demo 目录下。

## 3. 运行
在 demo 目录中存在两个 `.mp4` 文件，其内容完全相同，可以用于测试。以 `test_video.mp4` 为例，其内容如下表所示：
|文件名|时长|帧率|人数|位置|包含动作|
|:---|:---:|:---:|:---:|:---:|:---|
|test_video.mp4|17s|29.82/s|1|不变|跑、走、出拳、招手、蹲

执行以下命令以测试：
```sh
cd demo
python3 pose_detection_2.py --video 'test_video.mp4' --write
```
此时报错：
```sh
ModuleNotFoundError: No module named 'utils.my_transforms'
```
查看 lib/utils 目录，其中没有 my_transforms 文件，而在相似的 `transforms.py` 文件中含有所需的以 `transform_preds` 命名的函数。所以修改 lib/core 目录下的 `inference.py` 文件，将第 15 行修改为：
```python
from utils.transforms import transform_preds
```

再次运行时报错如下：
```sh
Traceback (most recent call last):
  File "pose_detection_2.py", line 542, in <module>
    main()
  File "pose_detection_2.py", line 425, in main
    image_bgr = cv2.putText(image_bgr, state_name, box[0], font, 1.2, (0, 0, 0), 2)
cv2.error: OpenCV(4.7.0) :-1: error: (-5:Bad argument) in function 'putText'
```
查看官方文档发现 org 是 putText 函数的第三个参数，应为所添加文字的左下角在图片上的坐标位置，类型为 cv::Point。查看相关代码目测没有发现类型及命名问题，考虑将相关变量打印至命令行。发现 box[0][0] 和 box[0][1] 为 numpy.float32 类型。推测错误可能由 putText 不支持该精度导致，而显示文字理应不需要位置及其精确，故尝试将其取整后输入函数。

经一小段等待时间后，开始缓慢显示处理后的图像，骨架识别准确。但是其速度过慢，根据经验推测由 ssh 传输结果时处理较慢导致，考虑不再显示，只将结果以文件形式保存。所以**使用 q 键退出**后，修改 `pose_detection_2.py` 代码对应位置，将 439 及 440 行含有 `imshow()` 函数的部分注释。  
此时运行中看不到处理进度，所以在循环内添加代码，将帧号打印至命令行。_因为修改较多，以下行号均为修改后的行号，可在对应行前后寻找合适的修改位置。另外在修改时请**注意调整缩进量**。_ 全部代码修改如下：

350 行添加：
```python
frame_index = 0
```
358 行添加：
```python
frame_index += 1
```
441 - 445 行修改：
```python
'''
if on_cloud_host == False:
    cv2.imshow('demo', image_bgr)
'''
print(f'当前为第{frame_index}帧')
```
修改后用与刚刚相同的命令运行：
```sh
python3 pose_detection_2.py --video 'test_video.mp4' --write
```
此时可以看到命令行在输出当前在处理的帧号，说明程序在正常运行，速度较刚刚有一定提高但是仍然较慢。  
_此过程暂时无法中断，在命令行输入 q 是无法结束程序的，而以 `CTRL+Z` 等方式中断时不能正常得到 `output.avi` 输出。稍后将修改此中途退出部分以能快速展示结果。_
运行至显示“当前为第517帧”时出现 `cannot load the video. `，约用时 20 - 30 分钟。视频的帧数可由乘法计算约为 506 帧左右，可见视频应当已经处理完毕，最后的输出是读取到视频结束后不能继续读取时的输出。此时可以查看输出 `demo/output.avi`。

_运行后视频的时长可能会略有变化，还没有确定是什么原因，可能是和原始帧率略有不同。_

> 可以看到，在第 354 行设定了输出视频的帧率为 24/s，略小于由原视频的属性中获得的帧率，可能是导致时长变化的原因。

## 4. 补充
为方便查看算法用时，在 `main()` 函数的其实和末尾分别读取当前时间戳并将差打印至命令行。
```python
time_start = time.time()                          # 302行添加

print('用时 %.1f s' %(time.time() - last_time))   # 447 行添加

time_len = time.time() - time_start               # 547 行起添加
print('用时 %.1f s' %(time.time() - last_time)) 
print('总用时 %.1f s' % time_len)
```

在根目录中还存在另一个 `.md` 文件，查看发现其中提到了另一条内容：建议禁用 cudnn。  
而在本例测试时，虽然命令行有警告输出，但是根据内容判断其并非由 cudnn 导致。  
目前 cudnn 的 enabled 参数由文件 `lib/config/default.py` 中第 33 行控制。
> 尝试将其修改为 False 后重复实验。没有发现其产生任何影响。本次用时 1213.3 s。
