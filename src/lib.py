import time
from multiprocessing import Process, Queue
from receive import receiving
import pigpio


class library:
    def __init__(self,username):
        self.pi = pigpio.pi()

        self.username = username + ": "
        
        # Writing: Ports we will be reading from
        self.pt1_r = 26
        self.pt2_r = 24
        self.pt3_r = 22
        self.pt4_r = 20
        
        # Sending: Ports we will be writing to
        self.pt1_w = 27
        self.pt2_w = 25
        self.pt3_w = 23
        self.pt4_w = 21
        
        self.pi.set_mode(self.pt1_w, pigpio.OUTPUT)
        self.pi.set_mode(self.pt2_w, pigpio.OUTPUT)
        self.pi.set_mode(self.pt3_w, pigpio.OUTPUT)
        self.pi.set_mode(self.pt4_w, pigpio.OUTPUT)
        
        self.indicator_time_delay = 0.01
        self.receive_time_delay = 0.02
        self.value_time_delay = 0.03
        self.clear_output_delay = 0.04
        #self.indicator_time_delay = 0.05
        #self.receive_time_delay = 0.1
        #self.value_time_delay = 0.15
        #self.clear_output_delay = 0.2

        # Create instance of receive.py for each output port
        self.pt1_receive = receiving(self.pt1_r, self.receive_time_delay)
        #self.pt2_receive = receiving(self.pt2_r, self.receive_time_delay)
        self.pt3_receive = receiving(self.pt3_r, self.receive_time_delay)
        self.pt4_receive = receiving(self.pt4_r, self.receive_time_delay)
        
        
        self.pt1_receive_thread = Process(target = self.pt1_receive.receive)
        #self.pt2_receive_thread = Process(target = self.pt2_receive.receive)
        self.pt3_receive_thread = Process(target = self.pt3_receive.receive)
        self.pt4_receive_thread = Process(target = self.pt4_receive.receive)

         
        self.pt1_receive_thread.start()
        #self.pt2_receive_thread.start()
        self.pt3_receive_thread.start()
        self.pt4_receive_thread.start()

        self.receive_queue = Queue()
        self.send_queue = Queue()
        
    def lib_receive(self):
         
        
        while(True):
            for i in range( self.pt1_receive.get_size()):
                pt1_msg = self.pt1_receive.get_queue()
                self.receive_queue.put(pt1_msg)
            '''
            for i in range( self.pt2_receive.get_size()):
                pt2_msg = self.pt2_receive.get_queue()
                self.receive_queue.put(pt2_msg)
            '''   
            for i in range( self.pt3_receive.get_size()):
                pt3_msg = self.pt3_receive.get_queue()
                self.receive_queue.put(pt3_msg)
            
            for i in range( self.pt4_receive.get_size()):
                pt4_msg = self.pt4_receive.get_queue()
                self.receive_queue.put(pt4_msg)
                  
            while(self.receive_queue.empty() == False):
                bin_message = self.receive_queue.get()
                #print("Message: " + bin_message)
                self.interpret_message(bin_message)
                self.send_queue.put(bin_message)

    # For turning binary messages into characters
    def interpret_message(self, bin_message):
        bin_message = bin_message[1:len(bin_message)-9]
        result_string = ""
        
        for i in range(int(len(bin_message)/9)):
            char = bin_message[i*9:(i*9)+8]
            char = "0b" + char
            result_num = int(char, 2)
            result_char = chr(result_num)
            result_string = result_string + result_char 
        print(result_string)

    def lib_send(self):
        self.pi.write(self.pt1_w, 0)
        self.pi.write(self.pt2_w, 0)
        self.pi.write(self.pt3_w, 0)
        self.pi.write(self.pt4_w, 0)
        
        while(True):
            while(self.send_queue.empty() == False):
                bin_message = self.send_queue.get()
                self.send_message(bin_message)
    
    def send_message(self, bin_message):
        # clears receiver
        self.pi.write(self.pt1_w, 0)
        self.pi.write(self.pt2_w, 0)
        self.pi.write(self.pt3_w, 0)
        self.pi.write(self.pt4_w, 0)
        time.sleep(self.clear_output_delay)
        sending_indicator = 1
        #print("Binary message: " + bin_message)
        input_port = 0
        if (len(bin_message)%9 != 0):
            input_port = int(bin_message[0])
            bin_message = bin_message[1:]
        #print(bin_message)
        bin_message = [*bin_message]
        for value in bin_message:
            self.send_value(value, sending_indicator, input_port)
            sending_indicator = self.switch_indicator(value, sending_indicator)
    
    def send_value(self, value, indicator, input_port):
        #print("Printing input port: " + str(input_port))
        if (input_port != 1):
            # Send to port 1
            self.pi.write(self.pt1_w, indicator)
            #print("Pt 1 Send Indicator: " + str(indicator))
            time.sleep(self.indicator_time_delay)
            self.pi.write(self.pt1_w, int(value))
            #print("Pt 1 Send Value: " + value)
        
        if (input_port != 2):
            # Send to port 2
            self.pi.write(self.pt2_w, indicator)
            #print("Pt 2 Indicator: " + str(indicator))
            time.sleep(self.indicator_time_delay)
            self.pi.write(self.pt2_w, int(value))
            #print("Pt 2 Value: " + value)
        
        if (input_port != 3):
            # Send to port 3
            self.pi.write(self.pt3_w, indicator)
            #print("Pt 3 Indicator: " + str(indicator))
            time.sleep(self.indicator_time_delay)
            self.pi.write(self.pt3_w, int(value))
            #print("Pt 3 Value: " + value)
        
        if (input_port != 4):
            # Send to port 4
            self.pi.write(self.pt4_w, indicator)
            #print("Pt 4 Indicator: " + str(indicator))
            time.sleep(self.indicator_time_delay)
            self.pi.write(self.pt4_w, int(value))
            #print("Pt 4 Value: " + value)
        
        time.sleep(self.value_time_delay)
    
    def switch_indicator(self, value, indicator):
        if (int(value) == 1):
            indicator = 0
        else:
            indicator = 1
        return indicator
    
    # For adding entries (words) to the send queue
    def add_send_queue(self, message):
        message = self.username + message
        bin_message = self.convert_to_bin(message)
        self.send_queue.put(bin_message)
        
    def convert_to_bin(self, message):
        message = [*message]
        bin_message = ""
        for char in message:
            ascii_char = ord(char)
            bin_char = bin(ascii_char)
            bin_char = bin_char[2:]
            bin_char = self.eight_bit(bin_char)
            bin_message = bin_message + bin_char + "1"
        
        # attach the closer of 100000000
        bin_message = bin_message + "100000000"
        return bin_message
    
    def eight_bit(self, char):
        if (len(char) < 8):
                for i in range(8-len(char)):
                    char = "0" + char
        return char

    def shut_down(self):
        self.pi.write(self.pt1_w, 0)
        self.pi.write(self.pt2_w, 0)
        self.pi.write(self.pt3_w, 0)
        self.pi.write(self.pt4_w, 0)
        self.pt1_receive_thread.kill()
        #self.pt2_receive_thread.kill()
        self.pt3_receive_thread.kill()
        self.pt4_receive_thread.kill()




