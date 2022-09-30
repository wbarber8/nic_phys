import pigpio
import time


pi = pigpio.pi()

# target ports
input_port = 27
output_port = 26
pi.set_mode(input_port, pigpio.OUTPUT)
pi.set_mode(output_port, pigpio.INPUT)

# time between messages sent
indicator_time_delay = 0.001
value_time_delay = 0.003

def send():
    # clears receiver
    pi.write(input_port, 0)
    #print("Clear")
    sending_indicator = 1
    
    running = True
    while(running):
        message = input()
        message = convert_to_bin(message)
        message = [*message]
        for value in message:
            send_value(value, sending_indicator)
            sending_indicator = switch_indicator(value, sending_indicator)
        #print("MSG sent!")

def send_value(value, indicator):
    pi.write(input_port, indicator)
    #print("Indicator: " + str(indicator))
    time.sleep(indicator_time_delay)
    pi.write(input_port, int(value))
    #print("Value: " + value)
    time.sleep(value_time_delay)

def switch_indicator(value, indicator):
    if (int(value) == 1):
        indicator = 0
    else:
        indicator = 1
    return indicator

def convert_to_bin(message):
    message = [*message]
    bin_message = ""
    for char in message:
        ascii_char = ord(char)
        bin_char = bin(ascii_char)
        bin_char = bin_char[2:]
        bin_char = eight_bit(bin_char)
        bin_message = bin_message + bin_char + "1"
    
    # attach the closer of 100000000
    bin_message = bin_message + "100000000"
    return bin_message

def eight_bit(char):
    if (len(char) < 8):
            for i in range(8-len(char)):
                char = "0" + char
    return char

