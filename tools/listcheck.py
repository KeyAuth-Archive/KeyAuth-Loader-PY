import time
import os
import re
import uuid
import wmi
import subprocess
import requests
from urllib.request import Request, urlopen


def get_ip():
    ip = "None"
    try:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except:
        pass
    return ip

ip = get_ip()

serveruser = os.getenv("UserName")
pc_name = os.getenv("COMPUTERNAME")
mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
computer = wmi.WMI()
os_info = computer.Win32_OperatingSystem()[0]
os_name = os_info.Name.encode('utf-8').split(b'|')[0]
os_name = str(os_name).replace("'", "")
os_name = str(os_name).replace("b", "")
gpu = computer.Win32_VideoController()[0].Name
hwid = subprocess.check_output(
    'wmic csproduct get uuid').decode().split('\n')[1].strip()
hwidlist = requests.get(
    'https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/hwid_list.txt')
pcnamelist = requests.get(
    'https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/pc_name_list.txt')
pcusernamelist = requests.get(
    'https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/pc_username_list.txt')
iplist = requests.get(
    'https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/ip_list.txt')
maclist = requests.get(
    'https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/mac_list.txt')
gpulist = requests.get(
    'https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/gpu_list.txt')
platformlist = requests.get(
    'https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/pc_platforms.txt')

def list_check():
    try:
        if hwid in hwidlist.text:
            print('BLACKLISTED HWID DETECTED')
            print(f'HWID: {hwid}')
            time.sleep(2)
            os._exit(1)
        else:
            pass
    except:
        print('[ERROR]: Failed to connect to database.')
        time.sleep(2)
        os._exit(1)

    try:
        if serveruser in pcusernamelist.text:
            print('BLACKLISTED PC USER DETECTED!')
            print(f'PC USER: {serveruser}')
            time.sleep(2)
            os._exit(1)
        else:
            pass
    except:
        print('[ERROR]: Failed to connect to database.')
        time.sleep(2)
        os._exit(1)

    try:
        if pc_name in pcnamelist.text:
            print('BLACKLISTED PC NAME DETECTED!')
            print(f'PC NAME: {pc_name}')
            time.sleep(2)
            os._exit(1)
        else:
            pass
    except:
        print('[ERROR]: Failed to connect to database.')
        time.sleep(2)
        os._exit(1)

    try:
        if ip in iplist.text:
            print('BLACKLISTED IP DETECTED!')
            print(f'IP: {ip}')
            time.sleep(2)
            os._exit(1)
        else:
            pass
    except:
        print('[ERROR]: Failed to connect to database.')
        time.sleep(2)
        os._exit(1)

    try:
        if mac in maclist.text:
            print('BLACKLISTED MAC DETECTED!')
            print(f'MAC: {mac}')
            time.sleep(2)
            os._exit(1)
        else:
            pass
    except:
        print('[ERROR]: Failed to connect to database.')
        time.sleep(2)
        os._exit(1)

    try:
        if gpu in gpulist.text:
            print('BLACKLISTED GPU DETECTED!')
            print(f'GPU: {gpu}')
            time.sleep(2)
            os._exit(1)
        else:
            pass
    except:
        print('[ERROR]: Failed to connect to database.')
        time.sleep(2)
        os._exit(1)
