#!/usr/bin/python

#MIDN 1/C Luke Loehr and MIDN 1/C Megan Fields

#used this resource to help with os.walk() syntax: https://stackoverflow.com/questions/16953842/using-os-walk-to-recursively-traverse-directories-in-python/54673093
#used ths source for help with excluding directories when using os.walk(): https://stackoverflow.com/questions/19859840/excluding-directories-in-os-walk
#used this source to write the hashed_browns function: https://www.pythoncentral.io/hashing-files-with-python/
#used this source for using the datetime library: https://www.programiz.com/python-programming/datetime/current-time
#used this source for getting the current date: https://wwww.programiz.com/python-programming/datetime/current-datetime
import csv
import os 
import stat
import hashlib
from datetime import datetime
from datetime import date

ignore = ["/dev", "/proc", "/run", "/sys", "/tmp", "/var", "/usr/share", "/usr/src", "/usr/include", "/usr/bin", "/home/luke/.cache", "/lib/modules", "/usr/lib", "/media"]

def main():
    if os.path.isfile("/tmp/baseline.csv"):
        print("\n\nBASELINE FILE ~'baseline.csv'~ FOUND!\n")
        print("\nCOMPUTING HASH OF FILE SYSTEM...\n")
        print("\nCOMPARING HASH TO BASELINE FILE...\n")
        update_list = run_run_rudolph(ignore)
        print("\n\nHASH COMPUTATION AND COMPARISON COMPLETE\n")
        print("\nCHANGES HAVE BEEN NOTICED IN THESE FILES: \n")
        print("\tKEY: (filename_with_full_path,sha256_hash,date_observed(mm/dd/yy),time_observed(hh:mm:ss)\n")
        for item in update_list:
            printstring = "\t" + str(item) + "\n"
            print(printstring)
        quit()
    else:
        print("\n\nNO BASELINE FILE ~'baseline.csv'~ FOUND!\n")
        print("\nCOMPUTING HASH OF FILE SYSTEM...\n")
        print("\nCREATING BASELINE FILE...\n")
        luke_path_walker(ignore)
        print("\nHASH COMPUTED AND BASELINE FILE CREATED\n")
        quit()

def hashed_browns(inputfile): 
    hasher = hashlib.sha256()
    BUFF_LEN = 10000
    with open (inputfile, "rb") as file1:
        buffer = file1.read(BUFF_LEN) 
        while len(buffer) > 0:
            hasher.update(buffer)
            buffer = file1.read(BUFF_LEN)
    returnhash = hasher.hexdigest()
    return(returnhash)


def luke_path_walker(ignorelist):
    with open("/tmp/baseline.csv", "w+") as file_write: 
        for root, dirs, files in os.walk("/", topdown =True):  
            if root in ignorelist:
                dirs[:] = [] 
                files[:] = []
            path = root.split(os.sep)
            for file in files:
                fpath = os.path.join(root,file)
                inputfile = fpath
                try:
                    hashvalue = hashed_browns(inputfile)
                except:
                    continue
                today = date.today()
                current_date = today.strftime("%d/%m/%y")
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                outputstring = str(inputfile) + "," + str(hashvalue) + ","  + current_date + "," + current_time + "\n"
                file_write.write(outputstring)
    file_write.close()

def run_run_rudolph(ignorelist):
    updates = [] 
    with open("/tmp/baseline.csv", "r") as file_read:
        baseline_list = file_read.readlines()
    file_read.close()
    with open("/tmp/baseline.csv", "w+") as file_write:
        for root, dirs, files in os.walk("/", topdown = True):  
            if root in ignorelist:
                dirs[:] = [] 
                files[:] = []
            path = root.split(os.sep)
            for file in files:
                fpath = os.path.join(root,file)
                inputfile = fpath
                try:
                    hashvalue = hashed_browns(inputfile)
                except:
                    continue
                today = date.today()
                current_date = today.strftime("%d/%m/%y")
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                outputstring = str(inputfile) + "," + str(hashvalue) + ","  + current_date + "," + current_time + "\n"
                for item in baseline_list:
                    if str(hashvalue) not in item:
                        updates.append(outputstring)
                file_write.write(outputstring)
    file_write.close()
    return(updates)


if __name__ == "__main__":
    main()