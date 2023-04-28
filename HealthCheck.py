import sys
import datetime as dt
import Services as s
import General as gen
import CPU as cpu
import ssdhdd as sh


inp = input(f"""
Hi {gen.get_user()}, Would you like to conduct a PC Health Check?
Y/N
""")
if inp[0].lower() == 'y':
    option = input(int("""
    Great! Do you have any specific areas you would like to scan? 
    1. All Aspects
    2. Storage
    3. CPU
    4. Memory (RAM)
    5. Network Information
    6. Services / Processes
    """))
    if option == 1:
        pass
    if option == 2:
        pass
    if option == 3:
        print(f"Hello, {gen.get_user()}")
        print(f"You are currently using {cpu.check_cpu_usage()}% of your CPUs maximum capability."
              f" This number is subject to change depending on how intensive the applications running on your computer are.")
        if cpu.check_cpu_usage() <= 70:
            print("It looks like your CPU useage is at a healthy level! Generally anything below 70% is good!")
        else:
            print("Your CPU is being pushed really hard! Try closing some applications to relieve some stress from your computer")
        cpu_info = cpu.boot_info()
        print(f"Now, lets go ahead and look more at the specifics of your CPU:\n"
              f"You have {cpu.core_count()} cores.\n"
              f"Your system has made {cpu_info['syscalls']} system calls, this is kernel level operations\n"
              f"Your system has made {cpu_info['ctx_switches']} context switches, this is the number of times your "
              f"computer has saved its current state / restored its state\n"
              f"Your system has had {cpu_info['interrupts']} interrupts, this is the number of times a signal is "
              f"recieved by the CPU\n"
              f"All of this information is based on the last time you powered on your computer.")

    if option == 4:
        pass
    if option == 5:
        pass
    if option == 6:
        services = s.get_serivces()
        print(f"""
{gen.get_user()}, you currently have {len(services)} services running on your system. They are detailed below:
________________________________________________________________________________________________________________________
""")
        for key, value in services.items():
            print(f"The service {key} is using the Process ID {value},")
        print("\n \nNow that we have a list of all the running services on your system, lets take a look at what is using the most of your resources.")
        s.mem_hungry_services()
        print("Above is your memory hungry services.")
        # bool variable to determine if they want to find out more information on another service.
        # Restructure this whole thing, if int, check if valid pid, return PID information, ask again
        # if not int, end loop
        toContinue = True
        user_input = input(f"If you would like to know more about a specific process please enter the number Otherwise, say no")
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

else:
    print("""
    :(
    """)
    sys.exit()



