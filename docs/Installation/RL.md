Control Policy Virtual Environment
===


---
<!-- 請參考 https://elsa-lab.github.io/training-noodles/guide/installation.html -->

### Prerequisites
1. Python 3.5 or higher
2. Linux-based terminal
3. ROS melodic version

---
### Create a Virtual Environment 
We recommend using a virtual environment to avoid any potential conflicts with your global configuration. 

First, create a virtual environment via virtualenv:
```bash
$ virtualenv -p=path-to-python3 rlenv
```

Activate the virtual environment:

```bash 
$ source rlenv/bin/acitvate
``` 


Then, install all required dependencies via pip:
```bash
(rlenv)$ pip install -r requirements.txt
```

You can exit your virtualenv after installation/using:
```bash
$ deactivate
```
---
