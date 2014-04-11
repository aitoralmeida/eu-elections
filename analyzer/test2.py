__author__ = 'juan'
import mem_database
import glob



db = mem_database.database()
files =  glob.glob("*.txt")
print files
