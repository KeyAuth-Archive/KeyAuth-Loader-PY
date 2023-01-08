import os
import sys
import time
import re
import uuid
import ctypes

def vm_check():
    def get_base_prefix_compat(): # define all of the checks
        return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix

    def in_virtualenv():
        return get_base_prefix_compat() != sys.prefix

    if in_virtualenv() == True: # if we are in a vm
        time.sleep(2)
        os._exit(1)
    else:
        pass

    def registry_check(): # VM Registry Check
        reg1 = os.system(
            "REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\DriverDesc 2> nul")
        reg2 = os.system(
            "REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\ProviderName 2> nul")

        if reg1 != 1 and reg2 != 1:
            print("VMware Registry Detected")
            time.sleep(2)
            os._exit(1)

    def processes_and_files_check():
        vmware_dll = os.path.join(
            os.environ["SystemRoot"], "System32\\vmGuestLib.dll")
        virtualbox_dll = os.path.join(
            os.environ["SystemRoot"], "vboxmrxnp.dll")

        process = os.popen(
            'TASKLIST /FI "STATUS eq RUNNING" | find /V "Image Name" | find /V "="').read()
        processList = []
        for processNames in process.split(" "):
            if ".exe" in processNames:
                processList.append(processNames.replace(
                    "K\n", "").replace("\n", ""))

        if "VMwareService.exe" in processList or "VMwareTray.exe" in processList:
            print("VMwareService.exe & VMwareTray.exe process are running")
            time.sleep(2)
            os._exit(1)

        if os.path.exists(vmware_dll):
            print("Vmware DLL Detected")
            time.sleep(2)
            os._exit(1)

        if os.path.exists(virtualbox_dll):
            print("VirtualBox DLL Detected")
            time.sleep(2)
            os._exit(1)

        try:
            sandboxie = ctypes.cdll.LoadLibrary("SbieDll.dll")
            print("Sandboxie DLL Detected")
            time.sleep(2)
            os._exit(1)
        except:
            pass

    def mac_check():
        mac_address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        vmware_mac_list = ["00:05:69", "00:0c:29", "00:1c:14", "00:50:56"]
        if mac_address[:8] in vmware_mac_list:
            print("VMware MAC Address Detected")
            time.sleep(2)
            os._exit(1)
    print("[*] Checking VM")
    registry_check()
    processes_and_files_check()
    mac_check()
    print("[+] VM Not Detected")
