# Force registration of custom deployment targets into qualia_core.deployment.qualia_codegen
import qualia_core.deployment.qualia_codegen as codegen

from .deployment.qualia_codegen import RedPitaya, RedPitaya_App, RedPitaya_Metrics

setattr(codegen, "RedPitaya", RedPitaya)
setattr(codegen, "RedPitaya_App", RedPitaya_App)
setattr(codegen, "RedPitaya_Metrics", RedPitaya_Metrics)

