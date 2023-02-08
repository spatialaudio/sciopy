import setuptools
try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setuptools.setup(
    name="sciopy",
    version="0.2.3",
    author="Jacob Peter Thönes",
    author_email="jacob.thoenes@uni-rostock.de",
    description="Python based interface module for serial communication with the ScioSpec Electrical Impedance Tomography (EIT) device.",
    long_description= long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/spatialaudio/sciopy.git",
)
