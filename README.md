# PA1473 - Software Development: Agile Project (Template)

## Template information
This template should help your team write a good readme-file for your project. (The file is called README.md in your project directory.)
You are of course free to add more sections to your readme if you want to.

Readme-files on GitHub are formatted using Markdown. You can find information about how to format using Markdown here: https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax

Your readme-file should include the following sections:


## Introduction
this project goes out on to make use of a lego ev3dev to perform varoius task in the form of user stories.The task ranges from picking up item and sorting based the color of the items.
The project also goes into the communication between two diffrent ev3 robots.


## Getting started

This section is supposed to guide a new developer through the steps of how to set up the project and install the deppendencies they need to start developing.


## Building and running
# shared runned 
if using the the two communication function for the robots, the robots when run will wait on the other robot to run too. after both robots are conncted and sends to the user that they are connected.they will start there init() fucnition which resets robot to there defult postions.
# client robot    
there from the the client robot with the use of the button interface of the ev3 pick the postion(height,angle) of the pickup zone it willl share with the server, and then you will choose 2 drop off zones for the robot.
# server robot
The server robot has it's defult postion, it only need with the same kind of button interface choose 3 drop off zones.

# after set up:
the server robot will start to try to pick up the item in the pickup zone,it will see what color it is, check if that said color is one part of its color to sort, if true it will sort it at that color asigned drop of zone. if false the robot will place the item down onthe pick up zone.
and move away and give the client robot signal for it to pick up the item.	  


## Features

Lastly, you should write which of the user stories you did and didn't develop in this project, in the form of a checklist. Like this:

- [x] US_1: As a user I want to...
- [ ] US_2: As a user I want to...
