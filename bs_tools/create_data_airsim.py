import hashlib
import pickle
import os
import json

import glob

import numpy as np
from pyquaternion import Quaternion

from bs_camera import *
from Triangle3D import Triangle3D

'''
构建BEV数据集
需要gt_3dbbox和图片作为输入
对于一帧数据而言
'''

import time
time_prefix = time.strftime("%Y-%m-%d_%H-%M-%S")


classes = ['drone']
swarm_nums = 10 + 1



root_dir = "./data/airsim"
dataset = {}
dataset["metadata"] = {"version":f"airsim_{time_prefix}"}
info_list = []

measure = [
    Triangle3D(fov=60,depth=50,theta=0),
    Triangle3D(fov=60,depth=50,theta=-45),
    Triangle3D(fov=60,depth=50,theta=45),
    Triangle3D(fov=60,depth=50,theta=180),
    Triangle3D(fov=60,depth=50,theta=135),
    Triangle3D(fov=60,depth=50,theta=-135),
]



def gen_info_dict(json_path):
    dirname = os.path.dirname(json_path)
    basename_without_ext = os.path.splitext(os.path.basename(json_path))[0]

    info_dict = {}
    # 读取数据
    with open(json_path) as fp:
        json_data = json.load(fp)
    data_basename = os.path.splitext(json_path)[0]

    timestamp = json_data["timestamp"]
    ego2global_translation = np.array(json_data["drone_00"]["pos"])
    ego2global_rotation = np.array(json_data["drone_00"]["quat"])

    info_dict["scene_token"] = hashlib.md5(f"{dirname}".encode(encoding='UTF-8')).hexdigest()
    info_dict["token"] = hashlib.md5(f"{json_path}".encode(encoding='UTF-8')).hexdigest()
    info_dict["timestamp"] = timestamp
    info_dict["ego2global_translation"] = ego2global_translation
    info_dict["ego2global_rotation"] = ego2global_rotation

    # 弃用的属性
    info_dict["lidar_path"] = None
    info_dict["lidar2ego_translation"] = [0,0,0]
    info_dict["lidar2ego_rotation"] = [1,0,0,0]

    # drone_00填充cam_dict
    cam_dict = cam_dict_templ.copy()
    for cam in cams:
        cam_dict[cam]["timestamp"] = timestamp
        data_path = f"{dirname}/{basename_without_ext}_{cam}.png"
        cam_dict[cam]["data_path"] = data_path
        cam_dict[cam]["sample_data_token"] = hashlib.md5(f"{data_path}".encode(encoding='UTF-8')).hexdigest()
        cam_dict[cam]["ego2global_translation"] = ego2global_translation
        cam_dict[cam]["ego2global_rotation"] = ego2global_rotation
    info_dict["cams"] = cam_dict

    # drone_01~drone10对应bbox真值
    # xyz,size,yaw
    gt_boxes = []
    gt_labels = []
    gt_names = []
    gt_velocitys = []
    valid_flag = []
    for i in range(1,swarm_nums):
        bbox_center = np.array(json_data[f"drone_{i:02d}"]["pos"])
        bbox_quat = np.array(json_data[f"drone_{i:02d}"]["quat"])
        bbox_vel = np.array(json_data[f"drone_{i:02d}"]["vel"])
        bbox_yaw = Quaternion(bbox_quat).yaw_pitch_roll[0]
        bbox_size = [1,1,0.2]
        gt_box = np.hstack([bbox_center,bbox_size,bbox_yaw,bbox_vel[:2]])
        gt_boxes.append(gt_box)
        gt_labels.append(classes.index("drone"))
        gt_names.append("drone")
        gt_velocitys.append(bbox_vel[:2])
        
        x,y,z = bbox_center - ego2global_translation
        valid_flag.append(any([m.in_triangel(x,y,z) for m in measure]))
    info_dict["ann_infos"] = (gt_boxes,gt_labels)
    info_dict["gt_names"] = gt_names
    info_dict["gt_velocity"] = gt_velocitys
    info_dict["valid_flag"] = valid_flag
    return info_dict

if __name__ == "__main__":
    # json_paths = glob.glob(f"{root_dir}/**/*.json",recursive=True)
    # mode = "train"
    # train_dirs = [ f"airsim_{i:02d}" for i in range(10) ]

    mode = "val"
    train_dirs = [ "airsim_val" ]

    json_paths = []
    for train_dir in train_dirs:
        json_paths += glob.glob(f"{root_dir}/{train_dir}/**/*.json",recursive=True)

    print(f"{len(json_paths)} json!")
    for json_path in json_paths:
        info_dict = gen_info_dict(json_path)
        info_list.append(info_dict)

    dataset["infos"] = info_list
    with open(f'{root_dir}/bs_airsim_infos_{mode}.pkl', 'wb') as fid:
        pickle.dump(dataset, fid)