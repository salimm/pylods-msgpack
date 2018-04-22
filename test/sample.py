'''
Created on Jan 21, 2018

@author: Salim
'''
from pylodsmsgpack.pylodsmsgpack import MsgPackGenerator, MsgPackObjectMapper,\
    MsgPackParser, MsgpackCMapperBackend, MsgPackDictionary
from _io import BytesIO
from pylods.backend.pylodsc.mapper import CObjectMapper
from pylods.backend.pylodsp.mapper import PyObjectMapper
from pylods.decorators import type_attr
import msgpackstream.backend.python.stream as msgpackp
import msgpackstream.backend.pyc.stream as msgpackc


gen = MsgPackGenerator()
        
class Test():
    def __init__(self, y=None):
        self.y = y
        
    def __str__(self):
        return "{Test: y:"+self.y+"}"

@type_attr("ylist",Test)
class XCls():
    
    def __init__(self, x=None,ylist=None):
        self.x = x
        self.ylist = ylist
    
    def __str__(self):
        return "{XCls: x:"+str(self.x)+", y:"+str(self.ylist)+"}"

data = [XCls({"test":1, 'list':range(1, 7), 'list2':range(1, 2 ** 8)
            , 'str':"xxxxxxx"},[Test(1),Test(2),Test(3)])]

# data = [Test(1),Test(2),Test(3)]
# data = [{"x":1},{"x":1},{"x":1},{"x":1}]
# data = {"x":[1,2,3,4,5]}
# data = [1,2,3,4]

mapper = MsgPackObjectMapper(PyObjectMapper(MsgPackDictionary()))

buff = BytesIO()
mapper.write(data, buff)


buff.seek(0)
mapper = MsgPackObjectMapper(PyObjectMapper(MsgPackDictionary()))
print(mapper.read_array(MsgPackParser().parse(buff), cls=XCls))
# 
buff.seek(0)
mapper = MsgPackObjectMapper(CObjectMapper(MsgPackDictionary()))
print(mapper.read_array(MsgPackParser().parse(buff), cls=XCls))

buff.seek(0)
mapper = MsgPackObjectMapper(MsgpackCMapperBackend(msgpackc))
print(mapper.read_array(MsgPackParser().parse(buff), cls=XCls))


data  = data[0]
buff = BytesIO()
mapper.write(data, buff)
buff.seek(0);
mapper = MsgPackObjectMapper(MsgpackCMapperBackend())
print(mapper.read_obj(MsgPackParser().parse(buff), cls=XCls))
