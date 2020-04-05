Control Policy Module
===
###### tags: `專題` `Sim-to-Real` `Virtual Guidance`

[TOC]


## Launch RL Module

<font color="red">Run the `control_policy.py` script to load the trained model and process the images. </font>

RL module would receive images from perception module and output corresponding actions to the AGV controller.

First of all, launch ROS in the terminal:

```
$ roscore
```

Then, you need to activate the RL environment:

```python
# Activate the RL Envrionment
$ source rlenv/bin/activate
```

After activation, use the following command to execute our code.

<font color="red">Argumnt:</font>
```
--port: Port that connect to the perception module.
If not specified, runs on default arguments.
```

<font color="red">Example Usage:</font>
```
# Run listener.py
(rlenv)$ python3 control_policy.py --port=5555
```

---

## Launch Goal-Receiver 

Goal-Receiver will receive a success message when the AGV reaches the goal. After that, the message will be sent to the AGV controller immediately to stop the AGV.

<font color="red">Argumnt:</font>
```
--port: Port that connect to the planner module.
If not specified, runs on default arguments.
```


<font color="red">Example Usage:</font>
```
(rlenv)$ python goal_converter.py --port=7777
```
---

## Launch AGV Controller
Run the `controller.py` script to launch the  AGV controller.

```python
(rlenv)$ python controller.py
```
