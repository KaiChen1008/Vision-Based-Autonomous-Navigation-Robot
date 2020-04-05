Planner Module
===
###### tags: `專題` `Sim-to-Real` `Virtual Guidance`

[TOC]

---
<!-- 請參考 https://elsa-lab.github.io/training-noodles/guide/installation.html -->


## Launch planner with Rviz
1. Run launch file to launch planner and Rviz.
```
$ roslaunch turtlebot3_navigation amcl_demo.launch
```
2. Change the global planner topic to **/move_base/GlobalPlanner/plan**.
![](https://i.imgur.com/BgUfY4v.png)

3. Click the **2D Nav Goal** button, then click on the desired destination on the map to generate a path. Beware that clicking on an obstacle is nonviable.
![](https://i.imgur.com/wjFrVxj.png)

**NOTE:** Always run the localization module before running the planner module.

