import os
from datetime import datetime
import pytz
from pymediainfo import MediaInfo
import subprocess
from json import loads
from colorama import Fore, Style
from typing import Union


dtobj_myt: datetime | None = None


def main(mediatype: str, filepath: str, exiftool_location: str):
  if mediatype.lower() == 'v':
    media_info = MediaInfo.parse( r"{}".format(filepath) )

    try:
      for track in media_info.tracks:
        if track.track_type == 'General':
          datetime_str = track.encoded_date

          # Remove UTC
          datetime_noUTCstr = datetime_str.replace(" UTC", "")
          # Convert the string to a datetime object
          dtobj_utc = datetime.strptime(datetime_noUTCstr, '%Y-%m-%d %H:%M:%S')
          
          # Localize the datetime object to UTC
          dtobj_utc = (pytz.utc).localize(dtobj_utc)
          
          # Convert to MYT timezone
          dtobj_myt = dtobj_utc.astimezone(pytz.timezone('Asia/Kuala_Lumpur'))

    except AttributeError:
      dtobj_myt = None

  elif mediatype.lower() == 'i':
    os.chdir(exiftool_location)
    try:
      command = [
        './exiftool',
        "-DateTimeOriginal",
        filepath
      ]

      # Run the command and capture the output
      result = subprocess.run(command, capture_output=True, text=True)

      # Find the line with the Date/Time Original information
      output_lines = result.stdout.splitlines()
      # datetime_original_line = None
      for line in output_lines:
        if "Date/Time Original" in line:
          datetime_original_line = line
          break
          
      # Extract the date and time from the line
      _, dts = datetime_original_line.split(": ", 1)
      # The underscore _ is used as a throwaway variable to ignore the first part of the split result (i.e., the label "Date/Time Original"). 
      # It's a common Python convention to use _ for variables that are not needed.

      # Convert to datetime object (string parse time)
      # print(dts)
      dtobj_myt = datetime.strptime(dts, '%Y:%m:%d %H:%M:%S')
    
    except UnboundLocalError:
    
      # print(Fore.MAGENTA, "Extract creation time failed. Using Json mode...", Style.RESET_ALL)
      command = [
        './exiftool',
        '-json',
        filepath
      ]

      # Run the command and capture the output
      # result = subprocess.run(command, capture_output=True, text=True)
      result = subprocess.check_output(command)
      output = result

      # load the output as json string json.loads
      # print(output) # DEBUG
      res_json = loads(output)

      try:
        # find "CreateDate" and store into var
        createdate:str = res_json[0]["CreateDate"]
        # output will be something like "2019:12:09 16:55:04+08:00" or "2019:12:09 16:55:04-04:00"
        if createdate[-6] == '+':   dts = createdate[:-6]
        elif createdate[-6] == '-': dts = createdate[:-6]
        else:                       dts = createdate

        # Convert to datetime object (string parse time)
        # print(dts)
        dtobj_myt = datetime.strptime(dts, '%Y:%m:%d %H:%M:%S')
      
      except KeyError:
        dtobj_myt = None




  return dtobj_myt