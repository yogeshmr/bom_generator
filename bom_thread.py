import os
import wx
import csv
import pcbnew
from .events import StatusEvent

class BomThread:
    def __init__(self, window, board):
        self.window = window  # Store reference to the window
        self.board = board
        self.output_dir = os.path.join(os.path.dirname(board.GetFileName()), 'bom_output')
        os.makedirs(self.output_dir, exist_ok=True)
        self.generate_bom()

    def progress(self, percent):
        """Update progress bar"""
        wx.PostEvent(self.window, StatusEvent(percent))  # Use stored window reference

    def generate_bom(self):
        try:
            self.progress(10)

            # Get all footprints from the board
            footprints = self.board.GetFootprints()

            self.progress(30)

            # Prepare BOM data
            bom_data = {}
            for footprint in footprints:
                # Skip footprints marked as "Exclude from BOM"
                if footprint.GetAttributes() & pcbnew.FP_EXCLUDE_FROM_BOM:
                    continue

                ref = footprint.GetReference()
                value = footprint.GetValue()
                footprint_name = str(footprint.GetFPID().GetLibItemName())

                # Create a unique key for grouping similar components
                key = f"{value}_{footprint_name}"

                if key not in bom_data:
                    bom_data[key] = {
                        'Reference': [ref],
                        'Value': value,
                        'Footprint': footprint_name,
                        'Quantity': 1
                    }
                else:
                    bom_data[key]['Reference'].append(ref)
                    bom_data[key]['Quantity'] += 1

            self.progress(60)

            # Write BOM to CSV file
            output_file = os.path.join(self.output_dir, 'bom.csv')
            with open(output_file, 'w', newline='') as csvfile:
                fieldnames = ['Reference', 'Value', 'Footprint', 'Quantity']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for component in bom_data.values():
                    # Join references with commas
                    component['Reference'] = ', '.join(sorted(component['Reference']))
                    writer.writerow(component)

            self.progress(90)

            # Open the output directory
            os.startfile(self.output_dir) if os.name == 'nt' else os.system(f'xdg-open {self.output_dir}')

            self.progress(100)
            # Signal completion
            wx.CallAfter(lambda: self.progress(-1))

        except Exception as e:
            wx.MessageBox(f"Error generating BOM: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)
            wx.CallAfter(lambda: self.progress(-1))