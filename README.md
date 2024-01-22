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

**FOR THE STABLE VERSION, PLEASE SEND EMAIL TO REQUEST DOWNLOAD PERMISSION to thang.luongcao@gmail.com**

**THE GITHUB VERSION IS DEVELOPING VERSION**

## INSTALLATION GUIDE

1. Download ```.zip``` file of the whole repository by click on ```Code``` button and select ```Download ZIP```

    <img src="https://github.com/ThangLC304/taa/blob/main/Bin/support/download_button.png" alt="image" width="450" height="auto">

2. Unzip the file, within the App Folder, run the ```setup.bat``` (Run as Admistrator) file to install independencies

3. Run the program using ```run.bat```

## APP NAVIGATION

<img src="https://github.com/ThangLC304/taa/blob/main/Bin/support/step01.png" alt="image" width="450" height="auto">


1. Create new Project from scratch using ```Create Project``` 

    <img src="https://github.com/ThangLC304/taa/blob/main/Bin/support/create_project_window.png" alt="image" width="450" height="auto">


2. Select Project from available ones within the ```Project List``` (A) -> ```Load Project```

    Detail information is listed in (B)

3. Import videos to desired Location for further analysis using tracker (in this example we used idTracker)

    <img src="https://github.com/ThangLC304/taa/blob/main/Bin/support/import_video.png" alt="image" width="450" height="auto">


4. Adjust parameters for each section using (A) and (B) *displayed in the following image*

<img src="https://github.com/ThangLC304/taa/blob/main/Bin/support/step02.png" alt="image" width="450" height="auto">


5. The loaded project is now fully equipped with functional parameters. Run analysis on the Data of the current Test (all treatments and batches within it) using ```Analyze``` button. The analysis process is displayed on the progress bars.

6. The result will be saved as "EndPoints.xlsx" at the Batch directory (e.g., [project_name]/[test_name]/EndPoints.xlsx) <br>

    <img src="https://github.com/ThangLC304/taa/blob/main/Bin/support/result_display.png" alt="image" width="450" height="auto">

    The following end-points are included: <br>

    **NOVEL TANK TEST**
    <br>
    - Total Distance (cm)
    - Average Speed (cm/s)
    - Freezing Percentage (%)
    - Swimming Percentage (%)
    - Rapid Movement Percentage (%)
    - Average distance to center (cm)
    - Time in top (%)
    - Time in bottom (%)
    - Time spent in top/bottom ratio
    - Distance traveled in top (cm)
    - Distance traveled top/bottom ratio
    - Latency in seconds (seconds)
    - Number of entries
    - Average entry (seconds)

    **SHOALING TEST**
    <br>
    - Total Distance (cm)	
    - Average Speed (cm/s)	
    - Freezing Percentage (%)	
    - Swimming Percentage (%)	
    - Rapid Movement Percentage (%)	
    - Time in top (s)	
    - Average distance to center (cm)	
    - Nearest distance (cm)	
    - Furthest distance (cm)	
    - Average inter-fish distance (cm)	
    - Shoaling Area (cm<sup>2</sup>)

    **MIRROR BITING TEST**
    <br>
    - Total Distance (cm)	
    - Average Speed (cm/s)	
    - Freezing Percentage (%)	
    - Swimming Percentage (%)	
    - Rapid Movement Percentage (%)	
    - Mirror biting time (%)	
    - Longest time mirror biting % (%)	
    - Average distance to mirror (cm)

    **SOCIAL INTERACTION TEST**
    <br>
    - Total Distance (cm)	
    - Average Speed (cm/s)	
    - Freezing Percentage (%)	
    - Swimming Percentage (%)	
    - Rapid Movement Percentage (%)	
    - Interaction time (%)	
    - Longest time in interaction % (%)	
    - Average distance to separator (cm)

    **PREDATOR AVOIDANCE TEST**
    <br>
    - Total Distance (cm)	
    - Average Speed (cm/s)	
    - Freezing Percentage (%)	
    - Swimming Percentage (%)	
    - Rapid Movement Percentage (%)
    - Predator avoiding time % (%)	
    - Predator approaching time % (%)	
    - Longest time approaching predator (s)	
    - Average distance to predator (cm)


**<!!!>: Please refrain from changing the Project directory name**

## Regular questions:

**Q:** What if I have changed the name of the directory name at the new location? <br>

**A:** If there is no other folder with the name exactly like the old name of the project, when you use the ```Load Project``` button, the App will ask you to select the new location of the project so it can update within its memory. <br>
If you changed the name of the directory and then you created a new directory with the same exact name, the App will recognize the new empty folder as the valid path for the Project, hence not asking you for relocation -> Mismatching issue. <br>

<br>

**Q:** When I want to update the program, do I have to go to your GitHub Repository to download new version and replace the old one? <br>

**A:** Fortunately no, you can use the ```updater.bat``` to check to update the app. Then check the Libs/\_\_about__.json to see if your version is up-to-date! <br>
