# ScioPY

This package contains functions and routiness to communicate with the ScioSpec-EIT device

## Install Requirements

All requirements are provided inside the `requirements.txt`. To install them navigate inside the sciopy directory and type:

    pip3 install -r requirements.txt # Linux, macOS, Windows
    pip install -r requirements.txt  # Windows


## Existing Python files

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

**(WIP)** Programming goal: Handling of the data stream within a serial connection of the ScioSpecEIT device.


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


## ToDo:

- Insert unknown parameter in `doteit.py`
- Add the type of a serial connection `type(serial)`


## Version

    1.0

## Contact

Email: jacob.thoenes@uni-rostock.de