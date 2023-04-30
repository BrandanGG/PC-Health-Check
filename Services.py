#!/usr/bin/env python3
# this is a health check for a computer
import psutil
import re
from pprint import pprint as pp


# This function is used to obtain all running services and store them in a dictionary. The key being the name and the
# value being the PID
# THIS WORKS!
def get_serivces():
    l = list(psutil.win_service_iter())  # Obtain the list of all services
    services = {}  # Storage for service name and PID
    for service in l:  # loop through each item in the list.
        match = re.search(r"name='(.*?)'", str(service))  # find the service name
        service_name = match.group(1)  # Assign the match
        z = psutil.win_service_get(service_name)  # get info on the specific service
        z = z.as_dict()  # turn the info above into a dictionary
        if z['pid'] is not None:
            services[z['display_name']] = z['pid']  # Take the display name as the key and pid as value and store into services
    return services


# Run the service information if the user wants to know what a specific PID is.
# generates readable information pertaining to the service in question.
# type check for pid is done in main. Method wont function unless typecheck returns int
# Works
def service_information(pid):
    if int(pid):
        if pid in get_serivces().values(): # checks if the pid is within the get_services returned dictionary.
            p = psutil.Process(pid) # create the process object.
        else:
            print("ERROR: INVALID PID")
        return p # Returns process object
    else:
        return # if for some reason the type check in main fails, nothing happens.


# Grabs processes using over 500Mbs of memory.
def mem_hungry_services():
    pp([(p.pid, p.info['name'], p.info['memory_info'].rss) for p in psutil.process_iter(['name', 'memory_info']) if
        p.info['memory_info'].rss > 500 * 1024 * 1024])




