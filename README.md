# PA1473 - Software Development: Agile Project 


## Introduction
this project goes out on to make use of a lego ev3dev to perform varoius task in the form of user stories.The task ranges from picking up item and sorting based the color of the items.
The project also goes into the communication between two diffrent ev3 robots.


## Getting started
### The robot
the robot is a legoev3 with a functioning crane and claw.

### coding enviroment
using vscode as platform with the programming langue python.
With the extension 'LEGO® MINDSTORMS® EV3 MicroPython' to able to run your code on the ev3dev.


### setup robots.
The robots can be set up in multiple ways.

#### with a computer
with a computer you can either with bluetoth or cable connect to the robot to run your program on 

#### runing code in ev3dev
you can with either with the blutoth connecction or cable download your code to the robot to run.
in use when running mulipte robots without acces to mulitple computers to help run the robots.

### connecting server and client
with the function to use one robot as bluetooth host and other 
robot can then connect  to the first and start a connection.
this connection is used for the robots to send messages




## Building and running
### shared runned 
if using the the two communication function for the robots, the robots when run will wait on the other robot to run too. after both robots are conncted and sends to the user that they are connected.they will start there init() fucnition which resets robot to there defult postions.
### client robot    
there from the the client robot with the use of the button interface of the ev3 pick the postion(height,angle) of the pickup zone it willl share with the server, and then you will choose 2 drop off zones for the robot.
### server robot
The server robot has it's defult postion, it only need with the same kind of button interface choose 3 drop off zones.

### after set up:
the server robot will start to try to pick up the item in the pickup zone,it will see what color it is, check if that said color is one part of its color to sort, if true it will sort it at that color asigned drop of zone. if false the robot will place the item down onthe pick up zone.
and move away and give the client robot signal for it to pick up the item.	  


## Features

Lastly, you should write which of the user stories you did and didn't develop in this project, in the form of a checklist. Like this:

- [x] US01: As a customer, I want the robot to pick up items 
- [x]US01B: As a customer, I want the robot to pick up items from a designated position 
- [x]US02: As a customer, I want the robot to drop off items
- [x]US02B: As a customer, I want the robot to drop items off at a designated position. 
- [x]US03: As a customer, I want the robot to be able to determine if an item is present at a given location.
- [x]US04: As a customer, I want the robot to tell me the color of an item.
- [x]US04B: As a customer, I want the robot to tell me the color of an item at a designated position. 
- [x]US05: As a customer, I want the robot to drop items off at different location based on the color of the item.
- [x]US06: As a customer, I want the robot to be able to pick up items from elevated positions.
- [x]US08 As a customer, I want to be able to calibrate maximum of three different colors and assign them to specific drop-off zones.
- [x]US08B As a customer, I want to be able to calibrate items with three different colors and drop the items off at specific drop-off zones based on color. 
- [x]US09: As a customer, I want the robot to check the pickup location periodically to see if a new item has arrived. 
- [x]US10: As a customer, I want the robots to sort items at a specific time. 
- [x]US11: As a customer, I want two robots to communicate and work together on items sorting without colliding with each other. 
- [x]US12: As a customer, I want to be able to manually set the locations and heights of one pick-up zone and two drop-off zones. (Implemented either by manually dragging the arm to a position or using buttons) 