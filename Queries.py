import mysql.connector
import random
import time
import calendar
from collections import defaultdict
from datetime import datetime, timedelta

Diff = timedelta(hours=6)


def TableExist(Core, Name: str):
    Core.Cursor.execute("SHOW TABLES;")
    for x in Core.Cursor:
        if x[0] == Name:
            return True
    return False


def DeleteTable(Core, Name: str):
    if TableExist(Core, Name):
        Core.Cursor.execute(f"DROP TABLE {Name};")
        return True
    return False


def InitTable(Core):
    if not TableExist(Core, "Entries"):
        Core.Cursor.execute(
            "CREATE TABLE Entries (EntryID INT AUTO_INCREMENT PRIMARY KEY,ID INT, EntryTime DATETIME,ExitTime "
            "DATETIME);")
        return True
    return False


def GetLastEntry(Core, ID):
    Core.Cursor.execute("SELECT EntryID, EntryTime, ExitTime FROM Entries WHERE ID = %s;", (ID,))
    result = Core.Cursor.fetchall()
    if len(result) > 0:
        return result[len(result) - 1]
    return []


def EntryStamp(Core, ID):
    Out = GetLastEntry(Core, ID)
    if len(Out) > 0:
        print(Out[0], datetime.now() - Out[1])
        if datetime.now() - Out[1] > Diff:
            Core.Cursor.execute(
                "INSERT INTO Entries(ID, EntryTime) VALUES (%s,CURRENT_TIMESTAMP());", (ID,))
            Core.Database.commit()
    else:
        Core.Cursor.execute(
            "INSERT INTO Entries(ID, EntryTime) VALUES (%s,CURRENT_TIMESTAMP());", (ID,))
        Core.Database.commit()


def ExitStamp(Core, ID):
    Out = GetLastEntry(Core, ID)
    if len(Out) > 0:
        print(Out)
        if Out[2] is not None and (datetime.now() - Out[2]).seconds < Diff.seconds:
            Core.Cursor.execute(
                "UPDATE Entries SET ExitTime = CURRENT_TIMESTAMP() WHERE EntryID = %s;", (Out[0],))
            Core.Database.commit()
        elif Out[2] is None:
            Core.Cursor.execute(
                "UPDATE Entries SET ExitTime = CURRENT_TIMESTAMP() WHERE EntryID = %s;", (Out[0],))
            Core.Database.commit()


def GetByUserID(Core, ID):
    Core.Cursor.execute("SELECT EntryID, EntryTime, ExitTime FROM Entries WHERE ID = %s;", (ID,))
    return Core.Cursor.fetchall()


def GetByTimelyReport(Core):
    Core.Cursor.execute("SELECT EntryID, ExitTime, EntryTime FROM Entries")
    Data = Core.Cursor.fetchall()
    Out = 0
    for i in Data:
        if i[1] is not None and i[2] is not None:
            Out += 1
    return Out


def GetInsideCount(Core):
    Core.Cursor.execute("SELECT EntryID, ExitTime, EntryTime FROM Entries WHERE DATE(EntryTime) = DATE(NOW());")
    Data = Core.Cursor.fetchall()
    Out = 0
    for i in Data:
        if i[1] is None:
            Out += 1
    return Out


def GetByDailyReport(Core):
    Out = defaultdict(int)
    Core.Cursor.execute("SELECT EntryID, ExitTime, EntryTime FROM Entries")
    Data = Core.Cursor.fetchall()
    for i in Data:
        if i[1] is not None and i[2] is not None:
            Out[i[2].hour] += 1
    return Out


def GetByWeeklyReport(Core):
    Out = defaultdict(int)
    Core.Cursor.execute("SELECT EntryID, ExitTime, EntryTime FROM Entries")
    Data = Core.Cursor.fetchall()
    for i in Data:
        if i[1] is not None and i[2] is not None:
            Out[i[2].strftime("%A")] += 1
    return Out


def GetByMonthlyReport(Core):
    Out = defaultdict(int)
    Core.Cursor.execute("SELECT EntryID, ExitTime, EntryTime FROM Entries")
    Data = Core.Cursor.fetchall()
    for i in Data:
        if i[1] is not None and i[2] is not None:
            Out[i[2].day] += 1
    return Out


def GetByYearlyReport(Core):
    Out = defaultdict(int)
    Core.Cursor.execute("SELECT EntryID, ExitTime, EntryTime FROM Entries")
    Data = Core.Cursor.fetchall()
    for i in Data:
        if i[1] is not None and i[2] is not None:
            Out[calendar.month_name[i[2].month]] += 1
    return Out


DatabaseUser = "root"
DatabasePassword = "rootcore@123"
DatabaseHost = "127.0.0.1"
DatabasePort = 3306


class Base:
    def __init__(self):
        self.__InitDatabase()

    def __InitDatabase(self):
        print("Initializing database")
        self.Database = mysql.connector.connect(host=DatabaseHost, user=DatabaseUser, password=DatabasePassword,
                                                port=DatabasePort, database="DataManagement")
        self.Cursor = self.Database.cursor(buffered=True)
        print("Database initialized")

#
# C = Base()
# InitTable(C)
#
#
# def random_date(start=datetime.strptime('1/1/2020 12:00 PM', '%m/%d/%Y %I:%M %p'),
#                 end=datetime.strptime('1/1/2021 12:00 PM', '%m/%d/%Y %I:%M %p')):
#     delta = end - start
#     int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
#     random_second = random.randrange(int_delta)
#     return start + timedelta(seconds=random_second)
#
#
# for i in range(200):
#     in_date = random_date()
#     out_date = random_date(in_date)
#     Id = random.randint(1, 100)
#     C.Cursor.execute(
#         "INSERT INTO Entries(ID, EntryTime,ExitTime) VALUES (%s,%s,%s);", (Id, in_date,out_date))
#     C.Database.commit()
#     print(i, "Where done")
#
# print(GetByMonthlyReport(C))
# print(GetByYearlyReport(C))
# print(GetByWeeklyReport(C))
