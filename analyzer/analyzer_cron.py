__author__ = 'juan'
import mem_database
import glob
import os.path, time

files =  glob.glob("../wrapper/*.txt")
readed_files = []
current_file = ''
starting_point = time.time()


while True:
    with open('read_files.log', 'r') as logfile:
        for line in logfile:
            readed_files.append(line.replace('\n', ''))

    for file in files:
        current_time= os.path.getmtime(file)
        last_time = 10000
        if current_time > last_time:
            last_time = current_time
            current_file = file

    for file in files:
        if (file not in readed_files) and (file != current_file):
            print file
            try:
             file = open(file,"r")
             try:
                 lines = file.readlines()
                 #db = mem_database.database()
                 #db.insert(lines)
             finally:
                 readed_files.append(file.name)
                 file.close()

            except IOError:
                pass

    with open('read_files.log', 'w') as logfile:
        for f in readed_files:
            logfile.write(str(f)+'\n')

    nsecs = (30*60)
    time.sleep(nsecs)


