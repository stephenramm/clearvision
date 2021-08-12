"""ClearVision Application. Design OpenVX graphs with a graphical interface"""
import wx


class ClearVisionApp(wx.App):
    """"The ClearVision Application Class, Uses MainFrame from cvxMain"""

    def OnInit(self):
        """Initialise the application"""
        import cvxMain
        self.SetAppName("ClearVision")
        self.frame = cvxMain.MainFrame(None, size=(1024, 768))
        self.frame.Show()
        return True


if __name__ == '__main__':
    #    import argparse
    #    parser = argparse.ArgumentParser(description='Clearvision for OpenVX')
    #    parser.add_argument('-q', dest='verbose', action='store_const',
    #                        const=False, default=True,
    #                        help='disable verbose mode')
    #    parser.add_argument('remoteuri', metavar='xxx', type=str, nargs='?',
    #                        help='a remote uri to use')
    #
    #    args = parser.parse_args()
    #    verbose = args.verbose
    #    remoteuri = args.remoteuri
    App = ClearVisionApp()
    App.MainLoop()
