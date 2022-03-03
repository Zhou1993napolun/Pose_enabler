from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import csv
import os
import shutil

from PIL import Image
import torch
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim
import torch.utils.data
import torch.utils.data.distributed
import torchvision.transforms as transforms
import torchvision
import cv2
import numpy as np
import time


import _init_paths
import models
from config import cfg
from config import update_config
from core.function import get_final_preds
from utils.transforms import get_affine_transform

from models.pose_hrnet import get_pose_net

def parse_args():
    parser = argparse.ArgumentParser(description='Train keypoints network')
    # general
    parser.add_argument('--cfg', type=str, default='./inference-config.yaml')
    parser.add_argument('--video', type=str)
    parser.add_argument('--webcam', action='store_true')
    parser.add_argument('--image', type=str)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--showFps', action='store_true')

    parser.add_argument('opts',
                        help='Modify config options using the command-line',
                        default=None,
                        nargs=argparse.REMAINDER)

    args = parser.parse_args()

    # args expected by supporting codebase
    args.modelDir = ''
    args.logDir = ''
    args.dataDir = ''
    args.prevModelDir = ''
    return args

if __name__ == '__main__':
    args = parse_args()
    update_config(cfg, args)

    pose_model = get_pose_net(cfg, False)
    print(pose_model)

