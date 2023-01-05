# Steps to configure

### clone the package to your home

```
cd
git clone https://github.com/Avi241/haptic_ws
```

### compile and source the package 

```
cd ~/haptic_ws
catkin_make
source devel/setup.bash
```

### Run the simulation assuming that both the falcon are connected first left then right is connected 

```
roslaunch haptic_pkg box_with_falcon.launch
```

### The main control script is box_with_falcon.py which is localted at  ~/haptic_ws/src/haptic_pkg/scripts . Edit this script according to you and run using the below command in new terminal



```
cd ~/haptic_ws
source devel/setup.bash
rosrun haptic_pkg box_with_falcon.py

```
