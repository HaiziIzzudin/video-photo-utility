import os
from version2.filesIngest import filesIngest
from prettytable import PrettyTable
from version2.get_date_taken import main as datetaken
from get_date_from_filename import main as datefromfname
from colorama import Fore, Style
from datetime import datetime
from time import sleep



# init variable
EXIFTOOL_LOCATION = r"C:\Program Files\XnViewMP\AddOn"


# init prettytable
table = PrettyTable()
table.field_names = ["No.", "Original File Name", "New File Name", "Date Taken"]
fi = filesIngest()


# prompt to get files list
os.system('cls' if os.name == 'nt' else 'clear')
mediatype = input("Please specify kind of media to process and press Enter to continue...\n\n(In capital letters)\n[I] Images\n[V] Videos\n\nSelect: ")
fi.select_files(mediatype)





# hold on
# before we write anything to table
# we need to extract the supposed datetime from any suitable method


count = 0
total = len(fi.getFileList())
for name in fi.getFileList():

  print(Fore.LIGHTMAGENTA_EX + f"Processing [{count+1}/{total}] {os.path.basename(name)}" + Style.RESET_ALL, end='\r')
  sleep(0.05)
  
  try:
    dt_t = datetaken(mediatype, fi.getFileList()[count], EXIFTOOL_LOCATION)
    dt_t_color = Fore.GREEN + datetime.strftime(dt_t[1], '%Y-%m-%d %H:%M:%S') + Style.RESET_ALL
  except:
    dt_t = datefromfname(mediatype, fi.getFileList()[count])
    dt_t_color = Fore.YELLOW + datetime.strftime(dt_t[1], '%Y-%m-%d %H:%M:%S') + Style.RESET_ALL
  
  table.add_row([count+1, os.path.basename(name), dt_t[0], dt_t_color])
  
  count += 1

print(table)
print("\nLegend:")
print(Fore.GREEN + "GREEN" + Style.RESET_ALL + " = date pulled from Metadata, only renaming necessary")
print(Fore.YELLOW + "YELLOW" + Style.RESET_ALL + " = date pulled from Filename")