"""
MainFrame for Clearvision.
Note that this module now requires wxPython Phoenix (i.e. version 4)
"""
import wx.aui
import wx.propgrid
from lxml import etree
from cvxConst import const
# Menus
from cvxMenus import MenuBar
# drawing area
from cvxTabs import DrawPanel, Notebook
# debug
from cvxtestobject import Test
from cvxXML import fixupReferences
# from wx.lib import imageutils, msgpanel
# ----------------------------------------------------------------------


class MainFrame(wx.Frame):
    """
    The class for the ClearVision Main Frame.

    Inherits from wx.Frame and uses wx.aui.AuiManager to manage the frame.
    Member variables:
        statusbar      wx.StatusBar    The statusbar
        filename       String          The name of the file being edited

    TODO:
    Update filename in status bar
    """

    def __init__(self, parent, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE |
                 wx.SUNKEN_BORDER | wx.CLIP_CHILDREN):
        """
        Initialise the MainFrame

        parent  wx.Window or None   Parent of this window
        id      integer             id of this window
        title   String              caption for this window
        pos     wx.Point            position of this window
        size    wx.Size             size of the window
        style   Integer             window style
        """
        wx.Frame.__init__(self, parent, wx.ID_ANY, "ClearVision", pos, size,
                          style)

        # tell FrameManager to manage this frame
        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)

        # Some class variables
        self.filename = ""        # Until we save or load, there is no filename
        
        # create menubar
        self.SetMenuBar(MenuBar())

        # create statusbar
        self.statusbar = self.MakeStatusBar()

        # min size for the frame itself isn't completely done.
        # see the end up FrameManager::Update() for the test
        # code. For now, just hard code a frame minimum size
        self.SetMinSize(wx.Size(400, 300))

        # Add the notebook pane that holds the drawing area
        self.nb = Notebook(self)
        self._mgr.AddPane(self.nb,
                          wx.aui.AuiPaneInfo().
                          Name("Notebook").
                          Center().
                          CloseButton(False).
                          CaptionVisible(False))

        # Add a text pane and set up as a log control
        log_ctrl = wx.TextCtrl(self,
                               style=wx.TE_MULTILINE | wx.TE_READONLY,
                               size=wx.Size(10, 100))
        log = wx.LogTextCtrl(log_ctrl)
        self._mgr.AddPane(log_ctrl,
                          wx.aui.AuiPaneInfo().
                          Name("Log").
                          Caption("Log Pane").
                          Bottom().
                          Layer(1).
                          Position(1).
                          CloseButton(False).
                          MaximizeButton(True))
        wx.Log.SetActiveTarget(log)
        # self.nb.AddPage(log_ctrl, "Log")
        self._mgr.GetPane("Log").Hide()

        # Add a grid that will be the properties page
        self.properties = wx.propgrid.PropertyGrid(self, size=wx.Size(250, 50))

        # self.properties.CreateGrid(1, 1)
        # self.properties.SetColLabelSize(0)
        # self.properties.SetRowLabelSize(wx.grid.GRID_AUTOSIZE)
        # self.properties.SetColMinimalAcceptableWidth(50)        
        # self.properties.SetColMinimalWidth(0, 100)
        # self.properties.SetDefaultColSize(250)
        self._mgr.AddPane(self.properties,
                          wx.aui.AuiPaneInfo().
                          Name("Properties").
                          Caption("Properties").
                          Right().MinSize(wx.Size(250, 50)).
                          Layer(1).
                          Position(1).
                          CloseButton(False).
                          MaximizeButton(True))

        # "commit" all changes made to FrameManager
        self._mgr.Update()

        # Bind events
        self.BindEvents()
        self.Bind = None

        # read the default graph file
        self.nb.DefaultGraph()

# Added Methods
    def BindEvents(self):
        """Bind all events (separated for clarity) returns nothing"""
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.propgrid.EVT_PG_CHANGED, self.OnPropertyChange)

        # Bind Menus
        self.BindFileMenu()
        self.BindEditMenu()
        self.BindInsertMenu()
        self.BindGraphMenu()
        self.BindViewMenu()
        self.BindHelpMenu()

    def BindFileMenu(self):
        """Bind the file menu"""
        self.Bind(wx.EVT_MENU, self.OnFileMenuSave,
                  id=const.ID_FileMenuSave)
        self.Bind(wx.EVT_MENU, self.OnFileMenuSaveAs,
                  id=const.ID_FileMenuSaveAs)
        self.Bind(wx.EVT_MENU, self.OnFileMenuOpenFile,
                  id=const.ID_FileMenuOpenFile)
        self.Bind(wx.EVT_MENU, self.OnFileMenuRevert,
                  id=const.ID_FileMenuRevert)
        self.Bind(wx.EVT_MENU, self.OnFileMenuClose,
                  id=const.ID_FileMenuClose)
        self.Bind(wx.EVT_MENU, self.OnFileMenuQuit,
                  id=const.ID_FileMenuQuit)

    def BindEditMenu(self):
        """Bind the Edit menu"""
        self.Bind(wx.EVT_MENU, self.OnEditMenuUndo,
                  id=const.ID_EditMenuUndo)
        self.Bind(wx.EVT_MENU, self.OnEditMenuRedo,
                  id=const.ID_EditMenuRedo)
        self.Bind(wx.EVT_MENU, self.OnEditMenuConnect,
                  id=const.ID_EditMenuConnect)
        self.Bind(wx.EVT_MENU, self.OnEditMenuRemoveObject,
                  id=const.ID_EditMenuRemoveObject)
        self.Bind(wx.EVT_MENU, self.OnEditMenuRemoveGraph,
                  id=const.ID_EditMenuRemoveGraph)
        self.Bind(wx.EVT_MENU, self.OnEditMenuClear,
                  id=const.ID_EditMenuClear)
        self.Bind(wx.EVT_MENU, self.OnEditMenuVirtual,
                  id=const.ID_EditMenuVirtual)
        self.Bind(wx.EVT_MENU, self.OnEditMenuReplicate,
                  id=const.ID_EditMenuReplicate)
        self.Bind(wx.EVT_MENU, self.OnEditMenuPreferences,
                  id=const.ID_EditMenuPreferences)

    def BindInsertMenu(self):
        """Bind the Insert menu"""
        self.Bind(wx.EVT_MENU, self.OnInsertMenuGraph,
                  id=const.ID_InsertMenuGraph)
        self.Bind(wx.EVT_MENU_RANGE, self.OnInsertNode,
                  id=const.ID_InsertNode, id2=const.ID_InsertNode+999)
        self.Bind(wx.EVT_MENU_RANGE, self.OnInsertData,
                  id=const.ID_InsertMenuDataFirst, id2=const.ID_InsertMenuDataLast)

    def BindGraphMenu(self):
        """Bind the Draw menu"""
        self.Bind(wx.EVT_MENU, self.OnGraphMenuAttach,
                  id=const.ID_GraphMenuAttach)
        self.Bind(wx.EVT_MENU, self.OnGraphMenuVerify,
                  id=const.ID_GraphMenuVerify)
        self.Bind(wx.EVT_MENU, self.OnGraphMenuExecute,
                  id=const.ID_GraphMenuExecute)
        self.Bind(wx.EVT_MENU, self.OnGraphMenuExport,
                  id=const.ID_GraphMenuExport)

    def BindViewMenu(self):
        self.Bind(wx.EVT_MENU, self.OnViewMenuShowVirtuals,
                  id=const.ID_ViewMenuShowVirtuals)
        self.Bind(wx.EVT_MENU, self.OnViewMenuZoomIn,
                  id=const.ID_ViewMenuZoomIn)
        self.Bind(wx.EVT_MENU, self.OnViewMenuZoomOut,
                  id=const.ID_ViewMenuZoomOut)
        self.Bind(wx.EVT_MENU, self.OnViewMenuZoomNormal,
                  id=const.ID_ViewMenuZoomNormal)
        self.Bind(wx.EVT_MENU, self.OnViewMenuData,
                  id=const.ID_ViewMenuData)
        self.Bind(wx.EVT_MENU, self.OnViewMenuProperties,
                  id=const.ID_ViewMenuProperties)
        self.Bind(wx.EVT_MENU, self.OnViewMenuLog,
                  id=const.ID_ViewMenuLog)
        self.Bind(wx.EVT_MENU, self.OnViewMenuNext,
                  id=const.ID_ViewMenuNext)
        self.Bind(wx.EVT_MENU, self.OnViewMenuPrevious,
                  id=const.ID_ViewMenuPrevious)
        self.Bind(wx.EVT_MENU, self.OnViewMenuSave,
                  id=const.ID_ViewMenuSave)
        self.Bind(wx.EVT_MENU_RANGE, self.OnViewMenuOrientation,
                  id=const.ID_ViewMenuTB, id2=const.ID_ViewMenuRL)
        self.Bind(wx.EVT_MENU_RANGE, self.OnViewMenuDPI,
                  id=const.ID_ViewMenuLowDPI, id2=const.ID_ViewMenuHighDPI)

    def BindHelpMenu(self):
        """Bind the Help menu"""
        self.Bind(wx.EVT_MENU, self.OnHelpMenuKeyStrokes,
                  id=const.ID_HelpMenuKeyStrokes)
        self.Bind(wx.EVT_MENU, self.OnHelpMenuHelp,
                  id=const.ID_HelpMenuHelp)
        self.Bind(wx.EVT_MENU, self.OnHelpMenuAbout,
                  id=const.ID_HelpMenuAbout)
        self.Bind(wx.EVT_MENU, self.OnHelpMenuTest,
                  id=const.ID_HelpMenuTest)
    # ---------- End of BindEvents

    def MakeStatusBar(self):
        """
        This function creates the status bar according to R07001 through R07009

        returns wx.StatusBar
        """
        statusbar = self.CreateStatusBar(2,
                                         wx.STB_SIZEGRIP | wx.STB_SHOW_TIPS |
                                         wx.STB_ELLIPSIZE_START)
        dc = wx.WindowDC(statusbar)
        dc.SetFont(statusbar.GetFont())
        statusbar.SetStatusWidths([-4, -4])#, -1, dc.GetTextExtent("400%")[0],
                                   #dc.GetTextExtent("4:1")[0],
                                   #dc.GetTextExtent("A0")[0],
                                   #dc.GetTextExtent("Landscape")[0],
                                   #dc.GetTextExtent("Transparent")[0],
                                   #dc.GetTextExtent("S")[0],
                                   #dc.GetTextExtent("G")[0]])
        statusbar.SetStatusText("Ready", const.SBF_Context)
        statusbar.SetStatusText("<no file>", const.SBF_Filename)
        return statusbar

    def Error(self, message, inBox=False):
        # Show the error message in the status bar, the log, stout, and optionally a message box
        # Returns False
        wx.LogError(message)
        print(message)
        self.Status(message)
        if inBox:
            wx.MessageBox(message, "Error", style=wx.ICON_ERROR)
        return False

    def Ready(self):
        self.Status("Ready")

    def Status(self, text):
        self.statusbar.SetStatusText(text, const.SBF_Context)
    
    def Filename(self, name):
        self.statusbar.SetStatusText("<no file>" if name=="" else name, const.SBF_Filename)
        self.GetMenuBar().FindItemById(const.ID_FileMenuClose).Enable(name!="")
        self.GetMenuBar().FindItemById(const.ID_FileMenuSave).Enable(name!="")
        self.GetMenuBar().FindItemById(const.ID_FileMenuRevert).Enable(name!="")
        self.filename = name

    def SaveInFile(self, filename):
        """
        TODO 
        trap errors

        String filename
        returns boolean
        updates self.filename
        Return True if all is well and the data is safe, otherwise False
        """
        self.Ready()
        if self.nb.tree is not None:
            if filename == "":
                fd = wx.FileDialog(self, message="Select OpenVX filename to save", defaultFile=self.filename, 
                                    wildcard='*.xml', style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
                if fd.ShowModal() == wx.ID_OK:
                    filename = fd.GetPath()
            if filename != "":
                try:
                    f = open(filename, 'w')
                    fixupReferences(self.nb.tree)
                    f.write(etree.tostring(self.nb.tree))
                    f.close()
                    self.Filename(filename)
                    return True
                except:
                    self.Error("Error writing to file '%s'"%self.filename)
        return False

    def SaveChanges(self):
        """
        If there are any changes, offer to save them either in the existing file
        or a new one, by calling SaveInFile
        """
        if len(self.nb.undoList) != 0 and wx.MessageBox("Save changes?", "You have made changes", style=wx.YES_NO|wx.ICON_QUESTION) == wx.YES:
            return self.SaveInFile(self.filename)
        return True

    def LoadFile(self, filename):
        """
        Load the file with the given name
        """
        if filename != "":
            try:
                self.nb.ReadGraphs(filename)
                self.Filename(filename)
            except:
                self.Error("Problem reading file '%s'"%filename, True)
                self.Filename("")
        
    def undoRedoEnable(self):
        """
        enable or disable undo and redo menus according to lists
        nb.undoList and nb.RedoList;
        if they are zero disable the corresponding menu else enable.
        """
        self.GetMenuBar().FindItemById(const.ID_EditMenuUndo).Enable(len(self.nb.undoList) != 0)
        self.GetMenuBar().FindItemById(const.ID_EditMenuRedo).Enable(len(self.nb.redoList) != 0)

# Event handlers

    def OnClose(self, _):
        """
        Don't close unless there are no unsaved changes or user really wants to.
        """
        if len(self.nb.undoList) == 0 or wx.MessageBox("Changes not saved, quit anyway?",
                                               "There are unsaved changes",
                                               style=wx.YES_NO|wx.ICON_QUESTION) == wx.YES:
            self._mgr.UnInit()
            self.Destroy()

    def OnSize(self, event):
        event.Skip()

    def OnExit(self, _):
        print("OnExit")
        self.Close()

    def OnPropertyChange(self, event):
        """
        Property changed - forward to the notebook
        """
        self.Ready()
        self.nb.OnPropertyChange(event)

    def OnSelectCell(self, event):
        print(event)
        event.Skip()

    def OnHelpMenuAbout(self, event):
        """
        Display the About dialog

        """
        wx.LogMessage("Menu Item " +
                      self.GetMenuBar().FindItemById(event.GetId()).GetText())
        msg = ("ClearVision 1.0\n" +
              "A Graphical Design Tool for OpenVX\n" +
              "(c) Copyright 2017, Imagination Technologies\n")
        dlg = wx.MessageDialog(self, msg, "About ClearVision",
                               wx.CLOSE | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        self.Ready()

    def OnEraseBackground(self, event):
        event.Skip()

    def OnFileMenuSave(self, event):
        """
        Save the drawing, operation cannot be undone

        """
        self.SaveInFile(self.filename)

    def OnFileMenuSaveAs(self, event):
        """
        Save the drawing in another file, operation cannot be undone

        """
        self.SaveInFile("")

    def OnFileMenuOpenFile(self, event):
        """
        Open drawing or OpenxVX XML file

        """
        self.Ready()
        self.SaveChanges()
        fd = wx.FileDialog(self, message="Select OpenVX file to open", defaultFile=self.filename, wildcard='*.xml', style=wx.FD_OPEN)
        if fd.ShowModal() == wx.ID_OK:
            filename = fd.GetPath()
            if filename != "":
                self.LoadFile(filename)

    def OnFileMenuRevert(self, event):
        """
        Discard changes and reload the current file
        Operation can't be undone
        """
        self.Ready()
        if self.filename == "":
            self.OnEditMenuClear(event)
        else:
            self.LoadFile(self.filename)
   

    def OnFileMenuClose(self, event):
        """
        Save the current drawing and start a new one.
        """
        if self.SaveChanges():          # offer to save data
            self.OnEditMenuClear(event) # Clear the drawing
            self.nb.Scrap()             # scrap the undo list
            self.Filename("")           # clear the filename

    def OnFileMenuQuit(self, event):
        """
        Offer to save changes and quit
        """
        if self.SaveChanges():
            self.nb.Scrap()
        self.Close()

    def OnEditMenuUndo(self, event):
        """
        Undo the last operation
        """
        self.nb.Undo()

    def OnEditMenuRedo(self, event):
        """
        Redo the last undone operation
        """
        self.nb.Redo()
    


    def OnEditMenuConnect(self, event):
        """
        """
        self.nb.ConnectObjects()

    def OnEditMenuRemoveObject(self, event):
        """
        """
        wx.LogMessage("Menu Item " +
                      self.GetMenuBar().FindItemById(event.GetId()).GetText())
        self.Ready()
        self.nb.RemoveObj()

    def OnEditMenuRemoveGraph(self, event):
        """
        Remove the current graph completely, including the tab
        Note we can't remove globals
        """
        self.Ready()
        self.nb.RemoveGraph()

    def OnEditMenuClear(self, event):
        """
        Clear all graphs
        """
        self.Ready()
        self.nb.DefaultGraph()

    def OnEditMenuVirtual(self, event):
        """
        Toggle the global/non-global state of a data object
        """
        self.Ready()
        self.nb.ToggleVirtual()

    def OnEditMenuReplicate(self, event):
        """
        Control the replication of nodes and their parameters
        """
        self.Ready()
        self.nb.Replicate()


    def OnEditMenuPreferences(self, event):
        """
        """
        wx.LogMessage("Menu Item " + self.GetMenuBar().
                      FindItemById(event.GetId()).GetText())

    def OnInsertMenuGraph(self, event):
        """
        Create a new tab with a graph on it
        """
        self.nb.NewGraph()

    def OnInsertNode(self, event):
        """
        Insert a new node in the current graph
        """
        self.Ready()
        kernel = self.GetMenuBar().FindItemById(event.GetId()).GetItemLabelText()
        if '.' not in kernel:
            kernel = "org.khronos.openvx." + kernel
        wx.LogMessage(kernel)
        self.nb.GetCurrentPage().insertNode(kernel)

    def OnInsertData(self, event):
        """
        Insert a new data item in the current graph
        """
        self.Ready()
        self.nb.InsertData(event.GetId())

    def OnGraphMenuAttach(self, event):
        """
        """
        wx.LogMessage("Menu Item " + self.GetMenuBar().
                      FindItemById(event.GetId()).GetText())

    def OnGraphMenuVerify(self, event):
        """
        """
        wx.LogMessage("Menu Item " + self.GetMenuBar().
                      FindItemById(event.GetId()).GetText())

    def OnGraphMenuExecute(self, event):
        """
        """
        wx.LogMessage("Menu Item " + self.GetMenuBar().
                      FindItemById(event.GetId()).GetText())

    def OnGraphMenuExport(self, event):
        """
        """
        wx.LogMessage("Menu Item " + self.GetMenuBar().
                      FindItemById(event.GetId()).GetText())

    def OnViewMenuShowVirtuals(self, event):
        """
        Show virtuals or not
        """
        self.Ready()
        self.nb.BuildGraphs()

    def OnViewMenuProperties(self, event):
        """
        Show or hide the properties pane
        """
        self.Ready()
        if self.GetMenuBar().FindItemById(event.GetId()).IsChecked():
            self._mgr.GetPane("Properties").Show()
        else:
            self._mgr.GetPane("Properties").Hide()
        self._mgr.Update()
    
    def OnViewMenuLog(self, event):
        """
        Show or hide the log pane
        """
        self.Ready()
        if self.GetMenuBar().FindItemById(event.GetId()).IsChecked():
            self._mgr.GetPane("Log").Show()
        else:
            self._mgr.GetPane("Log").Hide()
        self._mgr.Update()

    def OnViewMenuNext(self, event):
        """
        Switch to next tab, or to current tab if focus
        was elsewhere
        """
        curPage = self.nb.GetCurrentPage()
        if self.FindFocus() == curPage:
            num = self.nb.GetPageCount()
            current = self.nb.GetSelection()
            self.nb.SetSelection((current + 1) % num)
        else:
            curPage.SetFocus()

    def OnViewMenuPrevious(self, event):
        """
        Switch to next tab
        """
        curPage = self.nb.GetCurrentPage()
        if self.FindFocus() == curPage:
            num = self.nb.GetPageCount()
            current = self.nb.GetSelection()
            self.nb.SetSelection((current + num - 1) % num)
        else:
            curPage.SetFocus()

    def OnViewMenuData(self, event):
        """
        Show data for the selected object
        """
        wx.LogMessage("Menu Item " + self.GetMenuBar().
                      FindItemById(event.GetId()).GetText())
        event.Skip()

    def OnViewMenuZoomIn(self, event):
        """
        Zoom In the view by a factor of root 2
        """
        self.nb.zoom *= 1.4142135
        self.Ready()
        self.nb.Refresh()

    def OnViewMenuZoomOut(self, event):
        """
        Zoom Out the view by a factor of root 2
        """
        self.Ready()
        self.nb.zoom /= 1.4142135
        self.nb.Refresh()

    def OnViewMenuZoomNormal(self, event):
        """
        Set the current zoom factor to 1.0
        """
        self.Ready()
        self.nb.zoom = 1.0
        self.nb.Refresh()
    
    def OnViewMenuSave(self, event):
        """
        Save the currently displayed graph to a file
        """
        self.nb.GetCurrentPage().Write()

    def OnViewMenuOrientation(self, event):
        """
        Redraw with a new orientation
        """
        self.Ready()
        self.nb.Redraw(rankdir=self.GetMenuBar().FindItemById(event.GetId()).GetText()[1:3])

    def OnViewMenuDPI(self, event):
        """
        Set DPI for printing
        """
        self.Ready()
        self.nb.dpi = self.GetMenuBar().FindItemById(event.GetId()).GetText()[1:].split(' ')[0]

    def OnHelpMenuKeyStrokes(self, event):
        """
        TODO display the keystroke reference list
        """
        wx.LogMessage("Menu Item " +
                      self.GetMenuBar().FindItemById(event.GetId()).GetText())
        event.Skip()

    def OnHelpMenuHelp(self, event):
        """
        TODO show the help dialog

        """
        wx.LogMessage("Menu Item " +
                      self.GetMenuBar().FindItemById(event.GetId()).GetText())


    def OnHelpMenuTest(self, event):
        """Perform test operations.No specification requirement"""
        Test()
        self.nb.GetCurrentPage().Refresh()
