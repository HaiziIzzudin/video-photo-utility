from filesIngest import filesIngest

import subprocess
import os
from datetime import datetime
from prettytable import PrettyTable
from time import sleep
import platform

from colorama import just_fix_windows_console
just_fix_windows_console()
from colorama import Fore, Style



if platform.system() == 'Windows':
  import win32file
  import pywintypes



exiftool_location = r"C:\Program Files\XnViewMP\AddOn"


# change directory to the exiftool location first
os.chdir(exiftool_location)


def getImageDate(filepath):
  date_str = os.path.splitext(os.path.basename(filepath))[0].split("_")[1]
  date_obj = datetime.strptime(date_str, "%Y%m%d")
  return date_obj




#############
### MAINN ###
#############


# init class object
img = filesIngest()


# init prettytable
table = PrettyTable()
table.field_names = ["File Path", "File Name", "File Date Extract"]


# prompt to get files list
img.select_image_file()


# for listing in table
for i in img.getFileList():
  
  date_obj = getImageDate(i)

  date_formatted = date_obj.strftime("%d/%m/%Y")
  
  table.add_row([i, os.path.basename(i), date_formatted])
  

print(table)


# prompt to user what they are looking here.
print(Fore.YELLOW + 'This table displays date extracted from filename. These dates will be used for EXIF date creation, date digitized and date modified.\n\nPlease confirm and double check before proceed with this process.')


# dialog confirmation
while True:
  confirm1 = input(Fore.YELLOW + '\n\nConfirm change? (y/n) ' + Style.RESET_ALL)

  if confirm1 == 'n':
    print(Fore.RED + 'User cancelled process. Exiting...')
    print(Style.RESET_ALL)
    exit(0)
  elif confirm1 == 'y':
    break
  else:
    print(Fore.RED + 'Invalid input. Please try again.')


# dialog confirmation again
while True:
  confirm2 = input(Fore.YELLOW + '\n\nConfirm change? (DOUBLE CHECK AGAIN) (y/n) ' + Style.RESET_ALL)

  if confirm2 == 'n':
    print(Fore.RED + 'User cancelled process. Exiting...')
    print(Style.RESET_ALL)
    exit(0)
  elif confirm2 == 'y':
    print(Fore.YELLOW + 'Proceed with next instructions.')
    break
  else:
    print(Fore.RED + 'Invalid input. Please try again.')


print(Style.RESET_ALL)



for j in img.getFileList():
  
  try:
    

    ## change EXIF trio dates

    dateobj = getImageDate(j)
    command = f'./exiftool -AllDates="{dateobj}" -overwrite_original "{j}"'
    ### YES WINDOWS TERMINAL CAN ONLY INTERPRET DOUBLE QUOTE AS ENCLOSING FOR ANY THAT HAS SPACES!
    print(command)
    subprocess.run(command)
    


    ## change THE file creation date and modified date
    
    timestamp = dateobj.timestamp()
    if platform.system() == 'Windows':
      # Convert timestamp to Windows file time
      wintime = pywintypes.Time(timestamp)
      winfile = win32file.CreateFile(
        j, win32file.GENERIC_WRITE, win32file.FILE_SHARE_WRITE, None, win32file.OPEN_EXISTING, 0, 0
      )
      win32file.SetFileTime(winfile, wintime, wintime, wintime)
      winfile.close()
    else:
      # Set access and modification times (creation time not modifiable on Unix-like systems)
      os.utime(j, (timestamp, timestamp))
    
    
    ## print success statement
    print(Fore.GREEN + os.path.basename(j) + ' EXIF data has been changed to ' + dateobj.strftime("%d/%m/%Y"))
    print(Style.RESET_ALL)
    sleep(0.2)
  

  
  except Exception:
    print(Fore.RED + 'An error has occured. Please check the exception below for error.')
    print(Fore.RED + Exception)
    print(Style.RESET_ALL)
    exit(1)



print(Style.RESET_ALL)