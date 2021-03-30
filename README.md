The hash data is stored as baseline.csv in the /tmp directory.

If the file exists then ./hash.py will hash all the files on your system and compare them to the existing baseline.csv file. Then it wil print out any differences and write them to the baseline.csv file.

If the baseline.csv file does not exist, then ./hash.py will hash all of the files on your file system and save them in /tmp/baseline.csv in the following format:

filename_with_full_path, sha256_hash, date_observed(mm/dd/yy),  time_observed(hh:mm:ss)


