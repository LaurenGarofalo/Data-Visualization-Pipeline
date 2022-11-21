# Data-Visualization-Pipeline

This repository is used to develop a data manipulation and visualization tool to specifically handle data and metadata from robotic simulations conducted using Matlab's Simulink and Simscape software. The data produced by Simulink is a .csv matrix where the first column is the time and each subsequent column is a measurement that was taken at the given time. Examples of data that can be measured include velocity, acceleration, lateral forces, and torques. The metadata is also stored in a .csv format where the first column is the label of the metadata and the second column is the timestamp.

The goal of this pipeline is to provide an interface that allows the user to perform a variety of data visualization and manipulation tasks. Some of these tasks include: 
  - Accessing metadata  key/value pairs
  - Accessing statistical measurements of numerical columns
  - Manipulating/reformatting metadata
  - Plotting the data and saving the plot to a local drive
 
