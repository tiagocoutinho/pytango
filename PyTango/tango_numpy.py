################################################################################
##
## This file is part of PyTango, a python binding for Tango
## 
## http://www.tango-controls.org/static/PyTango/latest/doc/html/index.html
##
## Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
## 
## PyTango is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## PyTango is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
## 
## You should have received a copy of the GNU Lesser General Public License
## along with PyTango.  If not, see <http://www.gnu.org/licenses/>.
##
################################################################################

"""
This is an internal PyTango module.
"""

__all__ = [ "NumpyType", "numpy_type", "numpy_spectrum", "numpy_image" ]

__docformat__ = "restructuredtext"

import _PyTango

def _numpy_invalid(*args, **kwds):
    _PyTango.Except.throw_exception(
        "PyTango_InvalidConversion",
        "There's no registered conversor to numpy.",
        "NumpyType.tango_to_numpy"
    )

def _define_numpy():
    if not _PyTango.constants.NUMPY_SUPPORT:
        return None, _numpy_invalid, _numpy_invalid, _numpy_invalid
    
    try:
        import numpy
        import operator

        from attribute_proxy import AttributeProxy

        ArgType = _PyTango.CmdArgType
        AttributeInfo = _PyTango.AttributeInfo
        Attribute = _PyTango.Attribute

        class NumpyType(object):

            DevShort = numpy.int16
            DevLong = numpy.int32
            DevDouble = numpy.float64
            DevFloat = numpy.float32
            DevBoolean = numpy.bool8
            DevUShort = numpy.uint16
            DevULong = numpy.uint32
            DevUChar = numpy.ubyte
            DevLong64 = numpy.int64
            DevULong64 = numpy.uint64

            mapping = {
                ArgType.DevShort: DevShort,
                ArgType.DevLong: DevLong,
                ArgType.DevDouble: DevDouble,
                ArgType.DevFloat: DevFloat,
                ArgType.DevBoolean: DevBoolean,
                ArgType.DevUShort: DevUShort,
                ArgType.DevULong: DevULong,
                ArgType.DevUChar: DevUChar,
                ArgType.DevLong64: DevLong64,
                ArgType.DevULong: DevULong64,
            }

            @staticmethod
            def tango_to_numpy(param):
                if isinstance(param, ArgType):
                    tg_type = param
                if isinstance(param, AttributeInfo): # or AttributeInfoEx
                    tg_type = param.data_type
                elif isinstance(param, Attribute):
                    tg_type = param.get_data_type()
                elif isinstance(param, AttributeProxy):
                    tg_type = param.get_config().data_type
                else:
                    tg_type = param
                try:
                    return NumpyType.mapping[tg_type]
                except Exception:
                    _numpy_invalid()

            @staticmethod
            def spectrum(tg_type, dim_x):
                """
                numpy_spectrum(self, tg_type, dim_x, dim_y) -> numpy.array
                numpy_spectrum(self, tg_type, sequence) -> numpy.array

                        Get a square numpy array to be used with PyTango.
                        One version gets dim_x and creates an object with
                        this size. The other version expects any sequence to
                        convert.

                    Parameters:
                        - tg_type : (ArgType): The tango type. For convenience, it
                                    can also extract this information from an
                                    Attribute, AttributeInfo or AttributeProxy
                                    object.
                        - dim_x : (int)
                        - sequence:
                """
                np_type = NumpyType.tango_to_numpy(tg_type)
                if operator.isSequenceType(dim_x):
                    return numpy.array(dim_x, dtype=np_type)
                else:
                    return numpy.ndarray(shape=(dim_x,), dtype=np_type)

            @staticmethod
            def image(tg_type, dim_x, dim_y=None):
                """
                numpy_image(self, tg_type, dim_x, dim_y) -> numpy.array
                numpy_image(self, tg_type, sequence) -> numpy.array

                        Get a square numpy array to be used with PyTango.
                        One version gets dim_x and dim_y and creates an object with
                        this size. The other version expects a square sequence of
                        sequences to convert.

                    Parameters:
                        - tg_type : (ArgType): The tango type. For convenience, it
                                    can also extract this information from an
                                    Attribute, AttributeInfo or AttributeProxy
                                    object.
                        - dim_x : (int)
                        - dim_y : (int)
                        - sequence:
                """
                np_type = NumpyType.tango_to_numpy(tg_type)
                if dim_y is None:
                    return numpy.array(dim_x, dtype=np_type)
                else:
                    return numpy.ndarray(shape=(dim_y,dim_x,), dtype=np_type)
        
        return NumpyType, NumpyType.spectrum, NumpyType.image, NumpyType.tango_to_numpy
        numpy_spectrum = NumpyType.spectrum
        numpy_image = NumpyType.image
        numpy_type = NumpyType.tango_to_numpy
    except Exception:
        return None, _numpy_invalid, _numpy_invalid, _numpy_invalid

NumpyType, numpy_spectrum, numpy_image, numpy_type = _define_numpy()