#ifndef MSGPACK_DICTIONARY_H
#define MSGPACK_DICTIONARY_H

#include "Dictionary.h"
#include <Python.h>
#include <iostream>

enum EventType{
    ET_VALUE = 1,  // value event
    ET_ARRAY_START = 2,  // event that indicates start of an array
    ET_ARRAY_END = 3,  // event that indicates end of an array
    ET_MAP_START = 4,  // event that indicates start of a map
    ET_MAP_END = 5,  // event that indicates end of a map
    ET_MAP_PROPERTY_NAME = 6,  // event that indicates property name
    ET_EXT = 7,  // event that indicates ext value

    ET_NONE_EVENT = -1
};


 // Circle class declaration
class MsgpackDictionary : public Dictionary{
private:   // Accessible by members of this class only

    PyObject* pdict;
   
public:    // Accessible by ALL

    MsgpackDictionary(PyObject* pdict);
	/**
            indicates if the given or a tuple representing an start of object event
            :param event:
    */
    int is_obj_start(PyObject* event) ;

	/**
            indicates if the given or a tuple representing an end of object event
            :param event
    */
	int is_obj_end(PyObject* event) ;

	/**
            indicates if the given or tuple representing an event that represents a raw value
            :param event:
    */
	int is_value(PyObject* event) ;

	/**
            indicates if the given event or tuple representing an event is a property name. 
          This library expects to receive the value of the property next. If this value is 
          an object or array, start event for an array or map is expected.
          
        :param event:
    */
	int is_obj_property_name(PyObject* event) ;

	/**
             indicates if the given or tuple representing an event that indicates start of an array
            :param event:
    */
	int is_array_start(PyObject* event);

	/**
                indicates if the given or tuple representing an event that indicates end of an array
            :param event:
    */
	int is_array_end(PyObject* event) ;

	/**
            Returns the value in the given event or tuple representing the event
    */
	PyObject* read_value(PyObject* event);


    PyObject* get_pdict();

    ~MsgpackDictionary(){};


};


#endif