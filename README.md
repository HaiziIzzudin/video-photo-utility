### Video Date Created/ Encoded Date Changer from filename
1. Clone this repo
2. Open powershell to the cloned folder
2. Run `.\Scripts\Activate.ps1`
3. Run `python main.py`


### Photo Bulk Add EXIF Date from filename
1. Git clone this repo
2. `cd video-creation-date-changer`
2. run `python ./exif_date_from_filename.py`





check if contains EXIF

if EXIF exists: / 
  if filename comply: /
    // no changes necessary (DIM)
  elif filename did not comply: /
    if difference is minimal: /
      // change which is necessary ONLY (CYAN)
    elif different is huge: /
      // change based on dt_obj (GREEN)
elif EXIF not exists: /
  if filename comply: /
    // apply EXIF based on filename (YELLOW)
  elif filename did not comply: /
    // change failed. (RED)
