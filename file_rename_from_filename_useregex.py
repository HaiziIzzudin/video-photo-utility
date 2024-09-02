from dealing_with_file_exists import fixFileExists

from filesIngest import filesIngest
import re
from prettytable import PrettyTable
import os
from colorama import just_fix_windows_console
just_fix_windows_console()
from colorama import Fore, Style
RESET = Style.RESET_ALL
MAGENTA = Fore.LIGHTMAGENTA_EX
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
RED = Fore.RED
from time import sleep




def regexOps(filename):

  ### Uncomment which pattern u want to use

  # pattern = r"(IMG)_(\d{8})(\d)"
  # replacement = r"\1_\2_\3"
  
  # pattern = r"(IMG)_(\d{4})"
  # replacement = r"\1_\2"
  
  # pattern = r'PXL_(\d{8})_(\d{6})(\d{3})(.*).(\w{3})'   # eg. PXL_98765432_0123459876_ABC.jpg
  # replacement = r'IMG_\1_\2\4.\5'
  
  # pattern = r'VID_(\d{4})-(\d{2})-(\d{2})-(\d{2})-(\d{2})-(\d{2})-(\d{3})(.*).(\w{3})'  # VID_2022-11-09-12-09-52-254.x264_meta.mp4
  # replacement = r'IMG_\1\2\3_\4\5\6\8.\9'
  
  pattern = r'(\w+)\@(\d{2})-(\d{2})-(\d{4})_(\d{2})-(\d{2})-(\d{2}).(\w+)'  # photo_184@21-06-2024_16-59-36
  replacement = r'IMG_\4\3\2_\5\6\7.\8'
  
  return re.sub(pattern, replacement, filename)




if __name__ == '__main__':
  table = PrettyTable()
  table.field_names = ["No.", "Old Filename", "New Filename"]
  rr = filesIngest()
  rr.select_files('videos') ## IMAGES or VIDEOS valid

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
      print(YELLOW + 'Renaming '+ name + ' to new filename ' + newfilename+RESET)
      
      while True:
        
        try:
          os.rename(name, newfilename)
          print(GREEN + 'Renamed '+ name + ' to new filename '+newfilename+'.'+RESET)
          break
        
        except FileExistsError:
          print(MAGENTA + 'File '+ newfilename + ' already exists.'+RESET, end=' ')
          newfilename = fixFileExists(newfilename)
          print(MAGENTA + 'Change by 1 sec to ' + newfilename+RESET)

        sleep(0.1)
      
      sleep(0.1)

  else:
    print(RED + 'Not receiving correct input. Exiting...\n'+RESET)
    exit(0)

  print(RESET)