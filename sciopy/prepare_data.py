import os
from .sciopy_dataclasses import PreperationConfig

import numpy as np


def create_prep_directory(prep_cnf: PreperationConfig) -> str:
    """
    Creates the directory to prepare the environment for data preperation.

    Parameters
    ----------
    prep_cnf : PreperationConfig
        dataclass object for praperation options

    Returns
    -------
    str
        updated PreperationConfig
    """
    prep_cnf.n_samples = len(os.listdir(prep_cnf.lpath))
    prep_cnf.spath = prep_cnf.lpath[:-1] + str("_prepared/")
    try:
        os.mkdir(prep_cnf.spath[:-1])
        print("Created directory, return save path.\n")
    except BaseException:
        print("Directory already exists.\n\t-> Return: save path\n")
    for key, value in prep_cnf.__dict__.items():
        print(key, ":", value)
    return prep_cnf


def extract_potentials_from_sample_n_el_16(sample: np.lib.npyio.NpzFile) -> np.ndarray:
    """
    Extracts the potential values and other important information.

    Parameters
    ----------
    sample : np.lib.npyio.NpzFile
        single measurement sample

    Returns
    -------
    np.ndarray
        potential matrix
    """
    sample_data_shape_0 = sample["data"].shape[0]
    n_el = sample["config"].tolist().n_el

    pot_matrix = np.empty((sample_data_shape_0, 16), dtype=complex)

    for stage in range(sample_data_shape_0):
        for el in range(n_el):
            pot_matrix[stage, el] = sample["data"][stage].__dict__[f"ch_{el+1}"]
    return pot_matrix
