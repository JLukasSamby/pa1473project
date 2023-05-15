# PA1473 - Software Development: Agile Project 


## Introduction
this project goes out on to make use of a lego ev3dev to perform varoius task in the form of user stories.The task ranges from picking up item and sorting based the color of the items.
The project also goes into the communication between two diffrent ev3 robots.


## Getting started

### The robot
The used robot is similar to the H25 as seen in the ev3 docs: https://pybricks.com/ev3-micropython/examples/robot_arm.html.
An important difference being the placement of the color sensor in the bottom of the crane arm to identify
the colors of bricks held by the claw.

### Coding enviroment
We recommend using VisualStudio Code as the platform for working with the ev3 robot. 
With the extension 'LEGO® MINDSTORMS® EV3 MicroPython' to able to run your code on the ev3dev.
For a more in depth guide on how to setup EV3 Micropython see the ev3 docs: https://pybricks.com/ev3-micropython/startrun.html.

### Robot setup
The robots can be set up in multiple ways.


#### with a computer
With a computer you can either upload and run code with bluetooth or a cable connected to the ev3 hub. 
Preparing your computer

You’ll write your MicroPython programs using Visual Studio Code. Follow the steps below to download, install, and configure this application:

    1) Download Visual Studio Code.
    2) Follow the on-screen instructions to install the application.
    3) Launch Visual Studio Code.
    4) Open the extensions tab.
    5) Install the EV3 MicroPython extension as shown in Figure 2.


#### runing code in ev3dev
If code is already uploaded to the ev3 hub it can be run using the hub. See https://pybricks.com/ev3-micropython/startbrick.html.

You can press the F5 key in VSCode to run the program. Alternatively, you can start it manually by going to the debug tab and clicking the green start arrow, as shown in Figure 13.
When the program starts, a pop-up toolbar allows you to stop the program if necessary. You can also stop the program at any time using the back button on the EV3 Brick.

If your program produces any output with the print command, this is shown in the output window.

### Connecting server and client
To have the robots work as intended, please use two identical robots. They must be connected using
bluetooth which can be done in their corresponding ev3 hub menus. See https://pybricks.com/ev3-micropython/messaging.html.


## Program description
The program is split into two files. If observing the robots from the south with the arm south and ev3 hub north, then the western robot is the client and the eastern is the server. 
    

## Building and running
### Shared runned 
If using the the two communication function for the robots, the robots when run will wait on the other robot to run too. after both robots are conncted and sends to the user that they are connected.they will start there init() fucnition which resets robot to there defult postions.
### Client robot    
There from the the client robot with the use of the button interface of the ev3 pick the postion(height,angle) of the pickup zone it willl share with the server, and then you will choose 2 drop off zones for the robot.
### Server robot
The server robot has it's defult postion, it only need with the same kind of button interface choose 3 drop off zones.

### After set up:
The server robot will start to try to pick up the item in the pickup zone,it will see what color it is, check if that said color is one part of its color to sort, if true it will sort it at that color asigned drop of zone. if false the robot will place the item down on the pick up zone.
and move away and give the client robot signal for it to pick up the item.
Client will check the brick to see if its one its color to sort if true it places the item in its respictive drop off zone, if false it "throws" the item away.
Will wait for the server to look at a new brick. 	  


## Features

Lastly, you should write which of the user stories you did and didn't develop in this project, in the form of a checklist. Like this:

- [x] US01: As a customer, I want the robot to pick up items 
- [x] US01B: As a customer, I want the robot to pick up items from a designated position 
- [x] US02: As a customer, I want the robot to drop off items
- [x] US02B: As a customer, I want the robot to drop items off at a designated position. 
- [x] US03: As a customer, I want the robot to be able to determine if an item is present at a given location.
- [x] US04: As a customer, I want the robot to tell me the color of an item.
- [x] US04B: As a customer, I want the robot to tell me the color of an item at a designated position. 
- [x] US05: As a customer, I want the robot to drop items off at different location based on the color of the item.
- [x] US06: As a customer, I want the robot to be able to pick up items from elevated positions.
- [x] US08 As a customer, I want to be able to calibrate maximum of three different colors and assign them to specific drop-off zones.
- [x] US08B As a customer, I want to be able to calibrate items with three different colors and drop the items off at specific drop-off zones based on color. 
- [x] US09: As a customer, I want the robot to check the pickup location periodically to see if a new item has arrived. 
- [x] US10: As a customer, I want the robots to sort items at a specific time. 
- [x] US11: As a customer, I want two robots to communicate and work together on items sorting without colliding with each other. 
- [x] US12: As a customer, I want to be able to manually set the locations and heights of one pick-up zone and two drop-off zones. (Implemented either by manually dragging the arm to a position or using buttons) 
