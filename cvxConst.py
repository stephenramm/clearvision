"""
Global constants for the ClearVision application are all declared in
self.__init__ and cannot be modified elsewhere.

"""

import wx

# Basic constants
class Const(object):
    """
    Allow creation of constants, i.e. attributes that can't be re-bound.

    Any attempt to re-bind or delete attributes will result in an exception.
    All the constants for the application should be declared here.
    Any attempt to introduce new constants after self.__init__() will result in
    an exception.
    """

    class ConstError(TypeError):
        """Type of exception that will be raised if there is an attempt to
        modify a const"""

        pass

    def __setattr__(self, name, value):
        """Only allow attribute to be set if it does not exist, and then only
        in __init__; otherwise raise an exception"""
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const(%s)." % name)
        elif "__no_more_attributes__" in self.__dict__:
            raise self.ConstError("Can't bind const(%s);" \
                " Place new constants in _self.__init__ in %s module." % \
                (name, __name__))
        self.__dict__[name] = value

    def __delattr__(self, name):
        """Do not allow attributes to be deleted"""
        if name in self.__dict__:
            raise self.ConstError("Can't unbind const(%s)" % name)
        raise NameError(name)

    def __init__(self):
        """
        This is where all constants are defined

        Calls methods to set up each constant category, then inhibits further
        constants from being defined
        """
        self.OtherConstants()   # Types of constants separated out for clarity
        self.StatusBarConstants()
        self.MenuIdConstants()

        self.__no_more_attributes__ = True
        # will cause an exception to be raised if more attributes are added.

    def OtherConstants(self):
        """
        Constants not falling in other categories

        """

    def StatusBarConstants(self):
        """
        Constants to do with the status bar

        Status bar fields:
        SBF_Context         context help
        SBF_Filename        name of current file
        """
        self.SBF_Context = 0       # Status bar field for context help
        self.SBF_Filename = 1      # Status bar field for name of current file

    def MenuIdConstants(self):
        """Set up all the Menu Id constants"""
        self.FileMenuIds()
        self.EditMenuIds()
        self.InsertMenuIds()
        self.GraphMenuIds()
        self.ViewMenuIds()
        self.HelpMenuIds()
        # Reserve 1000 ids for Nodes
        self.ID_InsertNode = wx.NewId()
        for i in range(499):
            wx.NewId()
        self.ID_InsertXNode = wx.NewId()
        for i in range(499):
            wx.NewId()

    def FileMenuIds(self):
        """File menu constants"""
        self.ID_FileMenuSave = wx.NewId()
        self.ID_FileMenuSaveAs = wx.NewId()
        self.ID_FileMenuOpenFile = wx.NewId()
        self.ID_FileMenuRevert = wx.NewId()
        self.ID_FileMenuClose = wx.NewId()
        self.ID_FileMenuLoadLibrary = wx.NewId()
        self.ID_FileMenuLoadObjects = wx.NewId()
        self.ID_FileMenuLoadNN = wx.NewId()
        self.ID_FileMenuQuit = wx.ID_EXIT

    def EditMenuIds(self):
        """Edit Menu constants"""
        self.ID_EditMenuUndo = wx.NewId()
        self.ID_EditMenuRedo = wx.NewId()
        self.ID_EditMenuCopy = wx.NewId()
        self.ID_EditMenuPaste = wx.NewId()
        self.ID_EditMenuConnect = wx.NewId()
        self.ID_EditMenuRemoveObject = wx.NewId()
        self.ID_EditMenuRemoveGraph = wx.NewId()
        self.ID_EditMenuVirtual = wx.NewId()
        self.ID_EditMenuReplicate = wx.NewId()
        self.ID_EditMenuClear = wx.NewId()
        self.ID_EditMenuPreferences = wx.NewId()

    def InsertMenuIds(self):
        """Insert menu constants"""
        self.ID_InsertMenuGraph = wx.NewId()
        self.ID_InsertMenuNode = wx.NewId()
        self.ID_InsertMenuXNode = wx.NewId()
        self.ID_InsertMenuData = wx.NewId()
        self.ID_InsertMenuDataArray = wx.NewId()
        self.ID_InsertMenuDataConvolution = wx.NewId()
        self.ID_InsertMenuDataDistribution = wx.NewId()
        self.ID_InsertMenuDataDelay = wx.NewId()
        self.ID_InsertMenuDataDelayOfSelected = wx.NewId()
        self.ID_InsertMenuDataImage = wx.NewId()
        self.ID_InsertMenuDataLut = wx.NewId()
        self.ID_InsertMenuDataMatrix = wx.NewId()
        self.ID_InsertMenuDataObjectArray = wx.NewId()
        self.ID_InsertMenuDataPyramid = wx.NewId()
        self.ID_InsertMenuDataObjectArrayOfSelected = wx.NewId()
        self.ID_InsertMenuDataObjectArrayFromTensor = wx.NewId()
        self.ID_InsertMenuDataPyramidOfSelected = wx.NewId()
        self.ID_InsertMenuDataRemap = wx.NewId()
        self.ID_InsertMenuDataScalar = wx.NewId()
        self.ID_InsertMenuDataThreshold = wx.NewId()
        self.ID_InsertMenuDataTensor = wx.NewId()
        self.ID_InsertMenuDataROI = wx.NewId()
        self.ID_InsertMenuDataChannel = wx.NewId()
        self.ID_InsertMenuDataView = wx.NewId()
        self.ID_InsertMenuDataFirst = self.ID_InsertMenuDataArray
        self.ID_InsertMenuDataLast = self.ID_InsertMenuDataView

    def GraphMenuIds(self):
        """Graph Menu constants"""
        self.ID_GraphMenuAttach = wx.NewId()
        self.ID_GraphMenuVerify = wx.NewId()
        self.ID_GraphMenuExecute = wx.NewId()
        self.ID_GraphMenuExport = wx.NewId()

    def ViewMenuIds(self):
        self.ID_ViewMenuShowVirtuals = wx.NewId()
        self.ID_ViewMenuZoomIn = wx.NewId()
        self.ID_ViewMenuZoomOut = wx.NewId()
        self.ID_ViewMenuZoomNormal = wx.NewId()
        self.ID_ViewMenuProperties = wx.NewId()
        self.ID_ViewMenuData = wx.NewId()
        self.ID_ViewMenuLog = wx.NewId()
        self.ID_ViewMenuNext = wx.NewId()
        self.ID_ViewMenuPrevious = wx.NewId()
        self.ID_ViewMenuSave = wx.NewId()
        self.ID_ViewMenuTB = wx.NewId()
        self.ID_ViewMenuBT = wx.NewId()
        self.ID_ViewMenuLR = wx.NewId()
        self.ID_ViewMenuRL = wx.NewId()
        self.ID_ViewMenu96DPI = wx.NewId()
        self.ID_ViewMenu100DPI = wx.NewId()
        self.ID_ViewMenu200DPI = wx.NewId()
        self.ID_ViewMenu300DPI = wx.NewId()
        self.ID_ViewMenu600DPI = wx.NewId()
        self.ID_ViewMenu1200DPI = wx.NewId()
        self.ID_ViewMenuLowDPI = self.ID_ViewMenu96DPI
        self.ID_ViewMenuHighDPI = self.ID_ViewMenu1200DPI

    def HelpMenuIds(self):
        """Help Menu Constants"""
        self.ID_HelpMenuKeyStrokes = wx.NewId()
        self.ID_HelpMenuHelp = wx.NewId()
        self.ID_HelpMenuAbout = wx.NewId()
        self.ID_HelpMenuTest = wx.NewId()

const = Const()
"""Only one Const should ever be created"""
