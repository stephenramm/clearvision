'''
This module holds the preferences.
Eventually these will be stored to a file and be editable with a dialog.
For now, we have a set of constants...
'''
#The default graph:
defaultGraph = '<openvx xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' \
'xmlns="https://www.khronos.org/registry/vx/schema" ' \
'xsi:schemaLocation="https://www.khronos.org/registry/vx/schema ' \
'openvx-1-0.xsd" references="1"><graph name="graph" reference="0"/></openvx>'

# The layout and drawing engine
dotEngine = 'dot'

# Maximum number of tree copies in the undo list:
maxUndo = 5

# Things for graphs:
rankDir='TB'
# Define the shapes and styles of:
# a data object
dataShape = 'box'
dataStyle = 'solid'
dataColor = 'black'
dataFont = 'Helvetica'
dataFontSize = 12
dataFontColor = 'black'

# Specific data type shape overrides:
shapedict = {
    'delay': 'component',
    'object_array': 'box3d',
    'pyramid': 'house',
    'tensor': 'tab',
    'view' : 'tab',
    'roi': dataShape,
    'image': dataShape,
    'scalar': dataShape,
    'threshold': dataShape,
    'lut': dataShape,
    'distribution': dataShape,
    'matrix': dataShape,
    'convolution': dataShape,
    'array': dataShape,
    'remap': dataShape,
    'struct': 'note',
    'library': 'folder'
}
# A virtual data object
virtualStyle = 'dotted'
# a contained data object
containedColor = 'red'
# Style overrides for a graph
graphShape = 'parallelogram'
graphStyle = 'bold, rounded'
graphColor = 'darkorchid'

# an input graph Parameter
graphInputParameterShape = 'box'
graphInputParameterStyle = 'bold, rounded'
graphInputParameterColor = 'blue'
graphInputParameterFont = 'Helvetica'
graphInputParameterFontSize = 12
graphInputParameterFontColor = 'black'
# an output graph Parameter
graphOutputParameterShape = 'box'
graphOutputParameterStyle = 'bold, rounded'
graphOutputParameterColor = 'green2'
graphOutputParameterFont = 'Helvetica'
graphOutputParameterFontSize = 12
graphOutputParameterFontColor = 'black'
# a standard node
nodeShape = 'oval'
nodeStyle = 'solid'
nodeColor = 'maroon'
nodeFont = 'Helvetica'
nodeFontSize = 12
nodeFontColor = 'maroon'
# a standard node, replicated
nodeRepShape = 'oval'
nodeRepStyle = 'diagonals, solid'
nodeRepColor = 'maroon'
nodeRepFont = 'Helvetica'
nodeRepFontSize = 12
nodeRepFontColor = 'maroon'
# a custom node
nodeCustomShape = 'oval'
nodeCustomStyle = 'bold, dotted'
nodeCustomColor = 'maroon'
nodeCustomFont = 'Helvetica'
nodeCustomFontSize = 12
nodeCustomFontColor = 'maroon'
# a custom node, replicated
nodeRepCustomShape = 'oval'
nodeRepCustomStyle = 'diagonals, bold, dotted'
nodeRepCustomColor = 'maroon'
nodeRepCustomFont = 'Helvetica'
nodeRepCustomFontSize = 12
nodeRepCustomFontColor = 'maroon'
# A graph (on the globals page)
# A unidirectional edge arrowhead
normalArrow = 'empty'
normalTail = 'none'
normalStyle = 'solid'
normalColor = 'black'
# A bi-directional edge arrowhead
bidArrow = 'odiamond'
bidTail = 'odiamond'
bidStyle = 'solid'
bidColor = 'black'
# A replicated parameter edge style
replStyle = 'bold'
replColor = 'navy'
# for marking taillabels and headlabels:
paramFont = 'Helvetica'
paramFontColor = 'blue'
paramFontSize = 9
# for connecting contained data objects:
containerArrow = 'halfopen'
containerTail = 'halfopen'
containerStyle = 'dotted'
containerColor = 'slategrey'

def updateNormalEdge(edge, repl=False):
    '''
    Update an edge for normal attributes
    '''
    edge.attr.update(arrowhead=normalArrow, arrowtail=normalTail, style=replStyle if repl else normalStyle,
                    color=replColor if repl else normalColor,
                    font=paramFont, fontcolor=paramFontColor, fontsize=paramFontSize)

def updateBidEdge(edge, repl=False):
    '''
    Update an edge for bidirectional attributes
    '''
    edge.attr.update(arrowhead=bidArrow, arrowtail=bidTail, style=replStyle if repl else bidStyle,
                    color=replColor if repl else bidColor,
                    font=paramFont, fontcolor=paramFontColor, fontsize=paramFontSize)

def updateContainerEdge(edge):
    '''
    Update an edge for container attributes
    '''
    edge.attr.update(arrowhead=containerArrow, arrowtail=containerTail, style=containerStyle, color=containerColor,
                    font=paramFont, fontcolor=paramFontColor, fontsize=paramFontSize)

def updateObj(obj, Xref):
    '''
    update a graph node for data object styles
    '''
    obj.attr.update(shape=dataShape, style=dataStyle, color=dataColor,
            font=dataFont, fontsize=dataFontSize, fontcolor=dataFontColor)
    xobj = Xref.get(obj)
    if xobj.isChild():
        obj.attr.update(color=containedColor)
    if xobj.isVirtual():
        obj.attr.update(style=virtualStyle)
    tag = xobj.tag
    if tag in shapedict:
        obj.attr.update(shape=shapedict[tag])
    elif tag == 'graph':
        obj.attr.update(shape=graphShape, style=graphStyle, color=graphColor)
    elif tag == 'node':
        updateNodeObj(obj, xobj.repl)

def updateGraphInputParameterObj(obj):
    '''
    update a graph node for graphInputParameter object styles
    '''
    obj.attr.update(shape=graphInputParameterShape, style=graphInputParameterStyle, color=graphInputParameterColor,
            font=graphInputParameterFont, fontsize=graphInputParameterFontSize, fontcolor=graphInputParameterFontColor)

def updateGraphOutputParameterObj(obj):
    '''
    update a graph node for graphOutputParameter object styles
    '''
    obj.attr.update(shape=graphOutputParameterShape, style=graphOutputParameterStyle, color=graphOutputParameterColor,
            font=graphOutputParameterFont, fontsize=graphOutputParameterFontSize, fontcolor=graphOutputParameterFontColor)

def updateNodeObj(obj, repl=False):
    '''
    update a graph node for node object styles
    '''
    if repl:
        updateNodeRepObj(obj)
    else:
        obj.attr.update(shape=nodeShape, style=nodeStyle, color=nodeColor,
                font=nodeFont, fontsize=nodeFontSize, fontcolor=nodeFontColor)

def updateNodeRepObj(obj):
    '''
    update a graph node for nodeRep object styles
    '''
    obj.attr.update(shape=nodeRepShape, style=nodeRepStyle, color=nodeRepColor,
            font=nodeRepFont, fontsize=nodeRepFontSize, fontcolor=nodeRepFontColor)

def updateNodeCustomObj(obj, repl=False):
    '''
    update a graph node for nodeCustom object styles
    '''
    if repl:
        updateNodeRepCustomObj(obj)
    else:
       obj.attr.update(shape=nodeCustomShape, style=nodeCustomStyle, color=nodeCustomColor,
                font=nodeCustomFont, fontsize=nodeCustomFontSize, fontcolor=nodeCustomFontColor)

def updateNodeRepCustomObj(obj):
    '''
    update a graph node for nodeRepCustom object styles
    '''
    obj.attr.update(shape=nodeRepCustomShape, style=nodeRepCustomStyle, color=nodeRepCustomColor,
            font=nodeRepCustomFont, fontsize=nodeRepCustomFontSize, fontcolor=nodeRepCustomFontColor)

