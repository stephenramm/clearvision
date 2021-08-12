'''
This file holds the functions for parsing reading and writing XML,
converting them to graphs, and for rendering the graphs.
'''
import wx
import math
from lxml import etree
import pygraphviz as pgv
import cvxKernelDefs as kdefs
from cvxKernelDefs import KernelDef
import cvxDataDefs as ddefs
from cvxDataDefs import TypeDef
from cvxPreferences import updateBidEdge, updateContainerEdge, \
    updateGraphInputParameterObj, updateGraphOutputParameterObj, \
    updateNodeCustomObj, updateNormalEdge, updateObj

# Some strings: names of fields and tags
sroot = 'root'
sreference = 'reference'
sreferences = 'references'
snode = 'node'
slabel = 'label'
svirtual = 'virtual'
sname = 'name'
scount = 'count'
selemType = 'elemType'
sbins = 'bins'
sbin = 'bin'
sfrequency = 'frequency'
soffset = 'offset'
srange = 'range'
swidth = "width"
sheight = "height"
sformat = "format"
sscale = "scale"
slevels = "levels"
sinput_format = "input_format"
soutput_format = "output_format"
strue_value = "true_value"
sfalse_value = "false_value"
sthreshType = "threshType"
scolumns = "columns"
scolumn = "column"
srows = "rows"
srow = "row"
scapacity = "capacity"
ssrc_width = "src_width"
sdst_width = "dst_width"
ssrc_height = "src_height"
sdst_height = "dst_height"
sstart_x = "start_x"
sstart_y = "start_y"
send_x = "end_x"
send_y = "end_y"
sdata_type = "data_type"
sfixed_point_position = "fixed_point_position"
snumber_of_dims = "number_of_dims"
sdimension = "dimension"
ssize = "size"
sglobal ='global'
sconstant = 'constant'
sindex = 'index'
sparameter = 'parameter'
sgraph = 'graph'
skernel = 'kernel'
sdelay = 'delay'
slut = 'lut'
sdistribution = 'distribution'
spyramid = 'pyramid'
sthreshold = 'threshold'
smatrix = 'matrix'
spattern = 'pattern'
sorigin_x = 'origin_x'
sorigin_y = 'origin_y'
sconvolution = 'convolution'
sscalar = 'scalar'
sarray = 'array'
suint8 = 'uint8'
schar = 'char'
sint8 = 'int8'
suint16 = 'uint16'
sint16 = 'int16'
suint32 = 'uint32'
sint32 = 'int32'
sfloat32 = 'float32'
suint64 = 'uint64'
sint64 = 'int64'
senum = 'enum'
sdf_imgae = 'df_image'
skeypoint = 'keypoint'
sstrength = 'strength'
sorientation = 'orientation'
stracking_status = 'tracking status'
simage = 'image'
sremap = 'remap'
sobject_array = 'object_array'
stensor = 'tensor'
sroi = 'roi'
splane = 'plane'
schannel = 'channel'
sview = 'view'
svx_reference = 'vx_reference'
sreplicate_flag = 'replicate_flag'
strue = 'true'
sfalse = 'false'
sstruct = 'struct'
sis_replicated = 'is_replicated'
sVX_TYPE_INVALID = 'VX_TYPE_INVALID'
sVX_TYPE_UINT8 = "VX_TYPE_UINT8"
sVX_CHANNEL_Y = "VX_CHANNEL_Y"
sVX_CHANNEL_U = "VX_CHANNEL_U"
sVX_CHANNEL_V = "VX_CHANNEL_V"

# border modes
sbordermode = "bordermode"
sborderconst = "borderconst"
sUNDEFINED = "UNDEFINED"
sCONSTANT = "CONSTANT"
sREPLICATE = "REPLICATE"

borderModes = [sUNDEFINED, sCONSTANT, sREPLICATE]

# Map of data object tags and attributes with default values
dataObjectTags = {
    svx_reference:{},     # special tag for vx_reference parameters of select kernel
    sarray: {selemType: sVX_TYPE_INVALID, scapacity: "0"},
    sconvolution: {srows: "3", scolumns: "3", sscale: "16"},
    sdelay: {scount: "2"},
    sdistribution: {sbins: "16", soffset: "0", srange: "256"},
    simage: {swidth: "32", sheight: "32", sformat: "U008"},
    slut: {scount: "256", selemType: sVX_TYPE_UINT8},
    smatrix: {selemType: "VX_TYPE_FLOAT32", scolumns: "3", srows: "2", spattern: 'VX_PATTERN_OTHER', sorigin_x: "1", sorigin_y: "1"},
    sobject_array: {scount: "1"},
    splane: {schannel: "VX_CHANNEL_0"},
    spyramid: {swidth: "32", sheight: "32", sformat: "U008", sscale: "0.5", slevels: "4"},
    sremap: {ssrc_width:"32", ssrc_height:"32", sdst_width:"32", sdst_height:"32"},
    sroi: {sstart_x: "0", sstart_y: "0", send_x: "1", send_y: "1"},
    sscalar: {selemType: sVX_TYPE_INVALID},
    sthreshold: {sinput_format: "U008", soutput_format: "U008"},
    stensor: {snumber_of_dims: "3", sdata_type: sVX_TYPE_UINT8, sfixed_point_position: "0"},
    sview: {}
    }

# List of objects that can be in a delay
delayChoices = [sarray, sconvolution, sdistribution, simage, slut, smatrix, 
                sobject_array, spyramid, sremap, sscalar, sthreshold, stensor]

# List of objects that can be in an object array
objectArrayChoices = [sarray, sconvolution, sdistribution, simage, slut,
                smatrix, spyramid, sremap, sscalar, sthreshold, stensor]

# Map of tags to types
tagtypemap = {
    svx_reference:ddefs.s_vx_reference,
    sdelay: ddefs.s_vx_delay,
    slut: ddefs.s_vx_lut,
    sdistribution: ddefs.s_vx_distribution,
    spyramid: ddefs.s_vx_pyramid,
    sthreshold: ddefs.s_vx_threshold,
    smatrix: ddefs.s_vx_matrix,
    sconvolution: ddefs.s_vx_convolution,
    sscalar: ddefs.s_vx_scalar,
    sarray: ddefs.s_vx_array,
    simage: ddefs.s_vx_image,
    sremap: ddefs.s_vx_remap,
    sobject_array: ddefs.s_vx_object_array,
    stensor: ddefs.s_vx_tensor,
    sroi: ddefs.s_vx_image,
    splane: ddefs.s_vx_image,
    sview: ddefs.s_vx_tensor,
    sgraph: ddefs.s_vx_graph
    }
# list of information object tags
infoObjectTags = [
    'library',
    sstruct
]
sVIRT = "VIRT"
sRGB2 = "RGB2"
sRGBA = "RGBA"
sNV12 = "NV12"
sNV21 = "NV21"
sUYVY = "UYVY"
sYUYV = "YUYV"
sIYUV = "IYUV"
sYUV4 = "YUV4"
sU008 = "U008"
sU016 = "U016"
sS016 = "S016"
sU032 = "U032"
sS032 = "S032"

# Image formats used in the xml
imageFormatChoices = [sVIRT,
                    sRGB2,
                    sRGBA,
                    sNV12,
                    sNV21,
                    sUYVY,
                    sYUYV,
                    sIYUV,
                    sYUV4,
                    sU008,
                    sU016,
                    sS016,
                    sU032,
                    sS032]

# image formats supporting channels, and which ones
imageChannelFormats = {
    sYUV4: [sVX_CHANNEL_Y, sVX_CHANNEL_U, sVX_CHANNEL_V],
    sIYUV: [sVX_CHANNEL_Y, sVX_CHANNEL_U, sVX_CHANNEL_V],
    sNV12: [sVX_CHANNEL_Y],
    sNV21: [sVX_CHANNEL_Y]
}

# Map simple types to image formats used in XML
formatMap = {
    sVX_TYPE_UINT8: sU008,
    'VX_TYPE_UINT16': sU016,
    'VX_TYPE_UINT32': sU032,
    'VX_TYPE_INT16': sS016,
    'VX_TYPE_INT32': sS032
}

# TODO:
# Creation of data objects with proper attributes and default or calculated values

# TODO:
# Proper handling of the globals page (better name needed also), which should
# a summary of the graphs, graph parameters, objects connected to graph parameters
# and unconnected objects.

# TODO:
# Handling of replicated nodes, object arrays and pyramids

# TODO:
# handling of delays

# TODO:
# handling of ROI and tensor from view

# TODO:
# Enforcement of correct immutable graph semantics:
# No immutable parameters connected to graph parameters (silently remove upon reading)
# No global objects shared between graphs (silently duplicate upon reading)
# Allow and look at implications of virtual objects connected as graph parameters:
# a) Spec allows it
# b) Data cannot be access, so actually not very useful as such
# c) Provides a way to have 'unconnected' graph parameters since non-virtual objects
#   need connecting before use, but graph is still 'legal'

# The name of the 'globals' page:
globalsName = '.globals'

# Whether to show connected data or not
showVirtuals = False

# Utility to make a reference by joining several strings in a standard way
def Ref(*refs):
    return ",".join(refs)

# Class for graph parameter references
class GPRef(object):
    def __init__(self, rs):
        self.graph = rs[0]
        self.index = int(rs[1])

# Class for node parameter references
class NPRef(object):
    def __init__(self, rs):
        self.graph = rs[0]
        self.node = rs[1]
        self.index = int(rs[2])
    
# Utility to split a reference into graph, node and index references
def unRef(ref):
    rs = ref.split(",")
    if len(rs) == 2:
        return GPRef(rs)
    elif len(rs) == 3:
        return NPRef(rs)
    else:
        return rs

# Class for connection data
class Connection(object):
    def __init__(self, p):
        self.param=p
        self.ref=p.get(sreference)
        self.repl=p.get(sreplicate_flag)

# Class for replication information
class RepType(object):
    def __init__(self, kp, repl, ref, param, elem, num, ptag):
        self.kp = kp        # kernel parameter info
        self.repl = repl    # if the node is replicated
        self.ref = ref      # reference to the connected object
        self.param = param  # the xml parameter object
        self.elem = elem    # the xml conneected object
        self.num = num      # number of siblings
        self.ptag = ptag    # parent tag (object array or pyramid)

# Class for 
class Xref(object):
    """
    objects stored in a dictionary that locates references and holds necessary data
    General rules:
    1) A node in an Agraph is named by either its reference for a node representing an xml 
    entity corresponding to an OpenVX object, or by <graph ref>,<parameter index>
    2) An Xref index is a string either as (1) above or a node parameter index in the form <graphref>,<noderef>,<parameter index>
    for a node parameter reference, or "root" for the root tree.
    3) AGraph names are equal to their Xref entry, i.e. "root" or a reference.

    Members of an xref object are:
    elem - the xml element corresponding to the object, or None
    tagref - another referenced entry. For example in the case of a node parameter this is the reference of the object attached,
        for a graph parameter it is the reference of the node parameter, for a child data object it is the reference of the parent,
        for a virtual or a node it is the reference of the graph, for globals and for sroot it is sroot
    tag - the xml tag for the object
    index - where tagRef points at another data object, the index in object array, pyramid etc, Rect for ROI, plane for channel, view data for tensor,
        or if this isn't a child data object then this is None
    immutable - True for immuatble parameters
    writer - ref of the writer parameter, or None
    readers - set of references to reader parameters, or Node
    type - the type for the entry (eg type held by a scalar) (do we need this?)
    subtype - subtype (eg class of vx_enum)
    tooltip - data to show on the screen when mousing over
    name - the name given to the object
    graph - the set of agraphs in which the object may be found
    direction - for a node parameter index
    repl - replication flag
    isDirty - only valid for graphs; if set (True) it means a Redraw is necessary.
    """
    xref = {}
    # Whether the graphs need rebuilding.
    xmlDirty = True

    def __init__(self, elem, tagref, name, graph, direction=None, repl=False,
                isDirty=True, immutable=False, tag=None,
                kdef=None, subtype=None, datasize=0, isparent=False, ischild=False):
        self.elem = elem                # The xml element
        self.tagref = tagref            # The parent reference
        self.name = name                # The name given to the node in the dot graph
        self.graphs = {graph.name: graph}      # The graphs where you can find this node
        self.direction = direction      # The direction of a parameter
        self.repl = repl                # If the parameter is replicated
        self.graphdirty = isDirty       # If a graph redraw is required
        self._immutable = immutable     # if any of the readers make this immutable
        self.readers = set()            # set of readers of this object
        self.writer = None              # the writer of this object
        self.tag = tag                  # tag for this object
        self.kdef = kdef                # kernel definitions (if a node)
        self.subtype = subtype          # subtype of object if applicable
        self.datasize = datasize        # size of data in object or start index. For some types (e.g. remap) this becomes a dictionary
        self._child = ischild           # whether data object is a child
        self._parent = isparent         # whether data object is a parent
        self._virtual = None            # whether data object is virtual, initialised by calling isVirtual()
        self._filename = None           # File where data is stored (e.g. image, tensor, remap)

    def getFilename(self):
        """
        Return the filename for backing data storage (or None)
        """
        return self._filename

    def setFilename(self, filename):
        """
        Set the filename for backing data storage
        """
        self._load_filenameFile = filename

    def storeData(self):
        """
        Store the object's data in an appropriate format using the filename.
        If the filename is None, create one and assign it.
        The data is removed from the xml object.
        """
        if self._filename is None:
            wx.GetApp().frame.Error("Filename has not been set", True)
        if self.tag == simage:
            # Not uniform images, ROI, image from channel or object array of images from tensor
            # Image data is always stored.
            wx.GetApp().frame.Error("Storing image data is not supported yet", True)
            # Images are supported through standard image file formats, and XML
        elif self.tage == stensor:
            # Not views
            # Tensor data is alwasy stored
            wx.GetApp().frame.Error("Storing tensor data is not supported yet", True)
            # Tensors are supported through image file formats, NNEF, and XML
        elif self.tag == sremap:
            wx.GetApp().frame.Error("Storing remap data is not supported yet", True)
            # Remaps are supported through .csv and XML
            # Stored on request
        elif self.tag == slut:
            wx.GetApp().frame.Error("Storing LUT data is not supported yet", True)
            # LUT supported through XML and csv
            # Stored on request
        elif self.tag == sdistribution:
            wx.GetApp().frame.Error("Storing distribution data is not supported yet", True)
            # distribution supported through XML and csv
            # stored on request
        elif self.tag == smatrix:
            wx.GetApp().frame.Error("Storing remap data is not supported yet", True)
            # matrix supported through xml and csv
            # stored on request
        elif self.tag == sconvolution:
            wx.GetApp().frame.Error("Storing convolution data is not supported yet", True)
            # convolution supported through xml and csv
            # stored on request
        elif self.tag == sarray:
            wx.GetApp().frame.Error("Storing array data is not supported yet", True)
            # array supported through xml and csv
            # stored on request

        # The following are not supoprted:
        # vx_delay, vx_pyramid, vx_object_array - these are effectively supported at a higher level
        # vx_threshold, vx_scalar - data is trivial and does not need to be stored/ created externally


    def loadData(self):
        """
        Load data from the file given by filename, it it exists.
        Replace all the data in the xml object.
        If the file does not exist, then report an error.
        If the command is not appropriate for the tyupe of object (e.g. scalar) then do nothing at all
        """
        if self._filename is None:
            wx.GetApp().frame.Error("Filename has not been set", True)
        if self.tag == simage:
            # Not uniform images, ROI, image from channel or object array of images from tensor
            data = wx.Image(self._filename)
            wx.GetApp().frame.Error("Loading image data is not supported yet", True)
            # Images are supported through standard image file formats, and XML
        elif self.tage == stensor:
            # Not views
            wx.GetApp().frame.Error("Loading tensor data is not supported yet", True)
            # Tensors are supported through image file formats, NNEF, and XML
        elif self.tag == sremap:
            wx.GetApp().frame.Error("Loading remap data is not supported yet", True)
            # Remaps are supported through .csv and XML
        elif self.tag == slut:
            wx.GetApp().frame.Error("Loading LUT data is not supported yet", True)
            # LUT supported through XML and csv
        elif self.tag == sdistribution:
            wx.GetApp().frame.Error("Loading distribution data is not supported yet", True)
            # distribution supported through XML and csv
        elif self.tag == smatrix:
            wx.GetApp().frame.Error("Loading remap data is not supported yet", True)
            # matrix supported through xml and csv
        elif self.tag == sconvolution:
            wx.GetApp().frame.Error("Loading convolution data is not supported yet", True)
            # convolution supported through xml and csv
        elif self.tag == sarray:
            wx.GetApp().frame.Error("Loading array data is not supported yet", True)
            # array supported through xml and csv

        # The following are not supoprted:
        # vx_delay, vx_pyramid, vx_object_array - these are effectively supported at a higher level
        # vx_threshold, vx_scalar - data is trivial and does not need to be stored/ created externally


    def graph(self, exclude=set()):
        """
        return a graph that isn't in the set 'exclude'
        """
        for k, v in list(self.graphs.items()):
            if k not in exclude:
                return v
        return None

    def isData(self):
        """
        Return True if this represents a data object
        """
        return self.tag in dataObjectTags

    def isGraph(self):
        """
        Return True if this represents a graph object or the root container
        """
        return self.tag == sgraph

    def isVirtual(self):
        """
        Return True if this object is a data object and the child of
        a graph or of another virtual object
        """
        if self._virtual is None:
            if self.tagref == sroot:
                self._virtual = False
            else:
                p = Xref.get(self.tagref)
                self._virtual = False if p is None else p.isGraph() or p.isVirtual()

        return self._virtual

    def isChild(self):
        return self._child

    def isParent(self):
        return self._parent
    
    def isImmutable(self):
        return self._immutable

    @staticmethod
    def isDirty(graph=None):
        """
        Return True if the xml (default) needs rebuilding or a graph needs redrawing
        """
        return Xref.xmlDirty if graph is None else Xref.xref[graph.name].graphdirty

    @staticmethod
    def setDirty(graph=None, dirty=True):
        """
        Set the dirty flag for the xml or the graph
        """
        if graph is None:
            Xref.xmlDirty = dirty
        elif graph is sroot:
            Xref.xref[sroot].graphdirty = dirty
        else:
            Xref.xref[graph.name].graphdirty = dirty

    @staticmethod
    def clearDirty(graph = None):
        Xref.setDirty(graph, False)

    @staticmethod
    def update(ref, elem=None, tagref=None, name=None, graph=None, direction=None,
               repl=False, isDirty=None, reader=None, writer=None, immutable=None,
               tag=None, kdef=None, subtype=None, datasize=None,
               ischild=None, isparent=None):
        """
        update or add a reference to xref.
        """        
        if ref in Xref.xref:
            if elem is not None:
                Xref.xref[ref].elem = elem
            if tagref is not None:
                Xref.xref[ref].tagref = tagref
            if name is not None:
                Xref.xref[ref].name = name
            if graph is not None:
                Xref.xref[ref].graphs[graph.name] = graph
            if reader is not None:
                Xref.xref[ref].readers.add(reader)
            if writer is not None:
                Xref.xref[ref].writer = writer
            if direction is not None:
                Xref.xref[ref].direction = direction
            Xref.xref[ref].repl = repl
            if isDirty is not None:
                Xref.xref[ref].graphdirty = isDirty
            if immutable is not None:
                Xref.xref[ref]._immutable = immutable
            if tag is not None:
                Xref.xref[ref].tag = tag
            if kdef is not None:
                Xref.xref[ref].kdef = kdef
            if subtype is not None:
                Xref.xref[ref].subtype = subtype
            if datasize is not None:
                Xref.xref[ref].datasize = datasize
            if ischild is not None:
                Xref.xref[ref]._child = ischild
            if isparent is not None:
                Xref.xref[ref]._parent = isparent
        else:
            Xref.xref[ref] = Xref(elem, tagref, name, graph, direction=direction, repl=repl,
                                  immutable=immutable is True, tag=tag,
                                  kdef=kdef, subtype=subtype, 
                                  datasize=0 if datasize is None else datasize)

    @staticmethod
    def remove(ref):
        del Xref.xref[ref]

    @staticmethod
    def get(ref):
        """
        Return the entry for the given ref.
        """
        return Xref.xref.get(ref)

    @staticmethod
    def clear():
        Xref.xref.clear()

    @staticmethod
    def getroot():
        return Xref.xref[sroot]

    @staticmethod
    def setroot(elem, name, graph):
        Xref.clear()
        Xref.update(sroot, elem, sroot, name, graph, tag=sgraph)

    @staticmethod
    def connections(ref):
        """
        return the set of readers and writers
        """
        xobj = Xref.xref[ref]
        return  xobj.readers | (set() if xobj.writer is None else {xobj.writer})

    @staticmethod
    def items():
        return list(Xref.xref.items())

    @staticmethod
    def keys():
        return list(xref.keys())

    @staticmethod
    def contains(ref):
        return ref in Xref.xref


# Name management. We keep a dictionary of names and elements.
# Duplicate names are not allowed!

elementNames = {}

def getData(child, tag):
    """
    return data from child, which should be of type ptype.
    Return an list of values or a dictionary.
    Notice that no structure type currently contain arrays; if this
    changes then we have to revisit this method.
    If the data is of the wrong type, we return None
    The function is used for both scalars and arrays. We hope that
    there is only one child for scalars (as there should be)...
    """
    if etree.QName(child).localname != tag:
        print(("child is %s, tag is %s"%(child.tag, tag)))
        return None
    if len(child) > 0:
        # This is a struct type
        # Assume it contains no arrays or structures
        # We may have to look further to examine the type of each field?
        value = {}
        for field in child:
            value[etree.QName(field).localname] = field.text
    else:
        # single value, could be one or several
        s = child.text
        if s is None:
            value = None
        elif tag == 'char':
            value = [s]
        else:
            value = s.split()
    #print("getData about to return %s"%value)
    return value

def updateScalarValues(xobj, attr, value, stringValue, index=0):
    """
    Update the data in the child of xobj.elem.
    attr is one of:
    'data'
    'data[i]' if data is a user struct
    'data.fieldname' if data is a struct or union
    value is the value returned by the property editor (could be str, int, float, bool)
    stringValue is the value displayed by the property editor
    Handles arrays as well as scalars...
    """
    elem = xobj.elem
    num = len(elem)
    etype = elem.get(selemType)
    vxtype = TypeDef.typeFromEnum(etype)
    vxdef = TypeDef.get(vxtype)
    #print(xobj,attr,value,num,etype,vxtype)
    # create appropriate new value from stringValue or value
    if etype == 'VX_TYPE_ENUM':
        newvalue = str(value)
    elif etype == 'VX_TYPE_BOOL':
        newvalue = strue if value else sfalse
    elif etype == 'VX_TYPE_DF_IMAGE':
        newvalue = TypeDef.formatToString(int(value))
    else:
        newvalue = stringValue
    # check that the right number of data exists and is of the correct type
    if vxdef.isStruct():
        reqsize = xobj.datasize # number of children
        elsize = 1              # entries for each child
    elif vxdef.isArray():
        reqsize = xobj.datasize
        elsize = vxdef.size
    else:
        reqsize = 1             # number of children
        sindex = index
        index = 0
        elsize = xobj.datasize  # entries for each child
    if '[' in attr:
        sattr = attr[5:].split(']')
        sindex = int(sattr[0])
        if '.' in sattr:
            fname = sattr[1].split('.')[1]
        else:
            fname = ""
    else:
        sindex = index
        fname = attr[5:]
    # Correct the number of data
    for i in range(num, reqsize):
        # insert missing data
        child = etree.Element(etree.QName(elem,'new'))
        elem.append(child)
        insertChildData(child, vxtype, elsize, sindex, etype, fname, newvalue)
    # remove excess data
    elem[reqsize:num] = []
    # Now update according to type
    insertChildData(elem[index], vxtype, elsize, sindex, etype, fname, newvalue)

def insertChildData(elem, ptype, elsize, sindex, etype, attr, value):
    """
    Correct elem's data using supplied information
    ptype is the type (like vx_float32)
    elsize is the number of data expected in the data string
    sindex is the index of data in the element's text (e.g. where an array is expressed as a sequence of numbers)
    etype is the element's required data type as a VX_TYPE_XXX or user struct identifier
    value is is the correctly expressed new data for xml
    attr is either empty, or a fieldname.
    """
    #print("insertChildData ptype=%s, elsize=%s, sindex=%s, etype=%s, attr=%s, value=%s"%(ptype, elsize, sindex, etype, attr, value))
    sdata = TypeDef.defaultData(ptype)
    qtag = etree.QName(elem, TypeDef.tagFromEnum(etype))
    data = getData(elem, qtag.localname)
    if data is None:
        # data is wrong type. Correct the tag and get default data
        elem.tag = qtag.text
        if isinstance(sdata, (list, dict)):
            # user struct or other array type (is there one?)
            data = sdata
        else:
            # make a list of the appropriate size
            data = [sdata] * elsize
    # Now delete everything and rebuild, inserting new data along the way
    elem.clear()
    if TypeDef.get(ptype).isArray():
        # array data as bytes (are there any other array types used?)
        data[sindex] = value
        elem.text = " ".join([str(i) for i in data])
    elif isinstance(data, dict):
        # structure type
        print(("attr='%s', data is %s and value is %s"%(attr, data, value)))
        for k, v in list(data.items()):
            child = etree.Element(etree.QName(elem, k))
            elem.append(child)
            if k == attr:
                child.text = value
            else:
                print(("setting %s to %s"%(k,v)))
                child.text = v
    else:
        # data is a list - but of the correct size?
        lenvalues = len(data)
        if lenvalues > elsize:
            data[elsize:lenvalues] = [] # truncate to size
        elif lenvalues < elsize:
            data[lenvalues:elsize] = [sdata] * (elsize - lenvalues)
        data[sindex] = value
        elem.text = " ".join(data)

def updateArrayValues(xobj, attr, value, stringValue):
    """
    Update the data in the child of xobj.elem.
    attr is one of:
    'data[i]'
    'data[i][j]' if data is a user struct
    'data[i].fieldname' if data is a struct or union
    value is the value returned by the property editor (could be str, int, float, bool)
    stringValue is the value displayed by the property editor
    """
    # extract the name and index from the attribute
    lname = attr.split('[', 1)
    rname = lname[1].split(']', 1)
    name = lname[0] + rname[1]
    # now update that specific value
    updateScalarValues(xobj, name, value, stringValue, int(rname[0]))

def updateRowColumn(elem, rowCol, tag, value):
    """
    Update (or insert) child data for row and column of given matrix or convolution,
    remove any incorrect tags and put things in the correct order.
    rowCol is a row, column identifier in the form "[%d][%d]", and value is string data.
    """
    row, column = rowCol[1:-1].split("][")
    rows = elem.get(srows, str(int(row) + 1))
    columns = elem.get(scolumns, str(int(column) + 1))
    rcMap = {}
    # get existing data and remove existing children
    for child in list(elem):
        if etree.QName(child).localname == tag:
            rcMap["[%s][%s]"%(child.get(srow), child.get(scolumn))] = child.text
        elem.remove(child)
    # Update the correct element
    rcMap[rowCol] = value
    # Add new children in correct order
    for r in range(int(rows)):
        for c in range(int(columns)):
            child = etree.Element(etree.QName(elem, tag))
            child.set(srow, str(r))
            child.set(scolumn, str(c))
            child.text = rcMap.get("[%d][%d]"%(r, c), "0")
            elem.append(child)

def updateSubElement(elem, attridx, tag, value):
    """
    Update (or insert) child data for a bin or index value, removing
    any incorrect tags we encounter. We don't bother to try and order
    the children or even look at all the tags
    as there could potentially be a be a large number.
    """
    attr, index = attridx.split(' ')
    for child in list(elem):
        if etree.QName(child).localname == tag:
            if child.get(attr) == index:
                break
        else:
            elem.remove(child)
    else:
    # here without finding the child to update, so add a new one
        child = etree.Element(etree.QName(elem, tag))
        child.set(attr, index)
        elem.append(child)
    child.text = value
    
def makeNewName(tag, elem):
    '''
    Create a new name from the given tag, give the name to the element
    and put it in the dictionary along with the element.
    If the name already exists in the dictionary (for a different element)
    then a number is appended to make it unique.
    This is called by getNameRefTag and changeObjectName below.
    '''
    tag = tag.strip()
    newName = tag if len(tag) else 'object'
    oldName = elem.get(sname, '')
    trialName = newName
    seq = 0
    while trialName in elementNames and elementNames[trialName] != elem:
        trialName = newName + '_' + str(seq)
        seq += 1
    if oldName in elementNames:
        del elementNames[oldName]
    elem.set(sname, trialName)
    elementNames[trialName] = elem
    return trialName

def changeObjectName(name, elem, ref):
    """
    Change the object name, updating the Xref and objects on all AGraphs
    No need to re-build after this; just redraw
    Return True is a redraw is actually required (i.e. name did change)
    name - new name
    elem - xml element
    ref - the element reference
    """
    xobj = Xref.get(ref)
    oldName = xobj.name
    newName = makeNewName(name, elem)
    if newName == oldName:
        return False
    xobj.name = newName
    for g in list(xobj.graphs.values()):
        if g.has_node(ref):
            n = g.get_node(ref)
            label = n.attr[slabel].splitlines()
            label[0] = newName
            n.attr[slabel] = "\n".join(label)
            Xref.setDirty(g)
        else:
            wx.GetApp().frame.Error("Node '%s' could not be found in graph '%s'!"%(oldName, Xref.get(g.name).name))
    return True

def getNameRefTag(elem):
    """
    Check that the object name exists, if not then create it.
    Return a tuple of (name, reference, tag)
    """
    tag = etree.QName(elem).localname
    name = makeNewName(tag if sname not in elem.attrib else elem.attrib[sname], elem)
    ref = elem.get(sreference, name)
    return (name, ref, tag)

def fixupReferences(root):
    '''
    Count references and renumber them all, then put the count in the root
    'references' attribute.
    Note that renumbering the etree will completely invalidate xref and hence
    the graphs will need rebuilding.
    fixupReferences is called by buildGraphs() in this module and should also be
    called when saving the file (see cvxMain.MainFrame.SaveInFile())
    '''
    oldToNew = {}
    count = 0
    for elem in root.iter():                # iterate over everything
        if sreference in elem.attrib:       # Look at every 'reference' attribute
            ref = elem.attrib[sreference]
            if ref not in oldToNew:         # count references we haven't seen before
                oldToNew[ref] = str(count)  # and map them to a new value
                count += 1
    # Now we have our count, and re-numbering map.
    # First, put the count in the root attribute 'references'
    root.attrib[sreferences] = str(count)

    # Thee replace all the references in the tree:
    for elem in root.iter():
        if sreference in elem.attrib:
            elem.attrib[sreference] = oldToNew[elem.attrib[sreference]]
        elif snode in elem.attrib:          # Graph parameters use attribute 'node'
            elem.attrib[snode] = oldToNew[elem.attrib[snode]]
    # Done - mark xml as dirty and return the number of references
    Xref.setDirty()
    return count

def getNewRef():
    '''
    Get a new reference value based upon the count stored in root,
    and update that count. Assumes that references have been fixed-up
    at some point and the reference count is greater than the value
    of any existing references.
    '''
    root = Xref.getroot().elem
    ref = root.attrib[sreferences]
    root.attrib[sreferences] = str(int(ref) + 1)
    return ref

def updateAttributes(elem, dict, update=True):
    """
    Update the properties of the given elem to
    be those in dict. If update is False, don't
    change existing properties, only add new ones.
    Does not remove any properties.
    The properties need not be strings, so long as str()
    works on them.
    """
    for k, v, in list(dict.items()):
        if update or k not in elem.attrib:
            elem.set(k, str(v))
    return elem

def insertDefaultData(elem, kernelInfo, index, localGraph, repl=False):
    '''
    Insert a new default data object into the global root and graph that matches
    the kernel parameter (kps indexed by index) and return a new reference
    to it.
    This function will need a lot of expansion to deal with things like getting the
    correct values as determined by the constraints described in kernelInfo, and
    putting attributes in the xml tree corresponding to all the attributes required
    by the OpenVX data objects
    Note that the new object will be virtual (only in the localGraph) unless the
    parameter is immutable. The new object is otherwise always visible.
    '''
    xroot = Xref.getroot()
    root = xroot.elem
    rootGraph = xroot.graph()
    ref = getNewRef()
    kps = kernelInfo.params
    ptype = kps[index].ptype
    isConstant = kps[index].pstate == kdefs.kpImmutable
    ptdef = TypeDef.get(ptype)
    if ptype is None:
        ptdef = TypeDef.get('vx_enum')
        wx.GetApp().frame.Error("Missing type: %s"%ptype)
    if ptdef.objtype == ddefs.s_OBJECT:
        # standard object type
        tag = ptype[3:]
    else:
        if ptype == svx_reference:
            # special case where any object type is OK:
            # It will have to be determined by what else is connected
            # to the kernel.
            # for now,do nothing, but set tag equal to ptype
            tag = ptype
        else:
            tag = sscalar
    newElem = etree.Element(etree.QName(root, tag))
    newElem.set(sreference, ref)
    updateAttributes(newElem, dataObjectTags[tag])                             # add default properties
    newElem.set(sname, makeNewName(kps[index].pname, newElem))   # base the name on the kernel parameter name
    if repl:    # See if we need to make a parent object as well
        # Make an object array of two elements
        ws.GetApp().frame.Error("TODO - Help! Cannot currently create default replicated parameters", True)
    if isConstant:
        root.append(newElem)
    else:
        elem.append(newElem)
    if tag == sscalar and ptype != 'vx_scalar':
        # Special case for immutable scalars ****
        enumname = TypeDef.enumFromType(ptype, 'VX_TYPE_ENUM')
        newElem.attrib['elemType'] = enumname
    #     newValue = etree.Element(etree.QName(newElem, 'new'))
    #     # TODO: calculate default value from constraints
    #     newElem.append(newValue)

    # Load more stuff to do here for all the different types! TODO
    if tag == spyramid:
        changePyramidAttributes(newElem, localGraph, up=False)
    elif tag == stensor:
        for i in range(int(newElem.get(snumber_of_dims))):
            dim = etree.Element(etree.QName(newElem, sdimension))
            updateAttributes(dim, dict(index=i, size=2)) # Just an arbitray legal size for the dimension
            newElem.append(dim)
    
    # Finally put the new data object in the local graph, and update the immutability
    processDatum(newElem, localGraph)
    Xref.update(ref, immutable=isConstant)
    return ref

def getKernelInfo(obj):
    '''
    Return kernel information for a node
    '''
    for child in obj.iterchildren(etree.QName(obj, skernel).text):
        return KernelDef.get(child.text)
    return None

def processDatum(elem, graph, tagref=None):
    """
    See processData...
    """
    name, ref, tag = getNameRefTag(elem)
    objectsFound = set()
    if tag in list(dataObjectTags.keys()) + infoObjectTags:
        objectsFound = {ref}
        if tagref is None:
            xobj = Xref.get(ref)
            tagref = graph.name if xobj is None or xobj.tagref != sroot else sroot
        Xref.update(ref, elem, tagref, name, graph, tag=tag)
        if tag == sstruct:
            TypeDef.addUserStruct(elem.text, elem.get(ssize))
        tlabel = tag
        graph.add_node(ref, label = name + '\n' + tlabel)
        parent = graph.get_node(ref)
        updateObj(parent, Xref)
        parentDict = {
            sobject_array: 'Index ',
            sdelay: 'Slot ',
            spyramid: 'Level ',
            simage: 'ROI ',
            sroi: 'ROI ',
            splane: 'Plane ',
            stensor: 'View ',
            sview: 'View '
            }
        if tag in parentDict:
            count = 0
            for child in processData(elem, graph, ref):
                graph.add_edge(parent, child, headlabel=parentDict[tag] + str(count))
                updateContainerEdge(graph.get_edge(parent, child))
                count += 1
                Xref.update(child, ischild=True)
            if count > 0:
                Xref.update(ref, isparent=True)
    return objectsFound
    
def processData(tree, graph, tagref=None):
    """
    Insert objects recursively into the graph,
    return a list of graph objects (tagrefs)
    """
    objectsFound = set()
    for elem in tree.iterchildren():
        objectsFound |= processDatum(elem, graph, tagref)
    return objectsFound

def processNode(elem, obj, graph):
    """
    Process a new node object, putting it into the graph with default parameters
    if they are absent.
    Add border mode attribute as "DEFAULT" if not present.
    """
    if obj.get(sbordermode) is None:
        obj.set(sbordermode, sUNDEFINED)
    # add border const child if absent
    borderconst = None
    for child in obj.iterchildren(etree.QName(obj, sborderconst).text):
        borderconst = child
    if borderconst is None:
        borderconst = etree.Element(etree.QName(obj, sborderconst))
        borderconst.text = "#00000000"
        obj.append(borderconst)
    name, ref, tag = getNameRefTag(obj)
    # Get the replicated flag if present
    repl = obj.get(sis_replicated) == strue
    # Get the kernel name
    kernel = 'unknown'
    for child in obj.iterchildren(etree.QName(obj, skernel).text):
        kernel = child.text
    Xref.update(ref, obj, graph.name, name, graph, repl=repl, tag=tag)
    graph.add_node(ref, label=name + '\n' + kernel.rsplit('.', 1)[1])
    updateObj(graph.get_node(ref), Xref)
    kernelInfo = KernelDef.get(kernel)
    if kernelInfo is None:
        # skip further processing
        return wx.GetApp().frame.Error("Found unknown kernel %s, skipping processing"%kernel, True)
    Xref.update(ref, kdef=kernelInfo)
    # Now process the parameters as edges.
    # When we're not showing virtuals, this will need a little extra work later
    # And we'll have to duplicate globals, and show graph parameters differently,
    # and identify constants...
    # .. And if any parameters aren't connected, insert data objects of the correct type..
    # And of course we have to handle the replicate_flag

    kps = kernelInfo.params
    indicesFound = {}
    for edge in obj.iterchildren(etree.QName(obj, sparameter).text):
        index = int(edge.attrib[sindex])
        repl_flag = edge.get(sreplicate_flag) == strue
        if sreference not in edge.attrib or not Xref.contains(edge.attrib[sreference]):
            # Missing or invalid reference for this parameter
            pref = insertDefaultData(elem, kernelInfo, index, graph, repl_flag)
            edge.attrib[sreference] = pref
        else:
            pref = edge.attrib[sreference]
        indicesFound[index] = (pref, edge, repl_flag)
    for index in range(len(kps)):           # Search for missing required kernel parameters
        if index not in indicesFound and kps[index].pstate != kdefs.kpOptional:
            pref = insertDefaultData(elem, kernelInfo, index, graph)
            # Now fix up the xml by adding a parameter
            edge = etree.Element(etree.QName(obj, sparameter), index=str(index), reference=pref, replicate_flag=sfalse)
            obj.append(edge)
            indicesFound[index] = (pref, edge, False)
    for index in indicesFound:
        pref, edge, repl_flag = indicesFound[index]
        # Check to see if the object is in the current graph; if not then assume we need to insert
        xr = Xref.get(pref)
        pgraph = xr.getroot().graph()
        thisobj = pgraph.get_node(pref) if pgraph.has_node(pref) else None
        if not graph.has_node(pref):
            # add node if not present
            xr.graphs[graph.name] = graph
            processDatum(xr.elem, graph, tagref=Xref.get(pref).tagref)
        # Update immutable attribute according to immutability of the parameter
        Xref.update(pref, immutable=kps[index].pstate == kdefs.kpImmutable)
        kpname = kps[index].pname
        kpdir = kps[index].pdir
        # Add the parameter to the xref, but use kernel parameter name as name and add direction and repl_flag as extra elements
        npref = Ref(graph.name, ref, str(index))
        Xref.update(npref, edge, pref, kpname, graph, kpdir, repl_flag)
        # Now add edges to the local graph and update readers and writer
        if kpdir == kdefs.kpInput:
            Xref.update(pref, reader=npref)
            graph.add_edge(pref, ref, headlabel=kpname)
            updateNormalEdge(graph.get_edge(pref, ref), repl_flag)
        else: # output or bidirectional
            Xref.update(pref, writer=npref)
            graph.add_edge(ref, pref, taillabel=kpname)
            if kpdir == kdefs.kpBidirectional:
                updateBidEdge(graph.get_edge(ref, pref), repl_flag)
            else:
                updateNormalEdge(graph.get_edge(ref, pref), repl_flag)
        # process global graph if the data object is present there
        if thisobj is not None:
            # Update global according to immutability of the parameter
            updateObj(thisobj, Xref)
            gref = graph.name
            # Add edges to the global graph
            if kpdir == kdefs.kpInput:
                pgraph.add_edge(pref, gref, headlabel=name + ':' + kpname)
                updateNormalEdge(pgraph.get_edge(pref, gref), repl_flag)
            else: # output or bidirectional
                pgraph.add_edge(gref, pref, taillabel=name + ':' + kpname)
                if kpdir == kdefs.kpBidirectional:
                    updateBidEdge(pgraph.get_edge(gref, pref), repl_flag)
                else:
                    updateNormalEdge(pgraph.get_edge(gref, pref), repl_flag)

def processGraphParameter(obj, graph):
    # Graph parameters - these must be attached to non-virtual objects
    # Therefore the node and parameter attributes must reference objects
    # On the global page. They are duplicated on the graph tab however.
    # First, find graph parameter index, and the node and parameter to which it refers
    ix = obj.attrib[sindex]
    nd = obj.attrib[snode]
    nix = obj.attrib[sparameter]
    graphref = graph.name
    pTagref = Ref(graphref, ix)
    # Now, locate the node and the data object connected to that node
    nparam = Ref(graphref, nd, nix)
    sink = nd
    nodeObj = Xref.get(sink)
    dataObj = Xref.get(nparam)
    source = dataObj.tagref
    # Get the global root graph so we can insert parameters on that page
    rootGraph = Xref.getroot().graph()
    # (Note that one data object may be used for more than one graph parameter)
    # We've already added the data object connected to the node, so we introduce
    # a new graph parameter node between that data object and the node itself.
    # First, define the graph parameter node. Inputs and outputs are different.
    # Get the edge between the data object and the node
    pname = 'Graph Parameter ' + ix
    graph.add_node(pTagref, label=pname + '\n' + nodeObj.name + ':' + dataObj.name)
    Xref.update(pTagref, tagref=nparam, elem=obj, direction=dataObj.direction, graph=graph, name=pname, tag=sparameter)
    #Xref.get(pTagref)
    repl = dataObj.repl
    if dataObj.direction == kdefs.kpInput:
        updateGraphInputParameterObj(graph.get_node(pTagref))
        edge=graph.get_edge(source, sink)
        # Next, put an edge between the graph parameter and the node, with a headlabel & taillabel equal to that
        # of the original edge between the data object and the node
        graph.add_edge(pTagref, sink, headlabel=edge.attr['headlabel'])
        updateNormalEdge(graph.get_edge(pTagref, sink), repl)
        # Add an edge between the data object and the graph parameter
        graph.add_edge(source, pTagref)
        updateNormalEdge(graph.get_edge(source, pTagref), repl)
        # Update edge on root graph:
        rootGraph.get_edge(source, graphref).attr.update(headlabel='Parameter ' + ix)
    else:
        updateGraphOutputParameterObj(graph.get_node(pTagref))
        sink, source = source, sink
        edge=graph.get_edge(source, sink)
        # Next, put an edge between the graph parameter and the node, with a headlabel & taillabel equal to that
        # of the original edge between the data object and the node
        graph.add_edge(source, pTagref, taillabel=edge.attr['taillabel'])
        if dataObj.direction == kdefs.kpOutput:
            updateNormalEdge(graph.get_edge(source, pTagref), repl)
        else:
            updateBidEdge(graph.get_edge(source, pTagref), repl)
        # Add an edge between the data object and the graph parameter
        graph.add_edge(pTagref, sink)
        updateNormalEdge(graph.get_edge(pTagref, sink), repl)
        # And for root graph:
        rootGraph.get_edge(graphref, sink).attr.update(taillabel='Parameter ' + ix)
    # Remove the edge between the data object and the node
    graph.remove_edge(source, sink)

def processVirtuals(graph):
    # TODO: Get rid of this function, it is a kludge! we should not draw this stuff in the first place...
    # If we aren't showing virtual data objects, then we must remove them
    # Iterate over objects, and for virtual data objects iterate over edges,
    # insert new edges between the source and the sinks then remove the data objects.
    # For non-virtual objects without a writer, show them as constants unless
    # they are graph parameters
    # Show all graph parameters in the style for graph parameters
    # This function also removes all immutable parameter objects from the graphs
    nodes = graph.nodes()
    for n in nodes:
        xobj = Xref.get(n)
        if xobj.tag in dataObjectTags:
            if xobj.isVirtual() and not showVirtuals and not (xobj.isParent() or xobj.isChild() or xobj.isImmutable()):
                ins = graph.in_edges(n)
                outs = graph.out_edges(n)
                preds = graph.in_neighbors(n)
                succs = graph.out_neighbors(n)
                if len(ins) and len(outs):
                    # Only remove the object if it has inputs and outputs
                    # And only process the first input as it should only have one
                    for i in range(len(outs)):
                        # get arrowhead, font etc from previous edges
                        graph.add_edge(preds[0], succs[i], taillabel=ins[0].attr['taillabel'], headlabel=outs[i].attr['headlabel'],
                            arrowhead=ins[0].attr['arrowhead'], font=ins[0].attr['font'], fontcolor=ins[0].attr['fontcolor'],
                            fontsize=ins[0].attr['fontsize'])
                    # We keep the object in Xref, but remove it from the graph
                    graph.remove_node(n)
            elif xobj.isImmutable():
                graph.remove_node(n)
            else:
                # non-virtual or visible mutable data object
                updateObj(n, Xref)

def processGraph(root, elemGraph):
    elem, graph = elemGraph
    # First, process everything that is not a node or a graph parameter
    processData(elem, graph, graph.name)
    # Now, process nodes
    for obj in elem.iter(etree.QName(elem, snode).text):
        processNode(elem, obj, graph)
    # Process graph parameters
    for obj in elem.iterchildren(etree.QName(elem, sparameter).text):
        processGraphParameter(obj, graph)
    # hide virtual data
    processVirtuals(graph)

def newDotGraph(name=globalsName, ref=sroot, elem=None):
    """
    Create a new dot AGraph with the given name.
    The direction is given by options.globalRankDir if name is globalsName,
    otherwise by options.graphRankDir.
    The graph is directed.
    Note we have to have 'strict' and 'concentrate' both false in order
    to show two or more edges between nodes. or dor will merge them.
    """
    graph = pgv.AGraph(name=ref, directed=True, strict=False, concentrate=False)
    if name is not globalsName:
        rg = Xref.getroot().graph()
        Xref.update(ref, elem, sroot, name, rg, tag=sgraph)
        rg.add_node(ref, label=name)
        updateObj(rg.get_node(ref), Xref)
    return graph

def buildGraphs(tree):
    """
    Build graphs from the XML tree given. All nodes are named by their reference and labeled with their
    name and either the kernel name or the type for data objects.
    Clears the xml dirty flag
    Returns a tuple of xref and dictionary of graphs where each entry is a tuple of xref, element and graph
    """
    elementNames.clear()        # reset the name dictionary
    #print("Buildgraphs ", elementNames)
    fixupReferences(tree)       # re-number all the references to make them consecutive
    rg = newDotGraph()
    rg.edge_attr.update(dir='both', arrowtail='none')
    graphDict = {globalsName: (tree, rg)}
    Xref.setroot(tree, globalsName, rg)
    # First, process everything that is not a graph
    processData(tree, rg, sroot)
    # Then process graphs
    for elem in tree.iterchildren(etree.QName(tree, sgraph).text):
        name, ref, tag = getNameRefTag(elem)
        if name not in graphDict:
            g = newDotGraph(name, ref, elem)
            g.edge_attr.update(dir='both', arrowtail='none')
            graphDict[name] = (elem, g)
        processGraph(tree, graphDict[name])
    # TODO:
    # Massive Kludge which needs fixing. Because we have drawn the graphs 'on the fly' rather than
    # after fully assimilating all the data, we have drawn stuff which should not be there.
    # Here we remove all the immutable data from all graphs...
    for xref, xobj in list(Xref.xref.items()):
        if xobj.isImmutable():
            for g in list(xobj.graphs.values()):
                if g.has_node(xref):
                    g.remove_node(xref)
    Xref.clearDirty()
    return graphDict

# Functions that insert new items in the graph
def insertGraph():
    """
    Create a new graph
    """
    root = Xref.getroot().elem
    ref = getNewRef()
    elem = etree.Element(etree.QName(root, sgraph), reference=ref)
    name = makeNewName(sgraph, elem)
    root.append(elem)
    Xref.setDirty()
    return name, (elem, newDotGraph(name, ref, elem))

def insertNode(tree, graph, kernelName):
    """
    Insert a new node in the graph with the given kernel.
    """
    if tree == Xref.getroot().elem:
        wx.GetApp().frame.Error("Cannot insert node in %s; use a graph tab"%globalsName)
    else:
        # create node
        newNode = etree.Element(etree.QName(tree, snode), reference=getNewRef(), is_replicated=sfalse)
        # create kernel
        newKernel = etree.Element(etree.QName(newNode, skernel))
        newKernel.text = kernelName
        # put the kernel in the node
        newNode.append(newKernel)
        # put the node in the graph
        tree.append(newNode)
        # process the node
        processNode(tree, newNode, graph)
        # make sure parameters are shown correctly
        processVirtuals(graph)
        # Set the dirty flag on the graph & the root graph
        Xref.setDirty(graph)
        Xref.setDirty(sroot)

def insertGraphParameter(tree, graph, obj, nodeobj):
    """
    Insert a new graph parameter and make obj non-virtual.
    obj and nodeobj are dnodes, obj being a data object and nodeobj being an openvx node.
    Returns True on success
    Sets isDirty if it was not possible to fix-up the graph and Xref and the graphs need rebuilding
    (For now weset it - TODO: fix this!)
    """
    # count the existing graph parameters to get the next index:
    newIndex = 0
    for p in tree.iterchildren(etree.QName(tree, sparameter).text):
        newIndex += 1
    replant(Xref.get(obj).elem, Xref.getroot().elem)  # Make object non-virtual
    tree.append(etree.Element(etree.QName(tree, sparameter), node=nodeobj,
                parameter=paramWithRef(nodeobj, obj), index=str(newIndex)))
    Xref.setDirty()
    return True

def paramWithRef(noderef, objref):
    """
    Return the index property for the parameter of the node with the given
    noderef that references the given objref
    """
    nodeElem = Xref.get(noderef).elem
    for p in nodeElem.iterchildren(etree.QName(nodeElem, sparameter).text):
        if p.attrib[sreference] == objref:
            return p.attrib[sindex]
    return ""

def insertObjectArray(tree, graph, tag=simage, num=3):
    """
    Insert an object array of num items of type tag
    """
    return makeObjectArray(insertObject(tree, graph, tag), graph, num)

def insertDelay(tree, graph, tag=simage, num=3):
    """
    Insert a delay of num items of type tag
    """
    return makeDelay(insertObject(tree, graph, tag), graph, num)

def insertPyramid(tree, graph, levels=3, df='U008', scale=0.5, width=32, height=32):
    """
    Insert a pyramid of num images
    """
    return makePyramid(insertImage(tree, graph, df, width, height), graph, levels, scale)

def insertImage(tree, graph, df=sU008, width=32, height=32):
    """
    Insert an image
    """
    image = etree.Element(etree.QName(tree, simage))
    ref = getNewRef()
    updateAttributes(image, dict(reference=ref, width=width,
                                 height=height, format=df))
    Xref.update(ref, image, tree.get(sreference), makeNewName(simage, image), graph, tag=simage)
    tree.append(image)
    Xref.setDirty()
    return image
    
def changeTensorSize(elem, graph):
    """
    Change the size of a tensor by inserting or removing dimensions
    """
    length = int(elem.get(snumber_of_dims))
    i = 0
    # remove excess children
    for dim in elem.iterchildren(etree.QName(elem, sdimension).text):
        if i == length:
            elem.remove(dim)
        else:
            i += 1
    # insert missing children
    while i < length:
        dim = etree.Element(etree.QName(elem, sdimension))
        updateAttributes(dim, dict(index=i, size=1))
        elem.append(dim)
        i += 1
    # Now do we have to check views and object arrays?
    # TODO

def insertTensor(tree, graph, dims=[2, 2, 2], dtype='VX_TYPE_UINT8', fpp="0"):
    """
    Insert a tensor
    """
    tensor = etree.Element(etree.QName(tree, stensor))
    ref = getNewRef()
    updateAttributes(tensor, dict(reference=ref, number_of_dims=len(dims),
                                  data_type=dtype, fixed_point_position=fpp))
    Xref.update(ref, tensor, tree.get(sreference), makeNewName(stensor, tensor), graph, tag=stensor)        
    tree.append(tensor)
    for i in range(len(dims)):
        tensor.append(updateAttributes(etree.Element(etree.QName(tensor, sdimension)), 
                                       dict(index=i, size=dims[i])))
    Xref.setDirty()
    return tensor
    
def insertObject(tree, graph, tag, parentref=None, num=3):
    """
    Insert a default object of the given type, which could
    also be an object array, delay, or pyramid
    """
    if tag == spyramid:
        return insertPyramid(tree, graph, num)
    elif tag == sdelay:
        return insertDelay(tree, graph, simage, num=num)
    elif tag == sobject_array:
        return insertObjectArray(tree, graph, simage, num=num)
    elif tag == stensor:
        return insertTensor(tree, graph)
    else:
        elem = etree.Element(etree.QName(tree, tag))
        ref = getNewRef()
        elem.set(sreference, ref)
        updateAttributes(elem, dataObjectTags[tag])
        Xref.update(ref, elem,
                    tree.get(sreference) if parentref is None else parentref,
                    makeNewName(tag, elem), graph, tag=tag)        
        tree.append(elem)
        Xref.setDirty()
    return elem

# Functions that remove items from the graph
def removeGraphParameter(tree, graph, node):
    """
    Remove a graph parameter and renumber graph parameters if necessary.
    Returns True 
    Sets isDirty if the graphs need rebuilding.
    TODO: fixup things so the graph doesn't need rebuilding!
    """
    # Name of node is comma-separated graph reference and index
    pIndex = int(node.split(',')[1]) # get index
    paramtag = etree.QName(tree, sparameter).text
    for p in tree.iterchildren(paramtag):
        if int(p.attrib[sindex]) == pIndex:
            # We have found it, remove it.
            tree.remove(p)
            break
    pIndex = 0
    for p in tree.iterchildren(paramtag):
        # These are elements in the same graph with tag 'parameter'
        # Parameter index may not match our count; We must renumber
        p.attrib[sindex] = str(pIndex)
        pIndex += 1
    Xref.setDirty()
    return True

# Functions that merge objects in the graph

def checkCompatibleParents(sourceElem, sinkElem):
    """
    Return True if the parent objects are compatible for a merge
    """
    sourceTag = etree.QName(sourceElem).localname
    if  sourceTag in [sdelay, sobject_array]:
        # Check that the children are OK to be merged
        if etree.QName(sourceElem[0]) != etree.QName(sinkElem[0]):
            return wx.GetApp().frame.Error("Cannot merge %s with differing child types"%sourceTag)
        elif len(sourceElem) != len(sinkElem):
            return wx.GetApp().frame.Error("Cannot merge %s of different length"%sourceTag)
        else:
            for k, v in list(sourceElem[0].items()):
                if k not in {sreference, sname} and sinkElem[0].get(k) != v:
                    return wx.GetApp().frame.Error("Cannot merge %s when elements have differing attributes"%sourceTag)
        # We repeat to cope with delays of object arrays:
        return checkCompatibleParents(sourceElem[0], sinkElem[0])
    return True

def mergeToVirtual(tree, graph, source, sink, writer, nomatch):
    """
    tree is the graph element in the xml being amended
    graph is the dot graph being amended
    source and sink are the dot graph data objects being merged.
    writer is a dot graph node identified as the wrinter node for source, or is None
    nomatch is a dictionary of attributes that do not match but must be applied
    (the caller believes this is OK)
    only source may have a writer, as identified by the geometry of the dot graph; and
    also any writer is not in the successors of the sink. The caller guarantees this.
    
    returns false if:
    * further analysis of data relationships means that the objects cannot be merged
    * an error message has been logged
    
    returns true if data objects have been merged, but they are only made virtual if
    data relationships allow this.
    
    We have draconian family law.
    Fisrtly, do either the source or the sink have parents or children?
    Because we can't merge if:
    They both have parents
    One is a descendent of the other
    They both have at least one child - Note we will have to revise this!

    In the case of a merge where one object has a parent, it is the orphan
    that is removed

    Where one object is a parent, the merged object inherits its children

    The merged object inherits all attributes of both source and sink, except
    that it takes the name and the reference of the surviving object

    Finally, the merged object only becomes virtual if:
    - It has a writer, and
    - It has no parent.
    
    NOTE: currently we don't fix up anything but the xml, so graphs need rebuilding.
    TODO: fix up graphs and xref so stuff doesn't need rebuilding (possible performance enhancement)
    """
    sourceElem = Xref.get(source).elem
    sinkElem = Xref.get(sink).elem
        
    if hasParent(sourceElem) and hasParent(sinkElem):
        return wx.GetApp().frame.Error("Cannot merge two child data objects")

    if descendant(sinkElem, sourceElem) or descendant(sourceElem, sinkElem):
        return wx.GetApp().frame.Error("Cannot merge related data objects")

    # TODO: check that nomatch does not contain any show-stoppers!
    sourceTag = etree.QName(sourceElem).localname
    sinkTag = etree.QName(sinkElem).localname
    if isParent(sinkElem) and isParent(sourceElem):
        if len(nomatch) > 0 or sourceTag != sinkTag:
            return wx.GetApp().frame.Error("Cannot merge two parent objects with differing attributes")
        if not checkCompatibleParents(sourceElem, sinkElem):
            return False

    # At this stage we should have determined that a merge may proceed, but there are perhaps still some mis-matched
    # attributes, signified by nomatch being non-empty. We check with the user in this case:
    if len(nomatch) > 0 :
        print(nomatch)
    if len(nomatch) > 0 and wx.MessageBox("The data objects you have selected to merge have different attributes.\n"
                                          "Do you still wish to proceed ?", "Merging data objects", style=wx.YES_NO|wx.ICON_QUESTION) == wx.NO:
        return wx.GetApp().frame.Error("Data object merge was aborted")

    # If an object has a parent, then it is the one to survive.
    # Simplify subsequent processing by making sure it is the source.
    if hasParent(sinkElem):
        source, sourceElem, sink, sinkElem = sink, sinkElem, source, sourceElem
    
    # Make sure the survivor (source) gets the kids
    # Note that this only applies to roi, channel and view as we
    # don't merge object arrays, delays or pyramids with this mechanism
    for child in sinkElem.iterchildren():
        if etree.QName(child).localname in [sroi, splane, sview]:
            sourceElem.append(child)

    # Now add attributes to sourceElem that are only in sinkElem:
    #for attr, val in sinkElem.attrib.items():
    #    if attr not in sourceElem.attrib:
    #        sourceElem.attrib[attr] = val

    # Now we have to find all references to sink and replace them with references to source
    # Notice that we do this for only one level, so references to children of sink will
    # remain and when the tree is rebuilt virtual objects will be generated as necessary
    for elem in sourceElem.getroottree().getiterator():
        if elem.get(sreference) == sink:
            elem.set(sreference, source)

    # We can now remove the sink from the xml tree
    xmlRemove(sinkElem)

    # Now check whether this sourceElem is now connected to a graph parameter,
    # if it is, then we'll have to make it global. We do this by looking at
    # the connections in the dot graph to see if either source or sink was connected
    # to a graph parameter node:
    isGParam = False
    for n in graph.neighbors(source) + graph.neighbors(sink):
        if Xref.get(n).tag == sparameter:
            isGParam = True
            break
    if isGParam:
        replant(sourceElem, tree.getparent())

    # All done.
    Xref.setDirty()
    return True

def convertReferenceTo(refObj, exemplar):
    """
    Give the vx_reference object refObj the properties
    of the exemplar. Almost everything except the reference changes.
    """
    refRef = refObj
    refElem = Xref.get(refRef).elem
    egElem = Xref.get(exemplar).elem
    for k, v in list(egElem.attrib.items()):
        if k not in {sreference}:
            refElem.attrib[k] = v
    refElem.tag = egElem.tag
    for k, v in list(exemplar.attr.items()):
        refObj.attr[k] = v
    Xref.update(refRef, tag=etree.QName(refElem).localname)

def xmlRemove(elem):
    """
    Remove the given element from it's tree
    Show an error and return False if it could not be done.
    """
    p = elem.getparent()
    if p is not None:
        p.remove(elem)
        return True
    return wx.GetApp().frame.Error("Element %s has no parent"%elem, True)

def descendant(elem, parent):
    """
    return True if elem is some descendent of a parent data object
    """
    return elem is parent or elem in parent.iterdescendants()

def hasParent(elem):
    """
    return True if elem has a parent data object
    """
    for parent in elem.iterancestors():
        if etree.QName(parent).localname in dataObjectTags:
            return True     
    return False

def isParent(elem):
    """
    return True if elem has a child data object
    """
    for child in elem.iterchildren():
        if etree.QName(child).localname in dataObjectTags:
            return True
    return False

def makeCompatibleData(elem):
    """
    Create a new data object that is compatible with the given one, 
    with a new name and reference.
    TODO: Handle things like ROIs, where we don't make an
    exact copy, but a new object...
    """
    p = elem.getparent()
    #if p is not None and etree.QName(p).localname in dataObjectTags:
        # The object we are copying is a child of another
    tag = etree.QName(elem).localname
    if tag == sroi:
        # Special case for image ROI
        # We make an image with the same dimensions as the ROI and same format as the parent
        # TODO we maybe don't take into account an ROI made from an image made from a plane?
        width = elem.attrib[send_x] - elem.attrib[sstart_x]
        height = elem.attrib[send_y] - elem.attrib[sstart_y]
        format = "U008"
        p = elem.getparent()
        while p is not None and sformat not in p.attrib:
            p = p.getparent()
        if p is None:
            # Should not occur. default the format and show an error
            wx.GetApp().frame.Error("Found ROI without a parent with a format!!", True)
        else:
            format = p.attrib[sformat]
        newElem = etree.Element(etree.QName(elem, simage), width=width, height=height, format=format, name=simage)
    elif tag == splane:
        # Special case for image plane
        # TODO: not yet sure exactly how planes work
        # TODO: what if this plane was extracted from an ROI?
        # We make an image with the same dimensions as the parent but format U008
        format = "U008"
        width = 0
        height = 0
        while p is not None and swidth not in p.attrib:
            p = p.getparent()
        if p is None:
            # Should not occur. default the sizes and show an error
            wx.GetApp().frame.Error("Found image from plane without a parent with a width!!", True)
        else:
            width = p.attrib[swidth]
            height = p.attrib[sheight]
        newElem = etree.Element(etree.QName(elem, simage), width=width, height=height, format=format, name=simage)
    elif tag == sview:
        # special case for tensor view
        # No idea at all how this works?
        pass
    else:
        # 'normal' object 
        newElem = etree.fromstring(etree.tostring(elem)) # dumb but effective for now
    newElem.attrib[sreference] = getNewRef()
    makeNewName(elem.attrib[sname], newElem)
    return newElem

def replant(elem, tree):
    """
    Remove element from its parent tree and put it in the given tree
    Need to find an ancestor that is not a data object; the object
    before this one following backwards is the actual object moved
    If the element ultimately has no parent, this is not an issue.
    """
    o = elem
    p = elem.getparent()
    while p is not None and etree.QName(p).localname in dataObjectTags:
        o = p
        p = p.getparent()
    if p is not None:
        p.remove(o)
    tree.append(o)

def getOptionals(dnode):
    """
    Return optional unconnected parameters for dnode
    """
    elem = Xref.get(dnode).elem
    kernelInfo = getKernelInfo(elem)
    kps = kernelInfo.params
    connected = getConnected(elem)
    optionals = {}
    for kpi in range(len(kps)):
        if kps[kpi].pstate == kdefs.kpOptional:
            if kpi not in connected:
                optionals[kpi] = kps[kpi]
    return optionals

def getPossibleReplicates(dnode):
    """
    Return a dictionary of replicatable parameters for the node.
    They must be mutable, connected, and either not a child of a data object
    or the first child of an object array or pyramid
    For each valid index, returns an object of type RepType with members: 
    kp - kernel parameter data
    repl - replicate flag
    ref - object reference
    elem - xml object
    num - number of items in parent
    ptag - tag of parent
    """
    xobj = Xref.get(dnode)
    elem = xobj.elem
    kernelInfo = getKernelInfo(elem)
    kps = kernelInfo.params
    connected = getConnected(elem)
    possibles = {}
    for kpi in range(len(kps)):
        if kps[kpi].pstate != kdefs.kpImmutable:
            if kpi in connected:
                param = connected[kpi].param    # The parameter xml object
                oref = connected[kpi].ref       # The reference of the connected object
                repl = connected[kpi].repl      # The replicate flag
                xobj = Xref.get(oref)           # data for the connected object
                delem = xobj.elem               # xml element for the connected object
                dparent = delem.getparent()     # could be root, a graph, or a data object
                ptag = etree.QName(dparent).localname
                if ptag in {sobject_array, spyramid}:
                    # delem must be the first child
                    if list(dparent)[0] == delem:
                        possibles[kpi] = RepType(kp=kps[kpi], repl=repl, ref=oref, param=param, elem=delem, num=len(list(dparent)), ptag=ptag)
                elif ptag not in dataObjectTags:
                    possibles[kpi] = RepType(kp=kps[kpi], repl=repl, ref=oref, param=param, elem=delem, num=0, ptag=ptag)
    return possibles

def makeObjectArray(elem, graph, num, tag=sobject_array):
    """
    Create an object array of num objects based upon elem, which becomes the
    first child of the new object array
    This function also can create a delay when passed a different tag
    """
    p = elem.getparent()
    objarray = etree.Element(etree.QName(p, tag))
    ref = getNewRef()
    objarray.set(sreference, ref)
    Xref.update(ref, objarray, p.get(sreference), makeNewName(tag, objarray), graph, tag=tag)
    objarray.set(scount, str(num))
    p.append(objarray)
    p.remove(elem)
    objarray.append(elem)
    Xref.update(elem.get(sreference), tagref=ref)
    return changeDelayOrArrayCount(objarray, graph)

def changeDelayOrArrayCount(elem, graph):
    """
    Ensures that the number of elements in an object array or delay matches
    the count given in the tag 'count' of the parent elem
    Sets the dirty flag if any were added or removed
    If the first child of an object array is connected to a replicated parameter
    of a node, then the number of items is propageted to all other parameters of
    that node.
    """
    count = int(elem.get(scount))
    oldcount = len(elem)
    index = 0
    for child in elem:
        if index == count:
            Xref.remove(child.get(sreference))
            elem.remove(child)
            # TODO: remove all other references to this object
            # Will have to patch up connections... Currently
            # we are just relying upon a re-build to create new virtual
            # objects to staisfy missing references, this is probably OK?
        else:
            copyAttributes(child, graph, elem[0])
            index += 1
    while index < count:
        insertCopy(elem, graph, elem[0])
        index += 1
    if count != oldcount:
        # Now we must check all nodes connected to this element
        Xref.setDirty()
        changeReplicationCount(elem[0], count)
    return elem

def changeReplicationCount(elem, count):
    """
    Check and update any replication counts for nodes that
    are connected to this elem.
    count is the required count
    """
    count = str(int(count)) # make sure...
    ref = elem.get(sreference)
    paramtag = etree.QName(elem, sparameter).text
    for npref in Xref.connections(ref):
        ndxobj = Xref.get(unRef(npref).node)
        node = ndxobj.elem   # get node element
        graph = ndxobj.graph()
        for np in node.iterchildren(paramtag):
            # Check all the parameters of this node
            if np.get(sreplicate_flag) == strue:
                # In this case elem must be the first child - we don't check this.
                parent = Xref.get(np.get(sreference)).elem.getparent()
                ptag = etree.QName(parent).localname
                if ptag == sobject_array:
                    if parent.get(scount) != count:
                        parent.set(scount, count)
                        changeDelayOrArrayCount(parent, graph)
                elif ptag == spyramid:
                    if parent.get(slevels) != count:
                        parent.set(slevels, count)
                        changePyramidAttributes(parent, graph)
                else:
                    wx.GetApp().frame.Error("Found illegal replicated parameter for node '%s' index %s"%(
                                            node.get(sname), np.get(sindex)), True)

def insertCopy(tree, graph , elem):
    """
    Insert a copy of the element, with a new name and reference
    """
    Xref.setDirty()
    tag = etree.QName(elem).localname
    newElem = etree.Element(etree.QName(elem, tag))
    ref = getNewRef()
    newElem.set(sreference, ref)
    Xref.update(ref, newElem, tree.get(sreference), makeNewName(elem.get(sname), newElem), graph, tag=tag)
    updateAttributes(newElem, elem.attrib, False)   # Add only missing attributes
    tree.append(newElem)
    if tag in {sobject_array, sdelay}:
        insertCopy(newElem, graph, elem[0])
        changeDelayOrArrayCount(newElem, graph)
    elif tag == spyramid:
        insertCopy(newElem, graph, elem[0])
        changePyramidAttributes(newElem, graph)
    return newElem

def copyAttributes(dest, graph, source):
    """
    copy attributes from source to dest, and propgate to children
    if source is a container
    """
    tag = etree.QName(source).localname
    for k, v in list(source.items()):
        if k not in {sreference, sname}:
            dest.set(k, v)
    if tag in {sobject_array, sdelay}:
        copyAttributes(dest[0], graph, source[0])
        changeDelayOrArrayCount(dest, graph)
    elif tag == spyramid:
        changePyramidAttributes(dest, graph, up=False)

def changeDelayOrArrayChildAttributes(elem, graph, up=True):
    """
    Where a child of an object array or delay has had attributes changed,
    propgate to all siblings that have the same tag.
    Because the grandparent could be a delay, call again for the parent
    """
    parent = elem.getparent()
    if etree.QName(parent).localname in {sobject_array, sdelay}:
        tag = etree.QName(elem).text
        ltag = etree.QName(elem).localname
        for s in parent.iterchildren(tag):
            if s is not elem:
                copyAttributes(s, graph, elem)
        if up:
            changeDelayOrArrayChildAttributes(parent, graph)
    return elem

def makeDelay(elem, graph, num):
    """
    Create a delay of num objects based upon elem, which becomes the
    first child of the new delay
    This is actually identical to making an object array, so we
    just use that code with a different tag
    """
    return makeObjectArray(elem, graph, num, sdelay)

def makePyramid(elem, graph, levels=4, scale=0.5):
    """
    Create a pyramid of num images based upon elem, which becomes the
    first child of the new pyramid
    """
    p = elem.getparent()
    minDim = round(levels / scale)
    width = max(int(elem.get(swidth, str(minDim))), minDim)
    height = max(int(elem.get(sheight, str(minDim))), minDim)
    df = elem.get(sformat, sU008)
    updateAttributes(elem, dict(width=width, height=height, format=df))
    name = elem.get(sname)
    pyramid = etree.Element(etree.QName(p, spyramid))
    pref = getNewRef()
    updateAttributes(pyramid, dict(reference=pref, levels=levels, scale=scale,
                                   width=width, height=height, format=df))
    Xref.update(pref, elem, p.get(sreference), makeNewName(spyramid, pyramid), graph, tag=spyramid)
    p.append(pyramid)
    p.remove(elem)
    Xref.update(elem.get(sreference), tagref=pref)
    pyramid.append(elem)
    for i in range(levels - 1):
        width = int(math.ceil(width * scale))
        height = int(math.ceil(height * scale))
        newElem = etree.Element(etree.QName(pyramid, simage))
        ref = getNewRef()
        updateAttributes(newElem, dict(reference=ref, width=width,
                                       height=height, format=df))
        Xref.update(ref, newElem, pref, makeNewName(name, newElem), graph, tag=simage)
        pyramid.append(newElem)
    Xref.setDirty()
    return pyramid
    
def changePyramidAttributes(pyramid, graph, up=True):
    """
    This function makes sure that all elements of a pyramid
    have the correct width, height and format to conform with
    the parent, and also is able to change the number of levels
    in the pyramid. Sets the dirty flag if the number of images
    was changed, returns the pyramid
    If the first child of a pyramid is connected to a replicated parameter
    of a node, then the number of items is propageted to all other parameters of
    that node.
    """
    levels = int(pyramid.get(slevels))
    oldlevels = len(pyramid)
    #print("Change pyramid attributes, oldlevels=%d, newlevels=%d"%(oldlevels, levels))
    pref = pyramid.get(sreference)
    width = int(pyramid.get(swidth))
    height = int(pyramid.get(sheight))
    df = pyramid.get(sformat)
    scale = float(pyramid.get(sscale))
    count = 0
    name = pyramid[0].get(sname) if oldlevels > 0 else simage
    for image in pyramid:
        if count == levels:
            pyramid.remove(image)
            Xref.remove(image.get(sreference))
        else:
            updateAttributes(image, dict(width=width, height=height, format=df))
            width = int(math.ceil(width * scale))
            height = int(math.ceil(height * scale))
            count += 1
    while count < levels:
        newElem = etree.Element(etree.QName(pyramid, simage))
        ref = getNewRef()
        updateAttributes(newElem, dict(reference=ref, width=width,
                                       height=height, format=df))
        Xref.update(ref, newElem, pref, makeNewName(name, newElem), graph, tag=simage)
        pyramid.append(newElem)
        width = int(math.ceil(width * scale))
        height = int(math.ceil(height * scale))
        count += 1
    if oldlevels != levels:
        Xref.setDirty()
        changeReplicationCount(pyramid[0], levels)
    # in case parent is an object array or delay:
    if up and etree.QName(pyramid.getparent()).localname in {sobject_array, sdelay}:
        changeDelayOrArrayChildAttributes(pyramid, graph)
    return pyramid

def changePyramidChildAttributes(child, graph, up=True):
    """
    Checks the child attributes against the pyramid parent.
    If they do not match, then parent attributes are created
    that should generate child attributes appropriately and
    all the pyramid attributes are altered.
    Since the number of levels isn't going to change, this
    won't set the dirty flag.
    """
    p = child.getparent()
    cf = child.get(sformat)
    cw = int(child.get(swidth))
    ch = int(child.get(sheight))
    ps = float(p.get(sscale))
    pw = int(p.get(swidth))
    ph = int(p.get(sheight))
    pf = p.get(sformat)
    scale = ps ** list(p).index(child)
    change = False
    if cw != math.ceil(pw * scale):
        pw = int(round(cw / scale))
        change = True
    if ch != math.ceil(ph * scale):
        ph = int(round(ch / scale))
        change = True
    if change or pf != cf:
        updateAttributes(p, dict(format=cf, wifth=pw, height=ph))
        changePyramidAttributes(p, graph, up)
    return child

def addOptional(tree, graph, dnode, kps, index):
    """
    Add optional parameter into the node dnode of the graph
    tree is the xml graph element
    kp is the parameters information vector
    index is the index
    The added data object will be virtual, and because it
    is an optional, cannot be immutable.
    Returns True
    Only the xml is manipulated, and we set isDirty
    TODO: patch up the graph, Xref, and don't set isDirty
    """
    node = Xref.get(dnode).elem
    ref = getNewRef()
    ptype = kps[index].ptype
    ptdef = TypeDef.get(ptype)
    if ptdef is None:
        ptdef = TypeDef.get('vx_enum')
        return wx.GetApp().frame.Error("Missing type: %s"%ptype, True)
    if ptdef.objtype == ddefs.s_OBJECT:
        # standard object type
        tag = ptype[3:]
    else:
        if ptype == svx_reference:
            # special case where any object type is OK:
            # It will have to be determined by what else is connected
            # to the kernel.
            # for now,do nothing, but set tag equal to ptype
            tag = ptype
        else:
            return wx.GetApp().frame.Error("Found unrecognised type '%s' for optional node parameter %d"%(ptype, index), True)
    newElem = etree.Element(etree.QName(tree, tag))
    newElem.attrib[sreference] = ref
    newElem.attrib[sname] = makeNewName(kps[index].pname, newElem)   # base the name on the kernel parameter name
    for attribute in dataObjectTags[tag]:
        newElem.attrib[attribute] = dataObjectTags[tag][attribute]
    tree.append(newElem)
    # Now insert a new parameter in the node object
    newParam = etree.Element(etree.QName(node, sparameter))
    newParam.attrib[sindex] = str(index)
    newParam.attrib[sreference] = ref
    node.append(newParam)
    # all done
    Xref.setDirty()
    return True

def getConnected(nelem):
    """
    Return a dictionary of parameters connected to nelem.
    Each entry is an object of type Connection with members:
    param - xml parameter object
    ref - reference of connected object
    repl - replicate flag)
    """
    connected = {}
    for p in nelem.iterchildren(etree.QName(nelem, sparameter).text):
        connected[int(p.get(sindex))] = Connection(p)
    return connected

def connectDataNode(obj, dnode, kpInfo, index):
    """
    Connect the given graph data object to the given dnode parameter
    index is the number of the parameter
    kpInfo is the kernel parameter information for that index
    Returns True
    Set isDirty if a rebuild is necessary
    TODO: fix up the xref and graph
    """
    node = Xref.get(dnode).elem
    newParam = etree.Element(etree.QName(node, sparameter), index=str(index), reference=str(obj), replicate_flag=sfalse)
    node.append(newParam)
    Xref.setDirty()
    return True

def getVxType(obj):
    """
    Return the vx type of an object.
    """
    tag = Xref.get(obj).tag
    return tagtypemap[tag] if tag in tagtypemap else None
