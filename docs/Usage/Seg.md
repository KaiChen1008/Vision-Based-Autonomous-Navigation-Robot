Perception Module
===


---
<!-- 請參考 https://elsa-lab.github.io/training-noodles/guide/installation.html -->


### Run perception module
> Arguments:
```
--model: i or indoor for indoor model trained on ADE20K dataset,
         o or outdoor for outdoor model trained on Cityscapes datset
--output_ip: zmq sender ip to the control policy module
--output_port: zmq sender port to the control policy module
--input_ip: zmq listener ip from the camera and planner
--input_port: zmq listener port from the camera and planner
If not specified, runs on default arguments.
```

> Usage Example: 
```bash
python perception.py --model=outdoor --input_ip=192.168.0.125 --input_port=6666 --output_ip=192.168.0.198 --output_port=5555

python perception.py -m outdoor -ip 192.168.0.125 -io 6666 -op 192.168.0.198 -oo 5555
```



---
