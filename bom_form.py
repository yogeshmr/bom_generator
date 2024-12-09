import wx
import pcbnew
from .bom_thread import BomThread
from .events import StatusEvent

class BomGeneratorForm(wx.Frame):
    def __init__(self):
        wx.Dialog.__init__(
            self,
            None,
            id=wx.ID_ANY,
            title="BOM Generator",
            pos=wx.DefaultPosition,
            size=wx.DefaultSize,
            style=wx.DEFAULT_DIALOG_STYLE
        )

        self.SetSizeHints(wx.Size(400, 150), wx.DefaultSize)
        self.SetBackgroundColour(wx.LIGHT_GREY)

        # Create GUI elements
        self.mGenerateButton = wx.Button(self, label='Generate BOM', size=wx.Size(380, 40))
        self.mGenerateButton.Bind(wx.EVT_BUTTON, self.onGenerateButtonClick)

        self.mGaugeStatus = wx.Gauge(
            self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size(380, 20), wx.GA_HORIZONTAL)
        self.mGaugeStatus.SetValue(0)
        self.mGaugeStatus.Hide()

        # Layout
        boxSizer = wx.BoxSizer(wx.VERTICAL)
        boxSizer.Add(self.mGenerateButton, 0, wx.ALL, 5)
        boxSizer.Add(self.mGaugeStatus, 0, wx.ALL, 5)

        self.SetSizer(boxSizer)
        self.Layout()
        boxSizer.Fit(self)
        self.Centre(wx.BOTH)

        # Bind ESC key
        self.Bind(wx.EVT_CHAR_HOOK, self.onKey)

    def onKey(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close(True)
        else:
            event.Skip()

    def onGenerateButtonClick(self, event):
        self.mGenerateButton.Hide()
        self.mGaugeStatus.Show()
        self.SetTitle('BOM Generator (Processing...)')

        StatusEvent.invoke(self, self.updateDisplay)
        BomThread(pcbnew.GetBoard())

    def updateDisplay(self, status):
        if status.data == -1:
            self.SetTitle('BOM Generator (Done!)')
            pcbnew.Refresh()
            self.Destroy()
        else:
            self.mGaugeStatus.SetValue(int(status.data))