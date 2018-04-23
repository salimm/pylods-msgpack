#include <Python.h>
#include <iostream>
#include "Dictionary.h"
#include "pylodscapi.h"
#include "MsgpackDictionary.h"



enum ParserState convert_state(PyObject* state){
    return static_cast<ParserState>(int(PyInt_AsLong(state)));
}

static PyObject* read_object_msgpack_api(PyObject *self, PyObject *args){
    PyObject* events;
    PyObject* cls;
    PyObject* ctxt;
    PyObject* pdict;
    PyObject* deserializers;
    PyObject*  state;
    PyObject* pName = PyString_FromString("pylods.deserialize"); // new ref
    PyObject*  pModule = PyImport_Import(pName); // new ref
    Py_DECREF(pName); // dec ref
    if (pModule == NULL) {
        // throw exception
    }    


    PyObject* TYPED = PyObject_GetAttrString(pModule, "Typed");
    Py_DECREF(pModule);
    if (!PyArg_ParseTuple(args, "OOOOOO",  &events, &cls, &ctxt, &pdict, &deserializers, &state))
        return NULL;
    enum ParserState  converted_state = convert_state(state);
    MsgpackDictionary* dict = new MsgpackDictionary(pdict);
    PyObject*  result = PYLODSC_ReadObject(events,cls,ctxt, (Dictionary*)dict, deserializers, TYPED, converted_state);
    delete dict;    
    Py_DECREF(TYPED);
    Py_DECREF(state);

    return result;
}


static PyObject* read_array_msgpack_api(PyObject *self, PyObject *args){
    PyObject* events;
    PyObject* cls;
    PyObject* propname;
    PyObject* ctxt;
    PyObject* pdict;
    PyObject* deserializers;
    PyObject*  state;
    PyObject* pName = PyString_FromString("pylods.deserialize"); // new ref
    PyObject*  pModule = PyImport_Import(pName); // new ref
    Py_DECREF(pName); // dec ref
    if (pModule == NULL) {
        // throw exception
    }    
    PyObject* TYPED = PyObject_GetAttrString(pModule, "Typed");
    Py_DECREF(pModule);    
    if (!PyArg_ParseTuple(args, "OOOOOOO",  &events, &cls, &propname, &ctxt, &pdict, &deserializers, &state))
        return NULL;
    enum ParserState  converted_state = convert_state(state);
    MsgpackDictionary* dict = new MsgpackDictionary(pdict);
    PyObject*  result = PYLODSC_ReadArray(events, cls, propname,ctxt, (Dictionary*)dict,  deserializers, TYPED, converted_state);
    delete dict;

    Py_DECREF(TYPED);
    Py_DECREF(state);

    return result;
}


static PyObject * create_mp_class_event_iterator_api(PyObject *self, PyObject *args){
    PyObject* events;
    long int count;
    PyObject* pdict;
    if (!PyArg_ParseTuple(args, "OlO", &events, &count, &pdict))  return NULL;
    Py_INCREF(pdict);
    MsgpackDictionary* dict = new MsgpackDictionary(pdict);
    return PYLODSC_CreateClassEventIterator(events,dict, count );
}

PyMODINIT_FUNC
initplmsgpackcapi(void){    
    if (import_pylodsc() < 0)
        return;
    static PyMethodDef FindMethods[] = {

        {"read_obj",  read_object_msgpack_api, METH_VARARGS,
            "read object"},
        {"read_array",  read_array_msgpack_api, METH_VARARGS,
            "read array"},
        {"create_ClassEventIterator",  create_mp_class_event_iterator_api, METH_VARARGS,
            "creates iterator for custom class parsers for msgpack"},
        {NULL, NULL, 0, NULL}        /* Sentinel */
    };

    PyObject* m=Py_InitModule("plmsgpackcapi", FindMethods);
    if (m == NULL)
        return;
}


int main(int argc, char *argv[])
{
    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(argv[0]);

    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Add a static module */
    initplmsgpackcapi();         
    
    // process(NULL, NULL);
}

