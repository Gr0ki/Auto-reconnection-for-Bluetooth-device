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

def attempts_to_pair(counter):
# Recursive function decrementing the counter to 0, the rule may be broken if the attempt was successful
    attempt_result = pair_device()
    if counter > 1 and attempt_result != 0:
        time.sleep(1)                               # Delay is for scanning (in child process)
        return attempts_to_pair(counter - 1)
    else:
        return attempt_result

def connect():
    command = 'bluetoothctl connect ' + MAC_ADDRESS
    _ = os.system(command)

def set_as_trusted():
    command = 'bluetoothctl trust ' + MAC_ADDRESS
    _ = os.system(command)

def success_notification():
    _ = os.system('notify-send -t 3000 "Script" "Success!"')

def failure_notification():
    _ = os.system('notify-send -t 3000 "Script" "Failure!"')

def select_notification(case):
    if case == 0:
        success_notification()
    else:
        failure_notification()


bluetooth_reboot()
time.sleep(4)                                       # Delay is needed for bluetooth to turn on
remove_device()

pid = os.fork()                                     # Fork is for ability to stop scanning for bluetooth devices
child_pid = 0
if pid > 0:
    # Here is parent process
    time.sleep(5)                                   # Delay is for scanning (in child process)
    command_result = attempts_to_pair(5)
    connect()
    set_as_trusted()
    select_notification(command_result)
    command = 'kill '+ str(child_pid)
    os.system(command)
else:
    # Here is child process
    child_pid = os.getpid()
    scan_on()
