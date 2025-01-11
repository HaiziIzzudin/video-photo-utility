import os
import re
from subprocess import run
from filesIngest import filesIngest
from prettytable import PrettyTable
from get_date_taken import main as get_datetaken # returns dt_obj
from colorama import Fore, Style
from datetime import datetime
from time import sleep
from send2trash import send2trash
from dealing_with_file_exists import fixFileExists



# init variable
EXIFTOOL_LOC = r"C:\Program Files\XnViewMP\AddOn"



fi = filesIngest()


# prompt to get files list
# os.system('cls' if os.name == 'nt' else 'clear')
mediatype = input("Please specify kind of media to process and press Enter to continue...\n\n[I] Images\n[V] Videos\n\nSelect: ")
fi.select_files(mediatype)



def get_dtobj(fname: str): # returns new_basename (formatted IMG_20240205_121314.mp4) or None
  new_basename: str | None = None
  chg_mode: str | None = None # basename_only | basename_ref_EXIF | EXIF_ref_basename | Fail
  
  dt_obj = get_datetaken(mediatype, fname, EXIFTOOL_LOC)
  basename = os.path.basename(fname)
  
  if dt_obj:
    pattern = r"(IMG)(_)(\d{8})(_)(\d{6})(\w*).(\w+)"
    if re.match(pattern, os.path.basename(fname)):
      chg_mode = None
    else:
      pattern = r"(\w*)(_|-|)(\d{8})(_|-|)(\d{6}|WA\d{4})(\w*).(\w+)"
      repl_basename = r"IMG_\3_\5\6.\7"
      if re.match(pattern, os.path.basename(fname)):
        new_basename = re.sub(pattern, repl_basename, basename)
        chg_mode = "basename_only"
      else:
        new_basename = "IMG_" + datetime.strftime(dt_obj, '%Y%m%d_%H%M%S') + os.path.splitext(fname)[1]
        chg_mode = "basename_ref_EXIF"
  
  else:
    pattern = r"(\w*)(_|-|)(\d{8})(_|-|)(\d{6}|WA\d{4})(\w*).(\w+)"
    repl_basename = r"IMG_\3_\5\6.\7"
    if re.match(pattern, os.path.basename(fname)):
      new_basename = re.sub(pattern, repl_basename, basename)
      chg_mode = "EXIF_ref_basename"
    else:
      new_basename = None
      chg_mode = "Fail"

  return new_basename, chg_mode





# init prettytable
table = PrettyTable()
table.field_names = ["No.", "Original File Name", "New File Name"]

    
for fname in fi.getFileList():  # name is the full path of the file
  print(Fore.LIGHTMAGENTA_EX + f"Processing {os.path.basename(fname)}" + Style.RESET_ALL, end='\r')
  new_basename, chg_mode = get_dtobj(fname)
  if new_basename is not None and re.match(r"WA\d{4}", new_basename):
    new_basename = re.sub(r"WA", "00", new_basename)
  
  if chg_mode == "basename_only":       color = Fore.CYAN
  elif chg_mode == "basename_ref_EXIF": color = Fore.GREEN
  elif chg_mode == "EXIF_ref_basename": color = Fore.YELLOW
  elif chg_mode == "Fail":              color = Fore.RED
  elif chg_mode == None:                color = Style.DIM

  if new_basename is None:              new_basename = "No changes"
  table.add_row([len(table._rows) + 1, os.path.basename(fname), color+new_basename+Style.RESET_ALL])

print("\n\n")
print(table)
print("\nLegend:")
print("DIM = No Changes")
print(Fore.CYAN + "CYAN" + Style.RESET_ALL + " = Minimal change to filename")
print(Fore.GREEN + "GREEN" + Style.RESET_ALL + " = File name change based on date object")
print(Fore.YELLOW + "YELLOW" + Style.RESET_ALL + " = Exif applied based on file name")
print(Fore.RED + "RED" + Style.RESET_ALL + " = Unable to change. Manual intervention required.")






input("\nPress Enter to commence metadata and renaming...")





def file_rename(fname:str, new_basename:str):
  """
    the new_basename can only be the basename, not the full path.
    but the fname must be the full path.
  """
  newfilename = f'{os.path.dirname(fname)}/{new_basename}'
  while True:
    try:
      os.rename( fname , newfilename )
      break
    except FileExistsError:
      print(Fore.MAGENTA + 'File '+ newfilename + ' already exists.'+ Style.RESET_ALL)
      newfilename = fixFileExists(newfilename)




for fname in fi.getFileList():  # name is the full path of the file
  print(Fore.LIGHTMAGENTA_EX + f"Processing {os.path.basename(fname)}" + Style.RESET_ALL, end='\r')
  new_basename, chg_mode = get_dtobj(fname)

  if new_basename:
    pattern = r"IMG_(\d{8})_(\d{6}|WA\d{4})(\w*).(\w+)"
    repl_datetime = r"\1 \2"
    dt_str = re.sub(pattern, repl_datetime, new_basename) # utk nk parse w/ datetime, do not use for naming files. Use new_basename instead.
    dt_str = re.sub(r"WA\d{4}", "000000", dt_str) # for WA case, for parsing to datetime
    new_basename_WA = re.sub(r"WA", "00", new_basename) # for WA case, but can use new_basename_WA for naming files.
    print(dt_str + " " + new_basename_WA + " " + chg_mode, end='\r')

    if chg_mode == "EXIF_ref_basename":      
      dt_obj: datetime = datetime.strptime(dt_str, "%Y%m%d %H%M%S")
      if mediatype.lower() == 'v': ### WINDOWS TERMINAL CAN ONLY INTERPRET DOUBLE QUOTE AS ENCLOSING FOR ARGUMENT FLAGS THAT HAS SPACES!
        command = f'ffmpeg -hide_banner -loglevel error -y -i "{fname}" -c copy -metadata creation_time="{dt_obj.strftime("%Y-%m-%d %H:%M:%S")}" "{os.path.dirname(fname)}/temp_{new_basename}" '
      elif mediatype.lower() == 'i':
        command = f'./exiftool -TagsFromFile "{fname}" -AllDates="{dt_obj.strftime("%Y:%m:%d %H:%M:%S")}" -o "{os.path.dirname(fname)}/temp_{new_basename}" "{fname}"'
    
      run(command)
      sleep(0.1)

      send2trash( r"{}".format(fname.replace("/", "\\")) )
      sleep(0.2)
      
      file_rename(os.path.dirname(fname) + "/temp_" + new_basename, 
                  new_basename_WA )
      print(Fore.YELLOW + f"File {new_basename_WA} EXIF changes has been made based on basename." + Style.RESET_ALL)

    elif chg_mode == "basename_ref_EXIF":
      file_rename(fname, new_basename_WA)
      print(Fore.GREEN + f"File {new_basename_WA} basename changes has been made based on EXIF." + Style.RESET_ALL)

    elif chg_mode == "basename_only":
      file_rename(fname, new_basename_WA)
      print(Fore.CYAN + f"File {new_basename_WA} minor basename changes has been made." + Style.RESET_ALL)

    elif chg_mode == "Fail":
      print(Fore.RED + f"File {os.path.basename(fname)} unable to be processed." + Style.RESET_ALL)

  else:
    print(Style.DIM + f"File {os.path.basename(fname)} has nothing to change." + Style.RESET_ALL)
      



  





# pattern, replacement = r"(\w{3})(_|-)(\d{8})(_|-)(\d{6})(\w*)", r"IMG_\3_\5\6"

# for name in fi.getFileList():
#   basename = os.path.splitext(os.path.basename(name))[0]
#   extension = os.path.splitext(os.path.basename(name))[1]
  
#   if re.match(pattern, basename):
#     dt_t = list(datetaken(mediatype, name, EXIFTOOL_LOCATION))
#     dt_t[0] = re.sub(pattern, replacement, basename) + extension
  
#   else:
#     try:    dt_t = datetaken(mediatype, name, EXIFTOOL_LOCATION) # 0 = newfilename (incl extension), 1 = datetime_object
#     except: dt_t = datefromfname(mediatype, name)  # 0 = newfilename (incl extension), 1 = datetime_object
    
#     if mediatype.lower() == 'v':
#       ### YES WINDOWS TERMINAL CAN ONLY INTERPRET DOUBLE QUOTE AS ENCLOSING FOR ANY THAT HAS SPACES!
#       command = f'ffmpeg -hide_banner -loglevel error -y -i "{name}" -c copy -metadata creation_time="{dt_t[1].strftime("%Y-%m-%d %H:%M:%S")}" "{f'{os.path.dirname(name)}/temp_{dt_t[0]}'}"'
#     elif mediatype.lower() == 'i':
#       command = f'./exiftool -TagsFromFile "{name}" -AllDates="{dt_t[1].strftime("%Y:%m:%d %H:%M:%S")}" -o "{os.path.dirname(name)}/temp_{dt_t[0]}" "{name}"'

#     print(command)
#     if os.path.exists(name): countdown(Fore.YELLOW + 'File ' + os.path.basename(name) + ' will be overitten. Ctrl+C for a chance to cancel in', 1)
#     print(Style.RESET_ALL)
#     run(command)
#     sleep(0.1)
#     send2trash( r"{}".format(name.replace("/", "\\")) )
#     sleep(0.2)
#     newfilename = f'{os.path.dirname(name)}/{dt_t[0]}'
#     while True:
#       try:
#         os.rename( f'{os.path.dirname(name)}/temp_{dt_t[0]}' , newfilename )
#         break
#       except FileExistsError:
#         print(Fore.MAGENTA + 'File '+ newfilename + ' already exists.'+ Style.RESET_ALL)
#         newfilename = fixFileExists(newfilename)