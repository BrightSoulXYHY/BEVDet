# 基于autodl的镜像安装环境

CUDA=11.3
PYTHON_VERSION=3.8
TORCH_VERSION=1.10.0
TORCHVISION_VERSION=0.11.0
ONNXRUNTIME_VERSION=1.8.1
MMCV_VERSION=1.5.3
PPLCV_VERSION=0.7.0

WORKSPACE="/root/autodl-tmp/workspace"

# pytorch
conda install pytorch==${TORCH_VERSION} torchvision==${TORCHVISION_VERSION} cudatoolkit=${CUDA} -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/linux-64/

# mmcv-full
pip install mmcv-full==${MMCV_VERSION} -f https://download.openmmlab.com/mmcv/dist/cu${CUDA//./}/torch${TORCH_VERSION}/index.html  -i https://pypi.tuna.tsinghua.edu.cn/simple

# get onnxruntime
pushd ${WORKSPACE}
    wget https://github.com/microsoft/onnxruntime/releases/download/v${ONNXRUNTIME_VERSION}/onnxruntime-linux-x64-${ONNXRUNTIME_VERSION}.tgz
    tar -zxf onnxruntime-linux-x64-${ONNXRUNTIME_VERSION}.tgz
    pip install onnxruntime-gpu==${ONNXRUNTIME_VERSION} -i https://pypi.tuna.tsinghua.edu.cn/simple
popd

# install mmdeploy
pushd ${WORKSPACE}
    export ONNXRUNTIME_DIR=${WORKSPACE}/onnxruntime-linux-x64-${ONNXRUNTIME_VERSION}
    export TENSORRT_DIR=${WORKSPACE}/tensorrt
    git clone https://github.com/HuangJunJie2017/mmdeploy.git
    cd mmdeploy
    # if [ -z ${VERSION} ] ; 
    #     then echo "No MMDeploy version passed in, building on master" ; 
    # else 
    #     git checkout tags/v${VERSION} -b tag_v${VERSION} ; 
    # fi
    git submodule update --init --recursive
    mkdir -p build 
    cd build 
    cmake -DMMDEPLOY_TARGET_BACKENDS="ort;trt" .. 
    make -j$(nproc) 
    cd .. 
    pip install -e .  -i https://pypi.tuna.tsinghua.edu.cn/simple
popd


# install ppl.cv
pushd ${WORKSPACE}
    git clone https://github.com/openppl-public/ppl.cv.git 
    cd ppl.cv 
    git checkout tags/v${PPLCV_VERSION} -b v${PPLCV_VERSION} 
    ./build.sh cuda
popd

BACKUP_LD_LIBRARY_PATH=$LD_LIBRARY_PATH
pushd ${WORKSPACE}
    cd mmdeploy 
    rm -rf build/CM* build/cmake-install.cmake build/Makefile build/csrc
    mkdir -p build && cd build
    cmake .. \
        -DMMDEPLOY_BUILD_SDK=ON \
        -DMMDEPLOY_BUILD_EXAMPLES=ON \
        -DCMAKE_CXX_COMPILER=g++ \
        -Dpplcv_DIR=/root/workspace/ppl.cv/cuda-build/install/lib/cmake/ppl \
        -DTENSORRT_DIR=${TENSORRT_DIR} \
        -DONNXRUNTIME_DIR=${ONNXRUNTIME_DIR} \
        -DMMDEPLOY_BUILD_SDK_PYTHON_API=ON \
        -DMMDEPLOY_TARGET_DEVICES="cuda;cpu" \
        -DMMDEPLOY_TARGET_BACKENDS="ort;trt" \
        -DMMDEPLOY_CODEBASES=all
    make -j$(nproc) && make install
    echo "Built MMDeploy master for GPU devices successfully!" ;
popd

export LD_LIBRARY_PATH="${WORKSPACE}/mmdeploy/build/lib:${BACKUP_LD_LIBRARY_PATH}"
pip install mmdet==2.25.1 mmsegmentation==0.25.0  -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install pycuda \
    lyft_dataset_sdk \
    networkx==2.2 \
    numba==0.53.0 \
    numpy \
    nuscenes-devkit \
    plyfile \
    scikit-image \
    tensorboard \
    trimesh==2.35.39 -i https://pypi.tuna.tsinghua.edu.cn/simple