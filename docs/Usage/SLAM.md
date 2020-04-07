Localization Module
===


---
<!-- 請參考 https://elsa-lab.github.io/training-noodles/guide/installation.html -->

### Set up Map File

Move your map file (`file.bin`) to `home` directory.

```bash
$ cp path_to_your_map/file.bin ~/
```

### Set up Environment

```bash
$ export ROS_PACKAGE_PATH=path_to_workspace/catkin_ws/src/ORB_SLAM2/Examples/ROS/ORB_SLAM2:${ROS_PACKAGE_PATH}'
```

### Run ORB-SLAM2

Run ORB SLAM2 with the following command.
```bash
$ rosrun ORB_SLAM2 Monopub path_to_ORBvoc path_to_setting_yaml -1 camera_topic
```

In our situation, the command is : 

```bash
$ ~/Desktop/catkin_ws/src/ORB_SLAM2/Examples/ROS/ORB_SLAM2/Asus.yaml -1 /zed/left/raw_image'

```

---

### Run pose convertor

convert the ORB SLAM2 pose to rviz coordination.