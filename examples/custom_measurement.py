import numpy as np

from sciopy import (
    SystemMessageCallback,
    sciospec_measurement,
    connect_COM_port_usb_hs,
    set_measurement_config_usb_hs,
    SystemMessageCallback_usb_hs,
)

from sciopy.sciopy_dataclasses import ScioSpecMeasurementSetup

s_path = ""

Sciospec = connect_COM_port_usb_hs()

ssms = ScioSpecMeasurementSetup(
    burst_count=1,  # The number of measurements to be performed.
    total_meas_num=1,  # Repetitions of burst count
    n_el=32,  # Set 16, 32, 48 or 64 and do not forget to change the channel_group.
    channel_group=[
        1,
        2,
    ],  # Use [1] for n_el=16, [1,2] for n_el=32, [1,2,3] for n_el=48, and [1,2,3,4] for n_el=64
    exc_freq=125_000,  # 10,000Hz = 10kHz
    framerate=10,  # Measurements per second
    amplitude=0.01,  # 0.01A = 10mA (maximum)
    inj_skip=16,  # injection electrode skip
    gain=1,
    adc_range=1,  # +/- 1V
    notes="test measurement",  # add measurement information
    configured=True,
)

set_measurement_config_usb_hs(Sciospec, ssms)
SystemMessageCallback_usb_hs(Sciospec, prnt_msg=True)

sciospec_data = sciospec_measurement(Sciospec, ssms)

file_idx = 0
for bursts in sciospec_data:
    np.savez(
        s_path + "sample_{0:06d}.npz".format(file_idx),
        config=ssms,
        data=bursts,
    )
    file_idx += 1
SystemMessageCallback(COM_ScioSpec, prnt_msg=False)
