## Getting Started

This is installation guide on how to install `Edge TPU` to work with `Rpi Ubuntu`

Step 1: Install `python 3.9` library.
```
$ sudo apt update 
$ sudo apt install wget software-properties-common
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt update

Install this version if you're using Virtual Environment
$ sudo apt-get install python3.9-venv

Install this version if you're not using Virtual Environment
$ sudo apt-get install python3.9

If you encounter no disutils found. Then run below command to resolve this
sudo apt install python3.9-distutils
```

### Step 2: Create new Virtual Environment

For this one, you need to install python3.9-venv version 

```
$ mkdir EdgeTpu
$ cd EdgeTpu
$ python3.9 -m venv edge
$ source edge/bin/activate
```
Additionally you can install `pip` if this package is not found as follow
```
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ python3.9 get-pip.py
```

If you found `warning pip is not checked`. Run below command to remove it
```
rm -r ~/.cache/pip/selfcheck/
```

Install the `Tpu` Packages
```
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

sudo apt-get update
sudo apt-get install libedgetpu1-std
sudo apt-get install libedgetpu1-max

## Install TF Lite for the Edge TPU
python3.9 -m pip install tflite-runtime
python3.9 -m pip install tflite-support
python3.9 -m pip install protobuf
python3.9 -m pip install numpy

## Install PyCoral for Edge TPU
There is a problem to install this packages : sudo apt-get install python3-pycoral
due to unmet dependencies.

To resolve this run following command
you can download a specific PyCoral wheel file and pass it to pip install at this link : https://coral.ai/software/#pycoral-api
$ pip install https://github.com/google-coral/pycoral/releases/download/v2.0.0/pycoral-2.0.0-cp39-cp39-linux_aarch64.whl

$ pip install https://github.com/google-coral/pycoral/releases/download/v2.0.0/tflite_runtime-2.5.0.post1-cp39-cp39-linux_aarch64.whl#sha256=9839c3acb506b5003a9bd3860329a8ae20e675efbae14dbea02659b0054f42c6
```

Visit Official page of where you can find this library:
```
pycoral : https://coral.ai/software/#pycoral-api
tflite-runtime : https://google-coral.github.io/py-repo/tflite-runtime/
```

## Step 3: Non Virtual Environment

For this one, you need to install `sudo apt-get install python3.9` version.

Additionally you can install `pip` if this package is not found as follow
```
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ python3.9 get-pip.py
```

Install the `Tpu` Packages
```
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

sudo apt-get update
sudo apt-get install libedgetpu1-std
sudo apt-get install libedgetpu1-max

## Install TF Lite for the Edge TPU
python3.9 -m pip install tflite-runtime
python3.9 -m pip install tflite-support
python3.9 -m pip install protobuf
python3.9 -m pip install numpy

## Install PyCoral for Edge TPU
There is a problem to install this packages : sudo apt-get install python3-pycoral
due to unmet dependencies.

To resolve this run following command
you can download a specific PyCoral wheel file and pass it to pip install at this link : https://coral.ai/software/#pycoral-api
$ pip install https://github.com/google-coral/pycoral/releases/download/v2.0.0/pycoral-2.0.0-cp39-cp39-linux_aarch64.whl

$ pip install https://github.com/google-coral/pycoral/releases/download/v2.0.0/tflite_runtime-2.5.0.post1-cp39-cp39-linux_aarch64.whl#sha256=9839c3acb506b5003a9bd3860329a8ae20e675efbae14dbea02659b0054f42c6
```

Visit Official page of where you can find this library:
```
pycoral : https://coral.ai/software/#pycoral-api
tflite-runtime : https://google-coral.github.io/py-repo/tflite-runtime/
```

