from lib import library
from multiprocessing import Process

print("Chat opened")
print("Enter a username: ")
username = input()

lib = library(username)

receive_thread = Process(target = lib.lib_receive)
send_thread = Process(target = lib.lib_send)

receive_thread.start()
send_thread.start()

print("Enter message or /q to quit: ")
while(True):
    message = input()
    if message == "/q":
        lib.shut_down()
        receive_thread.kill()
        send_thread.kill()
        break
    else:
        lib.add_send_queue(message)

print("Chat closed")
