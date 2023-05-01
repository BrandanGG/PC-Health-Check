import sys
import re
import datetime as dt
import Services as s
import General as gen
import CPU as cpu
import ssdhdd as sh
import Memory
# This is strictly a windows program, may not function properly on linux or mac.


def pcharddrive():
    print(f"Hello {gen.get_user()}, lets take a look at your storage!\n"
          f"It looks like you have {sh.drive_count()} drives")
    storage = sh.storage_info()
    print(storage)
    for drive in storage:
        print(f"Your drive {drive}, has a total of {storage[drive][0]} and you've used {storage[drive][1]}\n"
              f"This means you've used {storage[drive][3]}%, leaving you with {storage[drive][2]}")
        if sh.good_storage_percent(70, drive):
            print("Great! Your hard drive is in good health and isn't close to being full!")
        else:
            print("Consider deleting some files or getting an additional hard drive")


def pcservices():
    services = s.get_serivces()
    print(f"""
    {gen.get_user()}, you currently have {len(services)} services running on your system. They are detailed below:
    ________________________________________________________________________________________________________________________
    """)
    for key, value in services.items():
        print(f"The service {key} is using the Process ID {value},")
    print(
        "\n \nNow that we have a list of all the running services on your system, lets take a look at what is using the most of your resources.")
    s.mem_hungry_services()
    print("Above is your memory hungry services.")
    # bool variable to determine if they want to find out more information on another service.
    # Restructure this whole thing, if int, check if valid pid, return PID information, ask again
    # if not int, end loop
    toContinue = True
    user_input = input(
        f"If you would like to know more about a specific process please enter the number Otherwise, say no")
    while toContinue is True:
        if user_input.isdigit():
            user_input = int(user_input)
            if user_input in services.values():
                p = s.service_information(user_input)
                print(f"""
                                {p.name()} is {p.status()} as of {dt.datetime.fromtimestamp(p.create_time())}
                                The location to launch this service is {p.exe()}
                                Other services that depend on {p.name()} is {p.children()}
                                Services that {p.name()} depends on is {p.parent()}
                                The service is using {p.memory_percent():.2f}% of your systems memory.""")
            else:
                print("Sorry, that PID isn't listed above.")
        try:
            if user_input[0].lower() == 'n':
                toContinue = False
                break
            else:
                print("Invalid Input...")
        except TypeError:
            pass
        user_input = input("Questions about another service? enter the PID, otherwise say 'No'")


def pcram():
    ram = Memory.ram_sticks()
    print(f"Hello {gen.get_user()}, lets take a look at your ram information\n"
          f"It looks like you have {len(ram)} sticks of ram installed on your machine")
    count = 0
    for stick in ram:
        print(f"Stick {count} has {stick} of memory")
        count += 1
    print("\n Now lets take a look at your virtual and swap memory."
          "\n Virtual memory is all the memory on your system and swap memory is the amount of memory that can be "
          "utilized for other computer functions rather than just ram")
    # object creation
    virtual = Memory.virtual()
    swap = Memory.swap()
    print(f"""

            VIRTUAL
            Your total memory is {virtual.total}
            You have {virtual.used} of used memory
            You've used {virtual.percent}% of your total memory
            You have {virtual.free} of free memory

            SWAP
            Your total memory is {swap.total}
            You have {swap.used} of used memory
            You've used {swap.percent}% of your total memory
            You have {swap.free} of free memory
    """)

def pccpu():
    print(f"Hello, {gen.get_user()}\n"
          f"You are currently using {cpu.check_cpu_usage()}% of your CPUs maximum capability.\n"
          f" This number is subject to change depending on how intensive the applications running on your computer are.")
    if cpu.check_cpu_usage() <= 70:
        print("It looks like your CPU useage is at a healthy level! Generally anything below 70% is good!")
    else:
        print(
            "Your CPU is being pushed really hard! Try closing some applications to relieve some stress from your computer")
    cpu_info = cpu.boot_info()
    print(f"Now, lets go ahead and look more at the specifics of your CPU:\n"
          f"You have {cpu.core_count()} cores.\n"
          f"Your system has made {cpu_info['syscalls']} system calls, this is kernel level operations\n"
          f"Your system has made {cpu_info['ctx_switches']} context switches, this is the number of times your "
          f"computer has saved its current state / restored its state\n"
          f"Your system has had {cpu_info['interrupts']} interrupts, this is the number of times a signal is "
          f"recieved by the CPU\n"
          f"All of this information is based on the last time you powered on your computer.")
    dictionary = cpu.core_info()
    print(f"\n-----------------------------------------------------------------------------------------------------"
          f"\n The information shown below is a break down of all {cpu.core_count()} of your CPU cores in usage percentage"
          f"\nIt indicates how much time of each core is spent doing what."
          f"\n User is time you are using your computer, System is everything going on behind the scenes"
          f"\n Idle is times when your core is not engaged in whatever is running on your computer"
          f"\n interrupt is times your core is involved in signals sent by hardware or software"
          f"\n Dpc is time spent servicing deferred procedure calls")
    for key, value in dictionary.items():
        s = str(value)
        # users, system, idle, interrupt, dpc
        matches = re.findall(r'=(\d+\.\d+)', s)
        print(f"User takes up {matches[0]}%, System takes up {matches[1]}%, Idle takes up {matches[2]}%, Interrupt "
              f"takes up {matches[3]}%, DPC Takes up {matches[4]}%")



inp = input(f"""
Hi {gen.get_user()}, Would you like to conduct a PC Health Check?
Y/N
""")
if inp[0].lower() == 'y':
    option = int(input("""
    Great! Do you have any specific areas you would like to scan? 
    1. All Aspects
    2. Storage
    3. CPU
    4. Memory (RAM)
    5. Network Information
    6. Services / Processes
    """))
    funcs = (pcharddrive, pccpu, pcram, pcservices)
    if option == 1:
        for func in funcs:
            func()
            inp = input("Press any key to continue...")
            if inp != "":
                continue
    else:
        index = 2
        funcs[index - 2]()

else:
    print("""
    :(
    """)
    sys.exit()