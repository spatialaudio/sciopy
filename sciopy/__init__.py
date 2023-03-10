from .doteit import (
    doteit_in_SingleEitFrame,
    list_eit_files,
    list_all_files,
    single_eit_in_pickle,
    load_pickle_to_dict,
    convert_fulldir_doteit_to_pickle,
    convert_fulldir_doteit_to_npz,
)

from .com_handling import (
    available_serial_ports,
    connect_COM_port,
    serial_write,
    disconnect_COM_port,
)

from .print_command_info import (
    print_syntax,
    print_general_system_messages,
    print_acknowledge_messages,
    print_command_list,
)

from .prepare_data import create_prep_directory, prepare_all_samples_for_16_el

from .visualization import plot_el_sign, plot_potential_matrix, plot_completeness

from .setup_m import (
    SystemMessageCallback,
    SaveSettings,
    SoftwareReset,
    ResetMeasurementSetup,
    SetMeasurementSetup,
    GetMeasurementSetup,
    SetBurstCount,
    StartStopMeasurement,
    single_hex_to_int,
    del_hex_in_list,
    bytesarray_to_float,
    bytesarray_to_int,
    bytesarray_to_byteslist,
    reduce_burst_to_less_x,
    reduce_burst_to_available_parts,
    parse_single_frame,
    reshape_full_message_in_bursts,
    split_bursts_in_frames,
    GetTemperature,
    SetBatteryControll,
    GetBatteryControll,
    SetLEDControl,
    GetLEDControl,
    SetLED_Mode,
    DisableLED_AutoMode,
    EnableLED_AutoMode,
    PowerPlugDetect,
    GetDevideInfo,
    GetFirmwareIDs,
)

from .configurations import (
    conf_n_el_16_adjacent,
    conf_n_el_32_adjacent,
    conf_n_el_16_opposite,
    conf_n_el_32_opposite,
    configuration_01,
    configuration_02,
    configuration_03,
    configuration_04,
    configuration_05,
    configure_configuration,
)

from .npztocsv import (
    clear_s_dict,
    single_measurement_to_csv_n_el_16,
    convert_measurement_directory_n_el_16,
    convert_measurement_directory_n_el_16_r_split,
)

# TBD from .configurations import configuration_01

__all__ = [
    # .doteit
    "doteit_in_SingleEitFrame",
    "list_eit_files",
    "list_all_files",
    "single_eit_in_pickle",
    "load_pickle_to_dict",
    "convert_fulldir_doteit_to_pickle",
    "convert_fulldir_doteit_to_npz",
    # .com_handling
    "available_serial_ports",
    "connect_COM_port",
    "serial_write",
    "disconnect_COM_port",
    # .print_command_info
    "print_syntax",
    "print_general_system_messages",
    "print_acknowledge_messages",
    "print_command_list",
    # .setup_m
    "SystemMessageCallback",
    "SaveSettings",
    "SoftwareReset",
    "ResetMeasurementSetup",
    "SetMeasurementSetup",
    "GetMeasurementSetup",
    "SetBurstCount",
    "StartStopMeasurement",
    "single_hex_to_int",
    "del_hex_in_list",
    "bytesarray_to_float",
    "bytesarray_to_int",
    "bytesarray_to_byteslist",
    "reduce_burst_to_less_x",
    "reduce_burst_to_available_parts",
    "parse_single_frame",
    "reshape_full_message_in_bursts",
    "split_bursts_in_frames",
    "GetTemperature",
    "SetBatteryControll",
    "GetBatteryControll",
    "SetLEDControl",
    "GetLEDControl",
    "SetLED_Mode",
    "DisableLED_AutoMode",
    "EnableLED_AutoMode",
    "PowerPlugDetect",
    "GetDevideInfo",
    "GetFirmwareIDs",
    # .configurations
    "conf_n_el_16_adjacent",
    "conf_n_el_32_adjacent",
    "conf_n_el_16_opposite",
    "conf_n_el_32_opposite",
    "configuration_01",
    "configuration_02",
    "configuration_03",
    "configuration_04",
    "configuration_05",
    "configure_configuration",
    # .prepare_data
    "create_prep_directory",
    "prepare_all_samples_for_16_el",
    # .visualization
    "plot_potential_matrix",
    "plot_el_sign",
    "plot_completeness",
    # .npztocsv
    "clear_s_dict",
    "single_measurement_to_csv_n_el_16",
    "convert_measurement_directory_n_el_16",
    "convert_measurement_directory_n_el_16_r_split",
]
