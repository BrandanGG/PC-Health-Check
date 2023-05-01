import psutil
import General
import subprocess
import re


# object that has information on swap memory
class swap:
    mem = psutil.swap_memory()
    total = General.bytes2human(mem.total)
    used = General.bytes2human(mem.used)
    free = General.bytes2human(mem.free)
    percent = General.bytes2human(mem.percent)


# Object that has information on virtual memory
class virtual:
    mem = psutil.virtual_memory()
    total = General.bytes2human(mem.total)
    used = General.bytes2human(mem.used)
    free = General.bytes2human(mem.free)
    percent = General.bytes2human(mem.percent)

# returns the size of each stick of ram
def ram_sticks():
    try: # windows command to return all memory information
        result = subprocess.run(['wmic', 'memorychip', 'list', 'full'], capture_output=True, text=True)
        matches = re.findall(r"Capacity=(\d+)", result.stdout) # finds all of the storage information
        ram_info = []
        count = 0
        for ram in matches: # add to the return list
            ram_info.append(General.bytes2human(int(ram)))
            count += 1
        return ram_info
    except FileNotFoundError:
        pass
