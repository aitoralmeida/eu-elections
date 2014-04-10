__author__ = 'juan'
import glob

files =  glob.glob("corpus_def/*.txt")
print files
nlines = 0
times = 0

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
		nlines += 1
     times += 30
 	     	
     print "Finished ",nlines
     print times / 60
     
