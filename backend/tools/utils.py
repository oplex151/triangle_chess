from flask import request
from .logger import  setupLogger

'''
this is a tool to validate and extract parameters from a request object,
you just need to provide a dictionary with the required parameters and their types, all data will be transformed to that specified type.
this will help your partners who work on the frontend to know what parameters they need to send to your API.

example usage:

```
from flask import request
from .utils import getParams

@app.route('/test', methods=['POST'])
def test():
    required_args = {'a': int, 'b': str}
    can_be_none = ['b']
    data = request.get_json()
    a,b = getParams(required_args, data, can_be_none)
    return jsonify({'a': a, 'b': b})

the paramster "can_be_none" is optional and can be used to specify which parameters can be None.
'''

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