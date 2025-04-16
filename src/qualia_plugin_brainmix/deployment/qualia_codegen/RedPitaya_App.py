from __future__ import annotations

import logging
import shutil
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

class RedPitaya_App(Linux):
    evaluator = QualiaEvaluator

    def __init__(self,
                 projectdir: str | Path | None = None,
                 outdir: str | Path | None = None) -> None:
        super().__init__(
            projectdir=projectdir if projectdir is not None else
                resources_to_path(files('qualia_codegen_core.examples')) / 'RedPitaya_App',
            outdir=outdir if outdir is not None else Path('out') / 'deploy' / 'RedPitaya_App'
        )
        self.__size_bin = 'arm-linux-gnueabihf-size'

    @override
    def deploy(self, tag: str) -> Deploy | None:
        logger.info('Running on RedPitaya — skipping deploy')
        return Deploy(
            rom_size=self._rom_size(self._outdir / tag / 'RedPitaya_App', str(self.__size_bin)),
            ram_size=self._ram_size(self._outdir / tag / 'RedPitaya_App', str(self.__size_bin)),
            evaluator=self.evaluator
        )

    @override
    def prepare(self, tag, model, optimize, compression):
        result = super().prepare(tag, model, optimize, compression)

        if result:
            import glob

            codegen_root = Path("out") / "qualia_codegen"
            match_prefix = tag.split('_q')[0]
            matches = sorted(codegen_root.glob(f"{match_prefix}*_q*"))
            if not matches:
                raise FileNotFoundError(f"No matching model C code folder for pattern: {match_prefix}*_q*")

            generated_model_dir = matches[-1]
            destination_root = Path('out') / 'deploy' / 'RedPitaya_App' / tag
            destination_model_dir = destination_root / 'model'
            destination_model_dir.mkdir(parents=True, exist_ok=True)

            # Copy generated model C code
            for item in generated_model_dir.iterdir():
                dest = destination_model_dir / item.name
                if item.is_dir():
                    shutil.copytree(item, dest, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, dest)

            logger.info(f"[RedPitaya_App] Model files copied from {generated_model_dir} to {destination_model_dir}")

            # Copy static template files from examples/RedPitaya_App
            template_base = resources_to_path(files('qualia_codegen_core.examples')) / 'RedPitaya_App'
            for folder in ['CMSIS', 'include', 'src', 'ModelOutput', 'DataOutput']:
                src_folder = template_base / folder
                dest_folder = destination_root / folder
                if src_folder.exists():
                    if dest_folder.exists():
                        shutil.rmtree(dest_folder)
                    shutil.copytree(src_folder, dest_folder)

            for file in ['Makefile', 'README.md', 'plot.py']:
                src_file = template_base / file
                if src_file.exists():
                    shutil.copy2(src_file, destination_root / file)

            logger.info(f"[RedPitaya_App] Template files copied from {template_base} to {destination_root}")

        return result
