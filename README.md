# nic_phys

Authors: Will Barber and Luca Espinosa
Languages Used: Python

Files:
README.md - this readme file
released_to.txt - anyone this code is released to
src/blinky/api.py - library module provides send and receives methods
src/blinky/blinky.py - experimenting with blinking the lights
src/blinky/light.py - main file that runs the functions in api.py
src/chat/send.py - contains the logic for sending a message as bits across the link layer
src/chat/receive.py - contains the logic for receiving the message and displaying it to the user
src/chat/run_chat.py - main file that uses threads to run send and receive at the same time
