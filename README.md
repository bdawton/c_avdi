# README
## _C-AVDI_

## Features
- Accompanying code for [C-AVDI: Compressive Measurement-Based Acoustic Vehicle Detection and Identification](https://www.researchgate.net/publication/356707239_C-AVDI_Compressive_Measurement-Based_Acoustic_Vehicle_Detection_and_Identification).
- The "modified_emlearn" code is a modified version of the ***emlearn*** library developed by Jon Nordby and available [here](https://github.com/emlearn/emlearn). (Licensed under the MIT License)

## Instructions
- Main implementation is in *"main_c_avdi.py"*.
- Place vehicle sounds (available for download [here](https://drive.google.com/drive/folders/1Ftmo3ABhBRx9agiW_8wErp9hzLtFZnF6?usp=sharing)) in the *VehicleSounds* folder and accompanying subfolders.
- For the MCU implementation in *"mcu_c_avdi.py"*, the generated files *"lab_Gx.txt"* and *"c_mea_Gx.txt"* need to be loaded onto the microcontroller (via SD card for example), and the corresponding *"classifier_to_test_Gx.h"* needs to be loaded onto the MCU, along with the rest of the *.h* and *.ino* files (or *.c* files depending on MCU/board). You also need the *"eml_trees.h"* file from the *"modified_emlearn" folder.

## Citations
- If you use any of the code or data made available on this page in any academic or professional publications, please reference with:

```tex
@ARTICLE{9632588,  
author={Dawton, Billy and Ishida, Shigemi and Arakawa, Yutaka},  
journal={IEEE Access},   
title={C-AVDI: Compressive Measurement-Based Acoustic Vehicle Detection and Identification},   
year={2021},  
volume={9},  
number={},  
pages={159457-159474},  
doi={10.1109/ACCESS.2021.3132061}}
}
```

## License
- BSD 3-Clause "New" or "Revised" License
