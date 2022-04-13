import json


class Header:
    Success = "Success"
    Failure = "Failure"


def Response(header, Type="", Image=""):
    Out = {
        "Header": header,
        "Type": Type,
        "Image": Image
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
