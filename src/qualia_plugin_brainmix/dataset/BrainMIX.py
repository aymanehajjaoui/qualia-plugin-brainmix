from __future__ import annotations

import logging
import pickle
import sys
from pathlib import Path
import numpy as np
from qualia_core.datamodel import RawDataModel
from qualia_core.datamodel.RawDataModel import RawData, RawDataSets
from .RawDataset import RawDataset

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

logger = logging.getLogger(__name__)

class BrainMIX(RawDataset):
    def __init__(self, path: str) -> None:
        super().__init__()
        self.__path = Path(path)
        self.sets.remove('valid')

    def _find_first_file(self, prefix: str) -> Path:
        matches = sorted(self.__path.glob(f"{prefix}*.pickle"))
        if not matches:
            raise FileNotFoundError(f"No file starting with '{prefix}' found in {self.__path}")
        return matches[0]

    @override
    def __call__(self) -> RawDataModel:
        train_path = self._find_first_file("traindata")
        valid_path = self._find_first_file("valid")

        with train_path.open("rb") as fd:
            traindata = pickle.load(fd)
        with valid_path.open("rb") as fd:
            testdata = pickle.load(fd)

        train_x = traindata["signal"]
        train_y = np.expand_dims(traindata["truth"], axis=1).astype(np.float32)
        test_x = testdata["signal"]
        test_y = np.expand_dims(testdata["truth"], axis=1).astype(np.float32)

        train = RawData(train_x, train_y)
        test = RawData(test_x, test_y)

        logger.info("Shapes: train_x=%s, train_y=%s, test_x=%s, test_y=%s",
                    train_x.shape,
                    train_y.shape,
                    test_x.shape,
                    test_y.shape)

        return RawDataModel(sets=RawDataSets(train=train, test=test), name=self.name)
