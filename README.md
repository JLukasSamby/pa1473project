# PA1473 - Software Development: Agile Project 


## Introduction
The program intends for two connected EV3 robot arms to sort lego bricks of type 3003 of different color together. The program is most easily used with pybricks and VSCode. Please see the pybricks docs for additional information about the EV3 system and its capabilities: https://pybricks.com/ev3-micropython/.


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
To get started, you’ll need:

    A Windows 10 or Mac OS computer

    Internet access and administrator access

        This is required during the installation only. You will not need special access to write and run programs later on.

    A microSD card

        You’ll need a card with a minimum capacity of 4GB and a maximum capacity of 32GB. This type of microSD card is also known as microSDHC. We recommend cards with Application Performance Class A1.

    A microSD card slot or card reader in your computer

        If your computer does not have a (micro)SD card slot, you can use an external USB (micro)SD card reader.

    A mini-USB cable, like the one included with your EV3 set

Read full guide here:
https://pybricks.com/ev3-micropython/startinstall.html#updating-the-microsd-card

#### with a computer
With a computer you can either upload and run code with bluetooth or a cable connected to the ev3 hub. 
Preparing your computer

You’ll write your MicroPython programs using Visual Studio Code. Follow the steps below to download, install, and configure this application:

    1) Download Visual Studio Code.
    2) Follow the on-screen instructions to install the application.
    3) Launch Visual Studio Code.
    4) Open the extensions tab.
    5) Install the EV3 MicroPython extension as shown in Figure 2.

Read full guide here:
https://pybricks.com/ev3-micropython/startrun.html
#### runing code in ev3dev
If code is already uploaded to the ev3 hub it can be run using the hub. See https://pybricks.com/ev3-micropython/startbrick.html.

You can press the F5 key in VSCode to run the program. Alternatively, you can start it manually by going to the debug tab and clicking the green start arrow, as shown in Figure 13.
When the program starts, a pop-up toolbar allows you to stop the program if necessary. You can also stop the program at any time using the back button on the EV3 Brick.

If your program produces any output with the print command, this is shown in the output window.

### Connecting server and client
To have the robots work as intended, please use two identical robots. They must be connected using
bluetooth which can be done in their corresponding ev3 hub menus. See https://pybricks.com/ev3-micropython/messaging.html.


## Program description
The purpose of the program is to sort large 2x2 lego bricks (Lego brick 3003) of different colors {Black, Blue, Green, Red, Yellow}. This is done by configuring zones where to sort the different bricks using two connected robot arms. The two Robot arms should be connected through bluetooth via the EV3 Hub interface. 

The program is split into two files. If observing the robots from the south with the arm north and ev3 hub south, then the western robot is the client and the eastern is the server. The client should run the `sorter_client.py` file and the server should run the `sorter_server.py` file. The server will handle Green, Red and Yellow bricks and the client Black and Blue bricks. 

When starting the programs the robots will attempt to connect to each other. If successful they will both proceed with an initialization procedure. After the initialization is done, 3 zones must be configured for both robots and then placing a brick inbetween the robots should have them sort the brick together (if the brick is Green, Red or Yellow the server will sort it, and otherwise the client will be told to sort it). When a brick is sorted the server will prompt the user that it is `waiting for next brick`, please place a new brick to continue sorting. If no brick is placed within 5 seconds, the robot will continue to loop and wait for a new brick to sort. To abort the procedure use the interface on the EV3 Hubs or cancel the program from the computer.
    

## Building and running

### Connecting the robots
To connect the robots please navigate the bluetooth menus. If the robots have been used before it might be easiest to remove all other bluetooth devices before setting one of the robots to visible, this way its clear which is the robot supposed to be connected to. After successful connection there will be a prompt on both EV3 Hubs, the prompt will ask to accept connection, please accept the connection to proceed. For more information please read the EV3 Documentation and specifically see: https://pybricks.com/ev3-micropython/messaging.html.

### Starting the program
Please refer to the pybricks documentation for a detailed guide. Documentation: https://pybricks.com/ev3-micropython/startrun.html. 

### Starting Order
It is recommended to start the server program first and wait until notified with `waiting for connection`. Then please start the client program.

### Server Robot
When the connection is finished and initialization of the server robot is done 3 zones need to be manually configured using the buttons on the EV3 Hub. The left and right buttons will rotate the robot counter-clockwise and clockwise respectively (seen from above), the up and down buttons will move the crane arm up and down to select a specific height. Note that it is important to select the specific height, for example, if the height is left unchanged the robot will drop the item at that height even though there is no platform at that height! When the robot arm is in the intended position please press the center button that will commmit the position. The first position commited will corresponds to that sorting Green bricks, the second for Yellow bricks and the third for Red bricks. When configuration of the server robot is done the robot will wait for the client to finish configuration before prompting the user to provide a brick for sorting.

### Client Robot
Just as with the server robot after initialization 3 zones must be configured in the same way. The first zone is the pick up zone. Please configure this zone to be the starting zone of the client robot, it might be easiest to configure this zone while configuring one of the other zones of the server robot as it can be manually moved out of the way. The second zone corresponds to the sorting location of Blue bricks and the last of Black bricks. After finishing configuration please continue.

### During Pick Up
The server robot will always check if there is an item present at the pick up location. If there is an item present the server robot will try to sort that item among its positions. Specifically it will determine if the color of the brick is either Green, Yellow or Red. If it is not the brick will once again be placed in the pick-up zone. Since the brick could not be sorted by the server robot it will move out of the way and message the client robot to sort the brick instead. If the client robot cannot sort the brick the program will shut down. Otherwise the client robot will sort the brick. 

After successful sorting by either the client or server robot, the server robot will get ready to pick up the next brick and the user will be notified of this. Please place the next brick in the pick up zone. If not done within the designated period of 5 seconds, the server will still attempt to pick up the item, if no item is found the robot will wait another 5 seconds and try again. When a brick is found it will be sorted as described above. This procedure will loop indefinitely. 

Import note! The robot is not aware of how many brick has been sorted in each position and will assume that a brick is removed from the sorting location after sorting. I.e., if sorting two red bricks in a row the robot might attempt to crush the first brick if it is not moved out of the way. 

### Shut Down
It is simple to shut down the procedure, please shut down the robots using the EV3 Hub as described in the documentation or cancel the debugging session started in VSCode (if VSCode is used).

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
