import base64, json,os
from datetime import datetime, date, timedelta
from random import randint

class Data(object):

    def __init__(self,file):
        self.file = file

    def _save_json(self):
        with open(self.file, encoding='utf-8', mode="w") as f:
            json.dump(self.__dict__, f, indent=4,sort_keys=True,
                separators=(',',' : '))
        return self.__dict__

    def read(self):
        with open(self.file, encoding='utf-8', mode="r") as f:
            data = json.load(f)
        self.from_json(**data)

    @property
    def save(self):
        return 1

    @save.getter
    def save(self):
        self._save_json()
        return 1

    def from_json(self,**kwarg):
        if not self.__dict__:
            self.__dict__ = {}
        for a,b in kwarg.items():
            if type(b) is dict:
                b = Data(**b)
            elif type(b) is list:
                c = []
                for d in b:
                    if type(d) is dict:
                        d = Data(**d)
                    c.append(d)
                b = c
            self.__dict__[a] = b
        
    def to_json(self):
        d = {}
        for key, value in self.__dict__.items():
            if value != None:
                if type(value) is Data:
                    value = value.to_json()
                elif isinstance(value, (str,int)):
                    value = value
                elif isinstance(value, bytes):
                    value = base64.b64encode(value).decode('ascii')
                elif isinstance(value, datetime):
                    value = value.isoformat()
                elif type(value) is list:
                    a = []
                    for b in value:
                        if type(b) is Data:
                            b = b.to_json()
                        elif isinstance(b, (str,int)):
                            b = b
                        elif isinstance(b, bytes):
                            b = base64.b64encode(b).decode('ascii')
                        elif isinstance(b, datetime):
                            b = b.isoformat()
                        a.append(b)
                    value = a
                else:
                    value = repr(value)
                d[key] = value
        return d

    def stringify(self):
        return json.dumps(self.to_json(),**{"sort_keys":True,"indent":4})

    def __repr__(self):
        return f"{self.stringify()}"

    def __setitem__(self, key, value):
        self.__dict__[key] = value
        self.save

    def __getitem__(self, key):
        return self.__dict__[key]

class Config(object):

    def __init__(self,file=None,**kwarg):
        if kwarg:
            self.from_json(**kwarg)
        elif file:
            self.file = file
            if not os.path.exists(self.file):
                os.makedirs(self.file)
            if not os.path.exists(self.file+"/settings.json"):
                open(self.file+"/settings.json","w").write("{}")
            self.file+="/settings.json"
            self.json = Data(self.file)

    def from_json(self,**kwarg):
        if not self.__dict__:
            self.__dict__ = {}
        for a,b in kwarg.items():
            if type(b) is dict:
                b = Config(**b)
            elif type(b) is list:
                c = []
                for d in b:
                    if type(d) is dict:
                        d = Config(**d)
                    c.append(d)
                b = c
            self.__dict__[a] = b
        
    def to_json(self):
        d = {}
        for key, value in self.__dict__.items():
            if value != None:
                if type(value) in [Config,Data]:
                    value = value.to_json()
                elif isinstance(value, (str,int)):
                    value = value
                elif isinstance(value, bytes):
                    value = base64.b64encode(value).decode('ascii')
                elif isinstance(value, datetime):
                    value = value.isoformat()
                elif type(value) is list:
                    a = []
                    for b in value:
                        if type(b) in [Config,Data]:
                            b = b.to_json()
                        elif isinstance(b, (str,int)):
                            b = b
                        elif isinstance(b, bytes):
                            b = base64.b64encode(b).decode('ascii')
                        elif isinstance(b, datetime):
                            b = b.isoformat()
                        a.append(b)
                    value = a
                else:
                    value = repr(value)
                d[key] = value
        return d

    def stringify(self):
        return json.dumps(self.to_json(),**{"sort_keys":True,"indent":4})

    def __repr__(self):
        return f"{self.stringify()}"

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

if __name__ == '__main__':
    b = {
            "Creator": "Aditya Nugraha",
            "Support": [
                "Ammar Faizi",
                "Lonami",
                "Hibiki"
            ]
        }
    a = Config(**b)
    print(a.stringify())
