import numpy as np

# Airsim理想内存矩阵
def fov2f(fov,w=1280):
    return w/(2*np.tan(np.deg2rad(fov/2)))

def constructK(fov=120,w=1280,h=720):
    f = fov2f(fov,np.max([w,h]))
    return np.array([
        [f,0,w/2],
        [0,f,h/2],
        [0,0,1],
    ],dtype=float)

cam_K60 = constructK(fov=60)
cam_K30 = constructK(fov=30)

cams = [
    "cam_front_lf",
    "cam_front_center",
    "cam_front_left",
    "cam_front_right",
    "cam_back_right",
    "cam_back_center",
    "cam_back_left",
]


cam_dict_templ = {
    "cam_front_lf":{
        'type': 'cam_front_lf',
        'timestamp': None,
        'data_path': "",
        'sample_data_token': "",
        'ego2global_translation': None,
        'ego2global_rotation': None,
        'cam_intrinsic': cam_K30,
        'sensor2ego_translation': [0.5,-0.15,0],
        'sensor2ego_rotation': [0.5, 0.5, 0.5, 0.5],
        'sensor2lidar_rotation': None,
        'sensor2lidar_translation': None,
    },
    "cam_front_center":{
        'type': 'cam_front_center',
        'timestamp': None,
        'data_path': "",
        'sample_data_token': "",
        'ego2global_translation': None,
        'ego2global_rotation': None,
        'cam_intrinsic': cam_K60,
        'sensor2ego_translation': [0.5,0.15,0],
        'sensor2ego_rotation': [0.5, 0.5, 0.5, 0.5],
        'sensor2lidar_translation': [0.5,0.15,0],
        'sensor2lidar_rotation': [0.5, 0.5, 0.5, 0.5],
    },
    "cam_front_left":{
        'type': 'cam_front_left',
        'timestamp': None,
        'data_path': "",
        'sample_data_token': "",
        'ego2global_translation': None,
        'ego2global_rotation': None,
        'cam_intrinsic': cam_K60,
        'sensor2ego_translation': [0.5,-0.5,0],
        'sensor2ego_rotation': [0.6532814824381883, 0.2705980500730985, 0.2705980500730985, 0.6532814824381883],
        'sensor2lidar_translation': [0.5,-0.5,0],
        'sensor2lidar_rotation': [0.6532814824381883, 0.2705980500730985, 0.2705980500730985, 0.6532814824381883],
    },
    "cam_front_right":{
        'type': 'cam_front_right',
        'timestamp': None,
        'data_path': "",
        'sample_data_token': "",
        'ego2global_translation': None,
        'ego2global_rotation': None,
        'cam_intrinsic': cam_K60,
        'sensor2ego_translation': [0.5,-0.5,0],
        'sensor2ego_rotation': [0.27059805007309856, 0.6532814824381883, 0.6532814824381883, 0.27059805007309856],
        'sensor2lidar_translation': [0.5,-0.5,0],
        'sensor2lidar_rotation': [0.27059805007309856, 0.6532814824381883, 0.6532814824381883, 0.27059805007309856],
    },
    "cam_back_right":{
        'type': 'cam_back_right',
        'timestamp': None,
        'data_path': "",
        'sample_data_token': "",
        'ego2global_translation': None,
        'ego2global_rotation': None,
        'cam_intrinsic': cam_K60,
        'sensor2ego_translation': [-0.5,-0.5,0],
        'sensor2ego_rotation': [-0.2705980500730985, 0.6532814824381883, 0.6532814824381883, -0.2705980500730985],
        'sensor2lidar_translation': [-0.5,-0.5,0],
        'sensor2lidar_rotation': [-0.2705980500730985, 0.6532814824381883, 0.6532814824381883, -0.2705980500730985],
    },
    "cam_back_center":{
        'type': 'cam_back_center',
        'timestamp': None,
        'data_path': "",
        'sample_data_token': "",
        'ego2global_translation': None,
        'ego2global_rotation': None,
        'cam_intrinsic': cam_K60,
        'sensor2ego_translation': [-0.5,0,0],
        'sensor2ego_rotation': [-0.5, 0.5000000000000001, 0.5000000000000001, -0.5],
        'sensor2lidar_translation': [-0.5,0,0],
        'sensor2lidar_rotation': [-0.5, 0.5000000000000001, 0.5000000000000001, -0.5],
    },
    "cam_back_left":{
        'type': 'cam_back_left',
        'timestamp': None,
        'data_path': "",
        'sample_data_token': "",
        'ego2global_translation': None,
        'ego2global_rotation': None,
        'cam_intrinsic': cam_K60,
        'sensor2ego_translation': [-0.5,-0.5,0],
        'sensor2ego_rotation': [-0.6532814824381883, 0.2705980500730986, 0.2705980500730986, -0.6532814824381883],
        'sensor2lidar_translation': [-0.5,-0.5,0],
        'sensor2lidar_rotation': [-0.6532814824381883, 0.2705980500730986, 0.2705980500730986, -0.6532814824381883],
    },
}