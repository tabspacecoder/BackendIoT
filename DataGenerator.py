import json


class Header:
    Success = "Success"
    Failure = "Failure"


class Type:
    All = "All"


def Report(Timely, Daily, Monthly, Yearly, Clustered):
    Data = {
        "Time": Timely,
        "Daily": Daily,
        "Monthly": Monthly,
        "Yearly": Yearly,
        "Clustered": Clustered
    }
    return Data


def Response(header, Type="", Values=None):
    if Values is None:
        Values = []
    Out = {
        "Header": header,
        "Type": Type,
        "Values": Values
    }
    return json.dumps(Out)


def Request(Type=""):
    Out = {
        Type: ""
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
