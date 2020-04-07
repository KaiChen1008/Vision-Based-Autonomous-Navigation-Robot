Robot Control
===

---
### Launch the AGV
Before making AGV start navigation, you need to activate AGV to receive message from other distributed devices.
Use ssh command to connect AGV device and execute the following commnad.


```bash
$ source rlenv/bin/activate
(rlenv)$ python others/huskyListener.py
```


Run the `controller.py`script in control policy module to start the nevigation. 

---

### Use Joystick To Control AGV

We also provide script that you can use joystick to control AGV. Please be sure you activate AGV device before using joystick.

Before execute our code, you need to install pygame libarary and download `communication.py` from our github repository.

```bash
$ pip install pygame
```
Plug your joystick device into any other devices and execute code.

```bash
$ roscore
$ cd others
$ python j.py
```
