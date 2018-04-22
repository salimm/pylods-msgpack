
#include "MsgpackDictionary.h"
#include <Python.h>
 
 

MsgpackDictionary::MsgpackDictionary(PyObject* pdict){
    this->pdict = pdict;
}

int MsgpackDictionary::is_obj_start(PyObject* event){
    return PyLong_AsLong(PyTuple_GetItem(event, 0)) == ET_MAP_START;
}

int MsgpackDictionary::is_obj_end(PyObject* event){
    return PyLong_AsLong(PyTuple_GetItem(event, 0)) == ET_MAP_END;
}


int MsgpackDictionary::is_value(PyObject* event){
    return PyLong_AsLong(PyTuple_GetItem(event, 0)) == ET_VALUE;
}


int MsgpackDictionary::is_obj_property_name(PyObject* event){
    return PyLong_AsLong(PyTuple_GetItem(event, 0)) == ET_MAP_PROPERTY_NAME;
}


int MsgpackDictionary::is_array_start(PyObject* event){
    return PyLong_AsLong(PyTuple_GetItem(event, 0)) == ET_ARRAY_START;
}


int MsgpackDictionary::is_array_end(PyObject* event){
    return PyLong_AsLong(PyTuple_GetItem(event, 0)) == ET_ARRAY_END;
}

PyObject* MsgpackDictionary::get_pdict(){
    return this->pdict;
}


PyObject* MsgpackDictionary::read_value(PyObject* event){
    PyObject* value = PyTuple_GetItem(event, 2);
    Py_INCREF(value);
    return value;
}
