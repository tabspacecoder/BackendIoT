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
