__author__ = 'juan'
import database


db = database.database("database.db")
corpus = "eu-elections-8-0.txt"
db.create()

try:
    file = open(corpus,"r")
    try:
        lines = file.readlines()
    finally:
        file.close()
except IOError:
    pass


for line in lines:
    db.insert(line)