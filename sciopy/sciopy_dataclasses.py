from dataclasses import dataclass
from typing import List
import numpy as np


@dataclass
class SingleFrame:
    start_tag: List[str]
    channel_group: str
    excitation_stgs: List[str]
    frequency_row: List[str]
    timestamp: int  # [ms]
    ch_1: complex
    ch_2: complex
    ch_3: complex
    ch_4: complex
    ch_5: complex
    ch_6: complex
    ch_7: complex
    ch_8: complex
    ch_9: complex
    ch_10: complex
    ch_11: complex
    ch_12: complex
    ch_13: complex
    ch_14: complex
    ch_15: complex
    ch_16: complex
    end_tag: str


@dataclass
class ScioSpecMeasurementConfig:
    com_port: str
    sample_per_step: int
    actual_sample: int
    s_path: str
    object: str


@dataclass
class SingleEitFrame:
    pass


@dataclass
class BaseSettingForEstimation:
    active_channel_groups: np.ndarray
    burst_count: int
