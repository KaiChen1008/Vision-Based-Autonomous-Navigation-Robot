Control Policy Module
===


## Launch RL Module

Run the `control_policy.py` script to load the trained model and process the images. 

RL module would receive images from perception module and output corresponding actions to the AGV controller.

First of all, launch ROS in the terminal:

```bash
$ roscore
```

Then, you need to activate the RL environment:

```bash
# Activate the RL Envrionment
$ source rlenv/bin/activate
```

After activation, use the following command to execute our code.

> Argument:

```
--port: Port that connect to the perception module.
If not specified, runs on default arguments.
```

> Usage Example :
```bash
# Run listener.py
(rlenv)$ python3 control_policy.py --port=5555
```

---

## Launch Goal-Receiver 

Goal-Receiver will receive a success message when the AGV reaches the goal. After that, the message will be sent to the AGV controller immediately to stop the AGV.

> Argument:
```
--port: Port that connect to the planner module.
If not specified, runs on default arguments.
```


> Usage Example:
```bash
(rlenv)$ python goal_converter.py --port=7777
```
---

## Launch AGV Controller
Run the `controller.py` script to launch the  AGV controller.

```bash
(rlenv)$ python controller.py
```
