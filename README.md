# FDS
Yonsei University Digital Media Lab's FDS code edited and uploaded on the EDISON platform.

Refer to the manual below on how to use the program on EDISON platform: https://www.edison.re.kr/
[[EDISON]Manual_2108_Yonsei_FDS_1_V01.pdf](https://github.com/yonseidmlab/FDS/files/7073481/EDISON.Manual_2108_Yonsei_FDS_1_V01.pdf)

Organization of the code 
1-1. Material 
1-2. Surface
1-3. Wall 
1-4. Operator 

2. Simulator 

Material 
![B01](https://user-images.githubusercontent.com/25164461/137667228-53d72eb1-b46d-456c-9796-3b3a260f4c2b.jpg)
Must use the output of this code in the next step "Surface"
Can use various setting of materials and gets saved in local PC for further use. 

Surface 
![B02](https://user-images.githubusercontent.com/25164461/137667317-4d1abd9e-c389-4a30-b9b3-086808186c44.jpg)
SURFACE (material design) is performed using the materials manufactured in the "Material" stage.
Up to three layers can be used per surface (material), and a single material/double material can be selected.
(Example) 
1 layer, 1 single material: 1 MATERIAL required 
1 layer, 2 MATERIAL required
3 layers, single material: 3 MATERIAL required 
3 layers, double material: up to 6 MATERIAL required (overlapping possible)

Wall 
![B03](https://user-images.githubusercontent.com/25164461/137668032-2a6ef8f0-61ae-42fe-ac2e-64fa8aa0b801.jpg)
Construct the space for fire simulation 
Have basic setting already set for material and its type
Can use the Advance Option to select the "Surface" made in the previous step

Operator 
![B04](https://user-images.githubusercontent.com/25164461/137668316-a4846eb5-911a-45b4-8205-028abfaa10fc.jpg)
Final Step of the making of the FDS file that will be used in the final process
Use walls from the previous selection
Choose simulation time, resolution, and hrrupa. 

Simulator 
![B05](https://user-images.githubusercontent.com/25164461/137668527-3d824967-fdc7-44c4-bb2c-6d84d54494c6.jpg)
With the FDS file made in the previous process, start the simulation
