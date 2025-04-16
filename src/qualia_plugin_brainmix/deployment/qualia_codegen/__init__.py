import sys
import qualia_core.deployment.qualia_codegen as codegen

from .RedPitaya import RedPitaya
from .RedPitaya_App import RedPitaya_App
from .RedPitaya_Metrics import RedPitaya_Metrics

# Expose plugin targets to the main core loader
setattr(codegen, "RedPitaya", RedPitaya)
setattr(codegen, "RedPitaya_App", RedPitaya_App)
setattr(codegen, "RedPitaya_Metrics", RedPitaya_Metrics)
