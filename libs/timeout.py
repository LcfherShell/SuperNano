import os, sys, psutil, shutil
try:
    from GPUtil import getGPUs
except:
    getGPUs = None

def timeout_v1():
    # Get CPU or GPU usage percentage
    if getGPUs==None:
        cpu_usage = psutil.cpu_percent()
    else:
        cpu_usage = getGPUs()
    # Get RAM usage percentage
    ram_usage = psutil.virtual_memory().percent
    # Divide both percentages by 1000
    cpu_usage_divided = cpu_usage / 100
    ram_usage_divided = ram_usage / 100
    if cpu_usage_divided<0.1:
        cpu_usage_divided = cpu_usage_divided*2
    if ram_usage_divided<0.1:
        ram_usage_divided = ram_usage_divided*2
    data =  [round(cpu_usage_divided, 1), round(ram_usage_divided, 1)]
    return round(sum(data) / data.__len__(), 1)


def timeout_v2(pid=os.getpid()):
    # Mendapatkan ID proses saat ini
    process = psutil.Process(pid)
    
    # Mendapatkan penggunaan CPU dan RAM untuk proses tersebut
    if getGPUs==None:
        cpu_usage = psutil.cpu_percent()
    else:
        cpu_usage = getGPUs()
    ram_usage = process.memory_percent()  # Persentase penggunaan RAM oleh proses
    
    # Pembagian dengan 100 untuk mendapatkan nilai antara 0 dan 1
    cpu_usage_divided = cpu_usage / 100
    ram_usage_divided = ram_usage / 100
    
    if cpu_usage_divided < 0.1:
        cpu_usage_divided = cpu_usage_divided * 2
    if ram_usage_divided < 0.1:
        ram_usage_divided = ram_usage_divided * 2
    
    data = [round(cpu_usage_divided, 1), round(ram_usage_divided, 1)]
    return round(sum(data) / len(data), 1)
