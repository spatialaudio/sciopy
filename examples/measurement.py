import numpy as np

from sciopy import (
    SystemMessageCallback,
    conf_n_el_16_adjacent,
    connect_COM_port,
    StartStopMeasurement,
    reshape_full_message_in_bursts,
    del_hex_in_list,
    split_bursts_in_frames,
)

from sciopy.sciopy_dataclasses import ScioSpecMeasurementConfig

scio_spec_measurement_config = ScioSpecMeasurementConfig(
    com_port="COM3",
    burst_count=10,
    n_el=16,
    channel_group=[1],
    actual_sample=0,
    s_path="",
    object="circle",
    size=0.1,
    material="PLA",
    saline_conductivity=0.0,
    temperature=20.0,
    water_lvl=20.0,
    exc_freq=10000.0,
)

# Connect ScioSpec device
COM_ScioSpec = connect_COM_port(port="COM3")
# Send configuration
scio_spec_measurement_config = conf_n_el_16_adjacent(
    COM_ScioSpec, scio_spec_measurement_config
)
# Read out system callback
SystemMessageCallback(COM_ScioSpec, prnt_msg=True)

# Start and stop single measurement
measurement_data_hex = StartStopMeasurement(COM_ScioSpec)
# Delete hex in mesured buffer
measurement_data = del_hex_in_list(measurement_data_hex)
# Reshape the full mesaurement buffer. Depending on number of electrodes
split_measurement_data = reshape_full_message_in_bursts(
    measurement_data, scio_spec_measurement_config
)
measurement_data = split_bursts_in_frames(
    split_measurement_data, scio_spec_measurement_config
)

# Set to "True" to save single measurement
save = False

if save:
    files_offset = scio_spec_measurement_config.actual_sample
    for bursts in measurement_data:
        np.savez(
            scio_spec_measurement_config.s_path
            + "sample_{0:06d}.npz".format(files_offset),
            config=scio_spec_measurement_config,
            data=bursts,
        )
        files_offset += 1
        scio_spec_measurement_config.actual_sample = files_offset

    SystemMessageCallback(COM_ScioSpec, prnt_msg=False)
