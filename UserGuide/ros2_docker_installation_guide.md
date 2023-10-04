# Getting Started

This is method on how to use `docker` for `ROS2 Humble`

## Step 1 - Install `Docker Desktop`
Please visit docker website and download the `Docker Application`.
Sign to your `docker`

## Step 2 - Pull `ROS2` image
Visit below page that provide `GUI` Desktop of `ROS2`
```
https://hub.docker.com/r/tiryoh/ros2-desktop-vnc

Docker Pull Command : docker pull tiryoh/ros2-desktop-vnc
```

Once you finish the download, please switch the `docker version` as `docker linux` from task manager

Next we're going to `pull` this image into our `local directory`. Please open your `Terminal` and run  below command and wait until the process complete 
```
 docker pull tiryoh/ros2-desktop-vnc 
```

## Step 3 - Run the `docker image`

To run the `ROS2 docker`, please use below command. Run the docker container and access with port 6080.
Change the shm-size value depending on the situation.

```
docker run -i 6080:80 --security-opt seccomp=unconfined --shm-size=512m tiryoh/ros2-desktop-vnc:humble
```

This will expose port `6080:80`. To access the `GUI` go to below link.

```
Browse http://127.0.0.1:6080/.
```

## Step 4 - Visit this comprehesive Guide on how to setup this `Docker`
```
https://hub.docker.com/r/tiryoh/ros2-desktop-vnc
https://github.com/Tiryoh/docker-ros2-desktop-vnc
```