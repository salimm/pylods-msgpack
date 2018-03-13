'''
Created on Jan 21, 2018

@author: Salim
'''
from pylodsmsgpack.pylodsmsgpack import MsgPackGenerator, MsgPackObjectMapper,\
    MsgPackParser
from _io import BytesIO
import umsgpack
import msgpack


def create_instream( bdata):
        buff = BytesIO()
        buff.write(bdata)
        buff.seek(0)
        return buff

gen = MsgPackGenerator()
        
out = BytesIO()
gen.write({"test":1, 'list':range(1, 7), 'list2':range(1, 2 ** 8)
            , 'str':"xxxxxxx"}, out)
out.seek(0)

val = umsgpack.unpackb(out.getvalue())
print(val)


bdata = msgpack.packb([{"x":[[1,2,3,4]]*4, "y":[{1:2}]*10}]*2)

buff = create_instream(bdata)
mapper = MsgPackObjectMapper()
mapper.read_array(MsgPackParser().parse(buff))


