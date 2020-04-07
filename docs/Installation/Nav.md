Navigation Package
===

---
<!-- 請參考 https://elsa-lab.github.io/training-noodles/guide/installation.html -->

### Installation Steps
1. Install **turtlebot3**.
```bash
$ sudo apt install ros-melodic-turtlebot3
```

2. Install **turtlebot3_navigation**.
```bash
$ sudo apt install ros-melodic-turtlebot3-navigation
```

3. Install **global_planner**.
```bash
$ sudo apt install ros-melodic-global-planner
```

4. Install **hector_slam**.
```bash
$ sudo apt install ros-melodic-hector-slam
```

5. Copy the provided **pose_tf** folder to **~/catkin_ws/src**.

6. Build the workspace.
```bash
$ cd ~/catkin_ws
$ catkin_make
```

7. Replace the **turtlebot3_navigation** and **turtlebot3_bringup** folders under **~/opt/ros/melodic/share** with the ones provided.
