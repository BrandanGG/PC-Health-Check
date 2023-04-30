import psutil
import General


# Returns total number of drives
def drive_count():
    disk_partitions = psutil.disk_partitions()
    return len(disk_partitions)


# Function used to loop through all the disks. and get the storage info for all of them
# Returns dictionary with Key being the mount point and value being the storage info
def storage_info():
    disk_partitions = psutil.disk_partitions()
    dictionary = {}
    for partitions in disk_partitions:
        l = [] # List that will be the value for the dictionary
        if 'cdrom' not in partitions.opts and partitions.fstype != '':
            disk_usage = psutil.disk_usage(partitions.mountpoint) # access to drive storage
            # Append drive storage info to the list
            l.append(General.bytes2human(disk_usage.total))
            l.append(General.bytes2human(disk_usage.used))
            l.append(General.bytes2human(disk_usage.free))
            l.append(disk_usage.percent)
            dictionary[partitions.mountpoint] = l # Mountpoint : List
    return dictionary


# Returns True or False based on the percent param... used to check storage %
# needs to be called for each specific mountpoint.
# returns true if theres a good amount of storage, false if the drive is getting too full, None if the drive is == percent
# mountpoint param needs to be structured as 'C:\\' the second \ is to cancel the escape
# Works
def good_storage_percent(percent:float, mountpoint:str):
    disk_partitions = psutil.disk_partitions() # Check how many drives there are
    for partitions in disk_partitions:
        if 'cdrom' not in partitions.opts and partitions.fstype != '': # If not network share or virtual drive
            if mountpoint == partitions.mountpoint:
                disk_usage = psutil.disk_usage(partitions.mountpoint) # access to drive storage
                if disk_usage.percent < percent:
                    return True
                elif disk_usage.percent == percent:
                    return None
                else:
                    return False
