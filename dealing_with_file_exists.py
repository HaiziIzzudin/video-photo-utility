from os import path # dlm code tulis je path.dirname(name)
from datetime import datetime, timedelta

def fixFileExists(file: str):

  base = path.basename(file)

  f = base.split("_")

  prefix = f[0]
  datestr: str = f[1]
  time_and_ext:str = f[2].split(".")  # 125959
  timestr:str = time_and_ext[0]
  extension:str = time_and_ext[1]

  timeobj = datetime.strptime(timestr, "%H%M%S")
  timeobj += timedelta(seconds=1)
  timestr = timeobj.strftime("%H%M%S")

  return path.dirname(file) + "/" + f"{prefix}_{datestr}_{timestr}.{extension}"


# print( fixFileExists("C:/IMG_9876542_101213.jpg") )