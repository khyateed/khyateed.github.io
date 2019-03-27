import re
import sqlite3
import glob

# ----------------------------------- PART 1: READING THE TEXT FILES INTO PYTHON DICTIONARIES------------------------------
# README:
# this program reads raw .dat files into an sqlite database.
# the database contains 5 different tables
# all raw input files must be .dat extension
# place all .dat files to be read into the database, into the raw_files directory
# To prevent duplicate entries into the database, do not run the code on the same raw files more than once.

def access(line):
    dic={}
    try:
        dic['ID'] = re.search('\[(\d*)\]', line).group(1)
    except:
        dic['ID'] = 'not given'
    try:
        dic['TIME'] = re.search('([A-Za-z 0-9- :]*) ::', line).group(1).strip()
    except:
        dic['TIME'] = 'not given'
    try:
        dic['USER'] = re.search("user\W'([A-Za-z 0-9- :]*)", line).group(1).strip()
    except:
        dic['USER'] = 'not given'
    try:
        dic['SHAREID'] = re.search("share id '(.*)'. ", line).group(1).strip()
    except:
        dic['SHAREID'] = 'not given'
    try:
        dic['SHAREE'] = re.search("Sharee '(.*)' ", line).group(1).strip()
    except:
        dic['SHAREE'] = 'not given'
    try:
        dic['RESTRICTED_TO'] = re.search("restricted to '(.*)'.", line).group(1).strip()
    except:
        dic['RESTRICTED_TO'] = 'not given'
    return(dic)

def transfer(line):
    dic={}
    try:
        dic['ID'] = re.search('\[(\d*)\]', line).group(1)
    except:
        dic['ID'] = 'Not Given'
    try:
        dic['TIME'] = re.search('([A-Za-z 0-9- :]*) ::', line).group(1).strip()
    except:
        dic['TIME'] = 'not given'
    try:
        dic['FILE'] = re.search('(transferring|transfer)..?([A-Za-z0-9._/\[\]-]*)', line).group(2).strip()
    except:
        dic['FILE'] = 'not given'
    return(dic)

def stats(line):
    dic={}
    try:
        dic['ID'] = re.search('\[(\d*)\]', line).group(1)
    except:
        dic['ID'] = 'not given'
    try:
        dic['TIME'] = re.search('([A-Za-z 0-9- :]*) ::', line).group(1).strip()
    except:
        dic['TIME'] ='not given'
    try:
        dic['DATE'] = re.search('DATE=([\d.]*)', line).group(1).strip()
    except:
        dic['DATE'] ='not given'
    try:
        dic['HOST'] = re.search('HOST=([A-Za-z0-9._/-]*)', line).group(1).strip()
    except:
        dic['HOST'] = 'not given'
    try:
        dic['PROG'] = re.search('PROG=([A-Za-z0-9._/-]*)', line).group(1).strip()
    except:
        dic['PROG'] ='not given'
    try:
        dic['NL'] = re.search('NL.EVNT=([A-Za-z0-9._/-]*)', line).group(1).strip()
    except:
        dic['NL'] ='not given'
    try:
        dic['START'] = re.search('START=([A-Za-z0-9._/-]*)', line).group(1).strip()
    except:
        dic['START'] ='not given'
    try:
        dic['USER'] = re.search('USER=([A-Za-z0-9._/-]*)', line).group(1).strip()
    except:
        dic['USER'] ='not given'
    try:
        dic['FILE'] = re.search('FILE=([A-Za-z0-9._/-]*)', line).group(1).strip()
    except:
        dic['FILE'] ='not given'
    try:
        dic['BUFFER'] = re.search('BUFFER=([A-Za-z0-9._/-]*)', line).group(1).strip()
    except:
        dic['BUFFER'] ='not given'
    try:
        dic['BLOCK'] = re.search('BLOCK=([A-Za-z0-9._/-]*)', line).group(1).strip()
    except:
        dic['BLOCK'] ='not given'
    try:
        dic['NBYTES'] = re.search('NBYTES=([A-Za-z0-9._/-]*)', line).group(1).strip()
    except:
        dic['NBYTES'] ='not given'
    try:
        dic['VOLUME'] = re.search('VOLUME=([A-Za-z0-9._/-]*)', line).group(1).strip()
    except:
        dic['VOLUME'] ='not given'
    try:
        dic['STREAMS'] = re.search('STREAMS=([A-Za-z0-9._/-]*)', line).group(1).strip()
    except:
        dic['STREAMS'] = 'not given'
    try:
        dic['STRIPES'] = re.search('STRIPES=([A-Za-z0-9._/-]*)', line).group(1).strip()
    except:
        dic['STRIPES'] ='not given'
    try:
        dic['DEST'] = re.search('DEST=\[([A-Za-z0-9._/-]*)\]', line).group(1).strip()
    except:
        dic['DEST'] ='not given'
    try:
        dic['TYPE'] = re.search('TYPE=([A-Za-z0-9._/-]*)', line).group(1).strip()
    except:
        dic['TYPE'] ='not given'
    try:
        dic['CODE'] = re.search('CODE=([A-Za-z0-9._/-]*)', line).group(1).strip()
    except:
        dic['CODE'] ='not given'
    try:
        dic['TASKID'] = re.search('TASKID=([A-Za-z0-9._/-]*)', line).group(1).strip()
    except:
        dic['TASKID'] ='not given'
    return(dic)

# -------------------------------------------------- PART 2: INSERTING DATA INTO DATABASE (Do not run this more than once)-------------------------------------
conn = sqlite3.connect("umtri_file_transfers.db", timeout=10)
cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS access_allowed(pkey int PRIMARY KEY ,'
               'ID varchar(255), '
               'TIME varchar(255), '
               'USER varchar(255), '
               'SHAREID varchar(255), '
               'SHAREE varchar(255), '
               'RESTRICTED_TO varchar(255), UNIQUE (ID, TIME, USER, SHAREID, SHAREE, RESTRICTED_TO))')
cursor.execute('CREATE TABLE IF NOT EXISTS finished_transferring(ID varchar(255), TIME varchar(255), FILE varchar(255))')
cursor.execute('CREATE TABLE IF NOT EXISTS failed_transfer(ID varchar(255), TIME varchar(255), FILE varchar(255))')
cursor.execute('CREATE TABLE IF NOT EXISTS started_transfer(ID varchar(255), TIME varchar(255), FILE varchar(255))')
cursor.execute('CREATE TABLE IF NOT EXISTS stats(ID varchar(255), TIME varchar(255), DATE varchar(255), HOST varchar(255), PROG varchar(255), NL varchar(255), START varchar(255), USER varchar(255), FILE varchar(255), BUFFER varchar(255), BLOCK varchar(255), NBYTES varchar(255), VOLUME varchar(255), STREAMS varchar(255), STRIPES varchar(255), DEST varchar(255), TYPE varchar(255), CODE varchar(255), TASKID varchar(255))')


# ---------- Parse through each line of each raw file and insert the data into the corresponding table of the database
path = '/Users/Khyatee1/GoogleDrive/CSCAR/umtridata/raw_files/*.dat'
raw_files = glob.glob(path)
for rfile in raw_files:
    f = open(rfile,'r')
    for line in f.readlines():
        if "Access allowed" in line: # "Access allowed for sharing of user..."
            dic = access(line)
            cursor.execute("INSERT INTO access_allowed VALUES(:ID,:TIME, :USER, :SHAREID,:SHAREE,:RESTRICTED_TO)", dic)

        elif "transferring" in line: # "Finished transferring..."
            dic = transfer(line)
            cursor.execute("INSERT INTO finished_transferring VALUES (:ID,:TIME, :FILE)", dic)

        elif "Failure" in line: # "Failure attempting to transfer..."
            dic = transfer(line)
            cursor.execute("INSERT INTO failed_transfer VALUES (:ID,:TIME, :FILE)", dic)

        elif "Starting to transfer" in line: # "Starting to transfer..."
            dic = transfer(line)
            cursor.execute("INSERT INTO started_transfer VALUES (:ID,:TIME, :FILE)", dic)

        elif "Transfer stats:" in line:
            dic = stats(line)
            cursor.execute("INSERT INTO stats VALUES (:ID,:TIME,:DATE,:HOST,:PROG,:NL,:START,:USER,:FILE,:BUFFER,:BLOCK,:NBYTES,:VOLUME,:STREAMS,:STRIPES,:DEST,:TYPE,:CODE,:TASKID)",dic)

    print("Entered",re.search('[a-zA-Z0-9]*\.dat',rfile).group(0))

conn.commit()
print("\nChanges to database:", conn.total_changes)

# ---------------------------Comment out above block to run queries below.----------------------------------------


cursor.close()
conn.close()
