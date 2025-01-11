from filesIngest import filesIngest
from dealing_with_file_exists import fixFileExists

import re
from prettytable import PrettyTable
import os
from colorama import just_fix_windows_console
just_fix_windows_console()
from colorama import Fore, Style
from time import sleep


### REVIEW MEDIA TYPE FIRST BEFORE RUNNING THE SCRIPT
mediatype = 'images'



table = PrettyTable()
table.field_names = ["No.", "Old Filename", "Datetime Extract", "New Filename"]
rr = filesIngest()
rr.select_files(mediatype)




def newFilename(oldfilepath, whatReturn):

  # fetch filename only
  fileonly = os.path.basename(oldfilepath)

  # fetch datetime
  dtobj = rr.getFile_EncodedDate(oldfilepath, mediatype)
  
  ### PLEASE CHANGE THE PATTERN HERE
  # pattern = r"(\w{3})_(\d{4}).(\w)"
  # replacement = f"IMG_{dtobj.strftime("%Y%m%d_%H%M%S")}." + r"\3"
  # pattern = r'^(.*?).(\w+)$'
  # replacement = f'IMG_{dtobj.strftime("%Y%m%d_%H%M%S")}.' + r"\2"
  
  # filename.jpg (for photoshop exported projects)
  pattern = r'^(.*?).(\w+)$'
  replacement = f'IMG_{dtobj.strftime("%Y%m%d_%H%M%S")}' + '.' + r"\2"

  if whatReturn == 'filename':
    return re.sub(pattern, replacement, fileonly)
  elif whatReturn == 'datetimestr':
    return dtobj.strftime("%Y-%m-%d %H:%M:%S")





count = 0
total = len(rr.getFileList())
for name in rr.getFileList():
  count += 1
  dt_extract = newFilename(name, 'filename')
  print(f"[{count}/{total}] {name}")
  newfilename = f"{os.path.dirname(name)}/{dt_extract}"
  table.add_row([count, name, dt_extract, newfilename])

print(table)





confirm = input("confirm rename? (y / enter other to quit) ")

if confirm == 'y':
  for name in rr.getFileList():
    newfilename = f"{os.path.dirname(name)}/{newFilename(name, 'filename')}"
    print(Fore.YELLOW + 'Renaming '+ name + ' to new filename ' + newfilename)
    
    while True:
      
      try:
        os.rename(name, newfilename)
        print(Fore.GREEN + 'Renaming '+ name + ' to new filename ' + newfilename + ' completed successfully.')
        break
      
      except FileExistsError:
        print(Fore.LIGHTMAGENTA_EX + 'File '+ newfilename + ' already exists.', end=' ')
        newfilename = fixFileExists(newfilename)
        print(Fore.LIGHTMAGENTA_EX + 'Decrement by 1 to ' + newfilename)

      sleep(0.1)
    
    sleep(0.1)

else:
  print(Fore.RED + 'Not receiving correct input. Exiting...\n')
  print(Style.RESET_ALL)
  exit(0)



print(Style.RESET_ALL)