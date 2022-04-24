import mysql.connector
import random
import time
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
        if datetime.now() - Out[1] > Diff:
            Core.Cursor.execute(
                "INSERT INTO Entries(ID, EntryTime) VALUES (%s,SYSDATE());", (ID,))
            Core.Database.commit()
    else:
        Core.Cursor.execute(
            "INSERT INTO Entries(ID, EntryTime) VALUES (%s,SYSDATE());", (ID,))
        Core.Database.commit()


def ExitStamp(Core, ID):
    Out = GetLastEntry(Core, ID)
    if len(Out) > 0:
        if Out[2] is None or datetime.now() - Out[2] < Diff:
            Core.Cursor.execute(
                "UPDATE Entries SET ExitTime = SYSDATE() WHERE EntryID = %s;", (Out[0],))
            Core.Database.commit()


def GetByUserID(Core, ID):
    Core.Cursor.execute("SELECT EntryID, EntryTime, ExitTime FROM Entries WHERE ID = %s;", (ID,))
    return Core.Cursor.fetchall()


def GetByTimelyReport(Core):
    Core.Cursor.execute("SELECT EntryID, ExitTime, EntryTime FROM Entries")
    Data = Core.Cursor.fetchall()
    Out = []
    for i in Data:
        if i[1] is not None and i[2] is not None:
            Out.append(i[1] - i[2])
    return Out


def GetByDailyReport(Core):
    Out = defaultdict(list)
    Core.Cursor.execute("SELECT EntryID, ExitTime, EntryTime FROM Entries")
    Data = Core.Cursor.fetchall()
    for i in Data:
        if i[1] is not None and i[2] is not None:
            Out[i[2].hour].append((i[1] - i[2]).seconds)
    return Out


def GetByWeeklyReport(Core):
    Out = defaultdict(list)
    Core.Cursor.execute("SELECT EntryID, ExitTime, EntryTime FROM Entries")
    Data = Core.Cursor.fetchall()
    for i in Data:
        if i[1] is not None and i[2] is not None:
            Out[i[2].strftime("%A")].append((i[1] - i[2]).seconds)
    return Out


def GetByMonthlyReport(Core):
    Out = defaultdict(list)
    Core.Cursor.execute("SELECT EntryID, ExitTime, EntryTime FROM Entries")
    Data = Core.Cursor.fetchall()
    for i in Data:
        if i[1] is not None and i[2] is not None:
            Out[i[2].day].append((i[1] - i[2]).seconds)
    return Out


def GetByYearlyReport(Core):
    Out = defaultdict(list)
    Core.Cursor.execute("SELECT EntryID, ExitTime, EntryTime FROM Entries")
    Data = Core.Cursor.fetchall()
    for i in Data:
        if i[1] is not None and i[2] is not None:
            Out[i[2].month].append((i[1] - i[2]).seconds)
    return Out


# DatabaseUser = "root"
# DatabasePassword = "rootcore@123"
# DatabaseHost = "127.0.0.1"
# DatabasePort = 3306
#
#
# class Base:
#     def __init__(self):
#         self.__InitDatabase()
#
#     def __InitDatabase(self):
#         print("Initializing database")
#         self.Database = mysql.connector.connect(host=DatabaseHost, user=DatabaseUser, password=DatabasePassword,
#                                                 port=DatabasePort, database="DataManagement")
#         self.Cursor = self.Database.cursor(buffered=True)
#         print("Database initialized")
#
#
# C = Base()
# InitTable(C)
#
# # for i in range(20):
# #     EntryStamp(C, random.randint(1, 10))
# #     print(i, "Where done")
# #     time.sleep(random.randint(1, 10))
#
# print(GetByMonthlyReport(C))
# print(GetByYearlyReport(C))
# print(GetByWeeklyReport(C))
