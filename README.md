# ScioPY

This package offers the serial interface for communication with an EIT device from ScioSpec. Commands can be written serially and the system response can be read out. With the current version, it is possible to start and stop measurements with defined burst counts and to read out the measurement data. In addition, the measurement data is packed into a data class for better further processing.

## Install Requirements

All requirements are provided inside the `requirements.txt`. To install them navigate inside the sciopy directory and type:

    pip3 install -r requirements.txt # Linux, macOS, Windows
    pip install -r requirements.txt  # Windows

## TBD:

- Insert unknown parameter in `doteit.py`
- Add the type of a serial connection `type(serial)`
- Implement the function `configure_configuration()`

## Version

    0.2.8

## Contact

Email: jacob.thoenes@uni-rostock.de