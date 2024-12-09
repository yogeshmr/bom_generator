try:
  from .bom_plugin import BomPlugin
  BomPlugin().register()
except Exception as e:
  import logging
  logging.error("Failed to register BOM Generator plugin: " + str(e))