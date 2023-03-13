# ![sciopy](https://github.com/spatialaudio/sciopy/blob/main/doc/images/logo_sciopy.png)


This package offers the serial interface for communication with an EIT device from ScioSpec. Commands can be written serially and the system response can be read out. With the current version, it is possible to start and stop measurements with defined burst counts and to read out the measurement data. In addition, the measurement data is packed into a data class for better further processing.

## Install Requirements

All requirements are provided inside the `requirements.txt`. To install them navigate inside the sciopy directory and type:

    pip3 install -r requirements.txt # Linux, macOS, Windows
    pip install -r requirements.txt  # Windows

## Run Example Script

For a single measurement, you can simply run the `measurement.py` script using the command:

    python measurement.py

This script establishes a serial connection to the ScioSpec device, sends the measurement configuration, and starts a 
measurement with a burst count of 10. For a successful measurement, you have to plug in the 16 electrodes to the port "channel 1-16" at the ScioSpec device. For saving the data, set `save = True` and insert a valid `s_path` to the `scio_spec_measurement_config` at the beginning of the script.

The second provided example script `prep_data_for_ml.py` can be used for the conversion of a finished measurement.
This script creates a new folder with the ending `_prepared` and puts together the potential values and object positions for all measurements. This could be useful for later application of machine learning. 


## TBD

- Measurement using 32 electrodes.
- Parsing measurements of 32 electrodes.
- Adjacent and opposite drive patterns for 32 electrodes.

## Contact

Email: jacob.thoenes@uni-rostock.de

```bibtex
@Unpublished{Thoenes2023,
  author = {Jacob Perter Thönes},
  title  = {Python based interface module for serial communication with the ScioSpec Electrical Impedance Tomography (EIT) device.},
  year   = {2023},
}
```