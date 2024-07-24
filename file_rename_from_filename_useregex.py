from dealing_with_file_exists import fixFileExists

from filesIngest import filesIngest
import re
from prettytable import PrettyTable
import os
from colorama import just_fix_windows_console
just_fix_windows_console()
from colorama import Fore, Style
from time import sleep



table = PrettyTable()
table.field_names = ["No.", "Old Filename", "New Filename"]
rr = filesIngest()
rr.select_files('images') ## IMAGES or VIDEOS valid




def regexOps(filename):

  ### Uncomment which pattern u want to use

  # pattern = r"(IMG)_(\d{8})(\d)"
  # replacement = r"\1_\2_\3"
  
  # pattern = r"(IMG)_(\d{4})"
  # replacement = r"\1_\2"
  
  pattern = r'PXL_(\d{8})_(\d{6})(.*).(\w{3})'
  replacement = r'IMG_\1_\2.\4'
  
  return re.sub(pattern, replacement, filename)




i = 0
for name in rr.getFileList():
  i += 1
  newfilename = regexOps(name)
  table.add_row([i, name, newfilename])

print(table)





confirm = input("confirm rename? (y / enter other to quit) ")

if confirm == 'y':
  for name in rr.getFileList():
    newfilename = regexOps(name)
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

      sleep(0.2)
    
    sleep(0.2)

else:
  print(Fore.RED + 'Not receiving correct input. Exiting...\n')
  print(Style.RESET_ALL)
  exit(0)



print(Style.RESET_ALL)