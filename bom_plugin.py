
import os
import wx
import pcbnew
from .bom_form import BomGeneratorForm

class BomPlugin(pcbnew.ActionPlugin):
    def __init__(self):
        super().__init__()
        self.name = "BOM Generator"
        self.category = "Manufacturing"
        self.description = "Generate Bill of Materials in CSV format"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png')
        self.dark_icon_file_name = self.icon_file_name

    def Run(self):
        board = pcbnew.GetBoard()
        if board is None:
            wx.MessageBox("Please open a board first!")
            return
        BomGeneratorForm().Show()

    def register(self):
        """Register the plugin"""
        pcbnew.ActionPlugin.register(self)