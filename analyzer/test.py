__author__ = 'juan'
import database
import glob



db = database.database("database.db")
db.create()
files =  glob.glob("corpus_def/*.txt")
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