import json


class Header:
    Success = "Success"
    Failure = "Failure"


class Type:
    All = "All"
    SetType = "SetType"
    Analytics = "Model1"
    Intruder = "Model2"


def Report(Timely, Daily, Monthly, Yearly, Clustered):
    Data = {
        "Time": Timely,
        "Daily": Daily,
        "Monthly": Monthly,
        "Yearly": Yearly,
        "Clustered": Clustered
    }
    return Data


def Response(header, ReqType="", Values=None):
    if Values is None:
        Values = []
    Out = {
        "Header": header,
        "Type": ReqType,
        "Values": Values
    }
    return json.dumps(Out)


def Request(ReqType="", Other=""):
    Out = {
        "Type": ReqType,
        "Other": Other
    }
    return json.dumps(Out)


def Data(Image, Command: str, Year: int, Month: int, Date: int, Hour: int, Min: int):
    Out = {
        "Image": Image,
        "Command": Command,
        "Year": Year,
        "Month": Month,
        "Date": Date,
        "Hour": Hour,
        "Min": Min
    }
    return json.dumps(Out).encode()
