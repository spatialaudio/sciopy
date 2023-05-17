from sciopy.prepare_data import comp_tank_relative_r_phi
import numpy as np
import os
from typing import Union
import pandas as pd
from tqdm import tqdm

s_dict_n_el_16 = {
    "n_sample": [],
    "datetime": [],
    "n_el": [],
    "n_el_skip": [],
    "channel_group": [],
    "object": [],
    "size": [],
    "material": [],
    "water_lvl": [],
    "r": [],
    "phi": [],
    "saline_conductivity": [],
    "temperature": [],
    "exc_freq": [],
    "inj_el_vcc": [],
    "inj_el_gnd": [],
    "el_1": [],
    "el_2": [],
    "el_3": [],
    "el_4": [],
    "el_5": [],
    "el_6": [],
    "el_7": [],
    "el_8": [],
    "el_9": [],
    "el_10": [],
    "el_11": [],
    "el_12": [],
    "el_13": [],
    "el_14": [],
    "el_15": [],
    "el_16": [],
}

s_dict_n_el_32 = {
    "n_sample": [],
    "datetime": [],
    "n_el": [],
    "n_el_skip": [],
    "channel_group": [],
    "object": [],
    "size": [],
    "material": [],
    "water_lvl": [],
    "r": [],
    "phi": [],
    "saline_conductivity": [],
    "temperature": [],
    "exc_freq": [],
    "inj_el_vcc": [],
    "inj_el_gnd": [],
    "el_1": [],
    "el_2": [],
    "el_3": [],
    "el_4": [],
    "el_5": [],
    "el_6": [],
    "el_7": [],
    "el_8": [],
    "el_9": [],
    "el_10": [],
    "el_11": [],
    "el_12": [],
    "el_13": [],
    "el_14": [],
    "el_15": [],
    "el_16": [],
    "el_17": [],
    "el_18": [],
    "el_19": [],
    "el_20": [],
    "el_21": [],
    "el_22": [],
    "el_23": [],
    "el_24": [],
    "el_25": [],
    "el_26": [],
    "el_27": [],
    "el_28": [],
    "el_29": [],
    "el_30": [],
    "el_31": [],
    "el_32": [],
}


def clear_s_dict(s_dict: dict) -> dict:
    """
    Reset the save dictionary to empty values.

    Parameters
    ----------
    s_dict : dict
        save dictionary with values

    Returns
    -------
    dict
        empty dictionary
    """
    for key in s_dict.keys():
        s_dict[key] = []
    return s_dict


def single_measurement_to_csv_n_el_16(
    sample: np.lib.npyio.NpzFile,
    s_dict_n_el_16: dict,
    r_split: float = -1.0,
) -> dict:
    """
    Converts a single measurement sample to a dictonary for a later CSV expot.
    The previous measurement has to be done in n_el = 16 electrode mode.

    Parameters
    ----------
    sample : np.lib.npyio.NpzFile
        single measurement sample
    s_dict_n_el_16 : dict
        dict to be filled
    r_split : float, optional
        only write a given radial value to the s_dict_n_el_16, by default -1.0,
        if default, the radial position is not inspected.
    material : str, optional
        material of the measurement object, by default "PLA"
    saline_conductivity : float, optional
        saline conductivity, by default 99.9
    temperature : float, optional
        environment temperature, by default 22.1

    Returns
    -------
    dict
        appended saving dictionary
    """
    config = sample["config"].tolist()
    if r_split != -1.0:
        r, phi = comp_tank_relative_r_phi(sample)
    if r_split == -1.0:
        r = -1

    if r == float(r_split) and r_split >= 0:
        n_el_skip = (
            sample["data"].tolist()[0].excitation_stgs[1]
            - sample["data"].tolist()[0].excitation_stgs[0]
        )

        for frame in sample["data"].tolist():
            s_dict_n_el_16["n_sample"].append(config.actual_sample)
            s_dict_n_el_16["datetime"].append(config.datetime)
            s_dict_n_el_16["n_el"].append(config.n_el)
            s_dict_n_el_16["n_el_skip"].append(n_el_skip)
            s_dict_n_el_16["channel_group"].append(config.channel_group)
            s_dict_n_el_16["object"].append(config.object)
            s_dict_n_el_16["size"].append(config.size)
            s_dict_n_el_16["material"].append(config.material)
            s_dict_n_el_16["r"].append(r)
            s_dict_n_el_16["phi"].append(phi)
            s_dict_n_el_16["water_lvl"].append(config.water_lvl)
            s_dict_n_el_16["saline_conductivity"].append(config.saline_conductivity[0])
            s_dict_n_el_16["temperature"].append(config.temperature)
            s_dict_n_el_16["exc_freq"].append(config.exc_freq)
            s_dict_n_el_16["inj_el_vcc"].append(frame.excitation_stgs[0])
            s_dict_n_el_16["inj_el_gnd"].append(frame.excitation_stgs[1])
            for el in range(config.n_el):
                s_dict_n_el_16[f"el_{el+1}"].append(frame.__dict__[f"ch_{el+1}"])
    if r_split == -1.0:
        n_el_skip = (
            sample["data"].tolist()[0].excitation_stgs[1]
            - sample["data"].tolist()[0].excitation_stgs[0]
        )

        for frame in sample["data"].tolist():
            s_dict_n_el_16["n_sample"].append(config.actual_sample)
            s_dict_n_el_16["datetime"].append(config.datetime)
            s_dict_n_el_16["n_el"].append(config.n_el)
            s_dict_n_el_16["n_el_skip"].append(n_el_skip)
            s_dict_n_el_16["channel_group"].append(config.channel_group)
            s_dict_n_el_16["object"].append(config.object)
            s_dict_n_el_16["size"].append(config.size)
            s_dict_n_el_16["material"].append(config.material)
            s_dict_n_el_16["r"].append(0)
            s_dict_n_el_16["phi"].append(0)
            s_dict_n_el_16["saline_conductivity"].append(config.saline_conductivity[0])
            s_dict_n_el_16["temperature"].append(config.temperature)
            s_dict_n_el_16["exc_freq"].append(config.exc_freq)
            s_dict_n_el_16["inj_el_vcc"].append(frame.excitation_stgs[0])
            s_dict_n_el_16["inj_el_gnd"].append(frame.excitation_stgs[1])
            for el in range(config.n_el):
                s_dict_n_el_16[f"el_{el+1}"].append(frame.__dict__[f"ch_{el+1}"])

    return s_dict_n_el_16


def convert_measurement_directory_n_el_16(
    lpath: str,
    s_dict_n_el_16: dict,
    r_split: float = -1.0,
    export_csv: bool = True,
) -> Union[None, dict]:
    """
    Converts all samples inside a measurement directory to a new generated
    directory or returns the corresponding dict.

    Parameters
    ----------
    lpath : str
        load path
    s_dict_n_el_16 : dict
        data dictionary
    r_split : float, optional
        only write a given radial value to the s_dict_n_el_16, by default -1.0,
        if default, the radial position is not inspected.
    export_csv : bool, optional
        export the dict as CSV using pandas, by default True

    Returns
    -------
    Union[None, dict]
        depending on export_csv nothing or the appended data dictionary
    """

    if len(s_dict_n_el_16["n_sample"]) != 0:
        # clear directory
        print("clearing: s_dict_n_el_16")
        s_dict_n_el_16 = clear_s_dict(s_dict_n_el_16)

    for ch_mod, ele in tqdm(enumerate(np.sort(os.listdir(lpath)))):
        if ch_mod % 10 != 0:
            tmp_sample = np.load(lpath + ele, allow_pickle=True)
            s_dict_n_el_16 = single_measurement_to_csv_n_el_16(
                tmp_sample, s_dict_n_el_16, r_split=r_split
            )

    if export_csv is True:
        try:
            os.mkdir(f"{lpath[:-1]}_csv")
            print(f"Created save directory at:\n\t{lpath[:-1]}_csv/")
        except BaseException:
            pass
        # save the data to csv

        df = pd.DataFrame(s_dict_n_el_16)
        if float(r_split) == -1.0:
            s_p_name = f"{lpath[:-1]}_csv/full.csv"
        else:
            s_p_name = f"{lpath[:-1]}_csv/r_{int(r_split)}_mm.csv"
        df.to_csv(s_p_name, index=False)

    if export_csv is False:
        # return the dictionary
        return s_dict_n_el_16


def get_radial_positions(lpath: str) -> np.ndarray:
    """
    Get all measurered radial positions of a full measurement directory.

    Parameters
    ----------
    lpath : str
        path to the measured data

    Returns
    -------
    np.ndarray
        array with the measured radial positions
    """
    print("Finding the measured radial positions:\n")
    radial_posis = []
    for ele in tqdm(os.listdir(lpath)):
        tmp_sample = np.load(lpath + ele, allow_pickle=True)
        r, _ = comp_tank_relative_r_phi(tmp_sample)
        radial_posis.append(r)
    radial_posis = np.unique(radial_posis)
    print(f"Returning:\n\t {radial_posis}")
    return radial_posis


def convert_measurement_directory_n_el_16_r_split(
    lpath: str, s_dict_n_el_16: dict
) -> None:
    """
    convert_measurement_directory_n_el_16_r_split does the full conversion of a
    data set and writes CSV data depending on the measured radiants.
    The reason for the splis is the resulting size of the .CSV files.

    Parameters
    ----------
    lpath : str
        _description_
    s_dict_n_el_16 : dict
        _description_
    """
    for r_splits in get_radial_positions(lpath):
        convert_measurement_directory_n_el_16(
            lpath=lpath,
            s_dict_n_el_16=s_dict_n_el_16,
            r_split=r_splits,
            export_csv=True,
        )
