# Getting Started

This is docker command
1. To pull images
```
docker pull osrf/ros:humble-desktop-full
```

2. To list out all the available images
```
docker list
```

3. To create container
```
docker run -it osrf/ros:humble-desktop-full
```

To run the container with r2_humble.
```
docker run --name r2_humble -it osrf/ros:humble-desktop-full
```

To run the container with display and name
```
docker run --name r2_humble -it -e DISPLAY=host.docker.internal:0.0 -it osrf/ros:humble-desktop-full
```

4. Check ubuntu version
```
lsb_release -a
```

5. To check what container is running now
```
docker ps
```

6.To produce interactive bash that point to same container. Name of docker is the ID
```
docker exec -it <name of docker> bash
```

7. To restart the docker with ID that previously close
```
docker restart aea45c71126a
docker exec -it aea45c71126a bash
```

8. To stop docker
```
docker stop aea45c71126a
```


