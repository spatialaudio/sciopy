# TBD: https://stackoverflow.com/questions/3898572/what-are-the-most-common-python-docstring-formats

import struct
from typing import Union, List
from .sciopy_dataclasses import SingleFrame
import numpy as np


def SystemMessageCallback(
    serial, prnt_msg: bool = True, ret_hex_int: Union[None, str] = None
):
    """Reads the message buffer of a serial connection. Also prints out the general system message.
    serial      ... serial connection
    prnt_msg    ... print out the buffer
    ret_hex_int ... Parameters -> ['none','hex', 'int', 'both']

    @v=1.0.4
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

    if ret_hex_int == None:
        return
    elif ret_hex_int == "hex":
        return received_hex
    elif ret_hex_int == "int":
        return received
    elif ret_hex_int == "both":
        return received, received_hex


def SaveSettings(serial) -> None:
    serial.write(bytearray([0x90, 0x00, 0x90]))
    SystemMessageCallback(serial)


def SoftwareReset(serial) -> None:
    serial.write(bytearray([0xA1, 0x00, 0xA1]))
    SystemMessageCallback(serial)


def ResetMeasurementSetup(serial):
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
    serial      ... Serial connection to the ScioSpecEIT device.
    burst_count ... Number of frames generated before measurement stops automatically.
    frame_rate  ... Number of EIT-frames per second.
    exc_freq    ... Add excitation frequency block in Hz: [fmin, fmax, fcount, ftype]
    exc_amp     ... Set excitation amplitude in ampere.

    Further information:

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
    """Get information about:
    - Burst Count
    - Frame Rate
    - Excitation Frequencies
    - Excitation Amplitude
    - Excitation Sequence
    - Single-Ended or Differential Measure Mode
    - Gain Settings
    - Excitation Switch Type
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


def SetOutputConfiguration(
    serial, exc_settings: int, curr_row_freq_stack: int, timestamp: int
) -> None:
    """
    This command is used to enable or disable additional information in output data stream of measured data (see
    section "Measured Data"). This command is only valid while no measurement is ongoing. In this case a not
    acknowledge (NACK) is returned.

    Excitation setting
        Enable or disable Excitation setting (additional 2 Byte in output stream).

        Syntax
        • Syntax set: [CT] 02 01 [enable/disable] [CT] [enable/disable]
        • 1 Byte unsigned integer value
        • 0 - disable, 1 - enable
    Current row in the frequency stack
        Enable or disable current row in the frequency stack (additional 2 Byte in output stream)

        Syntax
        • Syntax set: [CT] 02 02 [enable/disable] [CT] [enable/disable]
        • 1 Byte unsigned integer value
        • 0 - disable, 1 - enable
    Timestamp
        Enable or disable timestamp (additional 4 Byte in output stream).

        Syntax
        • Syntax set: [CT] 02 03 [enable/disable] [CT]
    """
    # write excitation setting
    serial.write(bytearray([0xB2, 0x02, 0x01, exc_settings, 0xB2]))
    SystemMessageCallback(serial)

    # write current row in the frequency stack
    serial.write(bytearray([0xB2, 0x02, 0x02, curr_row_freq_stack, 0xB2]))
    SystemMessageCallback(serial)

    # write timestamp
    serial.write(bytearray([0xB2, 0x02, 0x03, timestamp, 0xB2]))
    SystemMessageCallback(serial)


def GetOutputConfiguration(serial) -> None:
    """Returns the display option in the data stream of measured date."""
    pass


def StartStopMeasurement(serial) -> list:
    print("Starting measurement.")
    serial.write(bytearray([0xB4, 0x01, 0x01, 0xB4]))
    measurement_data_hex = SystemMessageCallback(
        serial, prnt_msg=False, ret_hex_int="hex"
    )
    print("Stopping measurement.")
    serial.write(bytearray([0xB4, 0x01, 0x00, 0xB4]))
    SystemMessageCallback(serial, prnt_msg=False, ret_hex_int="int")
    return measurement_data_hex


def del_hex_in_list(lst: list) -> np.ndarray:
    return np.array(
        [
            "0" + ele.replace("0x", "") if len(ele) == 1 else ele.replace("0x", "")
            for ele in lst
        ]
    )


def bytesarray_to_float(bytes_array: np.ndarray) -> float:
    bytes_array = [int(b, 16) for b in bytes_array]
    bytes_array = bytes(bytes_array)
    return struct.unpack("!f", bytes(bytes_array))[0]


def bytesarray_to_int(bytes_array: np.ndarray) -> int:
    bytes_array = bytesarray_to_byteslist(bytes_array)
    return int.from_bytes(bytes_array, "big")


def bytesarray_to_byteslist(bytes_array: np.ndarray) -> list:
    bytes_array = [int(b, 16) for b in bytes_array]
    return bytes(bytes_array)


def reshape_burst_buffer(lst: np.ndarray, burst_count: int) -> list:
    """TBD"""
    full_frame_len, shape_x, shape_y = 17920, 128, 140
    lst = lst[4:]
    full_frame = []
    for burst in range(burst_count):
        tmp_lst = lst[
            burst * full_frame_len : (burst + 1) * full_frame_len
        ]  # Select burst part
        full_frame.append(tmp_lst.reshape(shape_x, shape_y))
    return full_frame


def reduce_burst_to_less_x(
    brst_cnt: Union[int, list], leq: int = 100
) -> Union[List[int], int]:
    """TBD"""
    if type(brst_cnt) == list and brst_cnt[-1] > leq:
        rst = brst_cnt[-1] - leq
        brst_cnt[-1] = leq
        brst_cnt.append(rst)
        reduce_burst_to_less_x(brst_cnt, leq)
    if type(brst_cnt) == int and brst_cnt > leq:
        brst_cnt = [leq, brst_cnt - leq]
        reduce_burst_to_less_x(brst_cnt, leq)
    return brst_cnt


reduce_burst_to_less_x(520, 49)


def parse_single_frame(lst_ele: np.ndarray) -> SingleFrame:
    channels = {}
    enum = 0
    for i in range(11, 135, 8):
        enum += 1
        channels[f"ch_{enum}"] = complex(
            bytesarray_to_float(lst_ele[i : i + 4]),
            bytesarray_to_float(lst_ele[i + 4 : i + 8]),
        )

    excitation_stgs = np.array([ele for ele in lst_ele[3:5]])

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


def parse_to_full_frame(measurement_data: np.ndarray) -> np.ndarray:
    """Parses any measured byte representation into the dataclass SingleFrame"""
    data_frame = []
    for i, sf in enumerate(measurement_data):
        data_frame.append(parse_single_frame(sf))
    return np.array(data_frame)


def GetTemperature() -> None:
    print("No temperature sensor available")


def SetBatteryControll():
    """TBD"""


def GetBatteryControll():
    """TBD"""


def SetLEDControl(serial, led: int, mode: str) -> None:
    """
    Disable or enable auto mode.
    serial: serial connection
    led: number of led 1,2,3 or 4
        #1 ... Ready
        #2 ... Measure
        #3 ... ---
        #4 ... Status
    mode: "enable" or "disable"
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
    serial: serial connection
    led: number of led 1,2,3 or 4
        #1 ... Ready
        #2 ... Measure
        #3 ... ---
        #4 ... Status
    mode: "enable", "disable" or "blink"
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
    serial: serial connection
    led: number of led 1,2,3 or 4
        #1 ... Ready
        #2 ... Measure
        #3 ... ---
        #4 ... Status
    mode: "enable", "disable" or "blink"
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
    """Disable automode of all LEDs."""
    serial.write(bytearray([0xC8, 0x03, 0x01, 0x01, 0x00, 0xC8]))
    SystemMessageCallback(serial)
    serial.write(bytearray([0xC8, 0x03, 0x01, 0x02, 0x00, 0xC8]))
    SystemMessageCallback(serial)
    serial.write(bytearray([0xC8, 0x03, 0x01, 0x03, 0x00, 0xC8]))
    SystemMessageCallback(serial)
    serial.write(bytearray([0xC8, 0x03, 0x01, 0x04, 0x00, 0xC8]))
    SystemMessageCallback(serial)


def EnableLED_AutoMode(serial) -> None:
    """Enable automode of all LEDs."""
    serial.write(bytearray([0xC8, 0x03, 0x01, 0x01, 0x01, 0xC8]))
    SystemMessageCallback(serial)
    serial.write(bytearray([0xC8, 0x03, 0x01, 0x02, 0x01, 0xC8]))
    SystemMessageCallback(serial)
    serial.write(bytearray([0xC8, 0x03, 0x01, 0x03, 0x01, 0xC8]))
    SystemMessageCallback(serial)
    serial.write(bytearray([0xC8, 0x03, 0x01, 0x04, 0x01, 0xC8]))
    SystemMessageCallback(serial)


def FrontIOs():
    """TBD"""
    pass


def PowerPlugDetect(serial) -> None:
    serial.write(bytearray([0xCC, 0x01, 0x81, 0xCC]))
    SystemMessageCallback(serial)


def GetDevideInfo(serial) -> None:
    """Get device info"""
    serial.write(bytearray([0xD1, 0x00, 0xD1]))
    SystemMessageCallback(serial)


def TCP_ConnectionWatchdog():
    """TBD"""
    pass


def GetFirmwareIDs(serial) -> None:
    """Get firmware IDs"""
    serial.write(bytearray([0xD2, 0x00, 0xD2]))
    SystemMessageCallback(serial)
