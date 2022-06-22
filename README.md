# Overview

This project attempts to create a self driving model in the track racing game, "Trackmania". Vehicle autonomy has blown up over the last several years for numerous reasons such as convenience, safety, environmental, and more. The use of virtual environments have been an incredible boon for vehicle autonomy development by accelerating the testing process and lowering both physical and monetary costs. Not only does this benefit the industry, it creates an opportunity for individuals to experiment and learn about topics such as machine learning and computer vision.

## Variables
<ul>
  <li>Distances: How far away is the car to the walls at angles 30, 45, 60, 90, 120, 135, and 150 degrees</li>
  <li>Speed: How fast is the car moving</li>
 </ul>

## Screen Capture

Vision is an important sense that we tend to rely on, not just in driving, but throughout our daily lives. Our visual system is constantly working to collect and provide information about the environment. Computer vision is a field of study that tries to enable computers to do just that. So, to begin, I needed a way to capture the screen before I can begin collecting data.

![screen](https://user-images.githubusercontent.com/69861524/166872081-b76797fe-538b-4633-8e99-8470a535d271.jpg)

## Speed

Getting the speed simply involves another screen capture then using an image to text library to convert the image to a number 

Pytesseract and tesserocr are two potential libraries to convert the image to a number. When testing, tesserocr was roughly 3x faster but pytesseract was far more consistent. 

When collecting data, pytesseract was used for more consistent recordings. However, tesserocr was used when put into production since current speed can be estimated based on the previous movement.

## Region of Interest

I captured the screen only in the area I'm interested in by defining a region of interest. By getting rid of the unhelpful information, it will help speed up data collection.

![roi](https://user-images.githubusercontent.com/69861524/166872097-fbc1905e-fa95-4e52-ab85-3c30e5db15d0.jpg)

## Edge Detection

I'm interested in how for away the car is to the walls so in order to get the distance, I need to detect where the walls are. This was done using Canny.

Canny w/ Gaussian Blur

![edges](https://user-images.githubusercontent.com/69861524/166867758-c27b215f-5376-42c9-b3ec-3c0a5bb06a17.jpg)


## Template

The angles I chose to use (in degrees) were 30, 45, 60, 90, 120, 135, and 150. In order to get the pixels that correspond to these angles, I created a template of lines corresponding to those angles that could be masked onto the edges. The resulting image would be the pixels that correspond to these angles. With these pixels, I calculated the distances for the closest points along each angle. The image below is the template used in this project.

![template](https://user-images.githubusercontent.com/69861524/166853656-3ef664b1-1c96-4dca-b68d-29fa1a09b9b2.jpg)

## Computing Distances

Using the equation for a line, y=mx+b, I can determine if a point is along an angle. Knowing which point corresponds to which angle makes it easy to determine the closest point for each angle and their distances.

![pixels](https://user-images.githubusercontent.com/69861524/166868477-d427646d-c530-45e6-901e-ada3c3ef46e0.jpg)

![dist](https://user-images.githubusercontent.com/69861524/166868488-2f7e2499-33f9-47b5-8b98-458e33a504e9.jpg)

## Collecting Data

Distances and speed were taken from hours of gameplay footage and combined to form the data. K-means clustering was performed to create the labels and were manually checked. To do this, I recorded the buttons pressed for each screenshot.

![image](https://user-images.githubusercontent.com/69861524/174937120-759943be-6ab7-47be-bf20-9366bef38f65.png)

Background pixels were then removed in order to achieve well defined clusters. The image above indicates and forward button press and after removing the background, the image looks like the following

![image](https://user-images.githubusercontent.com/69861524/174937715-6342c072-1d7f-461c-9528-047f9f77368e.png)

Clusters in K-means were initialized using these color corrected images and the results were used to label the data.

## Creating and Testing Models

I looked at several models. KNNs, SVMs, RFs, Neural Nets, and an ensemble of Neural Nets. Results from hyperparameter and model selection showed that RFs had the highest testing accuracies, but when put into use, they were unable to navigate the tracks.

Neural Nets and the ensemble of Neural Nets testing accuracies were similar and slightly less than the RFs. The ensemble was formed using the top 3 performing Neural Nets from the results of hyperparameter selection. However, the ensemble track navigation was similar to that of the highest performing Neural Net. Therefore, the single Neural Net was chosen over the ensemble.

Overall, Neural Nets had the best track navigation. 

## Results

I created three tracks with varying difficulties. Easy, medium, and hard. On the easy and medium tracks, the model was able to navigate them with no issues. However, issues arose in the hard track. When stuck in the green areas of the track located on the sides, the model has difficulty getting out of the area and in some cases will ride the wall until it gets out. In the hard track, I introduced sharp U turns which were not present in the easy and medium tracks. The model struggled the most with these U turns due to understeering.

#### Easy Track

<img src ="https://user-images.githubusercontent.com/69861524/174934077-c5add074-c637-40c8-849e-040b00c9deab.gif" width="350" height="150"/>

#### Medium Track
<img src ="https://user-images.githubusercontent.com/69861524/174934142-64701f66-ad5b-4de5-9129-6220556743ff.gif" width="350" height="150"/>

#### Hard Track
<img src ="https://user-images.githubusercontent.com/69861524/174934153-341d70e8-3ee7-4ace-a716-1e4156fed714.gif" width="350" height="150"/>

## Issues/Discussion

#### Data Collection

Data collected came from recording my own gameplay which involved racing lines, drifting, and entering the green areas. All of which would be difficult for the model to learn. Also, the data is imbalanced and skewed towards forward movements since the purpose of the game is to move forward and reach the finish line. I created a track which would involve me slowing down and making backwards key presses as well as stratified sampling to slightly improve the imbalance, but the model still has issues moving backwards. In some cases, it would know when to reverse but in other cases, it gets stuck.

#### Input

The model simulates keyboard inputs as opposed to controller inputs which makes the car drive in an unsmooth manner (It makes many small turns instead of one fluid turn). This is because the data collected is also from keyboard. The model knows when to make a turn but understeers or oversteers due to the lack of input options which sends the car into the green area on the sides of the track where it struggled. With controller settings, the amount of steering could be recorded. Not only would this solve the over and understeering issue and allow for smoother and more precise driving, this would also remove the need for labeling with K-means clustering. 

#### Speed

Due to the over and understeering issues when simulating a keyboard, I programmed the model to make short, intermittent movements as opposed to continuous movements. This alleviates some of the oversteering issues, but limits speed. This means that the model is unable to reach speeds similar to that of the training and testing data which may affect the performance of the model. 

#### Edge Detection

Along with the walls, Canny also detects the text and images that's found at the start and end of every track. An ROI that covers the bottom of the screen would cover the text and image detections, but would also cover important edges later on in tracks, like the lanes. Using Hough Line transform solved this issue, but when comparing Hough Lines and Canny, there was less inconsistent pixel detections when using Hough Lines. Ultimately, only Canny was used since using Hough Lines still involves using Canny and only using Canny allows for faster capture rates.

#### Template

An issue with the method I used above is that I would need to find a way to determine which points correspond to which angle. Another method I came up with was to create individual templates, each corresponding to their own angle. That way, I could find the points and their corresponding angles. This method was too slow in testing since it required multiple masking operations.

In addition to this, the template only used 7 angles/sensors which may have hindered model performance. I think adding more angles/sensors would improve model performance and in the future, I plan to revisit this project and look at model performances with more angles/sensors.
