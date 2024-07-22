from filesIngest import filesIngest
import re
from prettytable import PrettyTable
import os
from colorama import just_fix_windows_console
just_fix_windows_console()
from colorama import Fore, Style
from time import sleep



table = PrettyTable()
table.field_names = ["Old Filename", "New Filename"]
rr = filesIngest()
rr.select_image_file()




def regexOps(filename):
  pattern = r"(IMG)_(\d{8})(\d)"
  replacement = r"\1_\2_\3"
  return re.sub(pattern, replacement, filename)





for name in rr.getFileList():
  newfilename = regexOps(name)
  table.add_row([name, newfilename])

print(table)





confirm = input("confirm rename? (y / enter other to quit) ")

if confirm == 'y':
  for name in rr.getFileList():
    newfilename = regexOps(name)
    print(Fore.YELLOW + 'Renaming '+ name + ' to new filename ' + newfilename)
    os.rename(name, newfilename)
    print(Fore.GREEN + 'Renaming '+ name + ' to new filename ' + newfilename + ' completed successfully.')
    sleep(0.2)
else:
  print(Fore.RED + 'Not receiving correct input. Exiting...\n')
  print(Style.RESET_ALL)
  exit(0)



print(Style.RESET_ALL)