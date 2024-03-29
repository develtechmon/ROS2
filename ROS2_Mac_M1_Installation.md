# Getting Started

This is userguide on how to install `ROS2 Humble` into my `Macbook M1`.

## Step 1: Install Homebrew

You can find any tutorial online on how to install `Homebrew` into you Macbook

## Step 2: Install `minconda`

Check this link for information
```
https://docs.anaconda.com/free/miniconda/#quick-command-line-install
```

In general, the step as follow.
```
Go to your home working directory

mkdir -p ~/miniconda3
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
```

After installing, initialize your installed `minconda`. The following command initialize `bash` and `zsh` shells
```
~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh
```

## Step 3: Install `ros2 humble`
To install ros2, we're going to use `RobotStack` flow. This is very helpful package.
See below link to find more on how to install the ros2 package
```
https://robostack.github.io/GettingStarted.html
```

After conda installation, you should see `(base)` terminal. Once you see this, run this command
```
conda install mamba -c conda-forge
```

Once done installing, next we're going to create our `ros2` environment using conda as follow
```
conda create -n ros2
conda activate ros2
```
You should see now you're in `(ros2)` environment instead of `(base)`. 
Inside this environment, run following command. 

```
conda config --env --add channels conda-forge
conda config --env --add channels robostack-staging
conda config --env --remove channels defaults
```

Install `ros2` as follow. This package installation might take some time.
```
conda install ros-humble-desktop
```
And install following packages
```
conda install compilers cmake pkg-config make ninja colcon-common-extensions catkin_tools rosdep
```

## Step 3: Install and setup `autocompletion` for our `ros2` environment

See below link to find the userguide
```
https://stackoverflow.com/questions/45947559/bash-conda-autocomplete-on-macos
```

While still inside our `ros` environment, install following packages.

```
conda install argcomplete
```

And add following into our `setup.bash`
```
open /Users/jlukas/miniconda3/envs/ros2/setup.bash

Add following line
eval "$(register-python-argcomplete conda)"
```

Complete code should look like following
```
# copied from ament_package/template/prefix_level/setup.bash

AMENT_SHELL=bash

# source setup.sh from same directory as this file
AMENT_CURRENT_PREFIX=$(builtin cd "`dirname "${BASH_SOURCE[0]}"`" && pwd)
# trace output
if [ -n "$AMENT_TRACE_SETUP_FILES" ]; then
  echo "# . \"$AMENT_CURRENT_PREFIX/setup.sh\""
fi
. "$AMENT_CURRENT_PREFIX/setup.sh"
eval "$(register-python-argcomplete conda)" <<----------- Like this !
```

Then `source` the `setup.bash`
```
source setup.bash
```

Now when type `ros2` and press `tab`, the autocompletion word should appear.

## Step 4: Test our `ros2`

Run following command

launch a demo node talker
```
ros2 run demo_nodes_cpp talker
```

from another terminal activate the conda env and launch a demo listener
```
ros2 run demo_nodes_cpp listener
```

And also launch below in other terminal of `ros2` environment
```
rviz2
```

It should work now !

## Step 5: Install `Gazebo` on Mac

Check this link on how to install it.
```
https://classic.gazebosim.org/tutorials?tut=install_on_mac
```

In general, the step is quite straightforward and might take some time. Chill up and get your milo during
the installation process.

To install, makesure you're in `(base)` environment. You might need to create new terminal for this step.

```
curl -ssL http://get.gazebosim.org | sh
```

Once installation complete, run following command
```
gazebo
```

## Step 6: Install packages

To install ros2 packages, please ensure you switch to `ros2` environment and install command as follow. 
Notice that we're using `conda install` instead of `sudo apt-get update` command. It should similar for rest of the package
```
conda install tree
conda install ros-humble-xacro
conda install ros-humble-joint-state-publisher-gui
conda install ros-humble-teleop-twist-keyboard
conda install ros-humble-teleop-twist-joy
conda install ros-humble-gazebo-ros-pkgs 
conda install ros-humble-robot-state
conda install joystick jstest-gtk evtest
conda install ros-humble-joy-tester
conda install v4l-utils
conda install ros-humble-twist-mux
```

