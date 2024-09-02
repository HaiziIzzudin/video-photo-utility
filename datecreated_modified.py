from filesIngest import filesIngest
from change_modtime import changeTo

from prettytable import PrettyTable
import os
from colorama import just_fix_windows_console
just_fix_windows_console()
from colorama import Fore, Style
from time import sleep
from datetime import datetime


table = PrettyTable()
table.field_names = ["No.", "Filename", "Datetime Taken/Encoded", "Old Date Created/Mod", "New Date Created/Mod"]

mediatype = 'videos' # IMAGES / VIDEOS

rr = filesIngest()
rr.select_files(mediatype)






index:int = 0
for name in rr.getFileList():
  index += 1
  dt_modtime = datetime.fromtimestamp(os.path.getmtime(name))

  encodedtime_obj = rr.getFile_EncodedDate(name, mediatype)

  table.add_row([index, name, encodedtime_obj.strftime("%Y-%m-%d %H:%M:%S"), dt_modtime.strftime("%Y-%m-%d %H:%M:%S"), encodedtime_obj.strftime("%Y-%m-%d %H:%M:%S")])

print(table)
totaldata = index
print(f"Total data: {totaldata}")





confirm = input("confirm change? (y / enter other to quit) ")

if confirm == 'y':
  index = 0
  for name in rr.getFileList():
    index += 1
    encodedtime_obj = rr.getFile_EncodedDate(name, mediatype)
    changeTo(encodedtime_obj, name)
    print(f"[{index}/{totaldata}]")
    print(Fore.GREEN + name + ' has been changed to ' + encodedtime_obj.strftime("%Y-%m-%d %H:%M:%S") + ' successfully.' + Style.RESET_ALL)

else:
  print(Fore.RED + 'Not receiving correct input. Exiting...\n')
  print(Style.RESET_ALL)
  exit(0)



print(Style.RESET_ALL)