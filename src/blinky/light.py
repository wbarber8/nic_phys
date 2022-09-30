from api import *

while(True):
    bit = input("Enter a 4 bit value: ")
    nic_send(bit)
    print(nic_recv())
