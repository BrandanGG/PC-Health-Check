import psutil

print(psutil.cpu_freq())
print(psutil.cpu_stats())
print(psutil.cpu_times(percpu=True))
test = psutil.cpu_times()
print(psutil.cpu_times_percent(interval=1, percpu=True))


# How many cores
def core_count():
    return psutil.cpu_count()


# return list of information on each core
def core_info():
    pass


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


