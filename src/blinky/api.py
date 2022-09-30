import pigpio
pi = pigpio.pi()

def nic_send(bit):
    if (check_bit(bit) == True):
        bits = [*bit]
        port_1 = int(bits[0])
        port_2 = int(bits[1])
        port_3 = int(bits[2])
        port_4 = int(bits[3])
        if (check_bits(port_1, port_2, port_3, port_4) == True):
            pi.set_mode(27, pigpio.OUTPUT)
            pi.set_mode(25, pigpio.OUTPUT)
            pi.set_mode(23, pigpio.OUTPUT)
            pi.set_mode(21, pigpio.OUTPUT)

            pi.write(27, port_1)
            pi.write(25, port_2)
            pi.write(23, port_3)
            pi.write(21, port_4)

        else:
            print("Please enter either 1 or 0")

    else:
        print("Please enter a 4 bit integer")

def nic_recv():
    pi.set_mode(26, pigpio.INPUT)
    pi.set_mode(24, pigpio.INPUT)
    pi.set_mode(22, pigpio.INPUT)
    pi.set_mode(20, pigpio.INPUT)

    port_1 = str(pi.read(26))
    port_2 = str(pi.read(24))
    port_3 = str(pi.read(22))
    port_4 = str(pi.read(20))

    new_bit = port_1 + port_2 + port_3 + port_4
    new_bit = int(new_bit)
    return new_bit

def check_bit(bit):
    if (type(int(bit)) == int and len(bit) == 4):
        return True
    else:
        return False

def check_bits(port_1, port_2, port_3, port_4):
    if (port_1 == 0 or port_1 == 1):
        if (port_2 == 0 or port_2 == 1):
            if (port_3 == 0 or port_3 == 1):
                if (port_4 == 0 or port_4 == 1):
                    return True
    else:
        return False
