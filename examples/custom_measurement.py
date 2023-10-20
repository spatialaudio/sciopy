import numpy as np

from sciopy import (
    SystemMessageCallback,
    set_measurement_config,
    connect_COM_port,
    StartStopMeasurement,
    reshape_full_message_in_bursts,
    del_hex_in_list,
    split_bursts_in_frames,
)

from sciopy.sciopy_dataclasses import ScioSpecMeasurementSetup

s_path = ""
files_offset = 0

sciospec_measurement_setup = ScioSpecMeasurementSetup(
    burst_count=1,  # The number of measurements to be performed.
    total_meas_num=10,  # Repetitions of burst count
    n_el=64,  # Set 16, 32, 48 or 64 and do not forget to change the channel_group.
    channel_group=[
        1,
        2,
        3,
        4,
    ],  # Use [1] for n_el=16, [1,2] for n_el=32, [1,2,3] for n_el=48, and [1,2,3,4] for n_el=64
    exc_freq=10_000,  # 10,000Hz = 10kHz
    framerate=5,  # Measurements per second
    amplitude=0.01,  # 0.01A = 10mA (maximum)
    inj_skip=0,  # injection electrode skip
    gain=1,
    adc_range=1,  # +/- 1V
    notes="None",  # add measurement information
    configured=False,
)

# Connect ScioSpec device
COM_ScioSpec = connect_COM_port(port="/dev/ttyACM0")

# Send configuration
set_measurement_config(serial=COM_ScioSpec, ssms=sciospec_measurement_setup)

# Read out system callback
SystemMessageCallback(COM_ScioSpec, prnt_msg=True)

# Start and stop single measurement
measurement_data_hex = StartStopMeasurement(COM_ScioSpec)
# Delete hex in mesured buffer
measurement_data = del_hex_in_list(measurement_data_hex)
# Reshape the full mesaurement buffer. Depending on number of electrodes
split_measurement_data = reshape_full_message_in_bursts(
    measurement_data, sciospec_measurement_setup
)
measurement_data = split_bursts_in_frames(
    split_measurement_data, sciospec_measurement_setup
)

# Set to "True" to save single measurement
save = True

if save:
    for bursts in measurement_data:
        np.savez(
            s_path + "sample_{0:06d}.npz".format(files_offset),
            config=sciospec_measurement_setup,
            data=bursts,
        )
        files_offset += 1
    SystemMessageCallback(COM_ScioSpec, prnt_msg=False)
