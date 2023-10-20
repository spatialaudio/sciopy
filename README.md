# ![sciopy](https://raw.githubusercontent.com/spatialaudio/sciopy/dev/doc/images/logo_sciopy.jpg)

This package offers the serial interface for communication with an EIT device from ScioSpec. Commands can be written serially and the system response can be read out. With the current version, it is possible to start and stop measurements with defined burst counts and to read out the measurement data. In addition, the measurement data is packed into a data class for better further processing.

## Install Requirements

All requirements are provided inside the `requirements.txt`. To install them navigate inside the sciopy directory and type:

    pip3 install -r requirements.txt # Linux, macOS, Windows
    pip install -r requirements.txt  # Windows

## Run Example Script

For a single measurement, you can simply run one of the `example` scripts using the command:

    python custom_measurement.py

To fing the right port you can use:


    from sciopy import available_serial_ports
    available_serial_ports()

This script establishes a serial connection to the ScioSpec device, sends the measurement configuration, and starts a 
measurement. For a successful measurement with 16 electordes, you have to plug in the 16 electrodes to the port "channel 1-16" at the ScioSpec device. For saving the data, set `save = True` and insert a valid `s_path` to the `scio_spec_measurement_config` at the beginning of the script. If you don't change the path the files will be saved to the current directory.

The example script `prep_data_for_ml.py` can be used for the conversion of a finished measurement.
This script creates a new folder with the ending `_prepared` and puts together the potential values and object positions for all measurements. This could be useful for later application of machine learning. 

## Explanation of stored files (.npz)

- `potential matrix` (e.g. variable P) is a 16x16 matrix (n_el=16). If you visualize it using `from sciopy import plot_potential_matrix` you can recognize the used excitation pattern or if an electrode is a defect.
- `p_with_exc` is the matrix P with the excitation electrodes
- `p_without_exc` is the matrix P without the excitation electrodes
- `abs_p_norm_without_ext` is the matrix, normalized between (I think) 0-1 without the excitation electrodes.
- `v_with_ext` is the computed voltage from the potential values containing the excitation electrodes
- `v_without_ext` is the computed voltage from the potential values without the excitation electrodes
- `abs_v_norm_without_ext` is the voltage data, normalized between 0-1 without the excitation electrodes.
- `config` contains some information regarding the measurement procedure.

## Contact

If you have ideas or other advises don't hesitate to contact me!

Email: jacob.thoenes@uni-rostock.de
