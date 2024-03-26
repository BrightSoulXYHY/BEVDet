import numpy as np 
# import matplotlib.pyplot as plt

class Triangle3D:
    def __init__(self,**kwargs):
        self.fov = kwargs["fov"] if "fov" in kwargs else 30
        self.depth = kwargs["depth"] if "depth" in kwargs else 10
        self.theta = kwargs["theta"] if "theta" in kwargs else 0
        self.x = kwargs["x"] if "x" in kwargs else 0
        self.y = kwargs["y"] if "y" in kwargs else 0
        self.z = kwargs["z"] if "z" in kwargs else 0

        fov_hf_rad = np.deg2rad(self.fov)/2
        theta_rad = np.deg2rad(self.theta)
        self.vc = self.depth*np.array([np.cos(theta_rad),np.sin(theta_rad),0])
        self.depth_cos = self.depth*np.cos(fov_hf_rad)

    def in_triangel(self,x,y,z):
        v = np.array([x-self.x,y-self.y,z-self.z])
        v_norm = np.linalg.norm(v)
        vv_dot = np.dot(self.vc,v)
        # 留一点裕度
        return v_norm*self.depth_cos <= vv_dot <= self.depth*self.depth + 1e-6





