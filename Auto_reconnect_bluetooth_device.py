#!/usr/bin/env python3

import os
import time

# Put the mac-address of the device you want to reconnect
MAC_ADDRESS = ''

def bluetooth_off():
    _ = os.system('rfkill block bluetooth')

def bluetooth_on():
    _ = os.system('rfkill unblock bluetooth')

def bluetooth_reboot():
    bluetooth_off()
    bluetooth_on()

def remove_device():
    command = 'bluetoothctl remove ' + MAC_ADDRESS
    _ = os.system(command)

def scan_on():
    _ = os.system('bluetoothctl scan on')

def pair_device():
    command = 'bluetoothctl pair ' + MAC_ADDRESS
    return os.system(command)

def connect():
    command = 'bluetoothctl connect ' + MAC_ADDRESS
    _ = os.system(command)

def set_as_trusted():
    command = 'bluetoothctl trust ' + MAC_ADDRESS
    _ = os.system(command)

def notification():
    _ = os.system('notify-send -t 3000 "Script" "I did my work here, check the result."')

def attempts_to_pair():
    counter = 0
    if pair_device() == 0 and counter >= 5:
        return
    else:
        counter += 1
        time.sleep(1)                   # Delay is for scanning (in child process)
        return attempts_to_pair()


bluetooth_reboot()
time.sleep(4)
remove_device()

pid = os.fork()                         # Fork is for ability to stop scanning for bluetooth devices
child_pid = 0
if pid > 0:
    # Here is parent process
    time.sleep(5)                       # Delay is for scanning (in child process)
    attempts_to_pair()
    connect()
    set_as_trusted()
    notification()
    command = 'kill '+ str(child_pid)
    os.system(command)
else:
    # Here is child process
    child_pid = os.getpid()
    scan_on()
