# QAPics
An *open source* visual testing tool designed for QA teams

## Directories
 
### UI

  The UI is a rudimentary Electron-based prototype for file navigation. 
  
  I hope to make this an interface for users to be able to add metadata to images (currently just to be stored in text files)  for ignore areas, Browser-specific differences, and things along those lines. I also hope to make this do more image processing, like adding image filters and such, to optimize the testing algorithm and push the slower part of that process to the UI side. The slowest part of the algorithm is iterating through pixels to add color filters; the other processes can be done without iteration using matrix operations, so it makes sense to move the image processing to the UI designed to display images. 
  
  **The UI is used by running 'npm start' from within the UI directory**
  
### API

  The API is designed to work directly with code in the analysis directory without testing code having to "get its hands dirty". 
  
  The API will be designed to run with Selenium. I hope to add more supported languages than Python, as I am aware of the diverse languages used for Selenium-based testing automation.
  
### Analysis

  Right now, analysis functions in a very basic way: achieving pixel comparisons using simple numpy matrix mathematics. 
  
  The speed of the algorithm is good, but I hope to add more features that align with what is useful for QA teams, and features that reduce manual verification time. One idea I am exploring for that is the implementation of a machine-learning algorithm that is further refined at each step of manual verification, adapting specifically to each team's needs. This is, of course, in the pre-exploritory stage. As explained in the UI section, I also hope to move image filters and decorations to the UI side to speed up the actual analysis section.
  
### Output

  This is where output images, formatted with color highlighting differences, go after analysis. I believe the current file system will be adapted when I know more specifically how each element is going to work together- for example, I may consider storing baselines and output in a directory together, and individually in their own sub-directories. Here is what outlook comes out as now: 
  
  ![alt text](https://github.com/josieoharrow/QAPics/blob/master/Output/Output_2019-01-21%2022:30:16.739397.png)
  
Note that this type of coloring works very well on images that do not have a lot of color; using a general add/subtract algorithm is less effective for images that are very colorful as the rgb filter looks less like one consistent color laid over the top of the image.  
  
### Masks

 Masks are used to store data for ignore regions (and eventually adjustable regions as well). It is efficient to store them as pngs with the same dimensions as the baseline image because you can generate a True/false array using basic threshold math with them to operate on your differences array and quickly adjust for ignore regions, all using optimized processes instead of pixel-by-pixel.
 
 Currently, there is only the capability for ignore areas. This is designated on the mask by a black space over every desired ignore area.

