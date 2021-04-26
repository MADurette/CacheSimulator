#Date 1/11/2021
#Class CS 4541
#Assignment: Assignment 2
#Author: Marcus Durette 

#Test Commandline instruction (PATH for python is set to run Python3, enter below like this for it to work): 
#FOR WINDOWS MACHINE, Change Values and Path name Accordingly
python <FILELOCATION>\Ass2-CacheSimulator.py -v -s 2 -E 1 -b 4 -t traces\dave.trace

#BeforeConversation folder
the code in that folder represents what i had done before i got the main simulator working... due to the amount of time 
and stress i had right before i got it working i kept it in there because of paranoia for my grade. However with testing
all the answers came out correctly for the simulator program finalized. So as long as you do not find much issue then disregard that code

#References:
https://docs.python.org/3/

Example Trace Answers(From Program given to us):
dave = h:2 m:3 e:1
yi = h:4 m:5 e:2
yi2 = h:9 m:8 e:6

Easy Matchups for Small Traces:

Dave -
M
H
M
H
M

Yi - 
M
M H
H
H
M
M E
M E H

Yi2 - 
M
H
M
H
M E
H
M E
H
M E
H
M E
H
M E
H
ME
H H

#Rest of Answers to problems
The CacheCA.py file is made to give the correct answers if the known file is put in, not for grading but for testing and determining difference in correctness