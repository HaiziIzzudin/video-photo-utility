from filesIngest import filesIngest
from change_modtime import changeTo

import re
from prettytable import PrettyTable
import os
from colorama import just_fix_windows_console
just_fix_windows_console()
from colorama import Fore, Style
from time import sleep
import platform
import time
from datetime import datetime

if platform.system() == 'Windows':
  import win32file
  import pywintypes
  import win32con



table = PrettyTable()
table.field_names = ["Filename", "Datetime Taken/Encoded", "Old Date Created/Mod", "New Date Created/Mod"]
rr = filesIngest()
rr.select_files('videos')







for name in rr.getFileList():

  dt_modtime = datetime.fromtimestamp(os.path.getmtime(name))

  encodedtime_obj = rr.getFile_EncodedDate(name)

  table.add_row([name, encodedtime_obj.strftime("%Y-%m-%d %H:%M:%S"), dt_modtime.strftime("%Y-%m-%d %H:%M:%S"), encodedtime_obj.strftime("%Y-%m-%d %H:%M:%S")])

print(table)





confirm = input("confirm change? (y / enter other to quit) ")

if confirm == 'y':
  for name in rr.getFileList():
    
    encodedtime_obj = rr.getFile_EncodedDate(name)
    changeTo(encodedtime_obj, name)
    print(Fore.GREEN + name + ' has been changed to ' + encodedtime_obj.strftime("%Y-%m-%d %H:%M:%S") + ' successfully.' + Style.RESET_ALL)

else:
  print(Fore.RED + 'Not receiving correct input. Exiting...\n')
  print(Style.RESET_ALL)
  exit(0)



print(Style.RESET_ALL)