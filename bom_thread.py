import os
import tempfile
import logging
from threading import Thread
from .bom_manager import BomManager
from .config import OUTPUT_FOLDER, BOM_FILENAME

class BomThread(Thread):
    def __init__(self, board):
        Thread.__init__(self)
        self.board = board
        self.bom_manager = BomManager(self.board)

    def run(self):
        try:
            # Create output directory
            project_directory = os.path.dirname(self.board.GetFileName())
            output_path = os.path.join(project_directory, OUTPUT_FOLDER)
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            # Generate BOM
            self.bom_manager.generate_bom(output_path)

            logging.info(f"BOM generated successfully in {output_path}")

        except Exception as e:
            logging.error(f"Error generating BOM: {str(e)}")