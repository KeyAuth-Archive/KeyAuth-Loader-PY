import os
import time
import os.path
import sys
import ctypes
import psutil
import threading
import getpass
import hashlib
from pystyle import *
from keyauth import api
from application.app import app
from tools.vmcheck import vm_check
from tools.listcheck import list_check


logo = """
  ██████  ▄████▄   ▄▄▄       ██▀███ ▓██   ██▓
▒██    ▒ ▒██▀ ▀█  ▒████▄    ▓██ ▒ ██▒▒██  ██▒
░ ▓██▄   ▒▓█    ▄ ▒██  ▀█▄  ▓██ ░▄█ ▒ ▒██ ██░
  ▒   ██▒▒▓▓▄ ▄██▒░██▄▄▄▄██ ▒██▀▀█▄   ░ ▐██▓░
▒██████▒▒▒ ▓███▀ ░ ▓█   ▓██▒░██▓ ▒██▒ ░ ██▒▓░
▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░ ▒▒   ▓▒█░░ ▒▓ ░▒▓░  ██▒▒▒
░ ░▒  ░ ░  ░  ▒     ▒   ▒▒ ░  ░▒ ░ ▒░▓██ ░▒░
░  ░  ░  ░          ░   ▒     ░░   ░ ▒ ▒ ░░
      ░  ░ ░            ░  ░   ░     ░ ░
         ░                           ░ ░    """

logo = Colorate.Vertical(Colors.DynamicMIX((Col.light_blue, Col.cyan)), Center.XCenter(logo))


def getchecksum():
    md5_hash = hashlib.md5()
    file = open(''.join(sys.argv), "rb")
    md5_hash.update(file.read())
    digest = md5_hash.hexdigest()
    return digest


keyauthapp = api(
    name = "name_here",
    ownerid = "ownerid_here",
    secret = "secret_here",
    version = "1.0",
    hash_to_check = getchecksum()
)

###############################################SETTINGS###############################################

vmcheck_switch = False # Checks if file is running on a virtual machine
listcheck_switch = False # Blocks all blacklisted virustotal machines
anti_debug_switch = False # Blocks debugger programs
live_ban_checking = False # Checks if user is banned and auto closes application
programblacklist = [
    "ksdumper.exe", "vmsrvc.exe", "vmacthlp.exe", "vmtoolsd.exe", "vgauthservice.exe", "regedit.exe", "ida64.exe", "qemu-ga.exe", "vmwaretray.exe", "taskmgr.exe", "joeboxcontrol.exe", "joeboxserver.exe", "pestudio.exe", "vmwareuser", "vboxtray.exe", "fiddler.exe", "prl_cc.exe", "prl_tools.exe", "x96dbg.exe", "x32dbg.exe", "xenservice.exe", "ollydbg.exe", "df5serv.exe", "vmusrvc.exe", "ksdumperclient.exe", "httpdebuggerui.exe", "HTTPDebuggerSvc.exe", "vboxservice.exe", "processhacker.exe", "wireshark.exe"
]

###############################################SETTINGS###############################################


# indefinite check for debugger programs
def block_debuggers():
    while True:
        time.sleep(1)
        for proc in psutil.process_iter():
            if any(procstr in proc.name().lower() for procstr in programblacklist):
                try:
                    print("\nBlacklisted program found: " + str(proc.name()))
                    proc.kill()
                    time.sleep(2)
                    os._exit(1)
                except(psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

# indefinite check for sandboxie dll
def block_dlls():
    while True:
        time.sleep(1)
        try:
            sandboxie = ctypes.cdll.LoadLibrary("SbieDll.dll")
            print("Sandboxie DLL detected")
            time.sleep(2)
            os._exit(1)
        except:
            pass


if anti_debug_switch == True:
    try:
        b = threading.Thread(name='AntiDebug', target=block_debuggers)
        b.start()
        b2 = threading.Thread(name='Anti-DLL', target=block_dlls)
        b2.start()
    except:
        pass
else:
    pass

if vmcheck_switch == True:
    vm_check()
else:
    pass

if listcheck_switch == True:
    list_check()
else:
    pass


def clear(): return os.system('cls' if os.name in ('nt', 'dos') else 'clear')


def tui() -> None:
    clear()
    print('\n')
    print(logo)
    print('\n'*3)


blue = Col.light_blue
lblue = Colors.StaticMIX((Col.light_blue, Col.white, Col.white))
red = Col.light_red
lred = Colors.StaticMIX((Col.light_red, Col.white, Col.white))
green = Col.light_green
lgreen = Colors.StaticMIX((Col.light_green, Col.white, Col.white))

def stage(text: str, symbol: str = '...') -> str:
    if symbol == '...':
      return f""" {Col.Symbol(symbol, lblue, blue)} {lblue}{text}{Col.reset}"""
    elif symbol == "!":
        return f""" {Col.Symbol(symbol, lred, red)} {red}{text}{Col.reset}"""
    elif symbol == "x":
        return f""" {Col.Symbol(symbol, lgreen, green)} {green}{text}{Col.reset}"""
    else:
      return f""" {Col.Symbol(symbol, blue, lblue)} {blue}{text}{Col.reset}"""


def main() -> None:
    choice = ""
    System.Title("Scary - Main Menu")
    tui()
    print(stage(f"Login {lblue}<- ", '1'))
    print(stage(f"Register {lblue}<- ", '2'))
    print(stage(f"Upgrade {lblue}<- ", '3'))
    print(stage(f"Exit {lblue}<- ", '4'))
    print('\n'*2)
    print(stage("Choose a number to continue", '...'))
    choice = input("\n > ")

    if choice == "1":
        System.Title("Scary - Login")
        tui()
        print(stage(f"Username: ", '?'))
        username = input("Username: ")
        username = username.replace("Username: ", "")
        print()
        print(stage(f"Password: ", '?'))
        password = getpass.getpass()
        print(stage(f"Checking...", "!"))
        time.sleep(3)
        if keyauthapp.login(username, password):
            print()
            print(stage(f"Success!", "x"))
            time.sleep(3)
            clear()
            app()
        else:
            time.sleep(3)
            clear()
            System.Title("Scary - Auth ERROR")
            print()
            print(stage(f"Authentication ERROR! Check your credentials", '!'))
            time.sleep(3)
            main()

    if choice == "2":
        System.Title("Scary - Register")
        tui()
        print(stage(f"Username: ", '?'))
        username = input("Username: ")
        username = username.replace("Username: ", "")
        print()
        print(stage(f"Password: ", '?'))
        password = getpass.getpass()
        print()
        print(stage(f"License Key: ", '?'))
        key = input("License Key: ")
        key = key.replace("License Key: ", "")
        print()
        print(stage(f"Checking...", "!"))
        time.sleep(3)
        if keyauthapp.register(username, password, key):
            print()
            print(stage(f"Success! Please login", "x"))
            time.sleep(3)
            clear()
            app()
        else:
            time.sleep(3)
            clear()
            System.Title("Scary - Auth ERROR")
            print()
            print(stage(f"Authentication ERROR! Check your credentials", '!'))
            time.sleep(3)
            main()


    if choice == "3":
        System.Title("Scary - Upgrade")
        tui()
        print(stage(f"Username: ", '?'))
        username = input("Username: ")
        username = username.replace("Username: ", "")
        print()
        print(stage(f"License Key: ", '?'))
        key = input("License Key: ")
        key = key.replace("License Key: ", "")
        print(stage(f"Checking...", "!"))
        time.sleep(3)
        if keyauthapp.upgrade(username, key):
            print()
            print(stage(f"Success! Please login", "x"))
            time.sleep(3)
            clear()
            main()
        else:
            time.sleep(3)
            clear()
            System.Title("Scary - Auth ERROR")
            print()
            print(stage(f"Authentication ERROR! Check your credentials", '!'))
            time.sleep(3)
            main()

    if choice == "4":
        clear()
        print()
        print(stage(f"Exiting. Goodbye..", '!'))
        time.sleep(2)
        exit()

    if choice != "1" and choice != "2" and choice != "3" and choice != "4":
        clear()
        print()
        print(stage(f"Invalid choice", '!'))
        time.sleep(2)
        main()


if __name__ == "__main__":
    main()
