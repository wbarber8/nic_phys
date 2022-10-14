import pigpio
import time
from multiprocessing import Queue

class receiving:
    
    def __init__(self, port, time_delay):
        self.port = port
        self.NIC_port = self.assign_NIC_port()
        self.pi = pigpio.pi()
        self.pi.set_mode(self.port, pigpio.INPUT)
        self.time_delay = time_delay
        self.bit_string = ""
        self.bit_message = ""
        self.latest_bit = "0"
        self.queue = Queue()
    
    def receive(self):
        while (True) :
            clear = self.pi.read(self.port)
            if(clear == 0):
                #print("Clear: "+ str(self.NIC_port) + str(clear))
                break
        while (True) :
            read = self.pi.read(self.port)
            #print("reading")
            if (read != int(self.latest_bit)) :
                #print("Indicator: " + str(read))
                time.sleep(self.time_delay)
                self.latest_bit = str(self.pi.read(self.port))
                #print("Value: " + self.latest_bit)
                self.bit_string = self.bit_string + self.latest_bit
                #print("Bit string: " + self.bit_string)
                if (len(self.bit_string) >= 9):
                    closer = self.bit_string[len(self.bit_string) - 9 : ]
                    #print(closer)
                    if (closer == "100000000"):
                        self.bit_string = str(self.NIC_port) + self.bit_string
                        self.queue.put(self.bit_string)
                        self.bit_string = ""
     
    def get_queue(self):
        msg = self.queue.get()
        return msg
    
    def assign_NIC_port(self):
        if (self.port == 26):
            return 1
        elif (self.port == 24):
            return 2
        elif (self.port == 22):
            return 3
        else:
            return 4

    def get_size(self):
        return self.queue.qsize()
