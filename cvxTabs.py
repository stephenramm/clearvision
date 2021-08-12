"""
This module contains the class which implements the drawing area of each page
in the notebook
"""
import wx.aui
import wx.propgrid
import tempfile
import os
from lxml import etree
from cvxConst import const
import cvxXML as bG
from cvxXML import Xref
import traceback
import cvxKernelDefs as kdefs
import cvxDataDefs as ddefs
from cvxDataDefs import TypeDef
import cvxPreferences as options
from cvxMenus import NodeMenu, XNodeMenu, DataMenu
from cvxDialogs import GridCellHexEditor

# Map menu IDs to xml object tags
idToTagMap = {
    const.ID_InsertMenuDataArray: bG.sarray,
    const.ID_InsertMenuDataChannel: bG.splane,
    const.ID_InsertMenuDataConvolution: bG.sconvolution,
    const.ID_InsertMenuDataDelay: bG.sdelay,
    const.ID_InsertMenuDataDelayOfSelected: bG.sdelay,
    const.ID_InsertMenuDataDistribution: bG.sdistribution,
    const.ID_InsertMenuDataImage: bG.simage,
    const.ID_InsertMenuDataLut: bG.slut,
    const.ID_InsertMenuDataMatrix: bG.smatrix,
    const.ID_InsertMenuDataObjectArray: bG.sobject_array,
    const.ID_InsertMenuDataObjectArrayFromTensor: bG.sobject_array,
    const.ID_InsertMenuDataObjectArrayOfSelected: bG.sobject_array,
    const.ID_InsertMenuDataPyramid: bG.spyramid,
    const.ID_InsertMenuDataPyramidOfSelected: bG.spyramid,
    const.ID_InsertMenuDataRemap: bG.sremap,
    const.ID_InsertMenuDataROI: bG.sroi,
    const.ID_InsertMenuDataScalar: bG.sscalar,
    const.ID_InsertMenuDataTensor: bG.stensor,
    const.ID_InsertMenuDataThreshold: bG.sthreshold,
    const.ID_InsertMenuDataView: bG.sview
}

def nearEnough(a, b):
    """
    test for "equality" of non-exact numbers
    """
    fa = float(a)
    fb = float(b)
    return abs(float(a) - float(b)) < 0.0001 * fa

def Large(rect):
    """
    Inflate a rect by a standard amount
    """
    return rect.Inflate(5, 5)

class Notebook(wx.aui.AuiNotebook):
    """
    Class to implement the notebook, and act on the various required

    Member variables:
        topframe    cvxMain.MainFrame   logical owner of the notebook
    """

    def __init__(self, parent):
        """
        Initialise the cvxNotebook object; binds the page change event

        cvxMain.MainFrame   parent
        """
        wx.aui.AuiNotebook.__init__(self,  # @UndefinedVariable
                                    parent,
                                    style=wx.NB_TOP)
        self.topframe = parent
        self.tree = None
        self.xrefs = None
        self.graphs = None
        self.undoList = []
        self.redoList = []
        self.zoom = 1.0
        self.rankdir = "TB"
        self.dpi = 96
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED,  # @UndefinedVariable
                  self.OnPageChanged)

    # Event handlers
    def OnPageChanged(self, event):
        """
        Here when the page changes.
        wx.Event event
        returns nothing
        """
        old_page = event.GetOldSelection()
        new_page = event.GetSelection()
        # can get confused by deletion / removal of pages.
        if old_page != -1 and new_page != -1 and old_page != new_page:
            thisPage = self.GetCurrentPage()
            thisPage.attrObj = None # properties most likely will need to be updated.
            thisPage.SetFocus()

    # added functions

    def GetGlobalsPage(self):
        for i in range(self.GetPageCount()):
            if self.GetPageText(i) == bG.globalsName:
                return self.GetPage(i)
        return None

    def ClearAll(self):
        """
        Clear out etree, graphs and pages
        """
        while self.GetPageCount():
            self.DeletePage(0)
        
    def DefaultGraph(self):
        # Read the default graph
        self.Save()
        self.tree = etree.XML(options.defaultGraph)
        self.BuildGraphs()
    
    def BuildGraphs(self):
        """
        Build the graphs. 
        Add pages as necessary, otherwise re-use them.
        Remove pages not now in the list
        Note: each entrey in self.graphs is a tuple of elem, graph
        """
        # Build all the graphs
        bG.showVirtuals = self.topframe.GetMenuBar().IsChecked(const.ID_ViewMenuShowVirtuals)
        self.graphs = bG.buildGraphs(self.tree)
        i = 0
        pageNames = set()
        while i < self.GetPageCount():
            # Remove any pages no longer required and update others:
            name = self.GetPageText(i)
            if name not in self.graphs:
                self.DeletePage(i)
            else:
                self.GetPage(i).Update(self.graphs[name])
                pageNames.add(name)
                i += 1
        # Add any new pages
        for name in self.graphs:
            if name not in pageNames:
                self.AddPage(DrawPanel(self, self.topframe, self.graphs[name]), name)
        self.Refresh()

    def Redraw(self, rankdir=None):
        """
        Mark all graphs for redraw and update the rank direction
        """
        if rankdir is not None:
            self.rankdir = rankdir
        for elem, graph in list(self.graphs.values()):
            Xref.setDirty(graph)
        self.Refresh()

    def ReadGraphs(self, filename):
        """
        Clear out any pages, and create new ones as per the given file.
        """
        self.Scrap()
        self.tree = etree.parse(filename).getroot()
        self.BuildGraphs()

    def Save(self):
        """
        Save the current state in the undo list
        The list doesn't grow larger than a defined size
        """
        self.topframe.Ready()
        if self.tree is not None:
            if len(self.undoList) >= options.maxUndo:
                self.undoList.pop(0)
            self.undoList.append(etree.tostring(self.tree))
        self.redoList = []
        self.topframe.undoRedoEnable()

    def Undo(self):
        """
        Undo the last saved operation
        """
        if len(self.undoList) > 0:
            self.redoList.append(etree.tostring(self.tree))
            self.tree = etree.fromstring(self.undoList.pop())
            Xref.setDirty()
            self.Refresh()
        else:
            self.topframe.Error("No operations to undo")
        self.topframe.undoRedoEnable()

    def ScrapIfSame(self):
        """
        If what we have saved for the undo operation is the
        same as what we have currently, scrap the last save
        """
        if len(self.undoList) > 0 and undoList[-1] == etree.tostring(self.tree):
            self.ScrapUndo()

    def Redo(self):
        """
        Redo the last undone operation
        """
        if len(self.redoList) > 0 :
            self.undoList.append(etree.tostring(self.tree))
            self.tree = etree.fromstring(self.redoList.pop())
            Xref.setDirty()
            self.Refresh()
        else:
            self.topframe.Error("No operations to redo")
        self.topframe.undoRedoEnable()

    def Scrap(self):
        """
        Scrap both the undo and redo lists
        """
        self.undoList = []
        self.redoList = []
        self.topframe.undoRedoEnable()

    def ScrapUndo(self):
        """
        Scrap the last save operation
        """
        self.undoList.pop()
        self.topframe.undoRedoEnable()
        
    def NewGraph(self):
        self.Save()
        name, val = bG.insertGraph()
        self.graphs[name] = val
        self.AddPage(DrawPanel(self, self.topframe, val), name)
        self.Refresh()

    def RemoveGraph(self, name=""):
        """
        Inverse of NewGraph()
        """
        p = -1
        if name=="":
            p = self.GetSelection()
            pname = self.GetPageText(p)
        else:
            pname = Xref.get(name).name
            for q in range(self.GetPageCount()):
                if self.GetPageText(q) == pname:
                    p = q
                    break
        if name == bG.globalsName:
            self.topframe.Error("Can't remove the '%s' tab. Did you mean to clear it?"%pname, True)
        elif p == -1:
            self.topframe.Error("Can't find the graph named '%s'"%pname, True)
        else:
            self.Save()
            self.tree.remove(self.graphs[pname][0])
            # Now fix up everything simply by requiring a rebuild:
            Xref.setDirty()
            self.Refresh()

    def RemoveObj(self):
        """
        Remove or disconnect the currently selected object, if there is one
        Handling of Save() is done here.
        """
        p = self.GetCurrentPage()
        obj = p.selectedObj
        if obj is None:
            self.topframe.Error("No object selected")
        else:
            xobj = Xref.get(obj)
            tag = xobj.tag
            if tag == bG.snode:
                self.Save()
                p.removeNode(obj)
            elif tag == bG.sparameter:
                p.removeGraphParameter(obj)
            elif tag in bG.dataObjectTags:
                # can't 'delete' contained or immutable data:
                if xobj.isImmutable():
                    self.topframe.Error("Can't delete immutable data")
                elif xobj.isChild() and tag not in {bG.sroi, bG.sview, bG.splane}:
                    #p.selectedObj = p.graph.get_node(xobj.tagref)
                    #self.RemoveObj() 
                    self.topframe.Error("Can't delete child - change number of elements in parent instead")
                else:
                    self.Save()
                    if p.removeData(obj):
                        self.Refresh()
                    else:
                        self.ScrapUndo()
            elif tag == bG.sgraph:
                self.RemoveGraph(obj)
            else:
                self.topframe.Error("Cannot currently remove that type of object")

    def ConnectObjects(self):
        """
        Connect 2 objects - just like drag from one to the other, or drag from
        nothing to node.
        """
        p = self.GetCurrentPage()
        if p.selectedObj is not None and p.upObj is not None:
            p.AddConnection(p.selectedObj, p.upObj)
        elif p.selectedObj is None:
            if Xref.get(p.upObj).tag == bG.snode:
                p.AddOptional(p.upObj)
        elif Xref.get(p.selectedObj).tag == bG.snode:
                p.AddOptional(p.selectedObj)
        self.Refresh()

    def InsertGraphParameter(self):
        """
        Insert a graph parameter is an object is selected
        Handling of Save() is done at a lower level
        """
        p = self.GetCurrentPage()
        obj = p.selectedObj
        if obj is None:
            self.topframe.Error("No object selected")
        else:
            p.insertGraphParameter(obj, p.upObj)
            self.Refresh()

    def ToggleVirtual(self):
        """
        Only for data objects...
        If contained, operate on parent
        If virtual, make non-virtual if:
        If non-virtual, then make virtual if:
        Not connected to a graph parameter on any graph, directly or via children
        Not immutable
        """
        p = self.GetCurrentPage()
        obj = p.selectedObj
        if obj is None:
            self.topframe.Error("No object selected")
        else:
            tag = Xref.get(obj).tag
            if tag in bG.dataObjectTags:
                ref = str(obj)
                xobj = Xref.get(ref)
                elem = xobj.elem
                root = self.graphs[bG.globalsName][0]
                if xobj.isChild():
                    ptagref = xobj.tagref
                    if p.graph.has_node(ptagref):
                        p.selectedObj = p.graph.get_node(ptagref)
                        self.ToggleVirtual() 
                    else:
                        p.selectedRect = p.LargeBoundingRect(p.selectedObj)
                        self.topframe.Error("Can't move child objects unless parent is on the same tab")
                elif xobj.isVirtual():
                    self.Save()
                    elem.getparent().remove(elem)
                    root.append(elem)
                    self.BuildGraphs()
                elif xobj.isImmutable():
                    self.topframe.Error("Immutable data must be global")
                else:
                    # Now go looking for graph parameters that reference this object, over
                    # the entire xml tree. First, build a set of references for the object
                    # and all it's dataObject children:
                    refs = {ref}
                    for child in elem.iterdescendants():
                        if etree.QName(child).localname in bG.dataObjectTags:
                            refs.add(child.attrib[bG.sreference])
                    # Now we iterate over all graphs looking for a graph parameter that references
                    # an object we have in the set, and also create a set of all graphs that reference
                    # the object:
                    graphs = set()
                    graphtag = etree.QName(root, bG.sgraph).text
                    paramtag = etree.QName(root, bG.sparameter).text
                    nodetag = etree.QName(root, bG.snode).text
                    for g in root.iterchildren(graphtag):           # check all the graphs
                        for gp in g.iterchildren(paramtag):         # check all graph parameters
                            nelem = Xref.get(gp.get(bG.snode)).elem # the node referenced by this graph parameter
                            nindex = gp.attrib[bG.sparameter]       # index of the node parameter
                            for np in nelem.iterchildren(paramtag): # check node parameters
                                # See if the node parameter references this element
                                if np.attrib[bG.sindex] == nindex and np.attrib[bG.sreference] in refs:
                                    return self.topframe.Error("Graph parameters must be global")
                        for n in g.iterchildren(nodetag):           # Check all nodes of the graph
                            for np in n.iterchildren(paramtag):
                                if np.attrib[bG.sreference] in refs:
                                    graphs.add(g)
                    if len(graphs) == 0:
                        self.topframe.Error("Can't do this as the object is not referenced in any graph")
                    elif len(graphs) > 1:
                        self.topframe.Error("Can't do this as the object or a child is referenced in more than one graph")
                    else:
                        # here when it's not a graph parameter and referenced in one graph only:
                        # we simply remove from root and append to the selected graph
                        self.Save()
                        root.remove(elem)
                        graphs.pop().append(elem)
                        self.BuildGraphs()
            else:
                self.topframe.Error("Must select a data object")

    def Replicate(self):
        """
        Here for replicate node
        Need to show a dialog that can capture which of the parameters are to be replicated
        and how many data objects must be there
        """
        pg = self.GetCurrentPage()
        obj = pg.selectedObj
        if obj is None:
            self.topframe.Error("No object selected")
        else:
            tag = Xref.get(obj).tag
            if tag == bG.snode:
                params = bG.getPossibleReplicates(obj)
                choices = []
                selections = []
                hadImage = False
                i = 0
                for o, p in list(params.items()):
                    choices.append("Parameter %d : %s (%s)"%(o, p.kp.pname, p.kp.pdir))
                    if p.kp.ptype == kdefs.s_vx_image:
                        hadImage = True
                    if p.repl == bG.strue:
                        selections.append(i)
                    i += 1
                numparams = len(choices)
                if numparams == 0:
                    return self.topframe.Error("There are no suitable parameters")
                else:
                    # There is a choice
                    if hadImage:
                        choices.append("Insert newly selected images as pyramids")
                    choiceDlg = wx.MultiChoiceDialog(self, "Select parameters to replicate", "Node replication", choices)
                    choiceDlg.SetSelections(selections)
                    if choiceDlg.ShowModal() == wx.ID_OK:
                        newSelections = choiceDlg.GetSelections()
                    else:
                        return self.topframe.Error("Node replication was canceled")
                # Here with the selections; we assume we will do something if newSelections are different.
                if hadImage and numparams in newSelections:
                    del newSelections[newSelections.index(numparams)]
                    insertAsPyramid = True
                else:
                    insertAsPyramid = False
                if newSelections == selections:
                    return self.topframe.Status("No changes were made")
                nelem = Xref.get(obj).elem
                # First - are any selected at all?
                if len(newSelections) == 0:
                    # Node is no longer replicated
                    # We have a shortcut and clean out all parameters as well as the node
                    self.Save()
                    for p in params.values():
                        p.param.attrib[bG.sreplicate_flag] = bG.sfalse
                    nelem.attrib[bG.sis_replicated] = bG.sfalse
                else:                    
                    # Create a set of parameter indices
                    selections = set()
                    for i in range(len(newSelections)):
                        selections.add(int(choices[newSelections[i]].split(' ')[1]))
                    # Now we have to check the number of replicates. Cannot replicate a parameter where the
                    # number of replicates has already been determined and it does not match the object's container
                    replicates = 0
                    for i in selections:
                        if params[i].ptag == bG.sobject_array:
                            if replicates > 0 and replicates != params[i].num:
                                return self.topframe.Error("Object array for parameter %d has a different number of elements"%i, True)
                            else:
                                replicates = params[i].num
                        elif params[i].ptag == bG.spyramid:
                            if replicates > 0 and replicates != params[i].num:
                                return self.topframe.Error("Pyramid for parameter %d has a different number of levels"%i, True)
                            else:
                                replicates = params[i].num
                    # Initial checks on suitability done. We may need a number of levels for object arrays we need to create:
                    if replicates == 0:
                        replicates = wx.GetNumberFromUser("The number of replicates is required", "Enter a number between 1 and 1024", "Node replication", 4, 1, 1024)
                        if replicates == -1:
                            return self.topframe.Error("Node replication was canceled")
                    # Here with the number of replicates to create where necessary, nothing more to go wrong at this stage
                    # (checks on graph may still fail) so we can save and proceed:
                    self.Save()
                    for p in params.values():    # Clear out old replicate flags
                        p.param.attrib[bG.sreplicate_flag] = bG.sfalse
                    for i in selections:
                        if params[i].ptag not in {bG.sobject_array, bG.spyramid}:
                            # We must create an object array or pyramid for the parameters.
                            if insertAsPyramid and params[i].kp.ptype == kdefs.s_vx_image:
                                bG.makePyramid(params[i].elem, pg.graph, replicates)
                            else:
                                bG.makeObjectArray(params[i].elem, pg.graph, replicates)
                        params[i].param.attrib[bG.sreplicate_flag] = bG.strue
                    nelem.attrib[bG.sis_replicated] = bG.strue
                self.BuildGraphs()
            else:
                self.topframe.Error("Must select a node")

    def RenameObject(self, newName):
        """
        Rename the selected object, or the graph
        Does not require a rebuild, only a redraw
        """
        p = self.GetCurrentPage()
        if p.selectedObj is None:
            # rename the graph
            elem = p.element
            tag = bG.sgraph
            ref = p.graph.name
        else:
            ref = str(p.selectedObj)
            elem = Xref.get(ref).elem
            tag = Xref.get(ref).tag
        oldName = Xref.get(ref).name
        if oldName == bG.globalsName:
            self.topframe.Error("You are not allowed to change the name of the %s tab"%oldName)
        else:
            if newName == oldName or newName == "":
                self.topframe.Status("Nothing was changed")
            elif newName == bG.globalsName:
                self.topframe.Error("Sorry, '%s' is a reserved name"%newName)
            else:
                self.Save()
                if bG.changeObjectName(newName, elem, ref):
                    if tag == bG.sgraph:
                        # rename the notebook page
                        for i in range(self.GetPageCount()):
                            if self.GetPageText(i) == oldName:
                                self.SetPageText(i, newName)
                                break
                    self.Refresh()
                else:
                    self.ScrapUndo()
                    self.topframe.Status("Nothing could be changed")

    def OnPropertyChange(self, event):
        """
        Here when a property of an object is changed by the user.
        """
        props = self.topframe.properties
        attr = event.GetPropertyName()
        value = event.GetPropertyValue()
        stringValue = event.GetProperty().GetValueAsString()
        p = self.GetCurrentPage()
        if attr == bG.sname:
            self.RenameObject(value)
        if p.selectedObj is not None:
            # Something to do
            self.Save()
            ref = str(p.selectedObj)
            xobj = Xref.get(ref)
            elem = xobj.elem
            tag = etree.QName(elem).localname
            if tag == bG.snode:
                if attr == bG.sborderconst:
                    for child in elem.iterchildren(etree.QName(elem, attr).text):
                        child.text = "#%8X"%value
                elif attr == bG.sbordermode:
                    elem.set(attr, stringValue)
                else:
                    # Here we have to update any immutable parameters
                    for param in elem.iterchildren(etree.QName(elem, bG.sparameter).text):
                        pref = param.get(bG.sreference)     # reference to the data object
                        pindex = int(param.get(bG.sindex))  # index of the parameter
                        # Lookup the parameter in Xref to see if it is immutable
                        kpi = xobj.kdef.params[pindex] # kernel parameter information
                        if kpi.pstate == kdefs.kpImmutable:
                            # OK, we have immutable data. The name for the property is the parameter name,
                            # the type is given by kpi.ptype and the data resides in the object referenced by pref.
                            parts = attr.split('.')
                            print(("Got immutable data change for %s; object name is %s, reference %s"%(attr, Xref.get(pref).name, pref)))
                            print(("kpi.name is %s, parts[0] is %s"%(kpi.pname, parts[0])))
                            if kpi.pname == parts[0]:
                                parts[0] = 'data'
                                bG.updateScalarValues(Xref.get(pref), '.'.join(parts), value, stringValue)

            elif attr == bG.sscale and tag == bG.spyramid:
                elem.set(attr, ["0.5", "0.8408964"][value])
            elif attr == bG.sformat:
                elem.set(attr, TypeDef.formatToString(value))
            elif attr.startswith(bG.sdimension):
                # tensor dimension size
                idx = attr.split(' ')[1]
                for dim in elem.iterchildren(etree.QName(elem, bG.sdimension).text):
                    if idx == dim.get(bG.sindex):
                        dim.set(bG.ssize, stringValue)
            elif attr == 'identifier':
                # user struct identifier change. Have to find the old one in the table
                # and replace it, if this is allowed
                ptype = TypeDef.get('vx_type_e')
                if stringValue in ptype.defs:
                    # Problem -name already exists
                    self.ScrapUndo()
                    p.attrObj = None
                    return self.topframe.Error("Cannot change user struct id to name of existing type", True)
                else:
                    ptype.defs[stringValue] = ptype.defs.get(elem.text)
                    del ptype.defs[elem.text]
                    elem.text = stringValue
            elif tag == bG.sscalar:
                if attr.endswith(' subtype'):
                    # just set sub-type for properties change
                    xobj.subtype = stringValue
                else:
                    if attr == bG.selemType:
                        elem.set(attr, stringValue)
                    else:
                        bG.updateScalarValues(xobj, attr, value, stringValue)
            elif tag == bG.sarray:
                if attr.endswith(' subtype'):
                    xobj.subtype = stringValue
                elif attr.endswith(' size'):
                    xobj.datasize = value
                else:
                    if attr in {bG.scapacity, bG.selemType}:
                        elem.set(attr, stringValue)
                    else:
                        bG.updateArrayValues(xobj, attr, value, stringValue)
            elif tag in {bG.smatrix, bG.sconvolution} and attr.startswith('data['):
                bG.updateRowColumn(elem, attr[4:],
                                   TypeDef.tagFromEnum(elem.get(bG.selemType)) if tag == bG.smatrix else bG.sint16,
                                   stringValue)
            elif tag in {bG.slut, bG.sdistribution} and attr.startswith("start "):
                xobj.datasize = value
            elif attr.startswith("index ") or attr.startswith("bin "):
                bG.updateSubElement(elem, attr, 
                                    TypeDef.tagFromEnum(elem.get(bG.selemType)) if tag == bG.slut else bG.sfrequency,
                                    stringValue)
            elif attr.startswith('dst_') and tag == bG.sremap:
                xobj.datasize[attr] = stringValue
            elif attr.startswith('src_') and tag == bG.sremap:
                splits = attr.split('[')
                name = splits[0]
                dst_y = splits[1][:-1]
                dst_x = splits[2][:-1]
                for child in list(elem):
                    if child.get('dst_x') == dst_x and child.get('dst_y') == dst_y:
                        break
                else:
                    # We have not been able to write the data; the subelement is missing, so we must create one
                    child = etree.Element(etree.QName(elem, 'point'))
                    child.set('dst_x', dst_x)
                    child.set('dst_y', dst_y)
                    child.set('src_x', dst_x)
                    child.set('src_y', dst_y)
                    elem.append(child)
                child.set(name, stringValue)
            else:
                elem.set(attr, stringValue)
            # check for change in compound object count or other attribute that
            # may need propagation
            if tag == bG.spyramid:
                bG.changePyramidAttributes(elem, p.graph)
            elif attr == bG.scount:
                bG.changeDelayOrArrayCount(elem, p.graph)
            elif attr == bG.snumber_of_dims:
                bG.changeTensorSize(elem, p.graph)
            # get parent and tag from xml
            pelem = elem.getparent()
            ptag = etree.QName(pelem).localname
            # check for child change to be propagated to parent
            if ptag == bG.spyramid:
                bG.changePyramidChildAttributes(elem, p.graph)
            elif ptag in {bG.sobject_array, bG.sdelay}:
                bG.changeDelayOrArrayChildAttributes(elem, p.graph)
    
            p.attrObj = None # properties most likely will need to be updated.
            self.Refresh()
    
    def InsertData(self, id):
        """
        Insert a data item. The menu enabling/disabling should
        have sorted out what can and can't be done
        We get passed the id of the menu item and have to decode further -
        this was to avoid a huge proliferation of bindings
        """
        p = self.GetCurrentPage()
        obj = p.selectedObj
        tag = None
        if id == const.ID_InsertMenuDataDelay:
            choice = wx.GetSingleChoice("Please select from available object types",
                                        "Select type for delay", bG.delayChoices)
            if choice != "":
                self.Save()
                bG.insertDelay(p.element, p.graph, choice)
        elif id == const.ID_InsertMenuDataObjectArray:
            choice = wx.GetSingleChoice("Please select from available object types",
                                        "Select type for object array", bG.objectArrayChoices)
            if choice != "":
                self.Save()
                bG.insertObjectArray(p.element, p.graph, choice)
        elif id == const.ID_InsertMenuDataDelayOfSelected:
            self.Save()
            bG.makeDelay(Xref.get(obj).elem, p.graph, 3)
        elif id == const.ID_InsertMenuDataObjectArrayOfSelected:
            self.Save()
            bG.makeObjectArray(Xref.get(obj).elem, p.graph, 3)
        elif id == const.ID_InsertMenuDataPyramidOfSelected:
            self.Save()
            bG.makePyramid(Xref.get(obj).elem, p.graph, 4)
        elif id == const.ID_InsertMenuDataObjectArrayFromTensor:
            pass
        elif id in {const.ID_InsertMenuDataROI, const.ID_InsertMenuDataChannel}:
            self.Save()
            bG.insertObject(Xref.get(obj).elem, p.graph, idToTagMap[id])
        elif id == const.ID_InsertMenuDataView:
            pass
        else:
            tag = idToTagMap[id]
        if tag is not None:
            self.Save()
            bG.insertObject(p.element, p.graph, tag)
        self.Refresh()

class DrawPanel(wx.ScrolledWindow):
    """
    Class to implement a drawing area for a graph on a tab

    Member variables:
    """

    def __init__(self, parent, topframe, elemGraph):
        """
        Initialise DrawPanel object, binds mouse, paint, and key_down events

        Notebook            parent      - the owning window, in this case
                                        (design case) the wx.notebook to which
                                        this has been added as a page
        cvxMain.MainFrame   topframe    - the application main frame;gives
                                        access to various objects required by
                                        this window
        tab                 Graph       - supplied if a pre-existing graph is
                                        to be shown
        """
        wx.ScrolledWindow.__init__(self, parent, -1, style=wx.HSCROLL|wx.VSCROLL|wx.SUNKEN_BORDER)

        self.topframe = topframe
        self.parent = parent
        self.SetBackgroundColour("WHITE")

        self.SetScrollRate(20, 20)

        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)
        self.Bind(wx.EVT_PAINT, self.OnPaintTab)
        self.InitPos()
        self.Update(elemGraph)
        # Set up a dictionary for key event handling for this window
        self.key_table = {(wx.ACCEL_NORMAL,
                           wx.WXK_RIGHT): self.MoveRight,
                          (wx.ACCEL_NORMAL,
                           wx.WXK_LEFT): self.MoveLeft,
                          (wx.ACCEL_NORMAL,
                           wx.WXK_DOWN): self.MoveDown,
                          (wx.ACCEL_NORMAL,
                           wx.WXK_UP): self.MoveUp,
                          (wx.ACCEL_SHIFT,
                           wx.WXK_RIGHT): lambda: self.MoveRight(False),
                          (wx.ACCEL_SHIFT,
                           wx.WXK_LEFT): lambda: self.MoveLeft(False),
                          (wx.ACCEL_SHIFT,
                           wx.WXK_DOWN): lambda: self.MoveDown(False),
                          (wx.ACCEL_SHIFT,
                           wx.WXK_UP): lambda: self.MoveUp(False),
                          (wx.ACCEL_NORMAL,
                           wx.WXK_PAGEDOWN): lambda: self.ScrollSome(0, 10),
                          (wx.ACCEL_NORMAL,
                           wx.WXK_PAGEUP): lambda: self.ScrollSome(0, -10),
                          (wx.ACCEL_SHIFT,
                           wx.WXK_PAGEDOWN): lambda: self.ScrollSome(10, 0),
                          (wx.ACCEL_SHIFT,
                           wx.WXK_PAGEUP): lambda: self.ScrollSome(-10, 0),
                          (wx.ACCEL_NORMAL,
                           wx.WXK_ESCAPE): self.SelectNone,
                          (wx.ACCEL_NORMAL,
                           wx.WXK_INSERT): self.insertNodeMenu,
                          (wx.ACCEL_SHIFT,
                           wx.WXK_INSERT): lambda: self.insertNodeMenu(True),
                          (wx.ACCEL_CTRL,
                           wx.WXK_INSERT): self.insertDataMenu,
                          (wx.ACCEL_NORMAL,
                           wx.WXK_MENU): lambda: self.topframe.properties.SetFocus()
                          }
        # Bind KEY_DOWN
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

    # Event handlers
    def OnPaintTab(self, evt):
        """
        called to update the visible area of the tab

        Just draw the bitmap...
        and the selection

        wx.Event evt
        
        """
        if Xref.isDirty():
            # We need to rebuild the graphs
            self.parent.BuildGraphs()
        if Xref.isDirty(self.graph):
            # We need to redraw
            self.Redraw()
        self.updateMenus()
        self.updateProperties()
        x, y = self.bitmap.GetSize()
        scale = self.parent.zoom
        self.SetVirtualSize(x * scale, y * scale)
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        dc.Clear()
        dc.SetUserScale(scale, scale)
        vr = self.getVisibleRect()
        br = wx.Rect(0, 0, x, y)
        br = br.Intersect(vr)
        if br.width > 0 and br.height > 0:
            dc.DrawBitmap(self.bitmap.GetSubBitmap(br), br.left, br.top)
        if self.selectedRect is not None:
            dc.SetBrush(wx.Brush('WHITE', style=wx.TRANSPARENT))
            dc.SetPen(wx.Pen('GREEN', style=wx.DOT))
            dc.DrawRectangle(self.selectedRect)
        if self.downPos is not None and self.dragPos is not None:
            dc.SetPen(wx.LIGHT_GREY_PEN)
            dc.DrawLine(self.downPos, self.dragPos)
        if self.upObj is not None and self.upObj != self.selectedObj:
            dc.SetBrush(wx.Brush('WHITE', style=wx.TRANSPARENT))
            dc.SetPen(wx.Pen('RED', style=wx.DOT))
            dc.DrawRectangle(self.upRect)

    def OnMouse(self, event):
        """
        Mouse event handler

        wx.Event event
        Process mouse events:
        Left button down
        Left button up
        Right button down
        Right button up
        Drag
        Left button double-click
        Right button double-click
        """
        scale = self.parent.zoom
        rawpos = self.CalcUnscrolledPosition(event.GetX(),event.GetY()) # Where on the screen the mouse is
        mpos = (rawpos[0] / scale, rawpos[1] / scale)
        self.dragPos = None
        if event.LeftDown():            # normal mouse click - will select something
            # Try and find an object under the mouse
            self.downPos = mpos         # Record where the button was clicked
            self.selectedObj, self.selectedRect = self.ObjAtPos(mpos)
            self.Refresh()
        elif event.Dragging():
            self.dragPos = mpos         # Record current mouse drag position
            # Process automatic scrolling
            ppu = self.GetScrollPixelsPerUnit()
            sx = event.GetX() / ppu[0]
            sy = event.GetY() / ppu[1]
            vs = self.GetViewStart()
            sz = self.GetClientSize()
            sz[0] = sx - sz[0] / ppu[0] + vs[0]
            sz[1] = sy - sz[1] / ppu[1] + vs[1]
            sx = vs[0] + sx if sx < 0 else sz[0] if sz[0] > vs[0] else vs[0]
            sy = vs[1] + sy if sy < 0 else sz[1] if sz[1] > vs[1] else vs[1]
            self.Scroll((sx,sy))
            self.Refresh()
        elif event.LeftUp():            # Action on leftUp depends upon what's selected
            self.dragPos = None
            self.upObj, self.upRect = self.ObjAtPos(mpos)
            self.LeftMouse(event.ControlDown(), event.ShiftDown(), event.AltDown())
            self.Refresh()
        elif event.LeftDClick():        # Always preceded by a LeftUp()
            pass
        elif event.RightDown():
            # Try and find an object under the mouse
            self.downPos = mpos         # Record where the button was clicked
            self.selectedObj, self.selectedRect = self.ObjAtPos(mpos)
            self.Refresh()
        elif event.RightUp():
            self.dragPos = None
            self.upObj = None
            self.upRect = None
            self.contextMenu(event.ControlDown(), event.ShiftDown(), event.AltDown())
            self.Refresh()
        elif event.RightDClick():       # Always precede by a RightUp()
            pass
        else:
            delta = - round(event.GetWheelRotation() / 60.0)
            if delta:
                if event.ShiftDown() or event.GetWheelAxis == wx.MOUSE_WHEEL_HORIZONTAL:
                    self.Scroll(self.GetViewStart() + wx.Point(delta, 0))
                else:
                    self.Scroll(self.GetViewStart() + wx.Point(0, delta))
                if event.ControlDown():
                    if delta > 0:
                        self.parent.zoom *= 1.4142135
                    else:
                        self.parent.zoom /= 1.4142135
                self.Refresh()

    def OnKeyDown(self, event):
        """
        The KEY_DOWN event handler. Processes key down events for this window
        wx.Event event
        """
        ix = (event.GetModifiers(), event.GetKeyCode())
        if ix in self.key_table:
            self.key_table[ix]()
        else:
            event.Skip()

    # Overridden methods
    # New methods

    def getData(self, tag, elem):
        """
        return data from the xml object elem,
        which should be have the given tag.
        Return an list of values, each of which could be a dictionary or a list.
        Notice that no structure type we use currently contain arrays or
        structures; if this changes then we have to revisit this method.
        For the moment, we ignore ptype except for chars and assume we have correct data.
        The function is used for both scalars and arrays. We hope that
        there is only one child for scalars (as there should be)...
        """
        values = []
        for child in elem:
            d = bG.getData(child, tag)
            if tag == 'user':
                values.append(d)
            elif isinstance(d, list):
                values += d
            elif d is not None:
                values.append(d)
        return values

    def insertArrayDataProperty(self, props, pname, pxtype, pref, isArray=True, needData=True):
        """
        Insert a scalar data property or multiple array data properties
        with label pname, type ptype and data from object referenced by pref.
        Notice that ptype may be either from the vx_type_e enumeration, or
        a type name. The first thing we do is to convert it to a type name
        """
        ptype = TypeDef.typeFromEnum(pxtype, pxtype)
        elem = Xref.get(pref).elem
        values = self.getData(TypeDef.tagFromEnum(elem.get(bG.selemType)), elem)
        xobj = Xref.get(pref)
        if ptype == 'vx_enum':
            # Need to select a sub-type for this object
            t = xobj.subtype  # get last recorded sub-type for this object
            if t is None:
                # default the type to a number if we haven't had this before
                t = ddefs.s_vx_uint32
            self.insertEnumProperty(props, pname + ' subtype', ptype, t)
            ptype = t
        if isArray:
            # We need to select the array size based upon current size
            # with a maximum of the given capacity
            cap = int(xobj.elem.get(bG.scapacity, "1"))
            cursize = xobj.datasize     # min(len(values), xobj.datasize)
            self.insertUintProperty(props, pname + ' size', cursize, max=cap)
        else:
            cursize = 1
        if needData and len(values) < cursize:
            values += [TypeDef.defaultData(ptype)] * (cursize - len(values))
        for i in range(cursize):
            if isArray:
                elname = "%s[%d]"%(pname, i)
            else:
                elname = pname
            self.insertScalarDataProperty(props, elname, ptype, values[i], pref)

    def insertScalarDataProperty(self, props, elname, ptype, value, pref):
        """
        Insert a scalar data property with label pname, type ptype and data given in value
        Notice that ptype is a type name.
        pref is the reference of the object, required for vx_enum
        """
        if isinstance(value, dict):
            # it's a structure. Iterate through the definition
            # getData will have provided the values in a dictionary
            for fname, ftype in TypeDef.items(ptype):
                print((fname, ftype))
                self.insertScalarDataProperty(props, "%s.%s"%(elname, fname), ftype, value[fname], pref)
        elif isinstance(value, list):
            # it must be a user struct. Iterate through byte values
            for i in range(len(value)):
                self.insertUintProperty(props, "%s[%d]"%(elname, i), value[i], max=255)
        elif ptype in {'vx_int8', 'vx_int16', 'vx_int32', 'vx_int64'}:
            self.insertIntProperty(props, elname, value)
        elif ptype in {'vx_uint8', 'vx_uint16', 'vx_uint32', 'vx_uint64', 'vx_size'}:
            self.insertUintProperty(props, elname, value)
        elif ptype in {'vx_float16', 'vx_float32', 'vx_float64'}:
            self.insertFloatProperty(props, elname, value)
        elif ptype == 'vx_char':
            self.insertStringProperty(props, elname, value)
        elif ptype == 'vx_bool':
            props.Append(wx.propgrid.BoolProperty(label=elname, name=elname, value=value == 'true'))
        elif ptype == 'vx_df_image':
            self.insertEnumProperty(props, elname, 'vx_df_image_e', TypeDef.formatToId(value))
        elif ptype == 'vx_enum':
            # Need to select a sub-type for this object - it may be a field in a structure
            # (Notice that will affect all vx_enum fields in the structure) TODO
            t = Xref.get(pref).subtype  # get last recorded sub-type for this object
            if t is None:
                # default the type to a number if we haven't had this before
                t = ddefs.s_vx_uint32
            self.insertEnumProperty(props, elname + ' subtype', ptype, t)
            if t == ddefs.s_vx_uint32:
                self.insertUintProperty(props, elname, value, max=0xFFFFFFFFFFFFFFFF)
            else:
                self.insertEnumProperty(props, elname, t, value)
        else:
            # Must be an enuemrated type
            self.insertEnumProperty(props, elname, ptype, value)

    def insertStringProperty(self, props, name, value, readOnly=False):
        """
        Insert a new string property in props
        value can be a string to show or an element from which to get the
        named attribute
        """
        svalue = value.get(name) if isinstance(value, etree._Element) else value
        if svalue is not None:
            objp = wx.propgrid.StringProperty(label=name, name=name, value=svalue)
            props.Append(objp)
            props.SetPropertyReadOnly(objp, readOnly)
            return objp
        return None

    def insertUintProperty(self, props, name, value, min=-1, max=-1):
        """
        Insert a new unsigned integer property in props
        value can be a string to show or an element from which to get the
        named attribute
        """
        svalue = value.get(name) if isinstance(value, etree._Element) else value
        if svalue is not None:
            objp = wx.propgrid.UIntProperty(name, name, int(svalue))
            if min >= 0:
                objp.SetAttribute('Min', min)
            if max >= 0:
                objp.SetAttribute('Max', max)
            props.Append(objp)
            return objp
        return None

    def insertIntProperty(self, props, name, value, min=None, max=None):
        """
        Insert a new unsigned integer property in props
        value can be a string to show or an element from which to get the
        named attribute
        """
        svalue = value.get(name) if isinstance(value, etree._Element) else value
        if svalue is not None:
            objp = wx.propgrid.IntProperty(name, name, int(svalue))
            objp.SetAttributes(dict(Min=min, Max=max))
            props.Append(objp)
            return objp
        return None

    def insertFloatProperty(self, props, name, value):
        """
        Insert a new unsigned integer property in props
        value can be a string to show or an element from which to get the
        named attribute
        """
        svalue = value.get(name) if isinstance(value, etree._Element) else value
        if svalue is not None:
            objp = wx.propgrid.FloatProperty(name, name, float(svalue))
            props.Append(objp)
            return objp
        return None

    def insertEnumProperty(self, props, name, enumname, value, start=None, end=None, excl=[]):
        """
        Insert a new enum property in props
        value can be:
        1) An element from which to get the named attribute
        2) A string to look up to get a value
        3) A value either as a string or an int
        4) None, in which case the property is not added
        enumname is the name of an enumeration in TypeDef
        start is None, the name of a value or the value itself from which to start the list (inclusive)
        end is None, the name of the value or the value itself before which to stop the list (exclusive)
        excl is a list or set of labels (string values) or actual values to exclude
        """
        print((props, name, enumname, value))
        svalue = value if isinstance(value, (int, type(None))) else  \
                 int(value) if isinstance(value, str) and value.isdigit() else \
                 TypeDef.getTypeVal(enumname, value.get(name) if isinstance(value, etree._Element) else value)
        startVal = TypeDef.getTypeVal(enumname, start) if isinstance(start, str) else start
        endVal = TypeDef.getTypeVal(enumname, end) if isinstance(end, str) else end
        if svalue is not None:
            labels, values = TypeDef.labelsValues(enumname, startVal, endVal, excl)
            objp = wx.propgrid.EnumProperty(label=name, name=name, labels=labels, 
                                            values=values, value=int(svalue))
            props.Append(objp)
            return objp
        return None

    def insertEnumPropertySubset(self, props, name, enumname, value, subset):
        """
        Insert a new enum property in props.
        Only values (string label or actual values) in the given subset are permitted
        """
        svalue = value.get(name) if isinstance(value, etree._Element) else value
        svalue = TypeDef.getTypeVal(enumname, svalue) if isinstance(svalue, str) else svalue
        if svalue is not None:
            values = []
            for i in range(len(subset)):
                v = subset[i]
                values.append(TypeDef.getTypeVal(enumname, v) if isinstance(v, str) else v)
            objp = wx.propgrid.EnumProperty(label=name, name=name, labels=subset, 
                                            values=values, value=int(svalue))
            props.Append(objp)
            return objp
        return None
            
    def insertMatrixProperties(self, props, elem, tag, displayName, rows, cols):
        """
        Insert properties to disply and set matrix and convolution data
        """
        props.Append(wx.propgrid.PropertyCategory('%s data in [row][column] order'%displayName))
        matMap = {}
        for child in elem:
            if etree.QName(child).localname == tag:
                matMap["data[%s][%s]"%(child.get(bG.srow, "."), child.get(bG.scolumn, "."))] = child.text
        for r in range(rows):
            for c in range(cols):
                matName = "data[%d][%d]"%(r, c)
                if tag == bG.sfloat32:
                    self.insertFloatProperty(props, matName, matMap.get(matName, 0.0))
                elif tag == bG.sint16:
                    self.insertIntProperty(props, matName, matMap.get(matName, 0), min=-0x8000, max=0x7FFF)
                elif tag == bG.sint32:
                    self.insertIntProperty(props, matName, matMap.get(matName, 0), min=-0x80000000, max=0x7FFFFFFF)
                elif tag == bG.uint8:
                    self.insertUintProperty(props, matName, matMap.get(matName, 0), max=255)
                else:
                    self.insertUintProperty(props, matName, matMap.get(matName, 42))    # secretly flag an unknown type with no data...

    def insertListDataProperty(self, props, ref, tag, attr, max, displayName):
        """
        Insert properties to display and edit data where there is one item per child, with
        tag tag and index attribute attr. Maximum number of children is max.
        The user is invited to edit up to 10 entries at a time, starting with the entry
        stored in the Xref.datasize property.
        """
        xobj = Xref.get(ref)
        curstart = xobj.datasize    # we re-use the size property as the start property
        self.insertUintProperty(props, 'start ' + attr, curstart, max=max - 1)

        props.Append(wx.propgrid.PropertyCategory('%s data from %s %d'%(displayName, attr, curstart)))

        # collect the data
        dataMap = {}
        for child in xobj.elem:
            if tag == etree.QName(child).localname:
                dataMap[child.get(attr, "?")] = child.text
        
        # display up to 10 data for editing
        for i in range(curstart, min(curstart + 10, max)):
            name = "%s %d"%(attr, i)
            value = dataMap.get(str(i), 0)
            if tag == bG.suint8:
                self.insertUintProperty(props, name, value, max=255)
            elif tag == bG.sint16:
                self.insertIntProperty(props, name, value, min=-0x80000, max=0x7FFF)
            elif tag == bG.sfrequency: # uint32
                self.insertUintProperty(props, name, value, max=0xFFFFFFFF)

    def updateProperties(self):
        """
        Show the properties of the selected object on the properties page.
        Don't do anything if the properties page is not visible or the object selected
        has not changed.
        We show properties by object type explicitly in order to preserve a common attribute order.
        """
        if self.topframe.GetMenuBar().FindItemById(const.ID_ViewMenuProperties).IsChecked() and self.attrObj != self.selectedObj:
            self.attrObj = self.selectedObj
            props = self.topframe.properties
            props.Clear()
            ref = self.selectedObj
            ref = self.graph.name if ref is None else str(ref)
            xobj = Xref.get(ref)
            elem = xobj.elem
            tag = etree.QName(elem).localname
            # Common to all: Tag, ref, name
            self.insertStringProperty(props, "object", tag, True)
            self.insertStringProperty(props, bG.sreference, ref, True)
            # cannot edit root name or graph parameter names
            self.insertStringProperty(props, bG.sname, xobj.name, ref == bG.sroot or tag == bG.sparameter)

            # data for each possible tag
            if tag == 'openvx':
                self.insertStringProperty(props, bG.sreferences, elem, False)
            elif tag == bG.sgraph:
                # attributes specific to graph
                self.insertStringProperty(props, 'nodes', elem, True)
            elif tag == bG.sparameter:
                # Graph parameter attributes
                for s in [bG.sparameter, bG.snode, bG.sindex]:
                    self.insertStringProperty(props, s, elem, True)
            elif tag == bG.snode:
                # Node attributes:
                # Kernel, replication flag, bordermode, border constant
                for k in elem.iterchildren(etree.QName(elem, bG.skernel).text):
                    self.insertStringProperty(props, bG.skernel, k.text, True)    
                self.insertStringProperty(props, bG.sis_replicated, elem, True)
                attr = bG.sbordermode
                props.Append(wx.propgrid.EnumProperty(label=attr, name=attr,
                                            labels=bG.borderModes,
                                            values=list(range(len(bG.borderModes))),
                                            value=bG.borderModes.index(elem.get(attr))))
                for bm in elem.iterchildren(etree.QName(elem, bG.sborderconst).text):
                    objp = wx.propgrid.UIntProperty(bG.sborderconst, bG.sborderconst, int(bm.text[1:], base=16))
                    objp.SetAttributes(dict(Min=0, Max=0xFFFFFFFF, Base=wx.propgrid.PG_BASE_HEX))
                    props.Append(objp)
                props.Append(wx.propgrid.PropertyCategory('Static or immutable parameters'))
                # And parameter data for immutable parameters
                for p in elem.iterchildren(etree.QName(elem, bG.sparameter).text):
                    pref = p.get(bG.sreference)     # reference to the data object
                    pindex = int(p.get(bG.sindex))  # index of the parameter
                    # Lookup the parameter in Xref to see if it is immutable
                    kpi = xobj.kdef.params[pindex] # kernel parameter information
                    if kpi.pstate == kdefs.kpImmutable:
                        # OK, we have immutable data. The name for the property is the parameter name,
                        # the type is given by kpi.ptype and the data resides in the object referenced by pref.
                        self.insertArrayDataProperty(props, kpi.pname, kpi.ptype, pref, False)
            elif tag == bG.sscalar:
                # Need to know if this scalar represents an immutable or not. If it does, we can't
                # change the type of the data.
                stype = elem.get(bG.selemType)
                self.insertEnumProperty(props, bG.selemType, 'vx_type_e', stype, end='VX_TYPE_REFERENCE')
                # Add data of the appropriate type
                if not xobj.isVirtual():
                    props.Append(wx.propgrid.PropertyCategory('Data'))
                    self.insertArrayDataProperty(props, 'data', stype, ref, False)
            elif tag == bG.sarray:
                self.insertUintProperty(props, bG.scapacity, elem, 1, 65536)
                self.insertEnumProperty(props, bG.selemType, 'vx_type_e', elem, end='VX_TYPE_REFERENCE')
                # Add data of the appropriate type
                if not xobj.isVirtual():
                    props.Append(wx.propgrid.PropertyCategory('Data'))
                    self.insertArrayDataProperty(props, 'data', elem.get(bG.selemType), ref)
            elif tag == bG.sroi:
                for attr in [bG.sstart_x, bG.send_x, bG.sstart_y, bG.send_y]:
                    self.insertUintProperty(props, attr, elem, 0, 8096)
            elif tag == bG.splane:
                self.insertEnumProperty(props, bG.schannel, 'vx_channel_e', elem)
            elif tag == bG.simage:
                self.insertUintProperty(props, bG.swidth, elem, 0, 8096)
                self.insertUintProperty(props, bG.sheight, elem, 0, 8096)
                self.insertEnumProperty(props, bG.sformat, 'vx_df_image_e', TypeDef.formatToId(elem.get(bG.sformat)))
                if not xobj.isVirtual():
                    pass # this is where we edit the data for this image
            elif tag == bG.spyramid:
                self.insertUintProperty(props, bG.slevels, elem, 1, 12)
                value = elem.get(bG.sscale)
                if nearEnough(value, 0.5):
                    value = 0
                else:
                    value = 1
                props.Append(wx.propgrid.EnumProperty(label=bG.sscale, name=bG.sscale,
                                                      labels=["VX_SCALE_PYRAMID_HALF", "VX_SCALE_PYRAMID_ORB"],
                                                      values=[0,1],
                                                      value=value))
                self.insertUintProperty(props, bG.swidth, elem, 0, 8096)
                self.insertUintProperty(props, bG.sheight, elem, 0, 8096)
                self.insertEnumProperty(props, bG.sformat, 'vx_df_image_e', TypeDef.formatToId(elem.get(bG.sformat)))
            elif tag == bG.sconvolution:
                for attr in [bG.scolumns, bG.srows, bG.sscale]:
                    self.insertUintProperty(props, attr, elem, 1)
                if not xobj.isVirtual():
                    self.insertMatrixProperties(props, elem, bG.sint16, 'Convolution', int(elem.get(bG.srows, '1')), int(elem.get(bG.scolumns, '1')))
            elif tag == bG.sdelay:
                self.insertUintProperty(props, bG.scount, elem, 1, 256)
            elif tag == bG.sdistribution:
                distBins = int(elem.get(bG.sbins, "256"))
                self.insertUintProperty(props, bG.sbins, distBins, 1)
                self.insertUintProperty(props, bG.soffset, elem)
                self.insertUintProperty(props, bG.srange, elem, 1)
                if not xobj.isVirtual():
                    self.insertListDataProperty(props, ref, bG.sfrequency, bG.sbin, distBins, 'Distribution')

            elif tag == bG.slut:
                lutCount = int(elem.get(bG.scount, "256"))
                self.insertUintProperty(props, bG.scount, lutCount, 1, 65536)
                lutType = elem.get(bG.selemType, bG.sVX_TYPE_UINT8)
                self.insertEnumPropertySubset(props, bG.selemType, ddefs.s_vx_type_e,
                                            lutType, [bG.sVX_TYPE_UINT8, 'VX_TYPE_INT16'])
                if not xobj.isVirtual():
                    self.insertListDataProperty(props, ref, TypeDef.tagFromEnum(lutType), bG.sindex, lutCount, 'LUT')

            elif tag == bG.smatrix:
                pattOther = 'VX_PATTERN_OTHER'
                matPatt = elem.get(bG.spattern, pattOther)
                matRows = int(elem.get(bG.srows))
                matCols = int(elem.get(bG.scolumns))
                matType = elem.get(bG.selemType, 'VX_TYPE_FLOAT32')
                matTag = TypeDef.tagFromEnum(matType)

                self.insertUintProperty(props, bG.scolumns, matCols, 1, 65536)
                self.insertUintProperty(props, bG.srows, matRows, 1, 65536)

                if matPatt == pattOther:
                    self.insertEnumPropertySubset(props, bG.selemType, ddefs.s_vx_type_e, matType,
                                                  [bG.sVX_TYPE_UINT8, 'VX_TYPE_INT32', 'VX_TYPE_FLOAT32'])
                if matType == bG.sVX_TYPE_UINT8:
                    self.insertEnumProperty(props, bG.spattern, 'vx_pattern_e', matPatt)
                    self.insertUintProperty(props, bG.sorigin_x, elem, max=matCols - 1)
                    self.insertUintProperty(props, bG.sorigin_y, elem, max=matRows - 1)

                if not xobj.isVirtual() and matPatt == pattOther:
                    self.insertMatrixProperties(props, elem, matTag, 'Matrix', matRows, matCols)

            elif tag == bG.sobject_array:
                self.insertUintProperty(props, bG.scount, elem, 1, 256)
            elif tag == bG.sremap:
                for name in [bG.ssrc_width, bG.ssrc_height, bG.sdst_width, bG.sdst_height]:
                    self.insertUintProperty(props, name, elem, 0, 8096)
                # Now the data. It is set per up to 16 items only increasing in the in the x direction most rapidly
                if not xobj.isVirtual():
                    remapData = {}
                    dstw = int(elem.get(bG.sdst_width, 16))
                    dsth = int(elem.get(bG.sdst_height, 16))
                    if not isinstance(xobj.datasize, dict):
                        xobj.datasize = dict(dst_x="0", dst_y="0")
                    dstx = int(xobj.datasize['dst_x'])
                    dsty = int(xobj.datasize['dst_y'])
                    self.insertUintProperty(props, 'dst_x', dstx, max=dstw - 1)
                    self.insertUintProperty(props, 'dst_y', dsty, max=dsth - 1)
                    keys = []
                    remapData = {}
                    for i in range(16):
                        # create lists of keys and map of default data
                        k = "[%d][%d]"%(dsty, dstx)
                        keys.append(k)
                        remapData[k] = (str(float(dsty)), str(float(dstx)))
                        dstx += 1
                        if dstx >= dstw:
                            dstx = 0
                            dsty += 1
                        if dsty >= dsth:
                            break
                    props.Append(wx.propgrid.PropertyCategory('Data: [y][x]pairs from the dst_y, dst_x values'))
                    # Find the data corresponding to the map
                    for child in list(elem):
                        k = "[%s][%s]"%(child.get('dst_y'), child.get('dst_x'))
                        if k in keys:
                            remapData[k] = (child.get('src_y'), child.get('src_x'))
                    for k in keys:
                        y, x = remapData[k]
                        self.insertFloatProperty(props, 'src_y' + k, y)
                        self.insertFloatProperty(props, 'src_x' + k, x)

            # elif tag == bG.sthreshold:
            elif tag == bG.stensor:
                self.insertUintProperty(props, bG.snumber_of_dims, elem, 1, 4)
                enumname = 'vx_type_e'
                self.insertEnumProperty(props, bG.sdata_type, enumname, elem, 
                                        start='VX_TYPE_INT8',
                                        end='VX_TYPE_BOOL',
                                        excl=['VX_TYPE_ENUM', 'VX_TYPE_SIZE', 'VX_TYPE_DF_IMAGE'])
                self.insertIntProperty(props, bG.sfixed_point_position, elem, -128, 127)
                props.Append(wx.propgrid.PropertyCategory('Dimension sizes'))
                for d in elem.iterchildren(etree.QName(elem, bG.sdimension).text):
                    self.insertUintProperty(props, "%s %s"%(bG.sdimension, d.get(bG.sindex)), d.get(bG.ssize))
                if not xobj.isVirtual():
                    pass # tensor data whatever
            # elif tag == bG.sview:
            elif tag == bG.sstruct:
                # User struct definition
                self.insertUintProperty(props, bG.ssize, elem, 1)
                self.insertStringProperty(props, 'identifier', elem.text)
            else:
                for attr in elem.attrib:
                    if attr not in {bG.sreference, bG.sname}:
                        self.insertStringProperty(props, attr, elem, True)


    def getMenuUpdateData(self):
        """
        Get data to update or create menus
        """
        withDelays = self.graph.name == bG.sroot
        tag = None
        if self.selectedObj is None:
            typeName = None
            withContainers = False
        else:
            xobj = Xref.get(self.selectedObj)
            tag = xobj.tag
            withContainers = (not xobj.isChild() and tag != bG.sdelay)
            if tag in [bG.sroi, bG.splane, bG.simage]:
                typeName = "vx_image"
                pimage = xobj.elem
                while pimage.get(bG.sformat) is None and pimage.get(bG.schannel) is None:
                    pimage = pimage.getparent()
                if pimage.get(bG.sformat) not in bG.imageChannelFormats:
                    tag = bG.splane             # Categorise the parent image format
            elif tag in [bG.sview, bG.stensor]:
                typeName = "vx_tensor"
            elif tag in bG.dataObjectTags:
                typeName = "vx_" + tag
            else:
                typeName = None
                withContainers = False
        return withContainers, typeName, withDelays, tag

    def updateMenus(self):
        """
        Update the menus according to current status
        """
        withContainers, typeName, withDelays, tag = self.getMenuUpdateData()
        self.topframe.GetMenuBar().FindItemById(const.ID_InsertMenuData).GetSubMenu().update(withContainers, typeName, withDelays, tag)
        self.topframe.GetMenuBar().FindItemById(const.ID_InsertMenuNode).Enable(not withDelays)
        self.topframe.GetMenuBar().FindItemById(const.ID_InsertMenuXNode).Enable(not withDelays)
        self.topframe.GetMenuBar().FindItemById(const.ID_EditMenuReplicate).Enable(tag == bG.snode)
        self.topframe.GetMenuBar().FindItemById(const.ID_EditMenuVirtual).Enable(tag in bG.dataObjectTags)
        self.topframe.GetMenuBar().FindItemById(const.ID_EditMenuConnect).Enable(tag is not None)
        self.topframe.GetMenuBar().FindItemById(const.ID_EditMenuRemoveObject).Enable(tag is not None)
        self.topframe.GetMenuBar().FindItemById(const.ID_EditMenuRemoveGraph).Enable(not withDelays)

    def contextMenu(self, control=False, shift=False, alt=False):
        """
        pop-up an appropriate context menu
        TODO
        """
        if not (control or shift or alt):
            self.insertNodeMenu()       # Insert standard node
        elif shift and not (control or alt):
            self.insertNodeMenu(True)   # Insert non-standard node
        elif control and not (shift or alt):
            self.insertDataMenu()
        else:
            pass    # deselect

    def insertNodeMenu(self, nonStandard=False):
        """
        pop-up appropriate insert Node menu
        """
        if self.graph.name == bG.globalsName:
            self.topframe.Error("Cannot insert node in %s; use a graph tab"%bG.globalsName)
        else:
            # TODO: make node menu appropriate for the selected object
            self.PopupMenu(XNodeMenu() if nonStandard else NodeMenu())

    def insertDataMenu(self):
        """
        pop-up insert data menu
        """
        self.PopupMenu(DataMenu(*self.getMenuUpdateData()))

    def Update(self, elemGraph):
        # Initialise the XML tree and graph:
        self.element, self.graph = elemGraph
        # Initialise attribute object
        self.attrObj = "None"
        # Initialise bitmap:
        self.Redraw()

    def InitPos(self):
        """
        Clear the selections
        (action on ESC key)
        """
        # Initialise selected object and rect
        self.selectedObj = None
        self.selectedRect = None
        # Up-mouse selection object and rect
        self.upObj = None
        self.upRect = None
        # Mouse action positions
        self.downPos = None
        self.dragPos = None

    def SelectNone(self):
        """
        Clear the selections and refresh
        (action on ESC key)
        """
        self.InitPos()
        self.Refresh()

    def getVisibleRect(self):
        """
        If the view start has a -ve coordinate, scroll so that
        it doesn't
        return the current visible rectangle in logical units
        """
        stx, sty = self.GetViewStart()
        stx = max(stx, 0)
        sty = max(sty, 0)
        self.Scroll((stx, sty))
        sz = self.GetClientSize()
        scale = self.parent.zoom
        ppu = self.GetScrollPixelsPerUnit()
        stx *= ppu[0]     # convert start to pixels
        sty *= ppu[1]
        stx = round(stx / scale)      # origin and size in bitmap units
        sty = round(sty / scale)
        szx = round(sz[0] / scale)
        szy = round(sz[1] / scale)
        return wx.Rect(stx, sty, szx, szy)
    
    def Move(self, test, isSel):
        """
        Change the selected object to the next one, using the given algorithm
        """
        nodes = self.graph.nodes()
        if isSel:
            sobj = self.upObj if self.selectedObj is None else self.selectedObj
        else:
            sobj = self.selectedObj if self.upObj is None else self.upObj
        if sobj is None:
            sobj = nodes[0] if len(nodes) > 0 else None
            if sobj is None:
                srect = None
            else:
                # Find most appropriate start node
                srect = self.BoundingRect(sobj)
                for n in nodes:
                    nrect = self.BoundingRect(n)
                    if not test(nrect, srect):
                        srect = nrect
                        sobj = n
        else:
            rect = self.BoundingRect(sobj)
            srect = rect
            rpos = rect.GetPosition()
            best = 1000000000000000
            for n in nodes:
                nrect = self.BoundingRect(n)
                ndiff = nrect.GetPosition() - rpos
                dist = ndiff.x * ndiff.x + ndiff.y * ndiff.y
                if test(nrect, rect) and dist < best:
                    best = dist
                    sobj = n
                    srect = nrect
        if sobj is not None:
            # Scroll if necessary to make sure object is visible
            self.ScrollToObj(sobj)
            if isSel:
                self.selectedRect = Large(srect)
                self.selectedObj = sobj
            else:
                self.upRect = Large(srect)
                self.upObj = sobj
            self.Refresh()

    def ScrollToObj(self, sobj):
        """
        Scroll if necessary to make sure object is visible
        """
        if sobj is not None:
            srect = self.BoundingRect(sobj)
            vrect = self.getVisibleRect()
            if not vrect.Contains(srect):
                ppu = self.GetScrollPixelsPerUnit()
                x, y = srect.GetPosition() + wx.Point(-100, -100)
                self.Scroll((x / ppu[0], y / ppu[1]))

    def MoveRight(self, isSel=True):
        """
        Change the selected object to the next one, using the "right" algorithm
        (picks the first found node to the right)
        """
        self.Move(lambda x, y: x.Left > y.Right, isSel)
    
    def MoveLeft(self, isSel=True):
        """
        Change the selected object to the next one, using the "left" algorithm
        """
        self.Move(lambda x, y: x.Right < y.Left, isSel)

    def MoveDown(self, isSel=True):
        """
        Change the selected object to the next one, using the "down" algorithm
        """
        self.Move(lambda x, y: x.Top > y.Bottom, isSel)

    def MoveUp(self, isSel=True):
        """
        Change the selected object to the next one, using the "up" algorithm
        """
        self.Move(lambda x, y: x.Bottom < y.Top, isSel)


    def ScrollSome(self, x, y):
        self.Scroll(self.GetViewStart() + wx.Point(x, y))

    def Redraw(self):
        '''
        Redraw the graph onto the bitmap, laying out.
        Also creates bounding boxes for each node of the graph:
        Note that coordinates obtained from the graph are in points,
        and the lower left corner is at (0,0)
        Width and height from the graph are in inches
        Graphs are drawn by dot assuming 96 DPI ("standard" screen resolution)
        There is (apparently) a margin of 4 pixels on the bitmap
        Required after modifications have been made.
        '''
        # Set the resolution
        dpi = 96        # dots per inch; always 96 for the screen
        # Assign positions and sizes to objects so we can select them
        self.graph.layout(prog='dot', args="-Grankdir=%s"%self.parent.rankdir)
        h, path = tempfile.mkstemp(suffix='.png')
        os.close(h)
        self.graph.draw(path)
        self.bitmap = wx.Bitmap(path)
        os.unlink(path)
        # Create bounding boxes in screen coordinates for each node
        ppi = 72.0          # points per inch
        ppp = dpi / ppi     # pixels per point
        margin = 4 * ppp    # Margin around the drawing
        for n in self.graph.nodes():
            width = n.attr['width']
            height = n.attr['height']
            pos = n.attr['pos']
            w = int(dpi * float(width) + 0.5)
            h = int(dpi * float(height) + 0.5)
            x, y = [int(float(p) * ppp + 0.5) + margin for p in pos.split(',')]
            y = self.bitmap.GetHeight() - y  # invert the y coordinate as lower left is at (0,0)
            # Now create the bounding rectangle of this object
            n.attr['brect'] = '%d,%d,%d,%d'%(x - w / 2, y - h / 2, w, h)
        # clear the 'dirty' flag in our graph:
        Xref.clearDirty(self.graph)
        # try and set the previously selected objects:
        if self.selectedObj is not None and self.graph.has_node(self.selectedObj):
            self.selectedObj = self.graph.get_node(self.selectedObj)
            self.selectedRect = self.LargeBoundingRect(self.selectedObj)
        else:
            self.selectedObj = None
            self.selectedRect = None
        if self.upObj is not None and self.graph.has_node(self.upObj):
            self.upObj = self.graph.get_node(self.upObj)
            self.upRect = self.LargeBoundingRect(self.upObj)
        else:
            self.upObj = None
            self.upRect = None
        self.ScrollToObj(self.upObj if self.selectedObj is None else self.selectedObj)

    
    def Write(self):
        """
        Write the current graph to a drawing file
        """
        filename = ""
        fd = wx.FileDialog(self, message="Select filename to save drawing", wildcard='Dot format(*.dot)|*.dot|'
                           'Compressed SVG format(*.svgz)|*.svgz|'
                           'Encapsulated postscript(*.eps)|*.eps|'
                           'GIF format(*.gif)|*.gif|'
                           'JPEG format(*.jpg)|*.jpg|'
                           'PIC format(*.pic)|*.pic|'
                           'PNG format(*.png)|*.png|'
                           'Portable document format(*.pdf)|*.pdf|'
                           'Postscript(*.ps)|*.ps|'
                           'Postscript for PDF(*.ps2)|*.ps2|'
                           'SVG format(*.svg)|*.svg|'
                           'Xfig format(*.fig)|*.fig|'
                           'All files(*.*|*.*', style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if fd.ShowModal() == wx.ID_OK:
            filename = fd.GetPath()
        if filename != "":
            try:
                self.graph.draw(filename, args="-Grankdir=%s -Gdpi=%s"%(self.parent.rankdir, self.parent.dpi))
            except:
                self.topframe.Error("Error writing to file '%s'"%filename, True)

    def LargeBoundingRect(self, obj):
        return Large(self.BoundingRect(obj))
        
    def BoundingRect(self, obj):
        return wx.Rect(*(int(i) for i in obj.attr['brect'].split(',')))

    def ObjAtPos(self, pos):
        '''
        Return a tuple of object at the given screen position, and the object's bounding rect
        If there is no object, return (None, None)
        '''
        for n in self.graph.nodes():
            # Now create the bounding rectangle of this object
            brect = self.LargeBoundingRect(n)
            if brect.Contains(pos):
                return (n, brect)
        return (None, None)

    def rightMouse(self, control, shift, alt):
        """
        Actions on right mouse up
        """
        pass

    def LeftMouse(self, control, shift, alt):
        '''
        Actions on left mouse up
        click on object -> select
        click on blank -> deselect
        ctrl-click on data object -> toggle virtual
        ctrl-click on node -> replicate
        alt-click on other object -> unassigned
        shift-click on data object -> unassigned
        shift-click on node -> add optional

        drag blank to node -> add optional
        drag data to data -> merge
        drag node to data, data to node -> add graph parameter or add optional

        drag object to blank -> diconnect / delete

        '''
        xup = Xref.get(self.upObj)
        if self.selectedObj is None:    # Click on blank screen
            if self.upObj is None:      # Release on blank screen
                pass    # deselect
            elif xup.tag == bG.snode:
                self.AddOptional(self.upObj)    # Add optional parameter to node
            else:
                # Drag from nowhere to a parameter or data object
                pass
        elif self.upObj is None:        # Drag from an object to nowhere
            # Drag from an object to nowhere >> remove object
            self.parent.RemoveObj()
        elif self.selectedObj == self.upObj:
            # Ctrl - toggle or replicate (for nodes)
            # Shift - Add optional (for nodes)
            # control-alt - rename
            if control and not shift and not alt:
                if xup.tag == bG.snode:
                    self.parent.Replicate()
                else:
                    self.parent.ToggleVirtual()
            elif shift and not control and not alt:
                if xup.tag == bG.snode:
                    self.AddOptional(self.upObj)    # Add optional parameter to node
                else:
                    pass
            else:
                pass                    # Click and release on same object - do nothing
        else:                           # Drag from one object to another
            # Add or merge a connection between nodes, data and nodes and data
            self.AddConnection(self.selectedObj, self.upObj)

    def AddConnection(self, source, sink):
        '''
        If source and sink are both nodes:
        Add a connection between an output or bidirectional parameter of source
        and an input of sink, if there are any compatible.
        Currently we process:
        From data to data
        From data to node
        From node to data
        '''
        self.topframe.Ready()
        fromTag = Xref.get(source).tag
        toTag = Xref.get(sink).tag
        
        if fromTag == bG.snode:
            if toTag in bG.dataObjectTags:
                self.connectDataNode(sink, source)
            else:
                pass    # Nothing to do
        elif fromTag in bG.dataObjectTags:
            if toTag in bG.dataObjectTags:
                self.parent.Save()
                if not self.connectDatas(source, sink):
                    self.parent.ScrapUndo()
            elif toTag == bG.snode:
                self.connectDataNode(source, sink)
            else:
                pass
        else:
            pass

    def isDescendant(self, elem, desc, seen=set()):
        """
        If a cycle is detected in the graph, log an error
        and return True
        If desc is a descendant of elem, return True
        Otherwise, return false
        """
        if elem == desc:
            return True
        if elem in seen:
            self.topframe.Error("Cycle detected in the graph!")
            return True
        for c in self.graph.successors(elem):
            if self.isDescendant(c, desc, seen | {elem}):
                return True
        return False
    
    def getWriter(self, dnode):
        """
        Find a node that writes to dnode, if any.
        The will be a 'node' in the predecessors of dnode
        """
        return Xref.get(dnode).writer

    def getReaders(self, dnode):
        """
        Return a set of all nodes that read from dnode, if any.
        The will be a 'node' in the successors of dnode
        """
        return Xref.get(dnode).readers

    def connectDataNode(self, source, sink):
        """
        If the data object is already connected to the node,
        and there is a graph parameter, nothing to do.
        If the data object is connected to the node and there is
        no graph parameter, insert a graph parameter between the
        data object and the node.
        Otherwise, if there is one unconnected optional parameter on
        the node of the right type and direction, connect to it.
        If there are more than one unconnected optional parameters on
        the node of the right type and direction, show a popup
        of the options, and connect to the chosen one.
        """
        source_neighbors = self.graph.neighbors(source)
        if sink in source_neighbors:
            self.insertGraphParameter(source, sink)
        else:
            # find if connected to this node or not
            # can only e via a graph parameter
            for nk in self.graph.neighbors_iter(sink):
                if nk in source_neighbors and Xref.get(nk).tag == bG.sparameter:
                    return self.topframe.Error("Nothing to do")
            # Can't be connectd.
            # Here to search for optional parameters on the node
            opts = bG.getOptionals(sink)
            wnode = self.getWriter(source)
            dtype = bG.getVxType(source)
            choices = []
            for o, kp in list(opts.items()):
                if kp.ptype == dtype and (kp.pdir == kdefs.kpInput or wnode is None):
                    choices.append("Index %d : %s (%s)"%(o, kp.pname, kp.pdir))
            if len(choices) == 0:
                return self.topframe.Error("There were no suitable optional parameters")
            if len(choices) > 1:
                # There is a choice
                choice = wx.GetSingleChoice("Please select from available optional parameters", "Select parameter to connect", choices)
            else:
                choice = choices[0]
            if choice == "":
                self.topframe.Error("Optional parameter connection was canceled")
            else:
                # OK to connect, so do it:
                o = int(choice.split(' ')[1])
                self.parent.Save()
                if not bG.connectDataNode(source, sink, opts[o], o):
                    self.parent.ScrapUndo()
    
    def AddOptional(self, dnode):
        opts = bG.getOptionals(dnode)
        choices = []
        for o, kp in list(opts.items()):
            choices.append("Parameter %d : %s (%s)"%(o, kp.pname, kp.pdir))
        if len(choices) == 0:
            return self.topframe.Error("There were no suitable optional parameters")
        if len(choices) > 1:
            # There is a choice
            choiceDlg = wx.MultiChoiceDialog(self, "Select available optional parameters to connect",
                                            "Optional parameters", choices)
            if choiceDlg.ShowModal() == wx.ID_OK:
                selections = choiceDlg.GetSelections()
        else:
            selections = [0]
        if selections == []:
            self.topframe.Error("Optional parameter connection was canceled")
        else:
            self.parent.Save()
            for choice in selections:
                # OK to connect, so do it:
                o = int(choices[choice].split(' ')[1])
                if not bG.addOptional(self.element, self.graph, dnode, opts, o):
                    self.parent.Undo()
                    break

    def connectDatas(self, source, sink):
        '''
        Merge two data objects if they are compatible
        This function returns False on failure.
        Handling of Save must be done at a higher level.
        '''
        xsource = Xref.get(source)
        xsink = Xref.get(sink)
        # First check. Cannot merge if both elements have writers

        fromWriter = self.getWriter(source)
        toWriter = self.getWriter(sink)
        if xsource.writer is not None and xsink.writer is not None:
            return self.topframe.Error("Cannot merge data objects when both are outputs")
        # Now let's simplify things by making the one written to (if any) the source:
        if xsink.writer is not None:
            source, sink, xsource, xsink = sink, source, xsink, xsource
        # Second check. Cannot merge if writer is a successor of the sink
        if fromWriter is not None and self.isDescendant(sink, fromWriter):
            return self.topframe.Error("Cannot merge data objects as it would create a cycle")
        
        fromTag = xsource.tag
        toTag = xsink.tag
        fromElem = xsource.elem
        toElem = xsink.elem
        imagetags = {bG.sroi, bG.splane, bG.simage}
        imagechildtags = {bG.sroi, bG.splane}
        # If the tags match that's a good start
        if fromTag == toTag or fromTag in imagetags and toTag in imagetags:
            # Now check attribute matching
            # Make maps of non-matching attributes
            nomatch = {}
            frimage = fromElem
            timage = toElem
            if fromTag in imagechildtags:
                while bG.sformat not in list(frimage.keys()):
                    frimage = frimage.getparent()
            elif toTag in imagechildtags:
                while bG.sformat not in list(timage.keys()):
                    timage = timage.getparent()
            # pick up nomatch and missingTo items
            for attr, fval in list(frimage.items()):
                # ignore 'name' and 'reference' as they should always differ
                if attr not in [bG.sname, bG.sreference]:
                    tval = timage.get(attr)
                    if fval != tval:
                        nomatch[attr] = (fval, tval)
            # We hand off the task of matching attributes to the bG function
            return bG.mergeToVirtual(self.element, self.graph, source, sink, fromWriter, nomatch)
        elif fromTag == bG.svx_reference:
            # Here we can merge two objects because one of them is a reference
            bG.convertReferenceTo(source, sink)
            return self.connectDatas(source, sink)
        elif toTag == bG.svx_reference:
            bG.convertReferenceTo(sink, source)
            return self.connectDatas(source, sink)
        else:
            return self.topframe.Error("Data objects are not compatible")
        return True
        

    def insertNode(self, kernel):
        """
        Inserts a new node for the given kernel.
        Handles saving of data from undo.
        """
        if self.graph.name == bG.globalsName:
            self.topframe.Error("Cannot insert node in %s; use a graph tab"%bG.globalsName)
        else:
            self.parent.Save()
            bG.insertNode(self.element, self.graph, kernel)

    def insertGraphParameter(self, obj, node=None):
        """
        obj is a data object
        node is an OpenVX node, or None. If it's not None, it must be connected to obj.
        this function won't insert multiple graph parameters and won't insert one at all unless
        either there is one writer or one consumer of the data.
        Otherwise a graph parameter is inserted for the first connected node that is found
        """
        if Xref.get(obj).tag not in bG.dataObjectTags:
            return self.topframe.Error("Must select a data object to insert a graph parameter")
        if Xref.get(obj).isImmutable():
            return self.topframe.Error("Cannot make immutable data a graph parameter")
        # find the first connected snode
        if node is None:
            for n in self.graph.neighbors_iter(obj):
                if Xref.get(n).tag == bG.snode:
                    node = n
                    break
        if node is None:
            return self.topframe.Error("Object must be an input or an output of a node.")
        elif node not in self.graph.neighbors(obj):
            return self.topframe.Error("Second selected object must be a directly connected node.")
        # We've done the checks, hand off to bG to do the work. We may have to rebuild:
        self.parent.Save()
        if not bG.insertGraphParameter(self.element, self.graph, obj, node):
            self.parent.ScrapUndo()

    def removeNode(self, obj):
        """
        Disconnect / remove node.
        Find all the connections of a node and remove them.
        If all the connections were to virtual objects or immutable connected only to this node,
        remove the node together with those objects.
        """
        nelem = Xref.get(obj).elem
        paramtag = etree.QName(self.element, bG.sparameter).text
        changes = 0
        # First, remove graph parameters:
        pIndex = 0  # for re-numbering
        for gp in self.element.iterchildren(paramtag):
            if gp.attrib[bG.snode] == obj:
                self.element.remove(gp)
                changes += 1
            else:
                gp.attrib[bG.sindex] = str(pIndex)  # renumber other graph parameters
                pIndex += 1

        # Now, remove node parameters that are connected to other things.
        # What we don't remove are parameters for virtuals that have only one neighbor.
        # We also build up a set of potentially orphaned virtual data objects
        vSet = set()
        for np in nelem.iterchildren(paramtag):
            pref = np.attrib[bG.sreference]
            xObj = Xref.get(pref)
            if xObj.elem.getparent() == self.element:
                # This is virtual
                # is degree of the parameter > 1?
                degree = 0
                for npr in self.element.iterdescendants(paramtag):
                    if npr.get(bG.sreference) == pref:
                        degree += 1
                        if degree > 1:
                            break
                if degree > 1:
                    nelem.remove(np)
                    changes += 1
                else:
                    vSet.add(xObj.elem)
            elif xObj.isImmutable():
                nelem.remove(np)
                if len(xObj.readers) == 1:
                    xObj.elem.getparent().remove(xObj.elem)
            else:
                # Non-virtual mutable
                nelem.remove(np)
                changes += 1
        # Now see if we need to delete the node or not
        if changes == 0:
            # We've done nothing so far, so we must delete the node
            # and all the virtual data objects
            self.element.remove(nelem)
            for vobj in vSet:   # Remove the (now orphaned) virtual data
                self.element.remove(vobj)
        else:
            # The node has been disconnected, therefore it can no longer be replicated
            nelem.attrib[bG.sis_replicated] = bG.sfalse
        Xref.setDirty()

    def removeGraphParameter(self, obj):
        """
        Remove a graph parameter.
        If the bG function returns false, we have to redbuild.
        """
        self.parent.Save()
        if not bG.removeGraphParameter(self.element, self.graph, obj):
            self.parent.ScrapUndo()

    def removeData(self, obj):
        """
        Disconnect or remove a data object.
        Remove all references to it and its children on nodes, including associated graph parameters.
        If there were no references, remove the data object unless it was a child.
        If the object is virtual and not a child, we leave it connected to a single node to avoid
        possible needless rebuilding.
        Return True if something was changed, False otherwise
        """
        ref = str(obj)
        xobj = Xref.get(ref)
        isChild = xobj.isChild() and xobj.tag not in {bG.sroi, bG.sview, bG.splane}
        isVirtual = xobj.isVirtual()
        elem = xobj.elem
        # Now go looking for graph parameters that reference this object, over
        # the entire xml tree. First, build a set of references for the object
        # and all it's dataObject children:
        refs = {ref}
        for child in elem.iterdescendants():
            if etree.QName(child).localname in bG.dataObjectTags:
                refs.add(child.attrib[bG.sreference])
        # Now we iterate over all graphs looking for a parameters that reference
        # an object we have in the set:
        root = Xref.getroot().elem
        graphtag = etree.QName(root, bG.sgraph).text
        paramtag = etree.QName(root, bG.sparameter).text
        nodetag = etree.QName(root, bG.snode).text
        changes = 0
        hadOne = isChild or not isVirtual
        for g in root.iterchildren(graphtag):           # check all the graphs
            params = set() # The parameters we have found
            for n in g.iterchildren(nodetag):
                kps = bG.getKernelInfo(n).params
                nref = n.attrib[bG.sreference]
                for p in n.iterchildren(paramtag):
                    pref = p.attrib[bG.sreference]
                    if pref in refs:
                        params.add((p.attrib[bG.sindex], nref))
                        if pref != ref or hadOne or kps[int(p.attrib[bG.sindex])].pstate == kdefs.kpOptional:
                            n.remove(p)
                            changes += 1
                        elif pref == ref:
                            hadOne = True
            pIndex = 0                                  # for re-numbering graph parameters
            for gp in g.iterchildren(paramtag):         # check all graph parameters
                affected = False                        # we'll set this True if this parameter is affected
                if (gp.attrib[bG.sparameter], gp.attrib[bG.snode]) in params:
                    g.remove(gp)                        # remove the graph parameter
                    changes += 1
                else:
                    gp.attrib[bG.sindex] = str(pIndex)  # renumber other graph parameters
                    pIndex += 1

        # here to see if we have disconnected anything - if not, we'll proceed as delete
        if changes == 0:
            if isChild:
                return self.topframe.Error("Cannot delete child objects - change number of elements in parent")
            elif hadOne and isVirtual:
                return self.topframe.Error("Nothing to do")
            else:
                elem.getparent().remove(elem)
        Xref.setDirty()
        return True
        
