import sqlite3
import serial
import time
from datetime import datetime

# Connect to database
try:
    logfile = open("log.txt", "a+")
    db = sqlite3.connect("HomeLCD.db")
except Error as e:
    logfile.write("Error connecting to log" + e)

cursor = db.cursor()

arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600)

dtten = datetime.now()

while True:
    time.sleep(10)
    # Get and prepare data
    data = str(arduino.readline())
    # Make sure that the data is inputed properly
    if len(data) == 16:
        data = data[-14:]
        data = data[:11]
    elif len(data) == 15:
        data = data[-13:]
        data = data[:10]
    else:
        continue
    # Format and prepare the data
    datalist = data.split("|")
    temp = datalist[0]
    humid = datalist[1]

    # Every 10 minutes, submit data to database
    dtnow = datetime.now()
    if dtnow == dtten + datetime.timedelta(minetes=10):
        dbtime = dtnow.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO temphumid(temp, humid, date) VALUES (?,?,?)", (temp, humid, dbtime))
        dtten = dtnow
    
    db.commit()

    # Output the data
    print(datalist + '\n' + dbtime)
    arduino.flushInput()

cursor.close()
