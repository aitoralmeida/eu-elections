__author__ = 'juan'
import mem_database
import glob



db = mem_database.database()
files =  glob.glob("*.txt")
print files

for file in files:
     try:
         file = open(file,"r")
         try:
             lines = file.readlines()
             db.insert(lines[:150])
         finally:
             file.close()
     except IOError:
         pass
