# import os
# import pcbnew
# from .bom_thread import BomThread

# class BomPlugin(pcbnew.ActionPlugin):
#     def __init__(self):
#         self.name = "BOM Generator"
#         self.category = "Manufacturing"
#         self.description = "Generate Bill of Materials in CSV format"
#         self.show_toolbar_button = True
#         self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png')

#     def Run(self):
#         # Start the BOM generation thread
#         board = pcbnew.GetBoard()
#         BomThread(board).start()


import os
import wx
import pcbnew
from .bom_form import BomGeneratorForm

class BomPlugin(pcbnew.ActionPlugin):
    def __init__(self):
        self.name = "BOM Generator"
        self.category = "Manufacturing"
        self.description = "Generate Bill of Materials in CSV format"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png')

    def Run(self):
        BomGeneratorForm().Show()