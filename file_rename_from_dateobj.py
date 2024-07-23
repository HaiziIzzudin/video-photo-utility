from filesIngest import filesIngest

import re
from prettytable import PrettyTable
import os
from colorama import just_fix_windows_console
just_fix_windows_console()
from colorama import Fore, Style
from time import sleep



table = PrettyTable()
table.field_names = ["Old Filename", "Datetime Extract", "New Filename"]
rr = filesIngest()
rr.select_files('videos')




def newFilename(oldfilepath, whatReturn):

  # fetch filename only
  fileonly = os.path.basename(oldfilepath)

  # fetch datetime
  dtobj = rr.getFile_EncodedDate(oldfilepath)
  

  pattern = r"(\w{3})_(\d{4}).(\w)"
  replacement = f"IMG_{dtobj.strftime("%Y%m%d_%H%M%S")}." + r"\3"

  if whatReturn == 'filename':
    return re.sub(pattern, replacement, fileonly)
  elif whatReturn == 'datetimestr':
    return dtobj.strftime("%Y-%m-%d %H:%M:%S")





for name in rr.getFileList():
  newfilename = f"{os.path.dirname(name)}/{newFilename(name, 'filename')}"
  table.add_row([name, newFilename(name, 'datetimestr'), newfilename])

print(table)





confirm = input("confirm rename? (y / enter other to quit) ")

if confirm == 'y':
  for name in rr.getFileList():
    newfilename = f"{os.path.dirname(name)}/{newFilename(name, 'filename')}"
    print(Fore.YELLOW + 'Renaming '+ name + ' to new filename ' + newfilename)
    os.rename(name, newfilename)
    print(Fore.GREEN + 'Renaming '+ name + ' to new filename ' + newfilename + ' completed successfully.')
    sleep(0.2)
else:
  print(Fore.RED + 'Not receiving correct input. Exiting...\n')
  print(Style.RESET_ALL)
  exit(0)



print(Style.RESET_ALL)