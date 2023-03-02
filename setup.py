import setuptools

setuptools.setup(
    name="sciopy",
    version="0.4.1",
    author="Jacob Peter Thönes",
    author_email="jacob.thoenes@uni-rostock.de",
    description="Python based interface module for serial communication with the ScioSpec Electrical Impedance Tomography (EIT) device.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="ScioSpec EIT".split(),
    platforms="any",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/spatialaudio/sciopy.git",
)
