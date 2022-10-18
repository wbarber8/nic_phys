# Raspberry Pi Computer Network

Authors: Will Barber and Luca Espinosa
Languages Used: Python

This repository contains our three main projects for this class. In the Blinky folder, we have code that enables the NIC lights to blink on and off. The Chat folder contains our Pairwise Communication chat between two Pis. Finally, our Network folder contains our Multi User Chat Room that can be run on more than two Pis at the same time.

Files:
README.md - this readme file.
released_to.txt - anyone this code is released to.
src/blinky/api.py - library module provides send and receives methods.
src/blinky/blinky.py - experimenting with blinking the lights.
src/blinky/light.py - main file that runs the functions in api.py.
src/chat/send.py - contains the logic for sending a message as bits across the link layer.
src/chat/receive.py - contains the logic for receiving the message and displaying it to the user.
src/chat/run_chat.py - main file that uses threads to run send and receive at the same time.
src/network/lib.py - contains different Processes for each port to send and receive from.
src/network/receive.py - receives messages and adds them to the Queue.
src/network/run_chat.py - contains a Receive Process and a Send Process to run simultaneously.
