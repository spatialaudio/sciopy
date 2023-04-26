import os
import math
from tqdm import tqdm
import numpy as np

from .sciopy_dataclasses import PreperationConfig
from .meshing import create_empty_2d_mesh, add_circle_anomaly


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


def extract_potentials_from_sample_n_el_16(
    sample: np.lib.npyio.NpzFile,
) -> np.ndarray:
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


def comp_tank_relative_r_phi(
    sample: np.lib.npyio.NpzFile,
    ender_x_y_center: float = 180.0,
) -> tuple:
    """
    comp_tank_relative_r_phi converts the absolute Ender5 cartesian position to tank relative polar position.

    Parameters
    ----------
    sample : np.lib.npyio.NpzFile
        single sample
    ender_x_y_center : float, optional
        center position of Ender5 x,y-axis, by default 180.0

    Returns
    -------
    tuple
        tank relative object position
    """
    x_abs = sample["enderstat"].tolist()["abs_x_pos"] - ender_x_y_center
    y_abs = sample["enderstat"].tolist()["abs_y_pos"] - ender_x_y_center

    r = np.round(np.sqrt(x_abs**2 + y_abs**2), 2)
    # Pay attention to the phi position due to the phantom tank alignment.
    phi = -np.round(math.degrees(np.arctan2(x_abs, y_abs)) - 90, 2)  # + 90

    return (r, phi)


def check_n_el_condition(
    prep_cnf: PreperationConfig, ch_group_to_check: list, n_el_to_check: int
) -> bool:
    """
    check_n_el_condition proofs, if a single random data point is in the right shape.

    Parameters
    ----------
    prep_cnf : PreperationConfig
        config for conversion
    ch_group_to_check : list
        predetermined channel group
    n_el_to_check : int
        predetermined number of electrodes

    Returns
    -------
    bool
        true if condition is fulfiled, false else
    """

    rand_sample = np.load(
        prep_cnf.lpath
        + "sample_{0:06d}.npz".format(np.random.randint(0, prep_cnf.n_samples)),
        allow_pickle=True,
    )
    set_ch_group = rand_sample["config"].tolist().channel_group
    set_n_el = rand_sample["config"].tolist().n_el
    if set_ch_group == ch_group_to_check and set_n_el == n_el_to_check:
        return True
    else:
        print("\tError: Data has not the right number of channels and/or electrodes!")
        return False


def extract_electrodepotentials(
    potential_matrix: np.ndarray,
    sample: np.lib.npyio.NpzFile,
    del_ex_stgs: bool = True,
) -> np.array:
    """
    Extracts the electrode signal without the corresponding excitation stages.

    Parameters
    ----------
    potential_matrix : np.ndarray
        potential matrix
    sample : np.lib.npyio.NpzFile
        sample description
    del_ex_stgs : bool, optional
        delete the excitations or not, by default True

    Returns
    -------
    np.array
        electrode signal
    """
    p_mat_shape = potential_matrix.shape

    if del_ex_stgs is False:
        return np.reshape(potential_matrix, (p_mat_shape[0] * p_mat_shape[1],))
    if del_ex_stgs is True:
        resh_pot = np.reshape(potential_matrix, (p_mat_shape[0] * p_mat_shape[1],))
        del_idx = []
        for r, dat in enumerate(sample["data"]):
            del_idx.append((dat.excitation_stgs - 1) + p_mat_shape[1] * r)
        del_idx = np.concatenate(del_idx)
        return np.delete(resh_pot, del_idx)


def norm_data(data: np.ndarray, low_bound: int = 0, high_bound: int = 1) -> np.ndarray:
    """
    Normalise data to a given boundary. If the data is complex the absolute value ist computed.

    Parameters
    ----------
    data : np.ndarray
        data
    low_bound : int, optional
        lower boundary, by default 0
    high_bound : int, optional
        above boundary, by default 1

    Returns
    -------
    np.ndarray
        absolute and normalized data
    """

    norm_data = []
    diff = high_bound - low_bound
    diff_arr = max(data) - min(data)
    for i in data:
        temp = (((i - min(data)) * diff) / diff_arr) + low_bound
        norm_data.append(temp)
    return np.array(norm_data)


def prepare_all_samples_for_16_el_single(prep_cnf: PreperationConfig):
    """
    Converts all samples inside one directory that were recorded in 16
    electrode mode and save the potential and data to a target directory.
    This function ignores the positional properties e.g. from "enderstat"

    Parameters
    ----------
    prep_cnf : PreperationConfig
        configuration dataclass
    """

    check_result = check_n_el_condition(
        prep_cnf, ch_group_to_check=[1], n_el_to_check=16
    )

    sf_numbering = 0
    if check_result:
        for ch_mod, sample_path in tqdm(enumerate(np.sort(os.listdir(prep_cnf.lpath)))):
            if ch_mod % 10 != 0:
                tmp_sample = np.load(prep_cnf.lpath + sample_path, allow_pickle=True)

                tmp_p_mat = extract_potentials_from_sample_n_el_16(tmp_sample)
                p_without_ext = extract_electrodepotentials(tmp_p_mat, tmp_sample, True)
                p_with_ext = extract_electrodepotentials(tmp_p_mat, tmp_sample, False)

                np.savez(
                    prep_cnf.spath + f"sample_{sf_numbering:06}.npz",
                    potential_matrix=tmp_p_mat,
                    p_with_ext=p_with_ext,
                    p_without_ext=p_without_ext,
                    abs_p_norm_without_ext=np.abs(norm_data(p_without_ext)),
                    v_with_ext=compute_v(p_with_ext),
                    v_without_ext=compute_v(p_without_ext),
                    abs_v_norm_without_ext=norm_data(compute_v(p_without_ext)),
                    config=tmp_sample["config"].tolist().__dict__,
                )
                sf_numbering += 1
            else:
                pass
                # Due to errors inside the ScioSpec software taking only burst_count-1 samples
    else:
        print("Could not start converting.")


def prepare_all_samples_for_16_el(
    prep_cnf: PreperationConfig,
    gen_mesh: bool = True,
    h0: float = 0.05,
    obj_perm: float = 10.0,
    x_y_offset: float = 180,
    tank_r_inner: float = 97.0,
) -> None:
    """
    Converts all samples inside one directory that were recorded in 16
    electrode mode and save the potential and positional data to a target directory.
    Furthermore a mesh is generated.

    Parameters
    ----------
    prep_cnf : PreperationConfig
        configuration dataclass
    gen_mesh : bool, optional
        generate a mesh, by default True
    obj_perm : float, optional
        permittivity of the circle object, by default 10.0
    x_y_offset : float, optional
        Ender 5 x,y-axis offset, by default 180
    tank_r_inner : float, optional
        inner tank radius, by default 97.0
    """

    check_result = check_n_el_condition(
        prep_cnf, ch_group_to_check=[1], n_el_to_check=16
    )

    if gen_mesh:
        mesh_empty = create_empty_2d_mesh(h0=h0)
    sf_numbering = 0
    if check_result:
        for ch_mod, sample_path in tqdm(enumerate(np.sort(os.listdir(prep_cnf.lpath)))):
            if ch_mod % 10 != 0:
                tmp_sample = np.load(prep_cnf.lpath + sample_path, allow_pickle=True)

                ender_stat = tmp_sample["enderstat"].tolist()
                cnfg = tmp_sample["config"].tolist()
                abs_x_pos = (ender_stat["abs_x_pos"] - x_y_offset) / tank_r_inner
                abs_y_pos = (ender_stat["abs_y_pos"] - x_y_offset) / tank_r_inner

                tmp_p_mat = extract_potentials_from_sample_n_el_16(tmp_sample)
                p_without_ext = extract_electrodepotentials(tmp_p_mat, tmp_sample, True)
                p_with_ext = extract_electrodepotentials(tmp_p_mat, tmp_sample, False)

                if gen_mesh:
                    mesh_obj = add_circle_anomaly(
                        mesh_empty, abs_x_pos, abs_y_pos, cnfg.size, obj_perm
                    )
                    np.savez(
                        prep_cnf.spath + f"sample_{sf_numbering:06}.npz",
                        mesh=mesh_obj,
                        potential_matrix=tmp_p_mat,
                        p_with_ext=p_with_ext,
                        p_without_ext=p_without_ext,
                        abs_p_norm_without_ext=np.abs(norm_data(p_without_ext)),
                        v_with_ext=compute_v(p_with_ext),
                        v_without_ext=compute_v(p_without_ext),
                        abs_v_norm_without_ext=norm_data(compute_v(p_without_ext)),
                        r_phi=comp_tank_relative_r_phi(tmp_sample),
                        config=tmp_sample["config"].tolist().__dict__,
                    )
                else:
                    np.savez(
                        prep_cnf.spath + f"sample_{sf_numbering:06}.npz",
                        potential_matrix=tmp_p_mat,
                        p_with_ext=p_with_ext,
                        p_without_ext=p_without_ext,
                        abs_p_norm_without_ext=np.abs(norm_data(p_without_ext)),
                        v_with_ext=compute_v(p_with_ext),
                        v_without_ext=compute_v(p_without_ext),
                        abs_v_norm_without_ext=norm_data(compute_v(p_without_ext)),
                        r_phi=comp_tank_relative_r_phi(tmp_sample),
                        config=tmp_sample["config"].tolist().__dict__,
                    )
                sf_numbering += 1
            else:
                pass
                # Due to errors inside the ScioSpec software taking only burst_count-1 samples
    else:
        print("Could not start converting.")


def compute_v(p: np.ndarray) -> np.ndarray:
    """
    Computes the voltage out of the potential.
    Therefore p[0,1,...,16] - p[1,2,...,0] is computed.

    Parameters
    ----------
    p : np.ndarray
        measured potentials

    Returns
    -------
    np.ndarray
        voltage vector
    """
    v = []
    for i in range(len(p) - 1):
        v.append(p[i] - p[i + 1])
    v.append(p[len(p) - 1] - p[0])

    return np.array(v)
