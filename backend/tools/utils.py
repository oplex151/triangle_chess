from flask import request
from .logger import  setupLogger
logger = setupLogger()

testdict = {'a': 1, 'b': 'dsa'}

def get_params(required_args:dict, data:dict)->tuple:
    params = {}
    try: 
        for k,t  in required_args.items():
            params[k] = t(data.get(k)) if data.get(k)!= None else None
    except ValueError:
        raise ValueError("Invalid parameter type")
    if None in (params.values()):
        raise ValueError("Missing required parameters")
    if len(params) ==1:
        return list(params.values())[0]
    else:
        return tuple(params.values())

if __name__ == '__main__':
   a,b=get_params({'a': int, 'b': int})
   print(a,b)