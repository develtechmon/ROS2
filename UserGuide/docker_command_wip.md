1. docker image ls
2. docker image pull ros:humble
3. docker image ls
4. docker run -it ros:humble

inside humble terminal
ls /opt/ros

lsb_release -a

docker container ls --> To list down all the container that is running

Let's go back to container terminal

Now let's create file below
touch my_file
exit --> and stop the container

then run docker container ls --> you will see our container is no longer there.
To start the container run below command
docker run -it ros:humble --> run the container

You will notice now that "my_file" is no longer there.

To pull image
docker image pull ros:humble --- > this is <name>:<tag>

alternatively, you can use
docker pull ros:humble

To force remove
docker image rm -rf hello-world

To run 
docker run ros:humble --> useful if you want run the software once docker startup. This will create a new name everytime.
docker run -it ros:humble --> To have an interactive terminal 

Then create a file --> touch aaaa

Then in other container run:
docker container ls to see existing container

Then check the NAMES : huiii

To stop container:
docker stop huiii

or exit or type quit
you will see our huiii file is no longer available there

To check our running container
docker ps

To sell a container list and status
docker ps -a

TO start previous run container again
docker container start -i huiii

You will see our file is "huiiii" is stil there.

To exit:
ctrl + D or type quite

To remove container 
docker comtaomer rm huii

To remove all the container. you will see only running docker is available. 
docker container prune

To start the run the container with our custom name
docker exec -it hello /bin/bash
