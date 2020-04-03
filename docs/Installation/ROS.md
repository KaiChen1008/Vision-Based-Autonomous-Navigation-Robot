ROS
===

---
<!-- 請參考 https://elsa-lab.github.io/training-noodles/guide/installation.html -->

### Prerequisites

OS: Ubuntu 18.04

---

### Install through Script
We provide a bash script to install ROS Melodic. Please clone the following git repository and run the command.

```bash
git clone https://github.com/KaiChen1008/install-ROS
cd install-ROS 
chmod +x install-ROS
./install-ROS [ROS-keygen]
```

!> You can find the keygen in [ROS installation website](http://wiki.ros.org/melodic/Installation/Ubuntu).

![](https://i.imgur.com/aoVbqIw.png)

---

### Install Manually

Setup your computer to accept software from packages.ros.org
```bash
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'

```

Find the keygen in [ROS installation website](http://wiki.ros.org/melodic/Installation/Ubuntu).

![](https://i.imgur.com/aoVbqIw.png)


Set up the ROS keygen.

```
sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key [KEYGEN]
```

Install ROS Melodic.
```
sudo apt-get install -y ros-melodic-desktop-full
```

Install dependencies.

```
sudo apt-get install -y ros-melodic-desktop-full
sudo apt-get install -y doxygen


pip install catkin_pkg
pip3 install catkin_pkg
```
---

### Set up ROS

Initialize ROS.

```
sudo rosdep init
rosdep update
```

Set up environment.
```
echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc
source ~/.bashrc
```


Install dependencies.
```
sudo apt install -y python-rosinstall python-rosinstall-generator python-wstool build-essential
```


---

### Create a Workspace

Set up a catkin workspace.

```
mkdir ~/catkin_ws
cd ~/catkin_ws
mkdir src
catkin_make

```
---