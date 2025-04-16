from __future__ import annotations

import logging
from pathlib import Path
from importlib.resources import files

from qualia_core.deployment.qualia_codegen.Linux import Linux
from qualia_core.evaluation.host.Qualia import Qualia as QualiaEvaluator
from qualia_core.utils.path import resources_to_path

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from qualia_core.deployment.Deploy import Deploy

import sys
if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

logger = logging.getLogger(__name__)

class RedPitaya_Metrics(Linux):
    evaluator = QualiaEvaluator
    target_name = 'RedPitaya_Metrics'

    def __init__(self,
                 projectdir: str | Path | None = None,
                 outdir: str | Path | None = None) -> None:
        super().__init__(
            projectdir=projectdir if projectdir is not None else
                resources_to_path(files('qualia_plugin_brainmix.examples')) / self.target_name,
            outdir=outdir if outdir is not None else Path('out') / 'deploy' / self.target_name
        )
        self.__size_bin = 'arm-linux-gnueabihf-size'

    @override
    def deploy(self, tag: str) -> Deploy | None:
        logger.info(f'Running on {self.target_name} — skipping deploy')
        return Deploy(
            rom_size=self._rom_size(self._outdir / tag / self.target_name, str(self.__size_bin)),
            ram_size=self._ram_size(self._outdir / tag / self.target_name, str(self.__size_bin)),
            evaluator=self.evaluator
        )

