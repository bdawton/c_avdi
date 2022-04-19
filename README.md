# README
## _C-AVDI_

## Features
- Accompanying code for [C-AVDI: Compressive Measurement-Based Acoustic Vehicle Detection and Identification](https://www.researchgate.net/publication/356707239_C-AVDI_Compressive_Measurement-Based_Acoustic_Vehicle_Detection_and_Identification).
- The "modified_emlearn" code is a modified version of the ***emlearn*** library developed by Jon Nordby and available [here](https://github.com/emlearn/emlearn). (Licensed under the MIT License)

## Instructions
- Main implementation is in *"main_c_avdi.py"*.
- Place vehicle sounds in the *VehicleSounds* folder and accompanying subfolders.
- For the MCU implementation in *"mcu_c_avdi.py"*, the generated files *"lab_Gx.txt"* and *"c_mea_Gx.txt"* need to be loaded onto the microcontroller (via SD card for example), and the corresponding *"classifier_to_test_Gx.h"* needs to be loaded onto the MCU, along with the rest of the *.h* and *.ino* files (or *.c* files depending on MCU/board).

## Coming Soon
- Link to test data (vehicle sounds) used in the research, along with spreadsheet.
- Arduino project files for MCU implementation.

## License
- BSD 3-Clause "New" or "Revised" License