# QAPics
An *open source* visual testing tool designed for QA teams

## Directories
 
### UI
  The UI is a rudimentary Electron-based prototype for file navigation. I hope to make this an interface for users to be able to add metadata to images (currently just to be stored in text files) for ignore areas, Browser-specific differences, and things along those lines.
### API
  The API is designed to work directly with code in the analysis directory without having to "get its hands dirty". The API will be designed to run with Selenium. I hope to add more supported languages than Python, as I am aware of the diverse languages used for Selenium-based testing automation.
### Analysis
  Right now, analysis functions in a very basic way: achieving pixel comparisons using simple numpy matrix mathematics. The speed of the algorithm is good, but I hope to add more features that align with what is useful for QA teams, and features that reduce manual verification time. One idea I am exploring for that is the implementation of a machine-learning algorithm that is further refined at each step of manual verification, adapting specifically to each team's needs. This is, of course, in the pre-exploritory stage.
### Output
  This is where output images, formatted with color highlighting differences, go after analysis. I believe the current file system will be adapted when I know more specifically how each element is going to work together- for example, I may consider storing baselines and output in a directory together, and individually in their own sub-directories.

