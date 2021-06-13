# Intro

Public code for an effective, easy-to-implement, and low-cost modular framework for robot navigation tasks.


[![documentation_link](https://img.shields.io/badge/docs-online-brightgreen.svg)](https://kaichen1008.github.io/Vision-Based-Autonomous-Navigation-Robot)

## Variants
- [Single Device Version](https://github.com/KaiChen1008/Sim-to-Real-Virtual-Guidance-for-Robot-Navigation) - The original one (reveive 48 stars)

We highly suggest to use the single-device one which is easier to install.


## Features

- Automatically navigate the robot to a specific goal without any high-cost sensors.
- Based on a single camera and use deep learning methods.
- Use Sim-to-Real technique to eliminate the gap between virtual environments and real world.
- Introduce "Virtual Guidance" to entice the agent to move toward a specific direction.
- Use Reinforcement learning to avoid obstacles while driving through crowds of people.

## Prerequisites

- Ubuntu 18.04
- gcc5 or higher
- Python 2.7.17 or higher
- Python 3.5 or higher

!> Both versions of Python required.

## How It Works

<!-- ![](https://i.imgur.com/fd0u5ws.png) -->

1. Our full architecture is split into four parts: the Perception module, Localization module, Planner module and Control policy module.
2.  The perception module translates the image into comprehensible segmented chunks
3. The Localization module calculates the agent’s position.
4. The Planner module generates a path leading to the goal. This path is then communicated to the control policy module via a “virtual guide”. 
5. The Control policy module then deploys deep reinforcement learning to control the agent. 

