from pyftdi.ftdi import Ftdi
import struct
from typing import Union
from sciopy.sciopy_dataclasses import (
    ScioSpecMeasurementSetup,
)
import numpy as np


def connect_COM_port_usb_hs(
    url: str = "ftdi://ftdi:232h/1", baudrate: int = 9000
) -> Ftdi:
    """
    Connect the USB-HS Port of the Sciospec device.

    Parameters
    ----------
    url : str, optional
        ftdi driver, by default "ftdi://ftdi:232h/1"
    baudrate : int, optional
        baud rate, by default 9000

    Returns
    -------
    Ftdi
        USB-HS serial connection
    """
    serial = Ftdi().create_from_url(url=url)
    serial.purge_buffers()
    serial.set_bitmode(0x00, Ftdi.BitMode.RESET)
    serial.set_bitmode(0x40, Ftdi.BitMode.SYNCFF)
    serial.PARITY_NONE
    serial.SET_BITS_HIGH
    serial.STOP_BIT_1
    serial.set_baudrate(baudrate)
    return serial


def set_measurement_config_usb_hs(serial: Ftdi, ssms: ScioSpecMeasurementSetup) -> None:
    """
    set_measurement_config sets the ScioSpec device configuration depending on the ssms configuration dataclass.

    Parameters
    ----------
    serial : Ftdi
        USB-HS serial connection
    ssms : ScioSpecMeasurementSetup
        dataclass with the measurement setup settings.
    """

    def clTbt_sp(val: Union[int, float]) -> list:
        """
        clTbt_sp converts an integer or float value to a list of single precision bytes.

        Parameters
        ----------
        val : Union[int, float]
            Value that has to be converted

        Returns
        -------
        list
            list with single precision byte respresentation
        """
        return [int(bt) for bt in struct.pack(">f", val)]

    def clTbt_dp(val: float) -> list:
        """
        clTbt_dp converts an integer or float value to a list of double precision bytes.

        Parameters
        ----------
        val : float
            value that has to be converted

        Returns
        -------
        list
            list with double precision byte respresentation
        """
        return [int(ele) for ele in struct.pack(">d", val)]

    # Set measurement setup:
    serial.write_data(bytearray([0xB0, 0x01, 0x01, 0xB0]))
    # Set burst count: "B0 03 02 00 03 B0" = 3
    serial.write_data(bytearray([0xB0, 0x03, 0x02, 0x00, ssms.burst_count, 0xB0]))

    # Excitation amplitude double precision
    # A_min = 100nA
    # A_max = 10mA
    if ssms.amplitude > 0.01:
        print(
            f"Amplitude {ssms.amplitude}A is out of available range.\nSet amplitude to 10mA."
        )
        ssms.amplitude = 0.01
    serial.write_data(
        bytearray(list(np.concatenate([[176, 9, 5], clTbt_dp(ssms.amplitude), [176]])))
    )

    # ADC range settings: [+/-1, +/-5, +/-10]
    # ADC range = +/-1  : B0 02 0D 01 B0
    # ADC range = +/-5  : B0 02 0D 02 B0
    # ADC range = +/-10 : B0 02 0D 03 B0
    if ssms.adc_range == 1:
        serial.write_data(bytearray([0xB0, 0x02, 0x0D, 0x01, 0xB0]))
    elif ssms.adc_range == 5:
        serial.write_data(bytearray([0xB0, 0x02, 0x0D, 0x02, 0xB0]))
    elif ssms.adc_range == 10:
        serial.write_data(bytearray([0xB0, 0x02, 0x0D, 0x03, 0xB0]))

    # Gain settings:
    # Gain = 1     : B0 03 09 01 00 B0
    # Gain = 10    : B0 03 09 01 01 B0
    # Gain = 100   : B0 03 09 01 02 B0
    # Gain = 1_000 : B0 03 09 01 03 B0
    if ssms.gain == 1:
        serial.write_data(bytearray([0xB0, 0x03, 0x09, 0x01, 0x00, 0xB0]))
    elif ssms.gain == 10:
        serial.write_data(bytearray([0xB0, 0x03, 0x09, 0x01, 0x01, 0xB0]))
    elif ssms.gain == 100:
        serial.write_data(bytearray([0xB0, 0x03, 0x09, 0x01, 0x02, 0xB0]))
    elif ssms.gain == 1_000:
        serial.write_data(bytearray([0xB0, 0x03, 0x09, 0x01, 0x03, 0xB0]))

    # Single ended mode:
    serial.write_data(bytearray([0xB0, 0x03, 0x08, 0x01, 0x01, 0xB0]))

    # Excitation switch type:
    serial.write_data(bytearray([0xB0, 0x02, 0x0C, 0x01, 0xB0]))

    # Set framerate:
    serial.write_data(
        bytearray(list(np.concatenate([[176, 5, 3], clTbt_sp(ssms.framerate), [176]])))
    )

    # Set frequencies:
    # [CT] 0C 04 [fmin] [fmax] [fcount] [ftype] [CT]
    f_min = clTbt_sp(ssms.exc_freq)
    f_max = clTbt_sp(ssms.exc_freq)
    f_count = [0, 1]
    f_type = [0]
    # bytearray
    serial.write_data(
        bytearray(
            list(np.concatenate([[176, 12, 4], f_min, f_max, f_count, f_type, [176]]))
        )
    )

    # Set injection config

    el_inj = np.arange(1, ssms.n_el + 1)
    el_gnd = np.roll(el_inj, -(ssms.inj_skip + 1))

    for v_el, g_el in zip(el_inj, el_gnd):
        serial.write_data(bytearray([0xB0, 0x03, 0x06, v_el, g_el, 0xB0]))

    # Get measurement setup
    serial.write_data(bytearray([0xB1, 0x01, 0x03, 0xB1]))
    # Set output configuration
    serial.write_data(bytearray([0xB2, 0x02, 0x01, 0x01, 0xB2]))
    serial.write_data(bytearray([0xB2, 0x02, 0x03, 0x01, 0xB2]))
    serial.write_data(bytearray([0xB2, 0x02, 0x02, 0x01, 0xB2]))

    ## start measurement
    # serial.write_data(bytearray([0xB4, 0x01, 0x01, 0xB4]))
    # stop measurement
    # serial.write_data(bytearray([0xB4, 0x01, 0x00, 0xB4]))


def SystemMessageCallback_usb_hs(
    serial: Ftdi, prnt_msg: bool = True, ret_hex_int: Union[None, str] = None
):
    """
    Reads the message buffer of a serial connection. Also prints out the general system message.

    Parameters
    ----------
    serial : Ftdi
        USB-HS serial connection
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
        "0x92": "Data holdup: Measurement data could not be sent via the master interface",
    }
    timeout_count = 0
    received = []
    received_hex = []
    data_count = 0

    while True:
        buffer = serial.read_data_bytes(size=1024, attempt=150)
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


def StartStopMeasurement_usb_hs(serial: Ftdi) -> list:
    """
    Start and stop the measurement and return the serial message buffer.

    Parameters
    ----------
    serial : Ftdi
        USB-HS serial connection

    Returns
    -------
    list
        message buffer
    """
    print("Starting measurement.")
    serial.write_data(bytearray([0xB4, 0x01, 0x01, 0xB4]))
    measurement_data_hex = SystemMessageCallback_usb_hs(
        serial, prnt_msg=False, ret_hex_int="hex"
    )
    print("Stopping measurement.")
    serial.write_data(bytearray([0xB4, 0x01, 0x00, 0xB4]))
    SystemMessageCallback_usb_hs(serial, prnt_msg=False, ret_hex_int="int")
    return measurement_data_hex
