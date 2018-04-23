'''
Created on Jan 21, 2018

@author: Salim
'''
from pylodsmsgpack.pylodsmsgpack import MsgPackGenerator, MsgPackObjectMapper,\
    MsgPackParser, MsgpackCMapperBackend, MsgPackDictionary
from _io import BytesIO
from pylods.backend.pylodsc.mapper import CObjectMapper
from pylods.backend.pylodsp.mapper import PyObjectMapper
from pylods.decorators import type_attr, order_attr
import msgpackstream.backend.pyc.stream as msgpackc
from pylods.deserialize import EventBasedDeserializer


gen = MsgPackGenerator()


class Job():
    
    def __init__(self, name=None, location=None):
        self.name = name
        self.location = location
        
@type_attr('jobs', Job)
@order_attr('firstname',1)
@order_attr('lastname',2)
@order_attr('jobs',3)
class PersonInfo():
    
    def __init__(self, firstname=None, lastname=None, jobs=None):
        self.firstname = firstname
        self.lastname = lastname
        self.jobs = jobs
    
    def __str__(self):
        return "{PersonInfo first: " + self.firstname + ", last: " + self.lastname + ", jobs: " + str(self.jobs) + "}";
        
class Test():
    def __init__(self, y=None):
        self.y = y
        
    def __str__(self):
        return "{Test: y:"+self.y+"}"
    
class PersonInfoDeserializer(EventBasedDeserializer):
     
    def deserialize(self, events, pdict, ctxt):
        print("xxxx??XxX??")
        mapper = MsgPackObjectMapper(PyObjectMapper(pdict))
        print(mapper.read_obj_property_name(events))        
        firstname = mapper.read_value(events)
#         print("fn "+firstname)
        mapper.read_obj_property_name(events)
        lastname = mapper.read_value(events)
#         print("ln "+str(lastname))
        mapper.read_obj_property_name(events)
        jobs = mapper.read_array(events,cls=Job)
        return PersonInfo(firstname, lastname, jobs)
#         

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



data = [PersonInfo("test", "Test", [Job("x", "xloc")]),PersonInfo("test2", "Test2", [Job("x", "xloc"),Job("y", "yloc")])]
buff = BytesIO()
mapper.write(data, buff)


buff.seek(0)
mapper = MsgPackObjectMapper(PyObjectMapper(MsgPackDictionary()))

print(mapper.read_array(MsgPackParser().parse(buff), cls=PersonInfo))
# 
buff.seek(0)
mapper = MsgPackObjectMapper(CObjectMapper(MsgPackDictionary()))
print(mapper.read_array(MsgPackParser().parse(buff), cls=PersonInfo))

buff.seek(0)
mapper = MsgPackObjectMapper(MsgpackCMapperBackend(msgpackc))
print(mapper.read_array(MsgPackParser().parse(buff), cls=PersonInfo))


print("##################################")

data = [PersonInfo("test", "Test", [Job("x", "xloc")]),PersonInfo("test2", "Test2", [Job("x", "xloc"),Job("y", "yloc")])]
buff = BytesIO()
mapper.write(data, buff)


buff.seek(0)
mapper = MsgPackObjectMapper(PyObjectMapper(MsgPackDictionary()))
mapper.register_deserializer(PersonInfo, PersonInfoDeserializer())
print(mapper.read_array(MsgPackParser().parse(buff), cls=PersonInfo))
# 
buff.seek(0)
mapper = MsgPackObjectMapper(CObjectMapper(MsgPackDictionary()))
mapper.register_deserializer(PersonInfo, PersonInfoDeserializer())
print(mapper.read_array(MsgPackParser().parse(buff), cls=PersonInfo))

buff.seek(0)
mapper = MsgPackObjectMapper(MsgpackCMapperBackend(msgpackc))
mapper.register_deserializer(PersonInfo, PersonInfoDeserializer())
print(mapper.read_array(MsgPackParser().parse(buff), cls=PersonInfo))