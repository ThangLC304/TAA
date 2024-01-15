# TOWER ASSAY ANALYZER

![alt text](https://github.com/ThangLC304/SpiderID_APP/blob/main/bin/support/universities.png?raw=true)

## Author

Luong Cao Thang (Vincent Luong)
PhD candidate, I-Shou University, Kaohsiung, Taiwan.  
Email: [thang.luongcao@gmail.com](mailto:thang.luongcao@gmail.com)  

## Correspondence:

Prof. Chih-Hsin Hung  
Laboratory of Biotechnology, I-Shou University, Kaohsiung, Taiwan.  
Email: [chhung@isu.edu.tw](mailto:chhung@isu.edu.tw)  

Prof. Chung-Der Hsiao  
Laboratory of Biotechnology, ChungYuan Christian University, Taoyuan, Taiwan.  
Email: [cdhsiao@cycu.edu.tw](mailto:cdhsiao@cycu.edu.tw)  


# TOWER ASSAY downstream analyzing application
TowerAssayAnalyzer is the new software we build to complement the Tower Assay Protocol. It was designed to streamline and automate the arduous data management and organize the processes associated with raw data.

## INSTALLATION GUIDE

1. Download ```.zip``` file of the whole repository by click on ```Code``` button and select ```Download ZIP```

    <img src="https://github.com/ThangLC304/taa/blob/main/Bin/support/download_button.png" alt="image" width="450" height="auto">

2. Unzip the file, within the App Folder, run the ```setup.bat``` (Run as Admistrator) file to install independencies

3. Run the program using ```run.bat```

## APP NAVIGATION

<img src="https://github.com/ThangLC304/taa/blob/main/Bin/support/step01.png" alt="image" width="450" height="auto">

<!-- ![App_Screen](https://github.com/ThangLC304/taa/blob/main/Bin/support/app_screen_with_num.png) -->


1. Create new Project from scratch using ```Create Project```(1)   

    <img src="https://github.com/ThangLC304/taa/blob/main/Bin/support/step01.png" alt="image" width="450" height="auto">

    <br>
    Example of a project detail
    <br>

    <img src="https://github.com/ThangLC304/taa/blob/main/Bin/support/create_project.png" alt="image" width="450" height="auto">


2. Copy recorded video files to desired locations for further analysis using tracker (in this example we used idTracker)

    <img src="https://github.com/ThangLC304/taa/blob/main/Bin/support/step02.png" alt="image" width="450" height="auto">


3. Select Project from available ones within the Project List -> ```Load Project``` (2)  

    If a new project is loaded **[1]** (or ```Re-measure```</ins> **[2]** is pressed), you will be redirected to a Measurer window **[3]** to measure the core coordinates, which subsequently help the program to calculate the required parameters.

    <img src="https://github.com/ThangLC304/taa/blob/main/Bin/support/step03.png" alt="image" width="450" height="auto">


4. Within the Measurer window, load the image (as first frame of the video, you can create a reference image manually or select the video itself and the program will automatically extract the first frame of the video as reference image)

    <img src="https://github.com/ThangLC304/taa/blob/main/Bin/support/step04.png" alt="image" width="450" height="auto">


5. The loaded project is now fully equipped with functional parameters **[3]**. Run analysis on the Data of the current Batch (all treatments within it) using ```Analyze``` button **[4]**. The analysis process is displayed on the progress bars **[5]**.

    <img src="https://github.com/ThangLC304/taa/blob/main/Bin/support/step05.png" alt="image" width="450" height="auto">


6. The result will be saved as "EndPoints.xlsx" at the Batch directory (e.g., [project_name]/[test_name]/EndPoints.xlsx) <br>

    <img src="https://github.com/ThangLC304/taa/blob/main/Bin/support/step06.png" alt="image" width="450" height="auto">


    The following end-points are included: <br>

    - Total Distance (cm) <br>
    - Average Speed (cm/s) <br>
    - Total Absolute Turn Angle (degree) <br>
    - Average Angular Velocity (degree/s) <br>
    - Slow Angular Velocity Percentage (%) <br>
    - Fast Angular Velocity Percentage (%) <br>
    - Meandering (degree/m) <br>
    - Freezing Time (%) <br>
    - Swimming Time (%) <br>
    - Rapid Movement Time (%) <br>
    - Time spent in Top (cm) <br>
    - Time spent in Mid (%) <br>
    - Time spent in Bot (%) <br>
    - Shoaling Area (cm<sup>2</sup>) <br>
    - Shoaling Volume (cm<sup>3</sup>) <br>


7. Display Shoaling Formation in 3D space

    <img src="https://github.com/ThangLC304/taa/blob/main/Bin/support/shoaling_plot.png" alt="image" width="450" height="auto">

    **LEFT SIDE** is Shoaling formation in 3D space <br>

    **RIGHT SIDE** is Shoaling Volume plot

