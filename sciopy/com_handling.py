try:
    import serial
except ImportError:
    print("Could not import module: serial")

import sys
import glob


def available_serial_ports() -> list:
    """
    Lists serial port names.

    Returns
    -------
    list
        a list of the serial ports available on the system

    Raises
    ------
    EnvironmentError
        on unsupported or unknown platforms
    OtherError
        when an other error
    """
    if sys.platform.startswith("win"):
        ports = ["COM%s" % (i + 1) for i in range(256)]
    elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob("/dev/tty[A-Za-z]*")
    elif sys.platform.startswith("darwin"):
        ports = glob.glob("/dev/tty.*")
    else:
        raise EnvironmentError("Unsupported platform")

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def connect_COM_port(port: str = "COM3", baudrate: int = 9600, timeout: int = 1):
    """
    Etablishes a serial connection to a com port.

    Parameters
    ----------
    port : str = "COM3"
        name of the com port
    baudrate : int = 9600
        communication rate
    timeout : = 1
        timeout in seconds if no connection is available

    Returns
    -------
    serial
        a serial connection
    """
    ser = serial.Serial(
        port=port,
        baudrate=baudrate,
        timeout=timeout,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
    )

    print("Connection to", ser.name, "is established.")
    return ser


def serial_write(ser, cmd: str) -> None:
    """
    Write a string to a serial connection.

    Parameters
    ----------
    ser :
        serial connection
    cmd : str
        message to write

    Returns
    -------
    None
    """
    ser.write(cmd)


def disconnect_COM_port(ser) -> None:
    """
    Disconnect serial connection.

    Parameters
    ----------
    ser :
        serial connection

    Returns
    -------
    None
    """
    ser.close()
    print("Disconnected from {port}.".format(port=ser.name))
