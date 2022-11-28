# Data-Visualization-Pipeline

This repository is used to develop a data manipulation and visualization tool to specifically handle data and metadata from robotic simulations conducted using Matlab's Simulink and Simscape software. The data produced by Simulink is a .csv matrix where the first column is the time and each subsequent column is a measurement that was taken at the given time. Examples of data that can be measured include velocity, acceleration, lateral forces, and torques. The metadata is also stored in a .csv format where the first column is the label of the metadata and the second column is the timestamp.

The goal of this pipeline is to provide an interface that allows the user to perform a variety of data visualization and manipulation tasks. Some of these tasks include: 
  - Accessing metadata  key/value pairs
  
  - Accessing statistical measurements of numerical columns
  
  - Manipulating/reformatting metadata
  
  - Plotting the data and saving the plot to a local drive
  
  ## Files
  
  ### process.py
  This is the module that contains the DataProcessor class. This class holds all of the capabilities highlighted above, including visualizing the data, producing data statistics, altering metadata, and preparing the metadata to be sent to some data management system, such as DataFed. A DataProcessor object must be initialized with the data and metadata being processed. The functions included in this class include: 

- get_metadata_dict : establishes key-value pairs in the metadata csv

- convert_metadata_to_JSON : converts the metadata .csv to a JSON format so it can be uploaded to DataFed

- get_data_labels : gets the column labels from the metadata, since they are not automatically exported by Matlab

- get_desired_data : prompts the user to select column data to plot/visualize

- get_valid_number : gets a positive, integer, number less than some specified maximum from the user

- visualize_data : plots timeseries data as specified by the user

- save_plot : saves the plot made by the user, in a file path specified by the user

- get_data_rundown : produces formatted table of statistical measures for numerical data

- get_valid_yes_no_choice : gets a valid yes or no choice from the user

- extract_timestamp : alters the timestamp metadata based on the user's specifications

### processor_tutorial.ipynb
This notebook was created for tutorial purposes and to demonstrate the functionality of the process.py module. This notebook can be run in Google Colab. To import the process module, it's important to first mount the tutorial file to the current working directory and upload the process.py module using `files.upload` functionality provided by Google Colab. The tutorial is able to be run without any explicit data input, as in includes a function that generates random data for the purposes of moduel functionality experimentation.  

  
 
