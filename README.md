# Overview

This project attempts to create a self driving model in the track racing game, "Trackmania". Vehicle autonomy has blown up over the last several years for numerous reasons such as convenience, safety, environmental, and more. The use of virtual environments have been an incredible boon for vehicle autonomy development by accelerating the testing process and lowering both physical and monetary costs. Not only does this benefit the industry, it creates an opportunity for individuals to experiment and learn about topics such as machine learning and computer vision.

## Variables
<ul>
  <li>Distances: How far away is the car to the walls at specific angles</li>
  <li>Speed: How fast is the car moving</li>
 </ul>

## Screen Capture

Vision is an important sense that we tend to rely on, not just in driving, but throughout our daily lives. Our visual system is constantly working to collect and provide information about the environment. Computer vision is a field of study that tries to enable computers to do just that. So, to begin, I need a way to capture the screen before I can begin collecting data.

## Speed

Getting the speed simply involves another screen capture then using pytesseract to convert the image to a number.

## Region of Interest

When capturing the screen, there's a lot information coming in from the background that won't be needed in this project. I can capture the screen only in the area I'm interested in by defining a region of interest. By getting rid of the unhelpful information, it will help speed up the distance calculations later.

#### Currently testing with different regions of interest

## Edge Detection

I'm interested in how for away the car is to the walls so in order to get the distance, I need to detect where the walls are.

#### Currently testing with different edge detections

## Template

The angles I chose to use (in degrees) were 30, 45, 60, 90, 120, 135, and 150. In order to get the pixels that correspond to these angles, I created a template of lines corresponding to those angles that could be masked onto the edges. The resulting image would be the pixels that correspond to these angles. With these pixels, I can calculate the distances for the closest points along each angle. The image below is the template used in this project.

![template](https://user-images.githubusercontent.com/69861524/166853656-3ef664b1-1c96-4dca-b68d-29fa1a09b9b2.jpg)

An issue with the method above is that I would need to find a way to determine which points correspond to which angle. Another method I came up with was to create individual templates, each corresponding to a single angle. That way, I could find the points and their corresponding angles. This method was too slow in testing since it required multiple masking operations.

## Computing Distances

As mentioned in the template section, I need a way to determine which points correspond to which angle. Using the equation for a line, y=mx+b, I can determine if a point is along an angle. Knowing which point corresponds to which angle makes it easy to determine the closest point for each angle and their distances.

## Collecting Data

## Creating and Testing Models

## Results
