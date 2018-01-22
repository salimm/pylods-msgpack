'''
Created on Jan 21, 2018

@author: Salim
'''
from pylodsmsgpack.pylodsmsgpack import MsgPackGenerator
from _io import BytesIO
import umsgpack


gen = MsgPackGenerator()
        
out = BytesIO()
gen.write({"test":1, 'list':range(1, 7), 'list2':range(1, 2 ** 8)
            , 'str':"xxxxxxx"}, out)
out.seek(0)

val = umsgpack.unpackb(out.getvalue())
print(val)