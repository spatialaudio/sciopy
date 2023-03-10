# TBD: https://stackoverflow.com/questions/3898572/what-are-the-most-common-python-docstring-formats

import struct
from typing import Union, List
from .sciopy_dataclasses import SingleFrame, ScioSpecMeasurementConfig
import numpy as np


def SystemMessageCallback(
    serial, prnt_msg: bool = True, ret_hex_int: Union[None, str] = None
):

    """
    Reads the message buffer of a serial connection. Also prints out the general system message.

    Parameters
    ----------
    serial :
        serial connection
    prnt_msg : bool
        if true print message, if false not
    ret_hex_int : Union[None, str]
        use ['none','hex', 'int', 'both'] to return nothing, hex or integer data or both.

    Returns
    -------
    [None, received_hex, received, (received, received_hex)]
        return depens on the ret_hex_int variable
    """
    msg_dict = {
        "0x01": "No message inside the message buffer",
        "0x02": "Timeout: Communication-timeout (less data than expected)",
        "0x04": "Wake-Up Message: System boot ready",
        "0x11": "TCP-Socket: Valid TCP client-socket connection",
        "0x81": "Not-Acknowledge: Command has not been executed",
        "0x82": "Not-Acknowledge: Command could not be recognized",
        "0x83": "Command-Acknowledge: Command has been executed successfully",
        "0x84": "System-Ready Message: System is operational and ready to receive data",
        "0x91": "Data holdup: Measurement data could not be sent via the master interface",
    }
    timeout_count = 0
    received = []
    received_hex = []
    data_count = 0

    while True:
        buffer = serial.read()
        if buffer:
            received.extend(buffer)
            data_count += len(buffer)
            timeout_count = 0
            continue
        timeout_count += 1
        if timeout_count >= 1:
            # Break if we haven't received any data
            break

        received = "".join(str(received))  # If you need all the data
    received_hex = [hex(receive) for receive in received]
    try:
        msg_idx = received_hex.index("0x18")
        if prnt_msg:
            print(msg_dict[received_hex[msg_idx + 2]])
    except BaseException:
        if prnt_msg:
            print(msg_dict["0x01"])
        prnt_msg = False
    if prnt_msg:
        print("message buffer:\n", received_hex)
        print("message length:\t", data_count)

    if ret_hex_int is None:
        return
    elif ret_hex_int == "hex":
        return received_hex
    elif ret_hex_int == "int":
        return received
    elif ret_hex_int == "both":
        return received, received_hex


def SaveSettings(serial) -> None:
    """
    Save the settings inside the ScioSpec device.

    Parameters
    ----------
    serial :
        serial connection

    Returns
    -------
    None
    """
    serial.write(bytearray([0x90, 0x00, 0x90]))
    SystemMessageCallback(serial)


def SoftwareReset(serial) -> None:
    """
    Reset the ScioSpec software.

    Parameters
    ----------
    serial :
        serial connection

    Returns
    -------
    None
    """
    serial.write(bytearray([0xA1, 0x00, 0xA1]))
    SystemMessageCallback(serial)


def ResetMeasurementSetup(serial):
    """
    Reset the measurement setup.

    Parameters
    ----------
    serial :
        serial connection

    Returns
    -------
    None
    """
    serial.write(bytearray([0xB0, 0x01, 0x01, 0xB0]))
    SystemMessageCallback(serial)


def SetMeasurementSetup(
    serial,
    burst_count: int = 10,
    frame_rate: int = 1,
    exc_freq: list = [100, 100, 1, 0],
    exc_amp: float = 0.01,
) -> None:
    """
    Configurate and write own measurement setup.
    ->!!! TBD !!!<-

    Parameters
    ----------
    serial :
        serial connection to the ScioSpecEIT device.
    burst_count : int
        number of measurement between start and stop command.
    frame_rate : int
        number of measurements per second.
    exc_freq : list
        [fmin, fmax, fcount, ftype] add excitation frequency block in Hz.
    exc_amp : float
        Set excitation amplitude in ampere.

    Further information
    -------------------

    [fmin]
        • minimum frequency fmin
        • 4 Byte floating point single precision value
        • range = 100 Hz - 10 MHz
        • Default: fmin = 100 kHz
    [fmax]
        • maximum frequency fmax
        • 4 Byte floating point single precision value
        • range = 100 Hz - 10 MHz
        • Default: fmax = 100 kHz
    [fcount]
        • frequency count fcount
        • 2 Byte unsigned integer value
        • range = 1 - 128
        • Default: fcount = 1
    [ftype]
        • frequency type ftype
        • 1 Byte unsigned interger value
        • ftype = 0: linear frequency distribution | 1: logarithmic frequency distribution
        • Default: ftype = 0
    [excitation amplitude]
        • 8 Byte Floating Point double precision value.
        • Amin = 100 nA
        • Amax = 10 mA
        • Step size see Chapter “Technical Specification”
        • Default: A = 0.01 A

    Returns
    -------
    None
    """

    def write_part(serial, msg) -> None:
        serial.write(msg)
        SystemMessageCallback(serial)

    if burst_count <= 255:
        burst_count = bytearray([0xB0, 0x03, 0x02, 0x00, burst_count, 0xB0])
        write_part(serial, burst_count)

    frame_rate = bytearray([0xB0, 0x05, 0x03, frame_rate, 0xB0])
    write_part(serial, frame_rate)

    exc_freq = bytearray(
        [0xB0, 0x0C, 0x04, exc_freq[0], exc_freq[1], exc_freq[2], exc_freq[3], 0xB0]
    )
    write_part(serial, exc_freq)

    # exc_amp = bytearray([0xB0, 0x05, 0x05, exc_amp, 0xB0])
    # write_part(serial, exc_amp)

    print("Setup done")


def GetMeasurementSetup(serial) -> None:
    """
    Print information about the current configuration.
    ->!!! TBD !!!<-

    Parameters
    ----------
    serial :
        serial connection

    Returns
    -------
    None
    """
    burst_count = bytearray([0xB1, 0x01, 0x02, 0xB1])
    serial.write(burst_count)
    print("Burst Count:")
    SystemMessageCallback(serial)  # [CT] 03 02 [burst count] [CT]

    frame_rate = bytearray([0xB1, 0x01, 0x03, 0xB1])
    serial.write(frame_rate)
    print("Frame Rate:")
    SystemMessageCallback(serial)  # [CT] 05 03 [frame rate] [CT]

    exc_freq = bytearray([0xB1, 0x01, 0x04, 0xB1])
    serial.write(exc_freq)
    print("Excitation Frequencies:")
    SystemMessageCallback(
        serial
    )  # [CT] [LE] 04 [fmin 1st block] [fmax 1st block] [fcount 1st block] [ftype 1st block] [fmin 2nd block] [fmax 2nd block] [fcount 2nd block] [ftype 2nd block] ... [CT]

    exc_amp = bytearray(
        [0xB1, 0x01, 0x05, 0xB1]
    )  # [CT] 05 05 [excitation amplitude] [CT]
    serial.write(exc_amp)
    print("Excitation Amplitude:")
    SystemMessageCallback(serial)

    exc_seq = bytearray([0xB1, 0x01, 0x06, 0xB1])
    serial.write(exc_seq)
    print("Excitation Sequence:")
    SystemMessageCallback(serial)  # [CT] [LE] 06 [excitation sequence] [CT]

    meas_mode = bytearray([0xB1, 0x01, 0x08, 0xB1])
    serial.write(meas_mode)
    print("Measure Mode:")
    SystemMessageCallback(serial)  # [CT] 03 08 [Mode] [Boundary] [CT]

    gain = bytearray([0xB1, 0x01, 0x09, 0xB1])
    serial.write(gain)
    print("Gain Settings:")
    SystemMessageCallback(serial)  # [CT] [LE] 09 [Mode] [Data] [CT]

    exc_switch = bytearray([0xB1, 0x01, 0x0C, 0xB1])
    serial.write(exc_switch)
    print("Excitation switch type:")
    SystemMessageCallback(serial)  # [CT] 02 0C [Type] [CT]


def SetBurstCount(serial, measuremen_cnf: ScioSpecMeasurementConfig) -> None:
    """
    Set the burst count to one of the provided values [1, 5, 10, 100].

    Parameters
    ----------
    serial :
        serial connection
    measuremen_cnf : ScioSpecMeasurementConfig
        dataclass object with configurations

    Returns
    -------
    None
    """
    if measuremen_cnf.burst_count == 1:
        serial.write(bytearray([0xB0, 0x03, 0x02, 0x00, 0x01, 0xB0]))
    elif measuremen_cnf.burst_count == 5:
        serial.write(bytearray([0xB0, 0x03, 0x02, 0x00, 0x05, 0xB0]))
    elif measuremen_cnf.burst_count == 10:
        serial.write(bytearray([0xB0, 0x03, 0x02, 0x00, 0x0A, 0xB0]))
    elif measuremen_cnf.burst_count == 100:
        serial.write(bytearray([0xB0, 0x03, 0x02, 0x00, 0x64, 0xB0]))
    print(f"Set burst count to {measuremen_cnf.burst_count}.")
    SystemMessageCallback(serial)


def StartStopMeasurement(serial) -> list:
    """
    Start and stop the measurement and return the serial message buffer.

    Parameters
    ----------
    serial :
        serial connection

    Returns
    -------
    list
        message buffer
    """
    print("Starting measurement.")
    serial.write(bytearray([0xB4, 0x01, 0x01, 0xB4]))
    measurement_data_hex = SystemMessageCallback(
        serial, prnt_msg=False, ret_hex_int="hex"
    )
    print("Stopping measurement.")
    serial.write(bytearray([0xB4, 0x01, 0x00, 0xB4]))
    SystemMessageCallback(serial, prnt_msg=False, ret_hex_int="int")
    return measurement_data_hex


def single_hex_to_int(str_num: str) -> int:
    """
    Delete the hexadecimal 0x python notation.

    Parameters
    ----------
    str_num : str
        single hexadecimal string

    Returns
    -------
    int
        integer number
    """
    if len(str_num) == 1:
        str_num = f"0x0{str_num}"
    else:
        str_num = f"0x{str_num}"
    return int(str_num, 16)


def del_hex_in_list(lst: list) -> np.ndarray:
    """
    Delete the hexadecimal 0x python notation.

    Parameters
    ----------
    lst : list
        list of hexadecimals

    Returns
    -------
    np.ndarray
        cleared message
    """
    return np.array(
        [
            "0" + ele.replace("0x", "") if len(ele) == 1 else ele.replace("0x", "")
            for ele in lst
        ]
    )


def bytesarray_to_float(bytes_array: np.ndarray) -> float:
    """
    Converts a bytes array to a float number.

    Parameters
    ----------
    bytes_array : np.ndarray
        array of bytes

    Returns
    -------
    float
        double precision float
    """
    bytes_array = [int(b, 16) for b in bytes_array]
    bytes_array = bytes(bytes_array)
    return struct.unpack("!f", bytes(bytes_array))[0]


def bytesarray_to_int(bytes_array: np.ndarray) -> int:
    """
    Converts a bytes array to int number.

    Parameters
    ----------
    bytes_array : np.ndarray
        array of bytes

    Returns
    -------
    int
        integer number
    """
    bytes_array = bytesarray_to_byteslist(bytes_array)
    return int.from_bytes(bytes_array, "big")


def bytesarray_to_byteslist(bytes_array: np.ndarray) -> list:
    """
    Converts a bytes array to a list of bytes.

    Parameters
    ----------
    bytes_array : np.ndarray
        array of bytes

    Returns
    -------
    list
        list of bytes
    """
    bytes_array = [int(b, 16) for b in bytes_array]
    return bytes(bytes_array)


def reduce_burst_to_less_x(
    brst_cnt: Union[int, list], leq: int = 100
) -> Union[List[int], int]:
    """
    Reduces a given burst count to a list of numbers smaller than a defined border.

    Parameters
    ----------
    burst_count : Union[int, list]
        number of planned measurements between start and stop command
    leq : int
        upper border of measurements between the start and stop commans

    Returns
    -------
    Union[List[int], int]
        burst count as number or list of numbers
    """
    if type(brst_cnt) == list and brst_cnt[-1] > leq:
        rst = brst_cnt[-1] - leq
        brst_cnt[-1] = leq
        brst_cnt.append(rst)
        reduce_burst_to_less_x(brst_cnt, leq)
    if type(brst_cnt) == int and brst_cnt > leq:
        brst_cnt = [leq, brst_cnt - leq]
        reduce_burst_to_less_x(brst_cnt, leq)
    return brst_cnt


def reduce_burst_to_available_parts(
    brst_cnt: int, leq_borders: list = [1, 5, 10, 100]
) -> list:
    """
    Reduces a given burst count to a set of numbers in a defined burst count border list.

    Parameters
    ----------
    burst_count : int
        total number of planned measurements
    leq_borders : list
        list of available burst configurations

    Returns
    -------
    list
        burst counts that have to be configured
    """
    for ele in leq_borders:
        if ele == brst_cnt:
            return [ele]
    for brdrs in leq_borders[::-1]:
        brst_cnt = reduce_burst_to_less_x(brst_cnt, brdrs)
    return brst_cnt


def parse_single_frame(lst_ele: np.ndarray) -> SingleFrame:
    """
    Parse single data to the class SingleFrame.

    Parameters
    ----------
    lst_ele : np.ndarray
        single measurement list element

    Returns
    -------
    SingleFrame
        dataclass eit frame
    """
    channels = {}
    enum = 0
    for i in range(11, 135, 8):
        enum += 1
        channels[f"ch_{enum}"] = complex(
            bytesarray_to_float(lst_ele[i : i + 4]),
            bytesarray_to_float(lst_ele[i + 4 : i + 8]),
        )

    excitation_stgs = np.array([single_hex_to_int(ele) for ele in lst_ele[3:5]])

    sgl_frm = SingleFrame(
        start_tag=lst_ele[0],
        channel_group=int(lst_ele[2]),
        excitation_stgs=excitation_stgs,
        frequency_row=lst_ele[5:7],
        timestamp=bytesarray_to_int(lst_ele[7:11]),
        **channels,
        end_tag=lst_ele[139],
    )
    return sgl_frm


def reshape_full_message_in_bursts(
    lst: list, cnf: ScioSpecMeasurementConfig
) -> np.ndarray:
    """
    Takes the full message buffer and splits this message depeding on the measurement configuration into the
    burst count parts.

    Parameters
    ----------
    lst : list
        full message buffer
    cnf : ScioSpecMeasurementConfig
        dataclass object configuration file

    Returns
    -------
    np.ndarray
        eit frame

    Examples
    --------
    - input: n_el=16 -> lst.shape=(44804) | n_el=32 -> lst.shape=(89604,)
    - delete acknowledgement message: lst.shape=(4480,0) | lst.shape=(89600,)
    - split this depending on burst count: split_list.shape=(5, 8960) | split_list.shape=(5, 17920)
    """
    split_list = []
    # delete acknowledgement message
    lst = lst[4:]
    # split in burst count messages
    split_length = lst.shape[0] // cnf.burst_count
    for split in range(cnf.burst_count):
        split_list.append(lst[split * split_length : (split + 1) * split_length])
    return np.array(split_list)


def split_bursts_in_frames(
    split_list: np.ndarray, cnf: ScioSpecMeasurementConfig
) -> np.ndarray:
    """
    Takes the splitted list from `reshape_full_message_in_bursts()` and parses the single frames.


    Parameters
    ----------
    split_list : np.ndarray
        splitted input list
    cnf : ScioSpecMeasurementConfig
        dataclass object configuration file

    Returns
    -------
    np.ndarray
        channel depending burst frames
    """
    msg_len = 140  # Constant
    frame = []  # Channel group depending frame
    burst_frame = []  # single burst count frame with channel depending frame
    subframe_length = split_list.shape[1] // msg_len
    for bursts in range(cnf.burst_count):  # Iterate over bursts
        tmp_split_list = np.reshape(split_list[bursts], (subframe_length, msg_len))
        for subframe in range(subframe_length):
            parsed_sgl_frame = parse_single_frame(tmp_split_list[subframe])
            # Select the right channel group data
            if parsed_sgl_frame.channel_group in cnf.channel_group:
                frame.append(parsed_sgl_frame)
        burst_frame.append(frame)
        frame = []  # Reset channel depending single burst frame
    return np.array(burst_frame)


def GetTemperature(serial) -> float:
    """
    Get temperature value.

    ->!!! TBD !!!<-

    Parameters
    ----------
    serial :
        serial connection

    Returns
    -------
    float
        temperature value
    """
    print("No temperature sensor available")


def SetBatteryControll(serial) -> None:
    """
    Set batterie controll.

    ->!!! TBD !!!<-

    Parameters
    ----------
    serial :
        serial connection

    Returns
    -------
    None
    """
    print("->!!! TBD !!!<-")


def GetBatteryControll(serial) -> None:
    """
    Get batterie controll information.

    ->!!! TBD !!!<-

    Parameters
    ----------
    serial :
        serial connection

    Returns
    -------
    None
    """
    print("->!!! TBD !!!<-")


def SetLEDControl(serial, led: int, mode: str) -> None:
    """
    Disable or enable auto mode.

    Parameters
    ----------
    serial :
        serial connection
    led : int
        [1,2,3,4] led number
    mode : str
        ['enable','disable'] mode

    Returns
    -------
    None
    """
    if mode == "disable":
        MODE = 0x00
    elif mode == "enable":
        MODE = 0x01

    byte_arr = bytearray([0xC8, 0x03, 0x01, led, MODE, 0xC8])
    serial.write(byte_arr)
    SystemMessageCallback(serial)


def GetLEDControl(serial, led: int, mode: str) -> None:
    """
    Set a defined led to mode off, on or blink.

    Parameters
    ----------
    serial :
        serial connection
    led : int
        [1,2,3,4] led number
    mode : str
        ['enable','disable', 'blink'] mode

    Returns
    -------
    None
    """
    if mode == "disable":
        MODE = 0x00
    elif mode == "enable":
        MODE = 0x01
    elif mode == "blink":
        MODE = 0x02

    byte_arr = bytearray([0xC8, 0x03, 0x02, led, MODE, 0xC8])
    print("sent:", byte_arr)
    serial.write(byte_arr)
    SystemMessageCallback(serial)


def SetLED_Mode(serial, led: int, mode: str) -> None:
    """
    Set a defined led to a mode.

    Parameters
    ----------
    serial :
        serial connection
    led : int
        [1,2,3,4] led number
    mode : str
        ['enable','disable', 'blink'] mode

    Returns
    -------
    None
    """
    # Disable automode
    serial.write(bytearray([0xC8, 0x03, 0x01, led, 0x00, 0xC8]))
    SystemMessageCallback(serial)
    if mode == "disable":
        MODE = 0x00
    elif mode == "enable":
        MODE = 0x01
    elif mode == "blink":
        MODE = 0x02
    serial.write(bytearray([0xC8, 0x03, 0x02, led, MODE, 0xC8]))
    SystemMessageCallback(serial)


def DisableLED_AutoMode(serial) -> None:
    """
    Disable automode of all LEDs.

    Parameters
    ----------
    serial :
        serial connection

    Returns
    -------
    None
    """
    serial.write(bytearray([0xC8, 0x03, 0x01, 0x01, 0x00, 0xC8]))
    SystemMessageCallback(serial)
    serial.write(bytearray([0xC8, 0x03, 0x01, 0x02, 0x00, 0xC8]))
    SystemMessageCallback(serial)
    serial.write(bytearray([0xC8, 0x03, 0x01, 0x03, 0x00, 0xC8]))
    SystemMessageCallback(serial)
    serial.write(bytearray([0xC8, 0x03, 0x01, 0x04, 0x00, 0xC8]))
    SystemMessageCallback(serial)


def EnableLED_AutoMode(serial) -> None:
    """
    Enable automode of all LEDs.

    Parameters
    ----------
    serial :
        serial connection

    Returns
    -------
    None
    """
    serial.write(bytearray([0xC8, 0x03, 0x01, 0x01, 0x01, 0xC8]))
    SystemMessageCallback(serial)
    serial.write(bytearray([0xC8, 0x03, 0x01, 0x02, 0x01, 0xC8]))
    SystemMessageCallback(serial)
    serial.write(bytearray([0xC8, 0x03, 0x01, 0x03, 0x01, 0xC8]))
    SystemMessageCallback(serial)
    serial.write(bytearray([0xC8, 0x03, 0x01, 0x04, 0x01, 0xC8]))
    SystemMessageCallback(serial)


def PowerPlugDetect(serial) -> None:
    """
    Print power plug detect information.

    Parameters
    ----------
    serial :
        serial connection

    Returns
    -------
    None
    """
    serial.write(bytearray([0xCC, 0x01, 0x81, 0xCC]))
    SystemMessageCallback(serial)


def GetDevideInfo(serial) -> None:
    """
    Print device information.

    Parameters
    ----------
    serial :
        serial connection

    Returns
    -------
    None
    """
    serial.write(bytearray([0xD1, 0x00, 0xD1]))
    SystemMessageCallback(serial)


def GetFirmwareIDs(serial) -> None:
    """
    Print devide firmware.

    Parameters
    ----------
    serial :
        serial connection

    Returns
    -------
    None
    """
    serial.write(bytearray([0xD2, 0x00, 0xD2]))
    SystemMessageCallback(serial)
