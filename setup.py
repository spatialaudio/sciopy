import setuptools

setuptools.setup(
    name="sciopy",
    version="0.2.2",
    author="Jacob Peter Thönes",
    author_email="jacob.thoenes@uni-rostock.de",
    description="Python based interface module for serial communication with the ScioSpec Electrical Impedance Tomography (EIT) device.",
    long_description="This package offers the serial interface for communication with an EIT device from ScioSpec.\n Commands can be written serially and the system response can be read out.\n With the current version, it is possible to start and stop measurements with defined burst counts and to read out the measurement data. In addition, the measurement data is packed into a data class for better further processing.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/spatialaudio/sciopy.git",
)
