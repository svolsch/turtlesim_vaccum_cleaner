# turtlesim_vaccum_cleaner

ROS Turtlesim Package

Developed by svolsch (GitHub) - Aditya Dhiman
GitHub - https://github.com/svolsch/turtlesim_vaccum_cleaner
Demo Link - https://youtu.be/xPvrKR9F-n4

Package Name - learning_pkg
ROS distro - noetic

Launch files description:

1. To launch turtlesim vaccum cleaning behavior that clean the turtlesim window - 
    >> roslaunch learning_pkg cleaner.launch 

        -> The turtlesim window will be launched and spawn 3 turtles in different location.
        -> Pen color set to white to specify clean area.
        -> Pen width set to 30. 
        -> Turtles avoid collision with the wall and with each other.
        -> As soon as the turtles get near to the wall or other Twist command is published to turn them in a different direction.
        -> Algorithm optimized to cover the whole turtlesim window in an efficient manner.
        -> Operation runs till Ctrl + C is pressed to shut down excecution. 

2. To launch autonomous navigation to entered coordinate - 
    >> roslaunch learning_pkg nav_to_cord.launch 
    
        -> Turtlesim window is launched alongwith a terminal window to input x,y coordinates and tolerance to move the turtle.
        -> Turtle uses Proportional control to move. The linear speed will consist of a constant multiplied by the distance between the turtle and the goal  and the angular speed will depend on the arctangent of the distance in the y-axis by the distance in the x-axis multiplied by a constant. 
        -> Use of euclidean_distance method to calculate point to point distance between the turtle ang the goal position.
        -> If the tolerance is set to a really small amount for eg. 0.01 the turtle will move in crazy motion. 
        -> As soon as the values are entered turtle moves towards the goal point ant achieve it's goal position. 
        -> Press Ctrl + C to exit session

3. To launch a teleoperator node that lets the user set speed of the turtle during the teleoperation session:
    >> roslaunch learning_pkg teleop.launch 

       -> Turtlesim window is launched with a turtle spawned in the centre of the window
       -> Another terminal window is opened that takes in linear and angular velocity from the user for the current teleoperation session.
       -> Turtle moves using the arrow keys with the entered speed.  
       -> Turtle moves only when the keys are pressed, as soon as the keys are released the turtle stops moving. 
       -> Press Ctrl + C to exit the session

       


