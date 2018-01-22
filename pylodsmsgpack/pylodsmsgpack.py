'''
Created on Nov 26, 2017

@author: Salim
'''
from pylods.deserialize import Parser
from pylods.dict import Dictionary
from pylods.mapper import ObjectMapper
from pylods.serialize import DataFormatGenerator
import msgpackstream.stream as msgpack
from msgpackstream.format import EventType, FormatType

import umsgpack
from _io import BytesIO


class MsgPackDictionary(Dictionary):
    
    def gen_events(self, instream):
        '''
            generates events from parsing the input stream
        '''
        return msgpack.unpack(instream)
    
    def is_obj_start(self, event):
        '''
            indicates if the given or a tuple representing an start of object event
            :param event:
        '''
        return event[1] == EventType.MAP_START
    
    def is_obj_end(self, event):
        '''
            indicates if the given or a tuple representing an end of object event
            :param event:
        '''
        return event[1] == EventType.MAP_END 
        
    def is_value(self, event):
        '''
            indicates if the given or tuple representing an event that represents a raw value
            :param event:
        '''
        return event[1] == EventType.VALUE  
        
    def is_obj_property_name(self, event):
        '''
         indicates if the given event or tuple representing an event is a property name. 
          This library expects to receive the value of the property next. If this value is 
          an object or array, start event for an array or map is expected.
          
        :param event:
        '''
        return event[1] == EventType.MAP_PROPERTY_NAME
         
    def is_array_start(self, event):
        '''
            indicates if the given or tuple representing an event that indicates start of an array
            :param event:
        '''
        return event[1] == EventType.ARRAY_START
    
    def is_array_end(self, event):
        '''
            indicates if the given or tuple representing an event that indicates end of an array
            :param event:
        '''
        return event[1] == EventType.ARRAY_END
    
    def read_value(self, event):
        '''
            Returns the value of an msgpack event 
        '''
        return event[3]
    
    
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
    
    
    def __init__(self):
        Parser.__init__(self, MsgPackDictionary())
        


class MsgPackObjectMapper(ObjectMapper):
    '''
        ObjectMapper for Msgpack
    '''
    
    
    def __init__(self):
        ObjectMapper.__init__(self, MsgPackDictionary());
        
        

class MsgPackGenerator(DataFormatGenerator):
    
    
    def __init__(self):
        super(MsgPackGenerator, self).__init__(MsgPackDictionary())
        
        
        


