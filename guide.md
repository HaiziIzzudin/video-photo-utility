Video encoded date = enable "Media created" column

Photo Encoded date = enable "Date taken" column


<!-- python "C:\Users\haizi\Documents\(Python) Change video creation date\exif_or_encodedate_from_filename.py"

python "C:\Users\haizi\Documents\(Python) Change video creation date\datecreated_modified.py"

python "c:/Users/haizi/Documents/(Python) Change video creation date/file_rename_from_dateobj.py"

python "c:/Users/haizi/Documents/(Python) Change video creation date/file_rename_from_filename_useregex.py" -->



Process:
1. Deal with major inconsistent naming cth: IMG_0001 (usually has encode metadata)
2. Deal with minor inconsistent naming cth: VID-01234567-890123
3. Deal with media creation/ date taken missing.
4. Deal with Date Created/ Modifed, make it same timestamp with the above.





UPDATE 22 DECEMBER 2024

main.py is the new entrypoint of the program.
file in use is only get_date_taken and get_date_from_filename.
Improved logic for auto determine if renaming or metadata change is necessary.
TODO: the changing command is still not implemented. soon.
TODO: dealing_with_file_exists
TODO: proj cleanup

Please run the proj in venv mode, install requirements.txt