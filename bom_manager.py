import os
import csv
from collections import defaultdict
from .config import BOM_FILENAME

class BomManager:
    def __init__(self, board):
        self.board = board
        self.bom = []
        self.bom_designators = defaultdict(int)

    def generate_bom(self, output_dir):
        """Generate the BOM file."""
        self._process_components()
        self._write_bom_file(output_dir)

    def _process_components(self):
        """Process board components and create BOM entries."""
        if hasattr(self.board, 'GetFootprints'):
            footprints = list(self.board.GetFootprints())
        else:
            footprints = list(self.board.GetModules())

        # Sort footprints by reference
        footprints.sort(key=lambda x: x.GetReference().upper())

        # Count unique designators
        for footprint in footprints:
            self.bom_designators[footprint.GetReference().upper()] += 1

        # Process each footprint
        for footprint in footprints:
            if not self._should_exclude_from_bom(footprint):
                self._process_single_component(footprint)

    def _process_single_component(self, footprint):
        """Process a single component for BOM."""
        # Get basic footprint information
        try:
            footprint_name = str(footprint.GetFPID().GetFootprintName())
        except AttributeError:
            footprint_name = str(footprint.GetFPID().GetLibItemName())

        # Handle duplicate designators
        unique_id = ""
        ref = footprint.GetReference().upper()
        if self.bom_designators[ref] > 1:
            unique_id = str(self.bom_designators[ref])
            self.bom_designators[ref] -= 1

        designator = f"{ref}{'' if unique_id == '' else '_'}{unique_id}"

        # Try to merge with existing components
        for component in self.bom:
            if (component['Value'].upper() == footprint.GetValue().upper() and
                component['Footprint'] == self._normalize_footprint_name(footprint_name)):
                component['Quantity'] += 1
                component['Designators'] += f", {designator}"
                return

        # Add as new component if no merge possible
        self.bom.append({
            'Designators': designator,
            'Value': footprint.GetValue(),
            'Footprint': self._normalize_footprint_name(footprint_name),
            'Quantity': 1,
            'References': footprint.GetReference(),
            'Package': footprint_name
        })

    def _write_bom_file(self, output_dir):
        """Write BOM data to CSV file."""
        if len(self.bom) > 0:
            output_file = os.path.join(output_dir, BOM_FILENAME)
            with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=self.bom[0].keys())
                writer.writeheader()
                writer.writerows(self.bom)

    def _should_exclude_from_bom(self, footprint):
        """Check if footprint should be excluded from BOM."""
        return (footprint.GetAttributes() & pcbnew.FP_EXCLUDE_FROM_BOM or
                self._is_dnp_component(footprint))

    def _is_dnp_component(self, footprint):
        """Check if component is marked as Do Not Place."""
        return (self._has_field(footprint, 'dnp') or
                footprint.GetValue().upper() == 'DNP')

    def _has_field(self, footprint, field_name):
        """Check if footprint has specific field."""
        try:
            return footprint.HasField(field_name)
        except:
            return False

    def _normalize_footprint_name(self, footprint):
        """Normalize footprint name for consistency."""
        import re
        # Replace footprint names with standardized format
        pattern = re.compile(r'^(\w*_SMD:)?\w{1,4}_(\d+)_\d+Metric.*$')
        return pattern.sub(r'\2', footprint)