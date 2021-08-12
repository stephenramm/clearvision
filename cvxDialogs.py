"""
Dialogs for clearvision.
Functions to get parameters for object insertion
Properties dialogs
Edit data dialogs
"""
import wx
import wx.grid
import cvxXML as bG
import cvxDataDefs as ddefs
import cvxKernelDefs as kdefs

class GridCellHexEditor(wx.grid.GridCellEditor):
    """
    Class to edit numbers in hex
    """
    def __init__(self, min=-1, max=-1):
        self.min = min
        self.max = max
        ctrl = wx.TextCtrl(self)
        id = ctrl.GetId()
        wx.EVT_TEXT(id, self.OnTextUpdate)
        wx.grid.GridCellEditor.SetControl(self, ctrl)
        
    def Create(self, parent, id, evtHandler):
        print("Create")
        wx.grid.GridCellTextEditor.Create(self, parent, id, evtHandler)
        wx.EVT_TEXT(id, self.OnTextUpdate)

    def OnTextUpdate(self, event):
        """
        Filter the keystrokes to only accept hex digits
        """
        text = self.GetControl().GetValue()
        print(("OnTextUpdate %s"%text))
        #return wx.grid.GridCellTextEditor.EndEdit(self, row, col, grid)
        # if char >= ord('0') and char <= ord('9') or char >= ord('A') and char <= ord('F'):
        #     return True
        # else:
        #     keyEvent.SetUnicodeKey(0)
        #     return False

    def EndEdit(self, row, col, grid, oldval):
        """
        """
        print(("EndEdit %s"%oldval))
        return wx.grid.GridCellTextEditor(self, row, col, grid, oldval)
