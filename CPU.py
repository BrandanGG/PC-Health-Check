import psutil
import re

# How many cores
def core_count():
    return psutil.cpu_count()


# return list of information on each core
def core_info():
    scputimes = str(psutil.cpu_times_percent(interval=1, percpu=True)) # Turn into str type so I can alter the string
    starting = 1 # Starting index
    ending = scputimes.index(']')-1 # Ending index
    scputimes = scputimes[starting:ending]
    scputimes += '),' # to lazy to fix regex
    matches = re.findall(r'\((.*?)\)', scputimes) # Splitting the string based on what is inside the ()
    individual_cores = {i+1: match for i, match in enumerate(matches)} # Create and assign keys / values
    return individual_cores



# Captures the information from cpu_stats
# returns a dictionary created from CPU Stats
def boot_info():
    info = {}
    stats = str(psutil.cpu_stats())  # Create the string
    starting = stats.index("(") + 1  # Find the starting index
    ending = stats.index(")")  # Find the ending index
    sub = stats[starting:ending]  # Store the substring
    split = sub.split(", ")  # Split by commas
    # Loop through each item in the list, and assign to the dictionary key being the name and value being the count
    for item in split:
        key, value = item.split("=")
        value = '{:,}'.format(int(value))
        info[key.strip()] = value.strip()
    return info


# See what percentage of CPU is being used
# Works
def check_cpu_usage():
    usage = psutil.cpu_percent(1)
    return usage

core_info()