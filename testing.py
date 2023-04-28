import psutil

print(psutil.pids())
print(len(psutil.pids()))
p = psutil.Process(712)
t = 1
if int(t):
    print("test")
    print(p)
