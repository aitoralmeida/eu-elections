__author__ = 'juan'
import mem_database
import glob




files =  glob.glob("corpus_def/*.txt")
print files
cont = 0

for file in files:
     try:
         file = open(file,"r")
         try:
             lines = file.readlines()
             db = mem_database.database()
             db.insert(lines)
             print "Finished ", file
             print cont ,"/", len(files)
             cont += 1
         finally:
             file.close()
     except IOError:
         pass
