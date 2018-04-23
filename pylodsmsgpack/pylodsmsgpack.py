'''
Created on Nov 26, 2017

@author: Salim
'''
from pylods.deserialize import Parser, ObjectMapperBackend, DecoratorsModule,\
    DeserializationContext, POPState
from pylods.dict import Dictionary
from pylods.mapper import ObjectMapper
from pylods.serialize import DataFormatGenerator
import msgpackstream.backend.python.stream as msgpackp

import umsgpack
from msgpackstream.defs import EventType, FormatType
from pylods.backend.pylodsp.mapper import PyObjectMapper
from abc import ABCMeta
import plmsgpackcapi
from pylods.error import ParseException


class MsgPackDictionary(Dictionary):
    
    def __init__(self, msgpack = msgpackp):
        super(MsgPackDictionary, self).__init__()
        self.msgpack = msgpack
        
    
    def gen_events(self, instream):
        '''
            generates events from parsing the input stream
        ''' 
        return self.msgpack.unpack(instream)
        
    
    def is_obj_start(self, event):
        '''
            indicates if the given or a tuple representing an start of object event
            :param event:
        '''
        return event[0] == EventType.MAP_START
    
    def is_obj_end(self, event):
        '''
            indicates if the given or a tuple representing an end of object event
            :param event:
        '''
        return event[0] == EventType.MAP_END
        
    def is_value(self, event):
        '''
            indicates if the given or tuple representing an event that represents a raw value
            :param event:
        '''
        return event[0] == EventType.VALUE
        
    def is_obj_property_name(self, event):
        '''
         indicates if the given event or tuple representing an event is a property name. 
          This library expects to receive the value of the property next. If this value is 
          an object or array, start event for an array or map is expected.
          
        :param event:
        '''
        return event[0] == EventType.MAP_PROPERTY_NAME
         
    def is_array_start(self, event):
        '''
            indicates if the given or tuple representing an event that indicates start of an array
            :param event:
        '''
        return event[0] == EventType.ARRAY_START
    
    def is_array_end(self, event):
        '''
            indicates if the given or tuple representing an event that indicates end of an array
            :param event:
        '''
        return event[0] == EventType.ARRAY_END
    
    def read_value(self, event):
        '''
            Returns the value of an msgpack event 
        '''
        return event[2]
    
    
    ######################### OBJECT
    
    def write_object_start(self, numfields, outstream):
        self.write_dict_start(numfields, outstream)

    def write_object_end(self, numfields, outstream):
        self.write_dict_end(numfields, outstream)
    
    def write_object_field_separator(self, name, value, outstream):
        self.write_dict_field_separator(name, value, outstream)
    
    def write_object_field_name(self, name, outstream):
        self.write_dict_field_name(name, outstream)
    
    def write_object_name_value_separator(self, name, value, outstream):
        self.write_dict_name_value_separator(name, value, outstream)

    ######################### ARRAY
    
    def write_array_start(self, length, outstream):
        
        if length <= 15:
            outstream.write(chr((FormatType.FIXARRAY.value.code | length)))  # @UndefinedVariable
        elif length <= (2 ** 16) - 1:
            outstream.write(chr((FormatType.ARRAY_16.value.code)) + chr(length / 256) + chr(length % 256))  # @UndefinedVariable
        else:
            outstream.write(chr((FormatType.ARRAY_32.value.code)) + chr(length / 256 / 256 / 256) + chr(length / 256 / 256 % 256) + chr(length / 256 % 256) + chr(length % 256))  # @UndefinedVariable
            
        
    
    def write_array_end(self, length, outstream):
        pass
    
    def write_array_field_separator(self, value, outstream):
        pass
     
    
    ######################### DICT
    
    def write_dict_start(self, numfields, outstream):
        if numfields <= 15:
            outstream.write(chr((FormatType.FIXMAP.value.code | numfields)))  # @UndefinedVariable
        elif numfields <= (2 ** 16) - 1:
            outstream.write(chr((FormatType.MAP_16.value.code)) + chr(numfields / 256) + chr(numfields % 256))  # @UndefinedVariable
        else:
            outstream.write(chr((FormatType.MAP_32.value.code)) + chr(numfields / 256 / 256 / 256) + chr(numfields / 256 / 256 % 256) + chr(numfields / 256 % 256) + chr(numfields % 256))  # @UndefinedVariable
    
    def write_dict_end(self, numfields, outstream):
        pass
    
    def write_dict_field_separator(self, name, value, outstream):
        pass    
    
    def write_dict_field_name(self, name, outstream):
        self.write_value(name, outstream)
    
    def write_dict_name_value_separator(self, name, value, outstream):
        pass
    
    def write_value(self, val, outstream):
        umsgpack.pack(val, outstream)
            
    
    


class MsgPackParser(Parser):
    '''
        Msgpack Parser extends PylodsParser while using a MsgpackDictionary
    '''
    
    
    def __init__(self, pdict= MsgPackDictionary()):
        Parser.__init__(self, pdict)
        



class MsgpackCMapperBackend(ObjectMapperBackend):
    '''
        Main Parser class to deserialize to objects, values and etc. This parser requires a dictionary to serialize/ deserialize from an input stream
    '''
    
    __classmeta__ = ABCMeta
    
    __slots__ = [ '__deserializers']
    
    
    def __init__(self,msgpack = msgpackp):
        pdict = MsgPackDictionary(msgpack)
        pdict.mapper_backend = self
        super(MsgpackCMapperBackend, self).__init__(pdict) 
        self.__deserializers = {}
        self.register_module(DecoratorsModule())
        
        
    def read_value(self, events):
        val = self._pdict.read_value(next(events))
        return val
            

    def read_obj_property_name(self, events):
        propname = self._pdict.read_value(next(events));
        return propname
    
        
    def read_obj(self, events, cls=dict, state=POPState.EXPECTING_OBJ_START, ctxt=DeserializationContext.create_context()):
        cnt = 0
        if state is POPState.EXPECTING_OBJ_START:
            cnt = 0;
        elif state is POPState.EXPECTING_OBJ_PROPERTY_OR_END:
            cnt = 1
        else:
            raise ParseException("Couldn't start reading an object at this state: " + str(state))
        deserializer = self.__lookup_deserializer(cls)
        if deserializer:
            val = deserializer.execute(plmsgpackcapi.create_ClassEventIterator(events, cnt, self._pdict), self._pdict, ctxt=ctxt)
        else:
            val = self._read_obj(events, cls, state, ctxt)
            
        return val    
    
    
        
    def _read_obj(self, events, cls=dict, state=POPState.EXPECTING_OBJ_START, ctxt=DeserializationContext.create_context()):
        return plmsgpackcapi.read_obj(events, cls, ctxt,self._pdict,self.__deserializers, state.value  );

            
    def read_array(self, events, state=POPState.EXPECTING_ARRAY_START, cls=None, propname=None, ctxt=DeserializationContext.create_context()):
        return plmsgpackcapi.read_array(events, cls, propname, ctxt,self._pdict,self.__deserializers, state.value  );

    

    
     
    
    def __lookup_deserializer(self, cls):
        deserializer = self.__deserializers.get(cls, None)
        if deserializer is None and hasattr(cls, '_pylods'):
            return cls._pylods[cls].get('deserializer', None)
        
        return deserializer;
    
    
    def register_module(self, module):
        for serializer in module.serializers.items():
            self.register_serializer(serializer[0], serializer[1])
            
        for deserializer in module.deserializers.items():
            self.register_deserializer(deserializer[0], deserializer[1])
        
    
    def register_deserializer(self, cls, deserializer):
        self.__deserializers[cls] = deserializer
        
        
    def copy(self):
        '''
         makes a clone copy of the mapper. It won't clone the serializers or deserializers and it won't copy the events
        '''
        try:
            tmp = self.__class__()
        except Exception:
            tmp = self.__class__(self._pdict)
            
        tmp._serializers = self._serializers
        tmp.__deserializers = self.__deserializers

        return tmp
    


class MsgPackObjectMapper(ObjectMapper):
    '''
        ObjectMapper for Msgpack
    '''
    
    
    def __init__(self, backend=PyObjectMapper(MsgPackDictionary())):
        ObjectMapper.__init__(self, backend);
        
        

class MsgPackGenerator(DataFormatGenerator):
    
    
    def __init__(self, pdict= MsgPackDictionary()):
        super(MsgPackGenerator, self).__init__(pdict)
        
        
        


