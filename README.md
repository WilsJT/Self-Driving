# Overview

This project attempts to create a self driving model in the track racing game, "Trackmania". Vehicle autonomy has blown up over the last several years for numerous reasons such as convenience, safety, environmental, and more. The use of virtual environments have been an incredible boon for vehicle autonomy development by accelerating the testing process and lowering both physical and monetary costs. Not only does this benefit the industry, it creates an opportunity for individuals to experiment and learn about topics such as machine learning and computer vision.

## Variables
<ul>
  <li>Distances: How far away is the car to the walls at specific angles</li>
  <li>Speed: How fast is the car moving</li>
 </ul>

## Screen Capture

Vision is an important sense that we tend to rely on, not just in driving, but throughout our daily lives. Our visual system is constantly working to collect and provide information about the environment. Computer vision is a field of study that tries to enable computers to do just that. So, to begin, I need a way to capture the screen before I can begin collecting data.

![screen](https://user-images.githubusercontent.com/69861524/166872081-b76797fe-538b-4633-8e99-8470a535d271.jpg)

## Speed

Getting the speed simply involves another screen capture then using an image to text library to convert the image to a number 

Pytesseract and tesserocr are two potential libraries to convert the image to a number. When testing, tesserocr was roughly 3x faster but pytesseract was far more consistent. 

#### Testing different capture methods

## Region of Interest

When capturing the screen, there's a lot information coming in from the background that won't be needed in this project. I can capture the screen only in the area I'm interested in by defining a region of interest. By getting rid of the unhelpful information, it will help speed up data collection.

![roi](https://user-images.githubusercontent.com/69861524/166872097-fbc1905e-fa95-4e52-ab85-3c30e5db15d0.jpg)

## Edge Detection

I'm interested in how for away the car is to the walls so in order to get the distance, I need to detect where the walls are.

Canny w/ Gaussian Blur

![edges](https://user-images.githubusercontent.com/69861524/166867758-c27b215f-5376-42c9-b3ec-3c0a5bb06a17.jpg)


## Template

The angles I chose to use (in degrees) were 30, 45, 60, 90, 120, 135, and 150. In order to get the pixels that correspond to these angles, I created a template of lines corresponding to those angles that could be masked onto the edges. The resulting image would be the pixels that correspond to these angles. With these pixels, I can calculate the distances for the closest points along each angle. The image below is the template used in this project.

![template](https://user-images.githubusercontent.com/69861524/166853656-3ef664b1-1c96-4dca-b68d-29fa1a09b9b2.jpg)

## Computing Distances

As mentioned in the template section, I need a way to determine which points correspond to which angle. Using the equation for a line, y=mx+b, I can determine if a point is along an angle. Knowing which point corresponds to which angle makes it easy to determine the closest point for each angle and their distances.

![pixels](https://user-images.githubusercontent.com/69861524/166868477-d427646d-c530-45e6-901e-ada3c3ef46e0.jpg)

![dist](https://user-images.githubusercontent.com/69861524/166868488-2f7e2499-33f9-47b5-8b98-458e33a504e9.jpg)

## Collecting Data

#### Work in Progress

## Creating and Testing Models

#### Work in Progress

## Results

#### Work in Progress

## Issues/Discussion

#### Speed

#### Input

The model simulates keyboard inputs as opposed to controller inputs which makes the car drive in an unsmooth manner. This is because the data collected is also from keyboard. With controller settings, I would be able to record the amount of steering and assign these values as the labels. This would remove the need for labeling with K-means clustering. In addition to this, with controller simulation, the car would be able to drive in all directions and allow for smooth driving.

#### Edge Detection

Along with the walls, Canny also detected the text and images that's found at the start and end of every track. An ROI that covers slightly above the bottom of the screen would cover the text and image detections, but would also cover important edges later on in tracks, like the lanes. Using Hough Line transform solved this issue, but when comparing Hough Lines and Canny, there was less inconsistent pixel detections when using Hough Lines.

#### Template

An issue with the method I used above is that I would need to find a way to determine which points correspond to which angle. Another method I came up with was to create individual templates, each corresponding to their own angle. That way, I could find the points and their corresponding angles. This method was too slow in testing since it required multiple masking operations.

In addition to this, the template only used 7 angles which may have hindered model performance. In the future, I plan to revisit this project and look at model performances with more angles.

#### Work in Progress
