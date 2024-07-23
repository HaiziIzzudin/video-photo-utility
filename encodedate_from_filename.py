from filesIngest import filesIngest
from countdown import countdown
from raw import convert2raw

import subprocess
import os
from datetime import datetime
from prettytable import PrettyTable
from time import sleep
import platform
from send2trash import send2trash

from colorama import just_fix_windows_console
just_fix_windows_console()
from colorama import Fore, Style



if platform.system() == 'Windows':
  import win32file
  import pywintypes







def getImageDate(filepath):
  date_str = os.path.splitext(os.path.basename(filepath))[0].split("_")[1]
  time_str = os.path.splitext(os.path.basename(filepath))[0].split("_")[2]
  date_obj = datetime.strptime(date_str, "%Y%m%d")  ## this must be true otherwise ERR
  
  try:
    time_obj = datetime.strptime(time_str, "%H%M%S")
  
  except:
    print(Fore.MAGENTA + 'Error parsing time string '+ time_str+ ', possibly invalid character. Replacing with 00:00:00' + Style.RESET_ALL)
    time_str = '000000'
    time_obj = datetime.strptime(time_str, "%H%M%S")
  
  datetime_obj = datetime.combine(date_obj.date(), time_obj.time())
  return datetime_obj




#############
### MAINN ###
#############


# init class object
img = filesIngest()


# init prettytable
table = PrettyTable()
table.field_names = ["File Path", "File Name", "File Datetime Extract"]


# prompt to get files list
img.select_files('videos')



# for listing in table
for i in img.getFileList():
  datetime_obj = getImageDate(i)
  date_formatted = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
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
    break
  else:
    print(Fore.RED + 'Invalid input. Please try again.')


print(Style.RESET_ALL)



for j in img.getFileList():
  
  try:
    
    datetime_obj = getImageDate(j)


    ## TODO: change date encoded
    date_formatted = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    tempfilename = f'{os.path.dirname(j)}/temp.mp4'
    command = f'ffmpeg -y -i "{j}" -c copy -metadata creation_time="{date_formatted}" "{tempfilename}"'
    ### YES WINDOWS TERMINAL CAN ONLY INTERPRET DOUBLE QUOTE AS ENCLOSING FOR ANY THAT HAS SPACES!
    print(command)
    print(tempfilename)
    
    if os.path.exists(j): countdown(Fore.YELLOW + 'File ' + j + ' will be overitten. Please cancel in', 1)
    print(Style.RESET_ALL)

    subprocess.run(command)
    sleep(0.5)
    send2trash( convert2raw(j) )
    sleep(0.5)
    os.rename( tempfilename , j )
    


    ## change THE file creation date and modified date
    
    timestamp = datetime_obj.timestamp()
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
    print(Fore.GREEN + os.path.basename(j) + ' video data has been changed to ' + datetime_obj.strftime("%d/%m/%Y"))
    print(Style.RESET_ALL)
    sleep(0.2)
  

  
  except Exception:
    print(Fore.RED + 'An error has occured. Please check the exception below for error.')
    print(Fore.RED + Exception)
    print(Style.RESET_ALL)
    exit(1)



print(Style.RESET_ALL)