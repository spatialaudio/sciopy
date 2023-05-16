# Issue

from sciopy.sciopy_dataclasses import PreperationConfig
from sciopy import prepare_all_samples_for_16_el_single
import os

path = "obj_d_10"

prep_conf = PreperationConfig(lpath=path, spath=path, n_samples=len(os.listdir(path)))

prepare_all_samples_for_16_el_single(prep_conf)
