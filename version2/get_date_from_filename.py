import os
import re
from datetime import datetime
from colorama import Fore, Style


def main(mediatype: str, filepath: str):
  basename = os.path.basename(filepath)
  
  if mediatype.lower() == 'v':
    regex = [ # 0 = pattern, 1 = replacement
      [r"(\w{3})_(\d{8})_(WA\d{4})(\w?).(.*)", r"IMG_\2_\3"], # whatsapp IMG_20241214_WA0029.mp4
      [r"(VID)-(\d{8})-(WA\d{4}).(.*)", r"IMG_\2_\3"], # whatsapp VID-20241214-WA0029.mp4
      [r"(lv)_(0)_(\d{8})(\d{6}).(.*)", r"IMG_\3_\4"], # capcut lv_0_20241130145017.mp4
      ]
  elif mediatype.lower() == 'i':
    regex = [ # 0 = pattern, 1 = replacement
      [r"(IMG)_(\d{8})_(WA\d{4}).(.*)", r"IMG_\2_\3"], # whatsapp IMG_20241130_WA0005.jpg
      [r"(IMG)-(\d{8})-(WA\d{4}).(.*)", r"IMG_\2_\3"], # whatsapp IMG-20241130-WA0005.jpg
      [r"(\w{3})_(\d{8})_(\d{6})(\w?).(.*)", r"IMG_\2_\3"], # (IMG|VID)_20241111_221753.jpg OR (IMG|VID)_20240105_211659_preview.mp4
      [r"(.*) (\d{4})-(\d{2})-(\d{2}) (\w{2}) (\d{2}).(\d{2}).(\d{2})(\w+).(\w+)", r"IMG_\2\3\4_\6\7\8"], # WhatsApp Image 2024-11-29 at 18.54.05_0a149e57.jpg
      ]

  for pattern, replacement in regex:
    if re.match(pattern, basename):
      new_name = re.sub(pattern, replacement, basename)
      break

  prefix = os.path.splitext(os.path.basename(new_name))[0].split("_")[0]
  date_str = os.path.splitext(os.path.basename(new_name))[0].split("_")[1]
  time_str = os.path.splitext(os.path.basename(new_name))[0].split("_")[2]
  date_obj = datetime.strptime(date_str, "%Y%m%d")  ## this must be true otherwise ERR
  

  try:
    time_obj = datetime.strptime(time_str, "%H%M%S")
  except:
    # print(Fore.MAGENTA + 'Error parsing time string '+ time_str+ ', possibly invalid character. Replacing with 00:00:00' + Style.RESET_ALL)
    time_str = '000000'
    time_obj = datetime.strptime(time_str, "%H%M%S")
  
  datetime_obj = datetime.combine(date_obj.date(), time_obj.time())
  returned_name = f"{prefix}_" + datetime.strftime(datetime_obj, '%Y%m%d_%H%M%S') + os.path.splitext(filepath)[1]

  return returned_name, datetime_obj





if __name__ == '__main__':
  dateobj = main('V', r"C:\Users\user\Downloads\VID-20241214-WA0029.mp4")
  print(dateobj)





