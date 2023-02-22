from sciopy import create_prep_directory, prepare_all_samples_for_16_el
from sciopy.sciopy_dataclasses import PreperationConfig

choice = input("Type 1 for programmed path, 2 for own path:")

if int(choice) == 1:
    lpath = "../../ScioSpecMeasurements/measurement_01/"
else:
    lpath = input("Type in the source directory")

# Initialise the configuration class object
prep_cnf = PreperationConfig(lpath, "", 0)

# Create the save directory.
prep_cnf = create_prep_directory(prep_cnf)

# Convert all samples from load path to save path.
prepare_all_samples_for_16_el(prep_cnf)
