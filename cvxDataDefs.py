# Standard OpenVX Data Definition dictionaries.
# There are two dictionaries:
# 1) standardAlias: Map OpenVX type enumeration names to OpenVX type names
# 2) standardTypes: Describe the OpenVX data types in detail

# Probably another day's work in this
# TODO:
# Finish tables
# TODO:
# Constants for each string to reduce size and increase efficiency

# Standard type strings and other things
s_vx_context = 'vx_context'
s_vx_graph = 'vx_graph'
s_vx_node = 'vx_node'
s_vx_kernel = 'vx_kernel'
s_vx_parameter = 'vx_parameter'
s_vx_delay = 'vx_delay'
s_vx_image = 'vx_image'
s_vx_scalar = 'vx_scalar'
s_vx_tensor = 'vx_tensor'
s_vx_reference = 'vx_reference'
s_vx_threshold = 'vx_threshold'
s_vx_lut = 'vx_lut'
s_vx_pyramid = 'vx_pyramid'
s_vx_matrix = 'vx_matrix'
s_vx_array = 'vx_array'
s_vx_convolution = 'vx_convolution'
s_vx_distribution = 'vx_distribution'
s_vx_remap = 'vx_remap'
s_vx_object_array = 'vx_object_array'
s_vx_int8 = 'vx_int8'
s_vx_uint8 = 'vx_uint8'
s_vx_int16 = 'vx_int16'
s_vx_uint16 = 'vx_uint16'
s_vx_int32 = 'vx_int32'
s_vx_uint32 = 'vx_uint32'
s_vx_int64 = 'vx_int64'
s_vx_uint64 = 'vx_uint64'
s_vx_float16 = 'vx_float16'
s_vx_float32 = 'vx_float32'
s_vx_float64 = 'vx_float64'
s_vx_char = 'vx_char'
s_vx_bool = 'vx_bool'
s_vx_size = 'vx_size'
s_vx_df_image = 'vx_df_image'
s_vx_enum = 'vx_enum'

s_vx_df_image_e = 'vx_df_image_e'
s_vx_type_e = 'vx_type_e'

s_input = 'input'
s_output = 'output'
s_input1 = 'input1'
s_input2 = 'input2'
s_in1 = 'in1'
s_in2 = 'in2'
s_out = 'out'
s_src = 'src'
s_dst = 'dst'
s_accum = 'accum'
s_policy = 'policy'
s_OBJECT = 'OBJECT'             # for defining vx_reference object types
s_BASE = 'BASE'                 # for defining base types (do we need this?)
s_OPAQUE = 'OPAQUE'             # for defining types we know nothing about
s_INHERENT = 'INHERENT'         # For defining inherent types (that we should know about)
s_ENUM = 'ENUM'                 # type of constant composed of vendor<<20, id<<12 and a constant
s_ATTRIBUTE = 'ATTRIBUTE'       # type of constant composed of vendor<<20, object type <<8 and a constant
s_KERNEL = 'KERNEL'             # type of constant composed of vendor <<20, lib<<12 and a constant
s_CONSTANT = 'CONSTANTS'        # type of constant that is just a constant
s_STRUCT = 'STRUCT'             # for defining structure types
s_UNION = 'UNION'               # for defining union types
s_ARRAY = 'ARRAY'               # for defining array types

s_VX_ID_KHRONOS = 'VX_ID_KHRONOS'

standardAlias = {
    'VX_TYPE_INVALID': 'vx_invalid',
    'VX_TYPE_CHAR': s_vx_char,
    'VX_TYPE_INT8': s_vx_int8,
    'VX_TYPE_UINT8': s_vx_uint8,
    'VX_TYPE_INT16': s_vx_int16,
    'VX_TYPE_UINT16': s_vx_uint16,
    'VX_TYPE_INT32': s_vx_int32,
    'VX_TYPE_UINT32': s_vx_uint32,
    'VX_TYPE_INT64': s_vx_int64,
    'VX_TYPE_UINT64': s_vx_uint64,
    'VX_TYPE_FLOAT16': s_vx_float16,
    'VX_TYPE_FLOAT32': s_vx_float32,
    'VX_TYPE_FLOAT64': s_vx_float64,
    'VX_TYPE_ENUM': s_vx_enum,
    'VX_TYPE_SIZE': s_vx_size,
    'VX_TYPE_DF_IMAGE': s_vx_df_image,
    'VX_TYPE_BOOL': s_vx_bool,

    'VX_TYPE_RECTANGLE': 'vx_rectangle_t',
    'VX_TYPE_KEYPOINT': 'vx_keypoint_t',
    'VX_TYPE_COORDINATES2D': 'vx_coordinates2d_t',
    'VX_TYPE_COORDINATES3D': 'vx_coordinates3d_t',
    'VX_TYPE_COORDINATES2DF': 'vx_coordinates2df_t',

    'VX_TYPE_NN_CONVOLUTION_PARAMS': 'vx_nn_convolution_params_t',
    'VX_TYPE_NN_DECONVOLUTION_PARAMS': 'vx_nn_deconvolution_params_t',
    'VX_TYPE_NN_ROI_POOL_PARAMS': 'vx_nn_roi_pool_params_t',
        
    'VX_TYPE_HOG_PARAMS': 'vx_hog_t',
    'VX_TYPE_HOUGH_LINES_PARAMS': 'vx_hough_lines_p_t',
    'VX_TYPE_LINE_2D': 'vx_line2d_t',
    'VX_TYPE_TENSOR_MATRIX_MULTIPLY_PARAMS': 'vx_tensor_matrix_multiply_params_t',

    'VX_TYPE_CLASSIFIER_MODEL': 'vx_classifier_model',

    'VX_TYPE_REFERENCE': s_vx_reference,
    'VX_TYPE_CONTEXT': s_vx_context,
    'VX_TYPE_GRAPH': s_vx_graph,
    'VX_TYPE_NODE': s_vx_node,
    'VX_TYPE_KERNEL': s_vx_kernel,
    'VX_TYPE_PARAMETER': s_vx_parameter,

    'VX_TYPE_DELAY': s_vx_delay,
    'VX_TYPE_LUT': s_vx_lut,
    'VX_TYPE_DISTRIBUTION': s_vx_distribution,
    'VX_TYPE_PYRAMID': s_vx_pyramid,
    'VX_TYPE_THRESHOLD': s_vx_threshold,
    'VX_TYPE_MATRIX': s_vx_matrix,
    'VX_TYPE_CONVOLUTION': s_vx_convolution,
    'VX_TYPE_SCALAR': s_vx_scalar,
    'VX_TYPE_ARRAY': s_vx_array,
    'VX_TYPE_IMAGE': s_vx_image,
    'VX_TYPE_REMAP': s_vx_remap,
    'VX_TYPE_OBJECT_ARRAY': s_vx_object_array,
    'VX_TYPE_TENSOR': s_vx_tensor
}

reverseAlias = {v:k for k,v in list(standardAlias.items())}

stClass = 0
stAttrs = 1
stType = 2
stNum = 3

class TypeDef(object):
    # Dictionary that keeps track of all typedefs
    typeDict = dict()
    userStructNext = 0x100

    def __init__(self, name, objtype, vendor=None, id=None, defs=dict(), attrs=dict(), size=None, eltype=None):
        """
        Initialise the type object and put an entry in typedict
        """
        self.objtype = objtype
        self.vendor = vendor
        self.id = id
        self.size = size
        self.eltype = eltype
        self.defs = dict()
        # Get the enum value modifier according to type
        mod = 0
        if objtype == s_KERNEL:
            # Get Vendor id
            v = TypeDef.getTypeVal('vx_vendor_id_e', vendor)
            # Get library id
            l = TypeDef.getTypeVal('vx_library_e', id)
            if v is not None and l is not None:
                mod = (v << 20) | (l << 12)
        elif objtype == s_ATTRIBUTE:
            # Get Vendor id
            v = TypeDef.getTypeVal('vx_vendor_id_e', vendor)
            # Get type id
            t = TypeDef.getTypeVal('vx_type_e', id)
            if v is not None and t is not None:
                mod = (v << 20) | (t << 8)
        elif objtype == s_ENUM:
            # Get Vendor id
            v = TypeDef.getTypeVal('vx_vendor_id_e', vendor)
            # Get enum id
            e = TypeDef.getTypeVal('vx_enum_e', id)
            if v is not None and e is not None:
                mod = (v << 20) | (e << 12)
        if isinstance(defs, list):
            # shortcut for definition when all values are consecutive
            i = 0
            for d in defs:
                self.defs[d] = i | mod
                i += 1
        elif mod != 0 and isinstance(defs, dict):
            for k, v in list(defs.items()):
                self.defs[k] = v | mod
        else:
            self.defs = defs
        self.attrs = attrs
        TypeDef.typeDict[name] = self

    @staticmethod
    def add(name, objtype, vendor=None, id=None, defs=dict(), attr=dict()):
        """
        If the entry with the given name does not exist, add it.
        Return the entry with the given name.
        """
        return TypeDef.get(name) if name in TypeDef.typedict else TypeDef(name, objtype, vendor, id, defs, attr)
    
    @staticmethod
    def getTypeVal(typeName, name, default=None):
        """
        Get an enum value or attribute for a given type
        """
        return TypeDef.typeDict[typeName].defs.get(name, default) if typeName in TypeDef.typeDict else default

    @staticmethod
    def getValueNameFromType(typeName, value, default=None):
        """
        Get the string for a given value in the given enumerated type
        """
        return TypeDef.typeDict[typeName].getLabel(value) if typeName in TypeDef.typeDict else default

    @staticmethod
    def getObjectTypeNameFromValue(value, default=None):
        """
        Get the string for a given type embedded in a value
        Note that this could give misleading results if used inappropriately
        """
        return TypeDef.getValueNameFromType("vx_type_e", TypeDef.getObjectTypeIdVal(value))

    @staticmethod
    def getEnumIdNameFromValue(value, default=None):
        """
        Get the name of the embedded enumeration id as given by vx_enum_e
        Note that this could give misleading results if used inappropriately
        """
        return TypeDef.getValueNameFromType("vx_enum_e", TypeDef.getEnumIdVal(value))

    @staticmethod
    def getEnumTypeNameFromValue(value, default=None):
        """
        Get the name of the enumeration type as given by the embedded enumeration id by
        looking in the definition of vx_enum (rather than vx_enum_e)
        Note that this could give misleading results if used inappropriately
        """
        return TypeDef.getValueNameFromType("vx_enum", TypeDef.getEnumIdVal(value))

    @staticmethod
    def getAttributeTypeNameFromValue(value, default=None):
        """
        Get the actual enumerated type name for an attribute value.
        """
        a = TypeDef.getObjectTypeNameFromValue(value)
        # Form an attribute enumeration name:
        # Type name is VX_TYPE_XXXX, attribute enumeration name is vx_xxxx_attribute_e
        return default if a is None else "vx_%s_attribute_e"%a[8:].lower()
        
    @staticmethod
    def getConstantNameFromValue(value):
        """
        Get the type and string for a given value, assuming that it is in a constant enumeration
        """
        for t, tobj in list(TypeDef.typeDict.items()):
            if tobj.objtype == s_CONSTANT:
                n = tobj.getLabel(value)
                if n is not None:
                    return t, n
        return None, None

    @staticmethod
    def getAttributeNameFromValue(value):
        """
        Get the type and string for a given value, assuming that it is in an attribute enumeration
        """
        for t, tobj in list(TypeDef.typeDict.items()):
            if tobj.objtype == s_ATTRIBUTE:
                n = tobj.getLabel(value)
                if n is not None:
                    return t, n
        return None, None

    @staticmethod
    def getEnumNameFromValue(value):
        """
        Get the type and string for a given value, assuming that it is in a kernel or enum enumeration
        """
        for t, tobj in list(TypeDef.typeDict.items()):
            if tobj.objtype in {s_ENUM, s_KERNEL}:
                n = tobj.getLabel(value)
                if n is not None:
                    return t, n
        return None, None
        
    @staticmethod
    def getValueNameFromValue(value):
        """
        Get the type and string for a given value without knowing the type
        Searches in the following order:
        Constants, enums & kernels, attributes, plain number as vx_uint32.
        """
        t, v = TypeDef.getConstantNameFromValue(value)
        if v is None:
            t, v = TypeDef.getEnumNameFromValue(value)
            if v is None:
                t, v = TypeDef.getAttributeNameFromValue(value)
                if v is None:
                    t, v = s_vx_uint32, value
        return t, v

    @staticmethod
    def getVendorIdVal(value):
        """
        Get the vendor id value from the given enum value
        """
        return (int(value) & 0xFFF00000) >> 20

    @staticmethod
    def getObjectTypeIdVal(value):
        """
        Get the type id from the given enum value
        """
        return (int(value) & 0xFFF00) >> 8

    @staticmethod
    def getEnumIdVal(value):
        """
        Get the enum type id from the given enum value
        """
        return (int(value) & 0xFF000) >> 12

    @staticmethod
    def getLibIdVal(value):
        """
        Get the library id from the given enum value
        """
        return (int(value) & 0xFF000) >> 12

    @staticmethod
    def get(name):
        """
        Get type information for the given name
        """
        return TypeDef.typeDict.get(name)

    @staticmethod
    def keys(name):
        """
        Return a list of the keys for the given name
        """
        return list(TypeDef.get(name).defs.keys()) if name in TypeDef.typeDict else []

    @staticmethod
    def values(name):
        """
        Return a list of the values for the given name
        """
        return list(TypeDef.get(name).defs.values()) if name in TypeDef.typeDict else []

    @staticmethod
    def items(name):
        """
        Return a list of the items for the given name
        """
        return list(TypeDef.get(name).defs.items()) if name in TypeDef.typeDict else []


    @staticmethod
    def labelsValues(name, start=None, end=None, excl=[], sortOnValues=True):
        """
        Return a list of labels and a list of values, sorted on the values
        (default) or labels if sortOnValues is False,
        and in the range start value to end value-1 inclusive but not in
        the iterable excl, which may hold either labels or values
        """
        if name in TypeDef.typeDict:
            defs = TypeDef.typeDict[name].defs
            labels = list(defs.keys())
            labels.sort(key=lambda x:defs[x] if sortOnValues else None)
            values = []
            newLabels = []
            for k in labels:
                v = defs[k]
                if (v >= start or start is None) and \
                   (v < end or end is None) and \
                   (k not in excl or v not in excl):
                    values.append(v)
                    newLabels.append(k)
            return newLabels, values
        else:
            return [], []

    @staticmethod
    def formatToString(value):
        """
        Takes a format id and returns the associated string as used in the XML
        """
        x = ""
        for i in [24, 16, 8, 0]:
            x = x + chr((value >> i) & 0xFF)
        return x

    @staticmethod
    def formatToId(value):
        """
        Takes a format string as used in teh XML and returns the associated integer id
        """
        if value is None:
            return None
        x = 0
        for c in value:
            x = (x << 8) | ord(c)
        return x

    @staticmethod
    def typeFromEnum(enumval, default=None):
        """
        Return a type name like vx_float32 from an enum name like VX_TYPE_FLOAT32
        """
        return standardAlias.get(enumval, default)

    @staticmethod
    def enumFromType(typeval, default=None):
        """
        return an enum name like VX_TYPE_FLOAT32 from a type name like vx_float32
        """
        return reverseAlias.get(typeval, default)

    @staticmethod
    def tagFromEnum(enumval):
        """
        return an XML tag name like 'float32' from an enum name like VX_TYPE_FLOAT32
        (this can have no reverse as all user structs have the same tag)
        """
        if enumval.startswith('VX_TYPE_'):
            tag = enumval[8:].lower()
        else:
            # must be a user type
            tag = 'user'
        return tag

    # @staticmethod
    # def tagFromType(typeval):
    #     """
    #     return an XML tag name like 'float32' from an enum name like VX_TYPE_FLOAT32
    #     (this can have no reverse as all user structs have the same tag)
    #     """
    #     return TypeDef.tagFromEnum(TypeDef.enumFromType(typeval))

    @staticmethod
    def addUserStruct(id, size):
        """
        Add a user struct to the vx_type_e enumeration,
        to the standard & reverse alias and as a new type,
        all if it does not yet exist.
        """
        if id not in TypeDef.typeDict:
            TypeDef.get('vx_type_e').defs[id] = TypeDef.userStructNext
            TypeDef.userStructNext += 1
            standardAlias[id] = id  # makes looking up this type a no-op
            reverseAlias[id] = id
            TypeDef(id, s_ARRAY, size=size, eltype=s_vx_uint8)

    @staticmethod
    def defaultData(name):
        """
        Get a default value for a given data type
        """
        return '0' if name == 'vx_enum' else TypeDef.get(name).getDefaultData()

    def getDefaultData(self):
        """
        Return default data for this type
        This is:
        For a struct, union or object, a dictionary
        For an array, a list of values as strings
        For an opaque type, an empty string
        Otherwise, a value as a string.
        """
        if self.objtype in {s_STRUCT, s_UNION, s_OBJECT}:
            data = {}
            for k, v in list(self.defs.items()):
                data[k] = TypeDef.defaultData(v)
            return data
        elif self.objtype == s_INHERENT:
            return self.eltype
        elif self.objtype == s_ARRAY:
            return [TypeDef.defaultData(self.eltype)] * int(self.size)
        elif self.objtype == s_OPAQUE:
            # we know nothing about this type, can only return an empty string
            return ""
        else:
            # pick the first value from the enumeration
            return str(list(self.defs.values())[0])
        
    def getVal(self, name, default=None):
        """
        Get an attribute value for this object.
        """
        if name in self.defs:
            return self.defs[name]
        else:
            return self.attr.get(name)

    def getLabel(self, value, default=None):
        """
        Return the label for the given enumerated value
        """
        # just look for the enum value in self.defs
        for k, v in list(self.defs.items()):
            if v == value:
                return k
        return default

    def isInherent(self):
        """
        Tests if the type is inherent
        """
        return self.objtype == s_INHERENT
    
    def isBase(self):
        """
        Tests if the type is a base type.
        If the type is a base type, it's defs have keys
        which are type names and values which are enum labels
        of vx_type_e, or None, if the type is not available there.
        """
        return self.objtype == s_BASE

    def isEnum(self):
        return self.objtype == s_ENUM

    def isAttribute(self):
        return self.objtype == s_ATTRIBUTE

    def isKernel(self):
        return self.objtype == s_KERNEL

    def isConstant(self):
        return self.objtype == s_CONSTANT

    def isAllEnum(self):
        """
        Tests if the type is an enumerated type, including
        attributes, kernels, and constants
        """
        return self.objtype in {s_ATTRIBUTE, s_CONSTANT, s_ENUM, s_KERNEL}
    
    def isStruct(self):
        """
        Tests if the type is a struct or union
        """
        return self.objtype in {s_STRUCT, s_UNION}

    def isArray(self):
        """
        Tests if the type is an array
        """
        return self.objtype == s_ARRAY

# Standard constants - must be entered first
TypeDef('vx_library_e', s_CONSTANT, defs=dict(VX_LIBRARY_KHR_BASE = 0x0))
TypeDef('vx_vendor_id_e', s_CONSTANT, defs=dict(
    VX_ID_KHRONOS   = 0x000, # The Khronos Group */
    VX_ID_TI        = 0x001, # Texas Instruments, Inc. */
    VX_ID_QUALCOMM  = 0x002, # Qualcomm, Inc. */
    VX_ID_NVIDIA    = 0x003, # NVIDIA Corporation */
    VX_ID_ARM       = 0x004, # ARM Ltd. */
    VX_ID_BDTI      = 0x005, # Berkley Design Technology, Inc. */
    VX_ID_RENESAS   = 0x006, # Renasas Electronics */
    VX_ID_VIVANTE   = 0x007, # Vivante Corporation */
    VX_ID_XILINX    = 0x008, # Xilinx Inc. */
    VX_ID_AXIS      = 0x009, # Axis Communications */
    VX_ID_MOVIDIUS  = 0x00A, # Movidius Ltd. */
    VX_ID_SAMSUNG   = 0x00B, # Samsung Electronics */
    VX_ID_FREESCALE = 0x00C, # Freescale Semiconductor */
    VX_ID_AMD       = 0x00D, # Advanced Micro Devices */
    VX_ID_BROADCOM  = 0x00E, # Broadcom Corporation */
    VX_ID_INTEL     = 0x00F, # Intel Corporation */
    VX_ID_MARVELL   = 0x010, # Marvell Technology Group Ltd. */
    VX_ID_MEDIATEK  = 0x011, # MediaTek, Inc. */
    VX_ID_ST        = 0x012, # STMicroelectronics */
    VX_ID_CEVA      = 0x013, # CEVA DSP */
    VX_ID_ITSEEZ    = 0x014, # Itseez, Inc. */
    VX_ID_IMAGINATION=0x015, # Imagination Technologies */
    VX_ID_NXP       = 0x016, # NXP Semiconductors */
    VX_ID_VIDEANTIS = 0x017, # Videantis */
    VX_ID_SYNOPSYS  = 0x018, # Synopsys */
    VX_ID_CADENCE   = 0x019, # Cadence */
    VX_ID_HUAWEI    = 0x01A, # Huawei */
    VX_ID_SOCIONEXT = 0x01B # Socionext */
    ))
TypeDef(s_vx_type_e, s_CONSTANT, defs=dict(
        VX_TYPE_INVALID = 0,
        VX_TYPE_CHAR = 1,
        VX_TYPE_INT8 = 2,
        VX_TYPE_UINT8 = 3,
        VX_TYPE_INT16 = 4,
        VX_TYPE_UINT16 = 5,
        VX_TYPE_INT32 = 6,
        VX_TYPE_UINT32 = 7,
        VX_TYPE_INT64 = 8,
        VX_TYPE_UINT64 = 9,
        VX_TYPE_FLOAT32 = 10,
        VX_TYPE_FLOAT64 = 11,
        VX_TYPE_ENUM = 12,
        VX_TYPE_SIZE = 13,
        VX_TYPE_DF_IMAGE = 14,
        VX_TYPE_FLOAT16 = 15,
        VX_TYPE_BOOL = 16,

        VX_TYPE_RECTANGLE = 0X20,
        VX_TYPE_KEYPOINT = 0X21,
        VX_TYPE_COORDINATES2D = 0X22,
        VX_TYPE_COORDINATES3D = 0X23,
        VX_TYPE_COORDINATES2DF = 0X24,
        
        VX_TYPE_NN_CONVOLUTION_PARAMS = 0X25,
		VX_TYPE_NN_DECONVOLUTION_PARAMS = 0X26,
		VX_TYPE_NN_ROI_POOL_PARAMS = 0X27,

        VX_TYPE_HOG_PARAMS = 0X28,
	    VX_TYPE_HOUGH_LINES_PARAMS = 0X29,
	    VX_TYPE_LINE_2D = 0X2A,
	    VX_TYPE_TENSOR_MATRIX_MULTIPLY_PARAMS = 0X2B,

        VX_TYPE_CLASSIFIER_MODEL = 0x2C,
        
        VX_TYPE_REFERENCE = 0X800,
        VX_TYPE_CONTEXT = 0X801,
        VX_TYPE_GRAPH = 0X802,
        VX_TYPE_NODE = 0X803,
        VX_TYPE_KERNEL = 0X804,
        VX_TYPE_PARAMETER = 0X805,
        
        VX_TYPE_DELAY = 0X806,
        VX_TYPE_LUT = 0X807,
        VX_TYPE_DISTRIBUTION = 0X808,
        VX_TYPE_PYRAMID = 0X809,
        VX_TYPE_THRESHOLD = 0X80A,
        VX_TYPE_MATRIX = 0X80B,
        VX_TYPE_CONVOLUTION = 0X80C,
        VX_TYPE_SCALAR = 0X80D,
        VX_TYPE_ARRAY = 0X80E,
        VX_TYPE_IMAGE = 0X80F,
        VX_TYPE_REMAP = 0X810,

        VX_TYPE_OBJECT_ARRAY = 0X813,
        VX_TYPE_TENSOR = 0X815))

TypeDef(s_vx_df_image_e, s_CONSTANT, defs=dict(
        VX_DF_IMAGE_VIRT = TypeDef.formatToId('VIRT'),
        VX_DF_IMAGE_RGB = TypeDef.formatToId('RGB2'),
        VX_DF_IMAGE_RGBX = TypeDef.formatToId('RGBA'),
        VX_DF_IMAGE_NV12 = TypeDef.formatToId('NV12'),
        VX_DF_IMAGE_NV21 = TypeDef.formatToId('NV21'),
        VX_DF_IMAGE_UYVY = TypeDef.formatToId('UYVY'),
        VX_DF_IMAGE_YUYV = TypeDef.formatToId('YUYV'),
        VX_DF_IMAGE_IYUV = TypeDef.formatToId('IYUV'),
        VX_DF_IMAGE_YUV4 = TypeDef.formatToId('YUV4'),
        VX_DF_IMAGE_U8 = TypeDef.formatToId('U008'),
        VX_DF_IMAGE_U16 = TypeDef.formatToId('U016'),
        VX_DF_IMAGE_S16 = TypeDef.formatToId('S016'),
        VX_DF_IMAGE_U32 = TypeDef.formatToId('U032'),
        VX_DF_IMAGE_S32 = TypeDef.formatToId('S032')))

TypeDef('vx_enum_e', s_CONSTANT, defs=dict(
    VX_ENUM_DIRECTION                   = 0x00, 
    VX_ENUM_ACTION                      = 0x01,
    VX_ENUM_HINT                        = 0x02,
    VX_ENUM_DIRECTIVE                   = 0x03,
    VX_ENUM_INTERPOLATION               = 0x04,
    VX_ENUM_OVERFLOW                    = 0x05,
    VX_ENUM_COLOR_SPACE                 = 0x06,
    VX_ENUM_COLOR_RANGE                 = 0x07,
    VX_ENUM_PARAMETER_STATE             = 0x08,
    VX_ENUM_CHANNEL                     = 0x09,
    VX_ENUM_CONVERT_POLICY              = 0x0A,
    VX_ENUM_THRESHOLD_TYPE              = 0x0B,
    VX_ENUM_BORDER                      = 0x0C,
    VX_ENUM_COMPARISON                  = 0x0D,
    VX_ENUM_MEMORY_TYPE                 = 0x0E,
    VX_ENUM_TERM_CRITERIA               = 0x0F,
    VX_ENUM_NORM_TYPE                   = 0x10,
    VX_ENUM_ACCESSOR                    = 0x11,
    VX_ENUM_ROUND_POLICY                = 0x12,
    VX_ENUM_TARGET                      = 0x13,
    VX_ENUM_BORDER_POLICY               = 0x14,
    VX_ENUM_GRAPH_STATE                 = 0x15,
    VX_ENUM_NONLINEAR                   = 0x16,
    VX_ENUM_PATTERN                     = 0x17,
    VX_ENUM_LBP_FORMAT                  = 0x18,
    VX_ENUM_COMP_METRIC                 = 0x19,
    VX_ENUM_NN_ROUNDING_TYPE            = 0x1A,
    VX_ENUM_NN_POOLING_TYPE	            = 0x1B,
    VX_ENUM_NN_NORMALIZATION_TYPE       = 0x1C,
    VX_ENUM_NN_ACTIVATION_FUNCTION_TYPE = 0x1D,
	VX_ENUM_CLASSIFIER_MODEL            = 0x1E, 
    VX_ENUM_IX_USE                      = 0x1F))

# Standard attributes
TypeDef('vx_delay_attribute_e', s_ATTRIBUTE, s_VX_ID_KHRONOS, 'VX_TYPE_DELAY',
        dict(VX_DELAY_TYPE = 0,
        VX_DELAY_SLOTS = 1))
TypeDef('vx_lut_attribute_e', s_ATTRIBUTE, s_VX_ID_KHRONOS, 'VX_TYPE_LUT',
        dict(VX_LUT_TYPE = 0,
        VX_LUT_COUNT = 1,
        VX_LUT_SIZE = 2,
        VX_LUT_OFFSET = 3))
TypeDef('vx_pyramid_attribute_e', s_ATTRIBUTE, s_VX_ID_KHRONOS, 'VX_TYPE_PYRAMID',
        ['VX_PYRAMID_LEVELS',
        'VX_PYRAMID_SCALE',
        'VX_PYRAMID_WIDTH',
        'VX_PYRAMID_HEIGHT',
        'VX_PYRAMID_FORMAT'])
TypeDef('vx_distribution_attribute_e', s_ATTRIBUTE, s_VX_ID_KHRONOS, 'VX_TYPE_PYRAMID',
        ['VX_DISTRIBUTION_DIMENSIONS',
         'VX_DISTRIBUTION_OFFSET',
         'VX_DISTRIBUTION_RANGE',
         'VX_DISTRIBUTION_BINS',
         'VX_DISTRIBUTION_WINDOW',
         'VX_DISTRIBUTION_SIZE'])
TypeDef('vx_threshold_attribute_e', s_ATTRIBUTE, s_VX_ID_KHRONOS, 'VX_TYPE_THRESHOLD',
        ['VX_THRESHOLD_TYPE',
        'VX_THRESHOLD_THRESHOLD_VALUE',
        'VX_THRESHOLD_THRESHOLD_LOWER',
        'VX_THRESHOLD_THRESHOLD_UPPER',
        'VX_THRESHOLD_TRUE_VALUE',
        'VX_THRESHOLD_FALSE_VALUE',
        'VX_THRESHOLD_DATA_TYPE',
        'VX_THRESHOLD_INPUT_FORMAT',
        'VX_THRESHOLD_OUTPUT_FORMAT'])
TypeDef('vx_matrix_attribute_e', s_ATTRIBUTE, s_VX_ID_KHRONOS, 'VX_TYPE_MATRIX',
        ['VX_MATRIX_TYPE',
        'VX_MATRIX_ROWS',
        'VX_MATRIX_COLUMNS',
        'VX_MATRIX_SIZE',
        'VX_MATRIX_ORIGIN',
        'VX_MATRIX_PATTERN'])
TypeDef('vx_convolution_attribute_e', s_ATTRIBUTE, s_VX_ID_KHRONOS, 'VX_TYPE_CONVOLUTION',
        ['VX_CONVOLUTION_ROWS',
        'VX_CONVOLUTION_COLUMNS',
        'VX_CONVOLUTION_SCALE',
        'VX_CONVOLUTION_SIZE'])
TypeDef('vx_scalar_attribute_e', s_ATTRIBUTE, s_VX_ID_KHRONOS, 'VX_TYPE_SCALAR',
        ['VX_SCALAR_TYPE'])
TypeDef('vx_array_attribute_e', s_ATTRIBUTE, s_VX_ID_KHRONOS, 'VX_TYPE_ARRAY',
        ['VX_ARRAY_ITEMTYPE',
        'VX_ARRAY_NUMITEMS',
        'VX_ARRAY_CAPACITY',
        'VX_ARRAY_ITEMSIZE'])
TypeDef('vx_image_attribute_e', s_ATTRIBUTE, s_VX_ID_KHRONOS, 'VX_TYPE_IMAGE',
        ['VX_IMAGE_WIDTH',
        'VX_IMAGE_HEIGHT',
        'VX_IMAGE_FORMAT',
        'VX_IMAGE_PLANES',
        'VX_IMAGE_SPACE',
        'VX_IMAGE_RANGE',
        'VX_IMAGE_SIZE'
        'VX_IMAGE_MEMORY_TYPE',
        'VX_IMAGE_IS_UNIFORM',
        'VX_IMAGE_UNIFORM_VALUE'])
TypeDef('vx_remap_attribute_e', s_ATTRIBUTE, s_VX_ID_KHRONOS, 'VX_TYPE_REMAP',
        ['VX_REMAP_SOURCE_WIDTH',
        'VX_REMAP_SOURCE_HEIGHT',
        'VX_REMAP_DESTINATION_WIDTH',
        'VX_REMAP_DESTINATION_HEIGHT'
        ])
TypeDef('vx_object_array_attribute_e', s_ATTRIBUTE, s_VX_ID_KHRONOS, 'VX_TYPE_OBJECT_ARRAY',
        ['VX_OBJECT_ARRAY_ITEMTYPE',
        'VX_OBJECT_ARRAY_NUMITEMS'])
TypeDef('vx_tensor_attribute_e', s_ATTRIBUTE, s_VX_ID_KHRONOS, 'VX_TYPE_TENSOR',
        ['VX_TENSOR_NUMBER_OF_DIMS',
        'VX_TENSOR_DIMS',
        'VX_TENSOR_DATA_TYPE',
        'VX_TENSOR_FIXED_POINT_POSITION'])

# Standard enumerations
TypeDef('vx_threshold_type_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_THRESHOLD_TYPE',
        ['VX_THRESHOLD_TYPE_BINARY',
        'VX_THRESHOLD_TYPE_RANGE'])
TypeDef('vx_pattern_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_PATTERN',
        ['VX_PATTERN_BOX',
        'VX_PATTERN_CROSS',
        'VX_PATTERN_DISK',
        'VX_PATTERN_OTHER'])
TypeDef('vx_color_space_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_COLOR_SPACE',
        ['VX_COLOR_SPACE_NONE',    
        'VX_COLOR_SPACE_BT601_525',
        'VX_COLOR_SPACE_BT601_625',
        'VX_COLOR_SPACE_BT709',
        'VX_COLOR_SPACE_DEFAULT'])
TypeDef('vx_channel_range_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_COLOR_RANGE',
        ['VX_CHANNEL_RANGE_FULL',
        'VX_CHANNEL_RANGE_RESTRICTED'])
TypeDef('vx_memory_type_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_MEMORY_TYPE',
        ['VX_MEMORY_TYPE_NONE',
        'VX_MEMORY_TYPE_HOST'])
TypeDef('vx_convert_policy_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_CONVERT_POLICY',
        ['VX_CONVERT_POLICY_WRAP',
        'VX_CONVERT_POLICY_SATURATE'])
TypeDef('vx_round_policy_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_ROUND_POLICY',
        ['VX_ROUND_POLICY_TO_ZERO',
        'VX_ROUND_POLICY_TO_NEAREST_EVEN'])
TypeDef('vx_termination_criteria_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_TERM_CRITERIA',
        ['VX_TERM_CRITERIA_ITERATIONS',
        'VX_TERM_CRITERIA_EPSILON',
        'VX_TERM_CRITERIA_BOTH'])
TypeDef('vx_non_linear_filter_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_NONLINEAR',
        ['VX_NONLINEAR_FILTER_MEDIAN',
        'VX_NONLINEAR_FILTER_MIN',
        'VX_NONLINEAR_FILTER_MAX'])
TypeDef('vx_interpolation_type_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_INTERPOLATION',
        ['VX_INTERPOLATION_NEAREST_NEIGHBOR',
        'VX_INTERPOLATION_BILINEAR',
        'VX_INTERPOLATION_AREA'])
TypeDef('vx_lbp_format_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_LBP_FORMAT',
        ['VX_LBP',
        'VX_MLBP',
        'VX_ULBP'])
TypeDef('vx_norm_type_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_NORM_TYPE',
        ['VX_NORM_L1', 'VX_NORM_L2'])
TypeDef('vx_channel_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_CHANNEL',
        ['VX_CHANNEL_0',
        'VX_CHANNEL_1',
        'VX_CHANNEL_2',
        'VX_CHANNEL_3',
        'VX_CHANNEL_R',
        'VX_CHANNEL_G',
        'VX_CHANNEL_B',
        'VX_CHANNEL_A',
        'VX_CHANNEL_Y',
        'VX_CHANNEL_U',
        'VX_CHANNEL_V'])
TypeDef('vx_scalar_operation_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_SCALAR_OPERATION',
        ['VX_SCALAR_OP_AND',
        'VX_SCALAR_OP_OR',
        'VX_SCALAR_OP_XOR',
        'VX_SCALAR_OP_NAND',
        'VX_SCALAR_OP_EQUAL',
        'VX_SCALAR_OP_NOTEQUAL',
        'VX_SCALAR_OP_LESS',
        'VX_SCALAR_OP_LESSEQ',
        'VX_SCALAR_OP_GREATER',
        'VX_SCALAR_OP_GREATEREQ',
        'VX_SCALAR_OP_ADD',
        'VX_SCALAR_OP_SUBTRACT',
        'VX_SCALAR_OP_MULTIPLY',
        'VX_SCALAR_OP_DIVIDE',
        'VX_SCALAR_OP_MODULUS',
        'VX_SCALAR_OP_MIN',
        'VX_SCALAR_OP_MAX'])
TypeDef('vx_comp_metric_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_COMP_METRIC',
        ['VX_COMPARE_HAMMING',
        'VX_COMPARE_L1',
        'VX_COMPARE_L2',
        'VX_COMPARE_CCORR',
        'VX_COMPARE_L2_NORM',
        'VX_COMPARE_CCORR_NORM'])
TypeDef('vx_border_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_BORDER',
        ['VX_BORDER_UNDEFINED',
        'VX_BORDER_CONSTANT',
        'VX_BORDER_REPLICATE'])
TypeDef('vx_direction_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_DIRECTION',
        ['VX_INPUT', 'VX_OUTPUT', 'VX_BIDIRECTIONAL'])
TypeDef('vx_hint_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_HINT',
        ['VX_HINT_PERFORMANCE_DEFAULT',
        'VX_HINT_PERFORMANCE_LOW_POWER',
        'VX_HINT_PERFORMANCE_HIGH_SPEED'])
TypeDef('vx_graph_state_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_GRAPH_STATE',
        ['VX_GRAPH_STATE_UNVERIFIED',
        'VX_GRAPH_STATE_VERIFIED',
        'VX_GRAPH_STATE_RUNNING',
        'VX_GRAPH_STATE_ABANDONED',
        'VX_GRAPH_STATE_COMPLETED'])
TypeDef('vx_directive_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_DIRECTIVE',
        ['VX_DIRECTIVE_DISABLE_LOGGING',
        'VX_DIRECTIVE_ENABLE_LOGGING',
        'VX_DIRECTIVE_DISABLE_PERFORMANCE',
        'VX_DIRECTIVE_ENABLE_PERFORMANCE'])
TypeDef('vx_action_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_ACTION',
        ['VX_ACTION_CONTINUE',
        'VX_ACTION_ABANDON'])
TypeDef('vx_ix_use_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_IX_USE',
        ['VX_IX_USE_APPLICATION_CREATE', 'VX_IX_USE_EXPORT_VALUES', 'VX_IX_USE_NO_EXPORT_VALUES'])
TypeDef('vx_nn_rounding_type_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_NN_ROUNDING_TYPE',
        ['VX_NN_DS_SIZE_ROUNDING_FLOOR', 'VX_NN_DS_SIZE_ROUNDING_CEILING'])
TypeDef('vx_nn_pooling_type_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_NN_POOLING_TYPE',
        ['VX_NN_POOLING_MAX', 'VX_NN_POOLING_AVG'])
TypeDef('vx_nn_norm_type_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_NN_NORMALIZATION_TYPE',
        ['VX_NN_NORMALIZATION_SAME_MAP', 'VX_NN_NORMALIZATION_ACROSS_MAPS'])
TypeDef('vx_nn_activation_function_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_NN_ACTIVATION_FUNCTION_TYPE',
        ['VX_NN_ACTIVATION_LOGISTIC', 'VX_NN_ACTIVATION_HYPERBOLIC_TAN', 'VX_NN_ACTIVATION_RELU',
        'VX_NN_ACTIVATION_BRELU', 'VX_NN_ACTIVATION_SOFTRELU', 'VX_NN_ACTIVATION_ABS',
        'VX_NN_ACTIVATION_SQUARE', 'VX_NN_ACTIVATION_SQRT', 'VX_NN_ACTIVATION_LINEAR'])
TypeDef('vx_classifier_model_format_e', s_ENUM, s_VX_ID_KHRONOS, 'VX_ENUM_CLASSIFIER_MODEL',
        ['VX_CLASSIFIER_MODEL_UNDEFINED'])
# Structures and unions
TypeDef('vx_border_t',s_STRUCT, defs=
                    {'mode':'vx_border_e',
                    'constant_value':'vx_pixel_value_t'})
TypeDef('vx_pixel_value_t', s_UNION, defs=
                    {'RGB':'vx_uint8[3]',
                    'RGBX':'vx_uint8[4]',
                    'YUV':'vx_uint8[3]',
                    'U8':s_vx_uint8,
                    'U16':s_vx_uint16,
                    'S16':s_vx_int16,
                    'U32':s_vx_uint32,
                    'S32':s_vx_int32,
                    'reserved':'vx_uint8[16]'})
TypeDef('vx_hog_t',s_STRUCT, defs=
        {'cell_width': s_vx_int32,
        'cell_height': s_vx_int32,
        'block_width': s_vx_int32,
        'block_height': s_vx_int32,
        'block_stride': s_vx_int32,
        'num_bins': s_vx_int32,
        'window_width': s_vx_int32,
        'window_height': s_vx_int32,
        'window_stride': s_vx_int32,
        'threshold': s_vx_float32})
TypeDef('vx_hough_lines_p_t',s_STRUCT, defs=
        {'rho': s_vx_float32,
        'theta': s_vx_float32,
        'threshold': s_vx_int32,
        'line_length': s_vx_int32,
        'line_gap': s_vx_int32,
        'theta_max': s_vx_float32,
        'theta_min': s_vx_float32}),
TypeDef('vx_tensor_matrix_multiply_params_t',s_STRUCT, defs=
        {'transpose_input1': s_vx_bool,
        'transpose_input2': s_vx_bool,
        'transpose_input3': s_vx_bool
        })
TypeDef('vx_keypoint_t', s_STRUCT, defs=dict(
        x = s_vx_int32,
        y = s_vx_int32,
        strength = s_vx_float32,
        scale = s_vx_float32,
        orientation = s_vx_float32,
        tracking_status = s_vx_int32,
        error = s_vx_float32))
TypeDef('vx_line2d_t', s_STRUCT, defs=dict(
        start_x = s_vx_float32,
        start_y = s_vx_float32,
        end_x = s_vx_float32,
        end_y = s_vx_float32))
TypeDef('vx_rectangle_t', s_STRUCT, defs=dict(
        start_x = s_vx_uint32,
        start_y = s_vx_uint32,
        end_x = s_vx_uint32,
        end_y = s_vx_uint32))
TypeDef('vx_coordinates2d_t', s_STRUCT, defs=dict(
        x = s_vx_uint32,
        y = s_vx_uint32))
TypeDef('vx_coordinates2df_t', s_STRUCT, defs=dict(
        x = s_vx_float32,
        y = s_vx_float32))
TypeDef('vx_coordinates3d_t', s_STRUCT, defs=dict(
        x = s_vx_uint32,
        y = s_vx_uint32,
        z = s_vx_uint32))
TypeDef('vx_nn_convolution_params_t', s_STRUCT, defs=dict(
        padding_x = s_vx_size,
        padding_y = s_vx_size,
        overflow_policy = 'vx_convert_policy_e',
        rounding_policy = 'vx_round_policy_e',
        down_scale_size_rounding = 'vx_nn_rounding_type_e',
        dilation_x = s_vx_size,
        dilation_y = s_vx_size))
TypeDef('vx_nn_deconvolution_params_t', s_STRUCT, defs=dict(
        padding_x = s_vx_size,
        padding_y = s_vx_size,
        overflow_policy = 'vx_convert_policy_e',
        rounding_policy = 'vx_round_policy_e',
        a_x = s_vx_size,
        a_y = s_vx_size))
TypeDef('vx_nn_roi_pool_params_t', s_STRUCT, defs=dict(
        pool_type = 'vx_nn_pooling_type_e'))
# Arrays
TypeDef('vx_uint8[3]', s_ARRAY, size=3, eltype=s_vx_uint8)
TypeDef('vx_uint8[4]', s_ARRAY, size=4, eltype=s_vx_uint8)
TypeDef('vx_uint8[16]', s_ARRAY, size=16, eltype=s_vx_uint8)

# Inherent types with their default values
TypeDef(s_vx_size, s_INHERENT, eltype="0")
TypeDef(s_vx_char, s_INHERENT, eltype='.')
TypeDef(s_vx_bool, s_INHERENT, eltype="false")
TypeDef(s_vx_int8, s_INHERENT, eltype="0")
TypeDef(s_vx_uint8, s_INHERENT, eltype="0")
TypeDef(s_vx_int16, s_INHERENT, eltype="0")
TypeDef(s_vx_uint16, s_INHERENT, eltype="0")
TypeDef(s_vx_int32, s_INHERENT, eltype="0")
TypeDef(s_vx_uint32, s_INHERENT, eltype="0")
TypeDef(s_vx_int64, s_INHERENT, eltype="0")
TypeDef(s_vx_uint64, s_INHERENT, eltype="0")
TypeDef(s_vx_float16, s_INHERENT, eltype="0.0")
TypeDef(s_vx_float32, s_INHERENT, eltype="0.0")
TypeDef(s_vx_float64, s_INHERENT, eltype="0.0")
TypeDef('vx_invalid', s_INHERENT, eltype="")
TypeDef(s_vx_df_image, s_INHERENT, eltype="U008")

# Opaque types
TypeDef('vx_classifier_model', s_OPAQUE)  # we know nothing about this

# Base types - first, vx_enum. We assign arbitrary indices to all enumerated types,
# and include 'vx_uint32' as the first item, after sorting the rest.
newlist = []
for name, obj in list(TypeDef.typeDict.items()):
    if name.endswith("_e"):
        newlist.append(name)
newlist.sort()
newlist.insert(0, s_vx_uint32)
TypeDef(s_vx_enum, s_BASE, defs=newlist)
del newlist

# Now the vx_reference objects
TypeDef(s_vx_reference, s_BASE, defs={
    s_vx_delay: 'VX_TYPE_DELAY',
    s_vx_lut: 'VX_TYPE_LUT',
    s_vx_distribution: 'VX_TYPE_DISTRIBUTION',
    s_vx_pyramid: 'VX_TYPE_PYRAMID',
    s_vx_threshold: 'VX_TYPE_THRESHOLD',
    s_vx_matrix: 'VX_TYPE_MATRIX',
    s_vx_convolution: 'VX_TYPE_CONVOUTION',
    s_vx_scalar: 'VX_TYPE_SCALAR',
    s_vx_array: 'VX_TYPE_ARRAY',
    s_vx_image: 'VX_TYPE_IMAGE',
    s_vx_remap: 'VX_TYPE_REMAP',
    s_vx_object_array: 'VX_TYPE_OBJECT_ARRAY',
    s_vx_tensor: 'VX_TYPE_TENSOR'})

# and the standard object reference types
# Probably this is not a lot of use for this
# application? Might be more useful to map them
# to the XML tags and remove that mapping from the
# xml module and where it appears randomly.
TypeDef(s_vx_delay, s_OBJECT, 
        defs={'VX_DELAY_TYPE': s_vx_type_e,
         'VX_DELAY_SLOTS': s_vx_size}, 
         attrs=dict(elemtype='VX_DELAY_TYPE',
        numelems='VX_DELAY_SLOTS'))
TypeDef(s_vx_lut, s_OBJECT, defs=
        {'VX_LUT_TYPE': s_vx_type_e,
         'VX_LUT_COUNT': s_vx_size,
         'VX_LUT_SIZE': s_vx_size,
         'VX_LUT_OFFSET': s_vx_uint32},
        attrs=dict(elemtype='VX_LUT_TYPE',  numelems='VX_LUT_COUNT'))
TypeDef(s_vx_distribution, s_OBJECT, defs=
        {'VX_DISTRIBUTION_DIMENSIONS': s_vx_size,
        'VX_DISTRIBUTION_OFFSET': s_vx_int32,
        'VX_DISTRIBUTION_RANGE': s_vx_uint32,
        'VX_DISTRIBUTION_BINS': s_vx_size,
        'VX_DISTRIBUTION_WINDOW': s_vx_uint32,
        'VX_DISTRIBUTION_SIZE': s_vx_size},
        attrs=dict(elemtype=s_vx_uint32,  numelems='VX_DISTRIBUTION_BINS'))
TypeDef(s_vx_pyramid, s_OBJECT, defs=
        {'VX_PYRAMID_LEVELS': s_vx_size,
        'VX_PYRAMID_SCALE': s_vx_float32,
        'VX_PYRAMID_WIDTH': s_vx_uint32,
        'VX_PYRAMID_HEIGHT': s_vx_uint32,
        'VX_PYRAMID_FORMAT': s_vx_df_image},
        attrs=dict(elemtype=s_vx_image,  numelems='VX_PYRAMID_LEVELS'))
TypeDef(s_vx_threshold, s_OBJECT, defs=
        {'VX_THRESHOLD_TYPE': 'vx_threshold_type_e',
        'VX_THRESHOLD_INPUT_FORMAT': s_vx_df_image_e,
        'VX_THRESHOLD_OUTPUT_FORMAT': s_vx_df_image_e})
TypeDef(s_vx_matrix, s_OBJECT, defs=
        {'VX_MATRIX_TYPE': s_vx_type_e,
        'VX_MATRIX_ROWS': s_vx_size,
        'VX_MATRIX_COLUMNS': s_vx_size,
        'VX_MATRIX_SIZE': s_vx_size,
        'VX_MATRIX_ORIGIN': 'vx_coordinates2d_t',
        'VX_MATRIX_PATTERN': 'vx_pattern_e'})
TypeDef(s_vx_convolution, s_OBJECT, defs=
        {'VX_CONVOLUTION_ROWS': s_vx_size,
        'VX_CONVOLUTION_COLUMNS': s_vx_size,
        'VX_CONVOLUTION_SCALE': s_vx_uint32,
        'VX_CONVOLUTION_SIZE': s_vx_size})
TypeDef(s_vx_scalar, s_OBJECT, defs={'VX_SCALAR_TYPE': s_vx_type_e})
TypeDef(s_vx_array, s_OBJECT, defs=
        {'VX_ARRAY_ITEMTYPE': s_vx_type_e,
        'VX_ARRAY_NUMITEMS': s_vx_size ,
        'VX_ARRAY_CAPACITY': s_vx_size,
        'VX_ARRAY_ITEMSIZE': s_vx_size},
        attrs=dict(elemtype='VX_ARRAY_ITEMTYPE',  numelems='VX_ARRAY_NUMITEMS'))
TypeDef(s_vx_image, s_OBJECT, defs=
        {'VX_IMAGE_WIDTH': s_vx_uint32,
        'VX_IMAGE_HEIGHT': s_vx_uint32,
        'VX_IMAGE_FORMAT': s_vx_df_image,
        'VX_IMAGE_PLANES': s_vx_size,
        'VX_IMAGE_SPACE': 'vx_color_space_e',
        'VX_IMAGE_RANGE': 'vx_channel_range_e',
        'VX_IMAGE_MEMORY_TYPE': 'vx_memory_type_e',
        'VX_IMAGE_IS_UNIFORM': s_vx_bool,
        'VX_IMAGE_UNIFORM_VALUE': 'vx_pixel_value_t'})
TypeDef(s_vx_remap, s_OBJECT, defs=
        {'VX_REMAP_SOURCE_WIDTH': s_vx_uint32,
        'VX_REMAP_SOURCE_HEIGHT': s_vx_uint32,
        'VX_REMAP_DESTINATION_WIDTH': s_vx_uint32,
        'VX_REMAP_DESTINATION_HEIGHT': s_vx_uint32
        })
TypeDef(s_vx_object_array, s_OBJECT, defs=
        {'VX_OBJECT_ARRAY_ITEMTYPE': s_vx_type_e,
        'VX_OBJECT_ARRAY_NUMITEMS':s_vx_size})
TypeDef(s_vx_tensor, s_OBJECT, defs=
        {'VX_TENSOR_NUMBER_OF_DIMS': s_vx_size,
        'VX_TENSOR_DIMS': 'vx_size *',
        'VX_TENSOR_DATA_TYPE': s_vx_type_e,
        'VX_TENSOR_FIXED_POINT_POSITION': s_vx_int8})
