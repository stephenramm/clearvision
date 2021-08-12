"""
Menus

This module implements stuff to do with menus
Note: requires wxPython Phoenix
"""
import wx
from cvxKernelDefs import KernelDef
from cvxXML import splane
from cvxConst import const

class FileMenu(wx.Menu):
    """Creates a file Menu"""

    def __init__(self):
        wx.Menu.__init__(self)
        self.Append(const.ID_FileMenuSave,
                    "&Save\tCtrl-S",
                    "Save the current drawing")
        self.Append(const.ID_FileMenuSaveAs,
                    "Save &As...\tCtrl-Shift-S",
                    "Save the current drawing with a new name")
        self.Append(const.ID_FileMenuOpenFile,
                    "Open &File...\tCtrl-O",
                    "Open a ClearVision drawing file or an OpenVX Graph file")
        self.Append(const.ID_FileMenuRevert,
                    "&Revert\tCtrl-R",
                    "Discard all changes and re-open the current file")
        self.Append(const.ID_FileMenuClose,
                    "&Close\tCtrl-W",
                    "Close the current drawing and show a blank tab")
        self.Append(const.ID_FileMenuQuit,
                    "&Quit\tCtrl-Q",
                    "Close all files and quit the program")
        self.Enable(const.ID_FileMenuRevert, False)
        self.Enable(const.ID_FileMenuSave, False)
        self.Enable(const.ID_FileMenuClose, False)

class EditMenu(wx.Menu):
    """Creates an edit menu"""

    def __init__(self):
        wx.Menu.__init__(self)
        self.Append(const.ID_EditMenuUndo,
                    "&Undo\tCtrl-Z",
                    "Undo the last operation")
        self.Append(const.ID_EditMenuRedo,
                    "&Redo\tCtrl-Y",
                    "Redo the last undone operation")
        self.Append(const.ID_EditMenuConnect,
                    "&Connect/merge\talt-C",
                    "Connect or merge the selected objects")
        self.Append(const.ID_EditMenuRemoveObject,
                    "&Disconnect/Delete\tDEL",
                    "Disconnect the selected object, or delete if not connected")
        self.Append(const.ID_EditMenuRemoveGraph,
                    "&Remove graph\tCtrl-DEL",
                    "Delete the current graph tab")
        self.Append(const.ID_EditMenuClear,
                    "Clear All\tShift-DEL",
                    "Delete all objects and connections on all tabs")
        self.Append(const.ID_EditMenuVirtual,
                    "&Toggle Global\talt-T",
                    "Toggle the global/local (virtual) property of a data object")
        self.Append(const.ID_EditMenuReplicate,
                    "&Node replication...\talt-R",
                    "Control the replication of nodes")
        self.Append(const.ID_EditMenuPreferences,
                    "&Options...\tAlt-O",
                    "Set global options using the options dialog")
        self.Enable(const.ID_EditMenuUndo, False)
        self.Enable(const.ID_EditMenuRedo, False)

class InsertMenu(wx.Menu):
    """Creates an insert menu"""

    def __init__(self):
        wx.Menu.__init__(self)
        self.Append(const.ID_InsertMenuNode,
                        "Standard &Node",
                        NodeMenu(),
                        "Insert a standard OpenVX processing node")
        self.Append(const.ID_InsertMenuXNode,
                        "E&xtension Node",
                        XNodeMenu(),
                        "Insert a vendor or user-defined OpenVX processing node")
        self.Append(const.ID_InsertMenuData,
                        "&Data Object",
                        DataMenu(),
                        "Insert a standard OpenVX data object or graph edge")
        self.Append(const.ID_InsertMenuGraph,
                        "&Graph\talt-INSERT",
                        "Insert a new tab for a graph")

class GraphMenu(wx.Menu):
    """Creates a graph menu"""

    def __init__(self):
        wx.Menu.__init__(self)
        self.Append(const.ID_GraphMenuAttach, "&Attach...\t",
                    "Attach to an OpenVX implementation")
        self.Append(const.ID_GraphMenuVerify, "&Verify\t",
                    "Verify the OpenVX graph")
        self.Append(const.ID_GraphMenuExecute, "E&xecute\t",
                    "Execute the OpenVX graph")
        self.Append(const.ID_GraphMenuExport, "&Export...\t",
                    "Export the OpenVX graph")

class ViewMenu(wx.Menu):
    """ Creates a View Menu """
    def __init__(self):
        wx.Menu.__init__(self)
        self.AppendCheckItem(const.ID_ViewMenuShowVirtuals, "&Show connected data objects\tctrl-alt-c",
                    "Always show data objects connected between OpenVX nodes")
        self.Check(const.ID_ViewMenuShowVirtuals, False)
        self.AppendCheckItem(const.ID_ViewMenuProperties, "&Properties\talt-P",
                    "Show the properties pane to view and edit properties of the selected object")
        self.Check(const.ID_ViewMenuProperties, True)
        self.AppendCheckItem(const.ID_ViewMenuLog, "&Log\talt-L",
                    "Show the log pane to see output messages")
        self.Check(const.ID_ViewMenuLog, False)
        self.Append(const.ID_ViewMenuNext, "Switch to &next tab\tctrl-t",
                    "Switch to the next tab")
        self.Append(const.ID_ViewMenuPrevious, "Switch to &previous tab\tctrl-shift-t",
                    "Switch to the previous tab")
        self.Append(const.ID_ViewMenuData,
                    "Displa&y Data...\talt-D",
                    "Display the data of the selected object")
        self.AppendSeparator()
        self.Append(const.ID_ViewMenuZoomIn, "Zoom &In\tctrl-+",
                    "Make things larger")
        self.Append(const.ID_ViewMenuZoomOut, "Zoom &Out\tctrl+-",
                    "Make things smaller")
        self.Append(const.ID_ViewMenuZoomNormal, "&Zoom 100%\tctrl+=",
                    "Make things the normal size")
        self.AppendSeparator()
        submenu = wx.Menu()
        submenu.AppendRadioItem(const.ID_ViewMenu96DPI, "&96 DPI",
                    "Set DPI for a typical screen")
        submenu.AppendRadioItem(const.ID_ViewMenu200DPI, "&200 DPI",
                    "Set DPI for low quality printer output")
        submenu.AppendRadioItem(const.ID_ViewMenu300DPI, "&300 DPI",
                    "Set DPI for draft printer output")
        submenu.AppendRadioItem(const.ID_ViewMenu600DPI, "&600 DPI",
                    "Set DPI for presentation printer output (slow)")
        submenu.AppendRadioItem(const.ID_ViewMenu1200DPI, "&1200 DPI",
                    "Set DPI for high resolution printer output (very slow)")
        submenu.Check(const.ID_ViewMenu96DPI, True)
        self.AppendSubMenu(submenu, "Set &DPI for file output...",
                    "Set resolution of output picture files" )
        self.Append(const.ID_ViewMenuSave, "Sa&ve the current drawing...\tctrl-P",
                    "Write the current drawing out to a file of your choice")
        self.AppendSeparator()
        self.AppendRadioItem(const.ID_ViewMenuTB, "&TB orientation\tctrl-alt-t",
                    "Draw graphs from top to bottom")
        self.AppendRadioItem(const.ID_ViewMenuBT, "&BT orientation\tctrl-alt-b",
                    "Draw graphs from bottom to top")
        self.AppendRadioItem(const.ID_ViewMenuLR, "&LR orientation\tctrl-alt-l",
                    "Draw graphs from left to right")
        self.AppendRadioItem(const.ID_ViewMenuRL, "&RL orientation\tctrl-alt-r",
                    "Draw graphs from right to left")
        self.Check(const.ID_ViewMenuTB, True)
        

class HelpMenu(wx.Menu):
    """Creates a help menu"""

    def __init__(self):
        wx.Menu.__init__(self)
        self.Append(const.ID_HelpMenuKeyStrokes,
                    "&Keystrokes...\tCtrl-K",
                    "Show list of short-cut keystrokes")
        self.Append(const.ID_HelpMenuHelp,
                    "&Help...\tCtrl-H",
                    "Show Help")
        self.Append(const.ID_HelpMenuAbout,
                    "&About...\tCtrl-Alt-H",
                    "Show About Dialog")
        self.Append(const.ID_HelpMenuTest,
                    "&Test\tshift-Ctrl-Alt-T",
                    "Run tests")

class MenuBar(wx.MenuBar):
    """Creates a menubar"""

    def __init__(self):
        wx.MenuBar.__init__(self)
        self.Append(FileMenu(), "&File")
        self.Append(EditMenu(), "&Edit")
        self.Append(InsertMenu(), "&Insert")
        self.Append(GraphMenu(), "&Graph")
        self.Append(ViewMenu(), "&View")
        self.Append(HelpMenu(), "&Help")

class NodeMenu(wx.Menu):
    """
    Creates an insert node menu,
    by reading the kernel data.
    """
    def __init__(self):
        wx.Menu.__init__(self)
        i = 0
        names = list(KernelDef.keys())
        names.sort()
        for name in names:
            self.Append(i + const.ID_InsertNode, "&" + name.rpartition('org.khronos.openvx.')[2])
            i += 1
            if (i % 25 == 0):
                self.AppendSeparator()
                self.Break()

class XNodeMenu(wx.Menu):
    """
    Creates an insert node menu,
    now deprecated.
    """
    def __init__(self):
        wx.Menu.__init__(self)

class DataMenu(wx.Menu):
    """
    Creates an insert data menu for general use
    """
    def __init__(self, withContainers=False, typeName=None, withDelays=True, tag=None):
        wx.Menu.__init__(self)
        self.Append(const.ID_InsertMenuDataArray,
                    "&Array",
                    "Insert an Array object")
        self.Append(const.ID_InsertMenuDataConvolution,
                    "&Convolution",
                    "Insert a Convolution data object")
        self.Append(const.ID_InsertMenuDataDelay,
                    "&Delay",
                    "Insert a Delay object")
        self.Append(const.ID_InsertMenuDataDistribution,
                    "&Distribution",
                    "Insert a Distribution object")
        self.Append(const.ID_InsertMenuDataImage,
                    "&Image",
                    "Insert an Image")
        self.Append(const.ID_InsertMenuDataLut,
                    "&LUT",
                    "Insert a Look-up table")
        self.Append(const.ID_InsertMenuDataMatrix,
                    "&Matrix",
                    "Insert a Matrix object")
        self.Append(const.ID_InsertMenuDataObjectArray,
                    "&Object Array",
                    "Insert an Array of OpenVX Data Objects")
        self.Append(const.ID_InsertMenuDataPyramid,
                    "&Pyramid",
                    "Insert a Pyramid of Images")
        self.Append(const.ID_InsertMenuDataRemap,
                    "&Remap",
                    "Insert a Remap object")
        self.Append(const.ID_InsertMenuDataScalar,
                    "&Scalar",
                    "Insert a Scalar object")
        self.Append(const.ID_InsertMenuDataTensor,
                    "&Tensor",
                    "Insert a Tensor object")
        self.Append(const.ID_InsertMenuDataThreshold,
                    "&Threshold",
                    "Insert a Threshold object")
        self.Append(const.ID_InsertMenuDataDelayOfSelected,
                    "&Delay of selected object",
                    "Insert a delay with the selected  object as the first element")
        self.Append(const.ID_InsertMenuDataObjectArrayOfSelected,
                    "&Object array of selected object",
                    "Insert an object array with the selected object as the first element")
        self.Append(const.ID_InsertMenuDataPyramidOfSelected,
                    "&Pyramid of selected image",
                    "Insert a pyramid with the selected vx_image object as the first level")
        self.Append(const.ID_InsertMenuDataROI,
                    "&ROI of selected image",
                    "Insert a region of interest object as a child of the selected vx_image")
        self.Append(const.ID_InsertMenuDataChannel,
                    "&Channel of selected image",
                    "Insert an image object extracted from a channel of the selected vx_image")
        self.Append(const.ID_InsertMenuDataObjectArrayFromTensor,
                    "&Image Object Array of selected tensor",
                    "Insert an object array of vx_image objects derived from the selected tensor")
        self.Append(const.ID_InsertMenuDataView,
                    "&View of selected tensor",
                    "Create a tensor object that is a view of the selected vx_tensor")
        self.update(withContainers, typeName, withDelays, tag)
    
    def update(self, withContainers=False, typeName=None, withDelays=True, tag=None):
        """
        Enable/disbale menu items and update text
        """
        isImage = typeName == "vx_image"
        isTensor = typeName == "vx_tensor"
        if typeName is not None:
            self.SetLabel(const.ID_InsertMenuDataDelayOfSelected, "&Delay of selected %s object"%typeName)
            self.SetHelpString(const.ID_InsertMenuDataDelayOfSelected,
                               "Insert a delay with the selected %s object as the first element"%typeName)
            self.SetLabel(const.ID_InsertMenuDataObjectArrayOfSelected, "&Object array of selected %s object"%typeName)
            self.SetHelpString(const.ID_InsertMenuDataObjectArrayOfSelected,
                               "Insert an object array with the selected %s object as the first element"%typeName)
        self.Enable(const.ID_InsertMenuDataDelayOfSelected, withContainers and withDelays)
        self.Enable(const.ID_InsertMenuDataObjectArrayOfSelected, withContainers and typeName != "vx_object_array")
        self.Enable(const.ID_InsertMenuDataPyramidOfSelected, isImage and withContainers)
        self.Enable(const.ID_InsertMenuDataROI, isImage)
        self.Enable(const.ID_InsertMenuDataChannel, isImage and tag != splane)
        self.Enable(const.ID_InsertMenuDataObjectArrayFromTensor, isTensor)
        self.Enable(const.ID_InsertMenuDataView, isTensor)
        self.Enable(const.ID_InsertMenuDataDelay, withDelays)
