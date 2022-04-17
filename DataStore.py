import pandas as pd
from datetime import datetime
import random


def InitDataset():
    return pd.read_csv("Data.csv")


def GetByID(Df: pd.DataFrame, ID: str):
    Tmp = Df.where((Df["Id"] == ID))
    return len(Tmp.dropna())


def GetByDate(Df: pd.DataFrame, Year: int, Month: int, Date: int):
    Tmp = Df.where((Df["Year"] == Year & Df["Month"] == Month & Df["Date"] == Date))
    return len(Tmp.dropna())


def GetByMonth(Df: pd.DataFrame, Year: int, Month: int):
    Tmp = Df.where((Df["Year"] == Year & Df["Month"] == Month))
    return len(Tmp.dropna())


def GetByYear(Df: pd.DataFrame, Year: int):
    Tmp = Df.where(Df["Year"] == Year)
    return len(Tmp.dropna())


def GetByDateRange(Df: pd.DataFrame, Year: int, Month: int, Date: int):
    Tmp = Df.where((Df["Year"] == Year & Df["Month"] == Month & Df["Date"] == Date))
    return len(Tmp.dropna())


def ClusteredMonthlyReport(Df: pd.DataFrame):
    Tmp = Df.groupby(["Year", "Month"])
    Data = []
    for i in Tmp.describe().index:
        Data.append((i[0], i[1], Tmp.describe()["Id"]["count"][i]))
    return Data


def MonthlyReport(Df: pd.DataFrame):
    Tmp = Df.groupby("Month")
    Data = []
    for i in Tmp.describe().index:
        Data.append((i, Tmp.describe()["Id"]["count"][i]))
    return Data


def YearlyReport(Df: pd.DataFrame):
    Tmp = Df.groupby(["Year"])
    Data = []
    for i in Tmp.describe().index:
        Data.append((i, Tmp.describe()["Id"]["count"][i]))
    return Data


def DailyReport(Df: pd.DataFrame):
    Tmp = Df.groupby(["Date"])
    Data = []
    for i in Tmp.describe().index:
        Data.append((i, Tmp.describe()["Id"]["count"][i]))
    return Data


def GetTimely(Df: pd.DataFrame):
    Data = []
    for i in Df.index:
        S_Time = datetime.strptime(str(Df.iloc[i]["Hour"]) + ":" + str(Df.iloc[i]["Min"]), "%H:%M")
        E_Time = datetime.strptime(str(Df.iloc[i]["E_Hour"]) + ":" + str(Df.iloc[i]["E_Min"]), "%H:%M")
        Data.append((E_Time - S_Time).seconds / 60)
    return Data


def AddRecord(Df: pd.DataFrame, Id: str, Year: int, Month: int, Date: int, Hour: int, Min: int, E_Hour: int,
              E_Min: int):
    Data = {
        "Id": [Id],
        "Year": [Year],
        "Month": [Month],
        "Date": [Date],
        "Hour": [Hour],
        "Min": [Min],
        "E_Hour": [E_Hour],
        "E_Min": [E_Min]
    }
    Tmp = pd.DataFrame(Data)
    return Df.append(Tmp, ignore_index=True)


def Save(Df: pd.DataFrame):
    Df.to_csv("Data.csv")


def AddEndTime(Df: pd.DataFrame, Id: str, Year: int, Month: int, Date: int, E_Hour: int, E_Min: int):
    Tmp = Df.where((Df["Id"] == Id) & (Df["Year"] == Year) & (Df["Month"] == Month) & (Df["Date"] == Date))
    Tmp = Tmp.dropna()
    if len(Tmp) != 0:
        Df.loc[(Df["Id"] == Id) & (Df["Year"] == Year) & (Df["Month"] == Month) & (Df["Date"] == Date),
               ["E_Hour", "E_Min"]] = [E_Hour, E_Min]
        Save(Df)
        return True
    return False


# DF = InitDataset()
#

# for i in range(10):
#     DF = AddRecord(DF, str(random.randint(1, 25)), random.randint(2019, 2020), random.randint(1, 12),
#                    random.randint(1, 30),
#                    5,
#                    random.randint(0, 59), 6, random.randint(0, 59))
#
# DF.to_csv("Data.csv")

# print(ClusteredMonthlyReport(DF))
# print(MonthlyReport(DF))
# print(YearlyReport(DF))
# print(DailyReport(DF))

# print(GetTimely(DF))
#
# print(AddEndTime(DF, 1, 2020, 10, 8, 5, 5))
