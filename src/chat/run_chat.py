from send import *
from receive import *
from threading import Thread

t1 = Thread(target = receive)
t2 = Thread(target = send)

t1.start()
t2.start()
