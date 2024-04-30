from flask import request

testdict = {'a': 1, 'b': 'dsa'}

def get_params(required_args:dict, data:dict)->tuple:
    params = {}
    try: 
        for k,t  in required_args.items():
            params[k] = t(data.get(k)) if data.get(k)!= None else None
    except ValueError:
        raise ValueError("Invalid parameter type")
    if not all (params.values()):
        raise ValueError("Missing required parameters")
    if len(params) ==1:
        return list(params.values())
    else:
        return tuple(params.values())

if __name__ == '__main__':
   a,b=get_params({'a': int, 'b': int})
   print(a,b)