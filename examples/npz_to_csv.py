from sciopy.npztocsv import s_dict_n_el_16
from sciopy.sciopy_dataclasses import PreperationConfig
from sciopy import prepare_all_samples_for_16_el_single

path = "obj_d_10"

prep_conf = PreperationConfig(lpath=path, spath=path, n_samples=len(os.listdir(path)))

prepare_all_samples_for_16_el_single(prep_conf)


# Only working with 3D printer object movement and class "enderstat"
# from sciopy import convert_measurement_directory_n_el_16_r_split
# convert_measurement_directory_n_el_16_r_split(lpath, s_dict_n_el_16)
