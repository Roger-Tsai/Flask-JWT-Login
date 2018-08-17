def returnTrueMsg(data, msg):
    return {
        "status": True,
        "data": data,
        "msg": msg
    }

def returnFalseMsg(data, msg):
    return {
        "status": False,
        "data": data,
        "msg": msg
    }