from flask import request
from .logger import  setupLogger
logger = setupLogger()

testdict = {'a': 1, 'b': 'dsa'}

def getParams(required_args:dict, data:dict, can_be_none:list=None)->tuple:
    params = {}
    try: 
        for k,t  in required_args.items():
            params[k] = t(data.get(k)) if data.get(k)!= None else None
    except ValueError:
        raise ValueError("Invalid parameter type")
    for k in params.keys():
        if params[k] == None and k not in can_be_none:
            raise ValueError("Missing required parameter: "+k)
    if len(params) ==1:
        return list(params.values())[0]
    else:
        return tuple(params.values())

if __name__ == '__main__':
   a,b=getParams({'a': int, 'b': int})
   print(a,b)