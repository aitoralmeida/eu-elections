__author__ = 'juan'
import remote_database
import glob



db = remote_database.database()
files =  glob.glob("*.txt")
print files

for file in files:
     try:
         file = open(file,"r")
         try:
             lines = file.readlines()
         finally:
             file.close()
     except IOError:
         pass

     for line in lines:
         db.insert(line)

     print "Finished ",file