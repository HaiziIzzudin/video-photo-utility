import re
from datetime import datetime
from colorama import Fore, Style

def main(basename:str):
  """
  Returns datetime object
  """
  
  pattern = r"(\w+)(_|-)(\d{8})(_|-)(\d{6}|WA\d{4})(\w*).(\w+)"
  
  if re.match(pattern, basename):
    repl_date = r"\3"
    repl_time = r"\5"

    date_str = re.sub(pattern, repl_date, basename)
    time_str = re.sub(pattern, repl_time, basename)

    try:
      time_obj = datetime.strptime(time_str, "%H%M%S")
    except:
      print(Fore.MAGENTA + 'Error parsing time string '+ time_str+ ', possibly invalid character. Replacing with 00:00:00' + Style.RESET_ALL, end="\r")
      time_str = '000000'
      time_obj = datetime.strptime(time_str, "%H%M%S")
    
    date_obj = datetime.strptime(date_str, "%H%M%S")
    dt_obj = datetime.combine(date_obj.date(), time_obj.time())

    return dt_obj
    
  else:
    return None