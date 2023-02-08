# ScioPY

This package offers the serial interface for communication with an EIT device from ScioSpec. Commands can be written serially and the system response can be read out. With the current version, it is possible to start and stop measurements with defined burst counts and to read out the measurement data. In addition, the measurement data is packed into a data class for better further processing.

## Install Requirements

All requirements are provided inside the `requirements.txt`. To install them navigate inside the sciopy directory and type:

    pip3 install -r requirements.txt # Linux, macOS, Windows
    pip install -r requirements.txt  # Windows


## Provided Python files and functions

### `com_handling.py`

Used for this serial connection.

    - available_serial_ports()
    - connect_COM_port()
    - serial_write()
    - disconnect_COM_port()

### `print_command_info.py` 

None of the listed functions calculate anything or return anything. They just write the appropriate system messages to the console.

    - print_syntax()
    - print_general_system_messages()
    - print_acknowledge_messages()
    - print_command_list()

### `doteit.py` 

The provided functions can handle and compile .eit Files.
It can be used for the transformation between .eit and .npz files for further processing. If the measurement data is aquired due to a serial connection, these functions are not in use.

    - doteit_in_SingleEitFrame()
    - list_eit_files()
    - list_all_files()
    - single_eit_in_pickle()
    - load_pickle_to_dict()
    - convert_fulldir_doteit_to_pickle()
    - convert_fulldir_doteit_to_npz()

### `setup_m.py`

    - SystemMessageCallback()
    - SaveSettings()
    - SoftwareReset()
    - ResetMeasurementSetup()
    - SetMeasurementSetup()
    - GetMeasurementSetup()
    - StartStopMeasurement()
    - del_hex_in_list()
    - bytesarray_to_float()
    - bytesarray_to_int()
    - bytesarray_to_byteslist()
    - reshape_burst_buffer()
    - reduce_burst_to_less_x()
    - parse_single_frame()
    - parse_to_full_frame()
    - GetTemperature()
    - SetBatteryControll()
    - GetBatteryControll()
    - SetLEDControl()
    - GetLEDControl()
    - SetLED_Mode()
    - DisableLED_AutoMode()
    - EnableLED_AutoMode()
    - PowerPlugDetect()
    - GetDevideInfo()
    - GetFirmwareIDs()

### `configurations.py`

Different standard measurement configurations. See the docstring to get further information about the defined settings.

    - configuration_01()
    - configuration_02()
    - configuration_03()
    - configuration_04()
    - configuration_05()

## TBD:

- Insert unknown parameter in `doteit.py`
- Add the type of a serial connection `type(serial)`
- Implement the function `configure_configuration()`

## Version

    0.2.5

## Contact

Email: jacob.thoenes@uni-rostock.de