'''
Data Processing Tool
Lauren Garofalo
'''


import json
import math
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import os


   
class DataProcessor():
    
    def __init__(self, data, metadata):
        
        #initialize the data processor with the data that needs to be processed
        self.data = data
        self.metadata = metadata
        
    def get_metadata_dict(self):
        
        """Creates a dictionary establishing metadata key-value pairs.
        
       Returns:
           meta_dict (dict): key-value metadata pairs.
        """
           
        meta_dict = {}
        
        #metadata was stored in a CSV from matlab, separate the columns 
        #into a dict to establish the relationship between the key-value pairs
        for i in range(self.metadata.shape[0]): 
            meta_dict[self.metadata.loc[i, 0]] = self.metadata.loc[i,1]
            
        return meta_dict     
        
    
    def convert_metadata_to_JSON(self): 
        
        """ Converts metadata to JSON format.
        
        Returns:
            JSON string format for metadata key-value pairs.
        """
        
        #JSON files are needed to upload metadata into Datafed
        meta_dict = self.get_metadata_dict()
        return json.dumps(meta_dict)    


    def get_data_labels(self, data_label = "columns", delimiter = "|"):
        
        """ Gets ordered column data from metadata.
        
        Args: 
            data_label (string): metadata key holding the given column label
            delimiter (string): delimiter separating the column labels in the metadata
            
        Returns: 
            columns (list): ordered labels for each column in the data
        """
            
        metadata_dict = self.get_metadata_dict()
        column_names = metadata_dict[data_label]   
        columns = column_names.split(delimiter) 
        return columns

    
    def get_desired_data(self):
        
        """ Prompts user to select desired columns for data visualization purposes.
        
        Returns:
            cols_to_plot (list): column names selected by the user.
        """
            
        columns = self.get_data_labels()
        user_options = {}
        for index, column in enumerate(columns):
            if column != "time":
                user_options[int(index)] = column
        print(f"DATA OPTIONS: {user_options}")   
        print("How many columns would you like to select?")
        num_cols = self.get_valid_number(len(user_options))    
        cols_to_plot = []
        if num_cols == len(user_options):
                for key in user_options.keys():
                    cols_to_plot.append(user_options[key])
           
        else:
            while len(cols_to_plot) < num_cols:
            #print(len(cols_to_plot), num_cols)
                print("Select a column number.")
                print(f"Options: {user_options}")
                col_num = self.get_valid_number()
                while col_num not in user_options.keys():
                    print("Please enter a valid column number.")
                    print(f"Options: {user_options}")
                    col_num = self.get_valid_number()   
                cols_to_plot.append(user_options[col_num])  
                del user_options[col_num]   
        return cols_to_plot    
           
    def get_valid_number(self, max_num = math.inf):
        
        """ Collects a positive integer value less than some specified maximum from the user.
        
        Args:
            max_num (int): The largest acceptable integer. 
            
        Returns:
            input_num (int): A valid number specified by the user. 
        """
            
        invalid_num = True
        
        while invalid_num: #get user selection until we have a positive integer value
        
            is_int = False
            is_pos = False
            under_or_eq_max = False
            try: 
                if max_num < math.inf:
                    print(f"The maximum number is: {max_num}")
                user_input = input("Enter number:\n")
                
                user_input = float(user_input)
                input_num = int(user_input)
                if user_input == input_num: #user did not enter a decimal/fraction
                    is_int = True
                else:
                    print("Please enter an integer value.\n")
                    
                if input_num > 0: #needs to be a positive number
                    is_pos = True 
                else:
                    print("Please enter a value greater than 0.\n")
                    
                if input_num <= max_num:
                    under_or_eq_max = True
                else:
                    print(f"Please enter a number less than {max_num}")
                     
            except ValueError: #if the user did not enter a numerical value
                
                print("Please enter an integer value.\n")
                    
            if (is_int and is_pos and under_or_eq_max):
                invalid_num = False
                
        return input_num          


    def visualize_data(self, time_label = "time"):
        
        """ Plots data columns (specified by user) with respect to time.
            Gives user the option to locally save the plot.
        
        Args:
            time_label (string): The column name in which the time data is held.    
        """
        
        ordered_columns = self.get_data_labels()
        ordered_units = self.get_data_labels(data_label = "col_units")
        time = self.data[self.data.columns[ordered_columns.index(time_label)]]
        data_to_plot = self.get_desired_data()
        units = []
        for col_name in data_to_plot:
            col_index = ordered_columns.index(col_name)
            units.append(ordered_units[col_index])
            dependent_variable = self.data[self.data.columns[ordered_columns.index(col_name)]]
            plt.plot(time, dependent_variable)
                
        plt.title(f"{data_to_plot} vs Time")    
        plt.xlabel(f"Time ({ordered_units[0]})")
        plt.ylabel(f"{set(units)}")
        plt.legend(data_to_plot)
        fig1 = plt.gcf()
        plt.show()
        print("Would you like to save the plot?")
        user_choice = self.get_valid_yes_no_choice()
        if user_choice == "yes":
            self.save_plot(fig1)
           


    def save_plot(self, plot):
        
        """ Saves the visualized data plot to a file/directory of the user's choosing.
        
        Args:
            plot (matplotlib Figure): The plot to save.
            
        Returns:
            file_name (string): The name of the saved file indicating a successful save.
        
        """
        
        print(f"Your cwd is {os.getcwd()}. Would you like to save here?")
        print(type(plot))
        user_choice = self.get_valid_yes_no_choice()
        if user_choice == "yes":
            file_name = input("Enter a file name:") + ".png"
            plot.savefig(file_name)
            return file_name
        else:
            while True:
                try:
                    file_path = input("Enter desired file path:")
                    file_name = input("Enter desired file name:")
                    plt.savefig(file_path + file_name + ".png")
                    return file_name
                except FileNotFoundError:
                    print("Please enter a valid file path.")

    def get_data_rundown(self):
        
        """ Prints table displaying the units, common statistical measures*, 
            and emptiness of user-selected numerical data columns.
            
            *min, max, average, median, standard deviation
        """ 
        
        #numerical data only
        ordered_columns = self.get_data_labels()
        ordered_units = self.get_data_labels(data_label = "col_units")
        cols_to_display = self.get_desired_data()
        t = PrettyTable(["Parameter"])
        t.add_row(["Column Units"])
        t.add_row(["Min Value"])
        t.add_row(["Max Value"])
        t.add_row(["Average"])
        t.add_row(["Median"])
        t.add_row(["Standard Deviation"])
        t.add_row(["Missing Data %"])
        for col_name in cols_to_display:
            data_column = self.data[self.data.columns[ordered_columns.index(col_name)]]
            col_index = ordered_columns.index(col_name)
            t.add_column(col_name, [ordered_units[col_index], 
                                    data_column.min(), data_column.max() , 
                                    data_column.mean(), data_column.median(), 
                                    data_column.std(), 
                                    data_column.isnull().sum()/len(data_column)*100])
                 
        print(t)        
        
    def get_valid_yes_no_choice(self): 
            
            """ Collects a case-insensitive yes or no choice from the user.
            
            Returns:
                "yes"/"no" (string) : User's respective yes/no selection. 
            """
            
            while True: #until we return valid choice
            
                #use .lower() so selection is case insensitive
                user_choice = input("Enter choice:").lower()
                
                
                #accept "yes"/"y" and "no"/"n" as valid options
                if user_choice in ["yes",  'y']:
                    return "yes"
                
                elif user_choice in [ "no" ,'n']: 
                    return "no"
                
                else: #we did not get a valid response from the user
                    print("Invalid response. Please type 'yes' or 'no'.")    
    
    def extract_timestamp(self, timestamp_label = "start_time"):
        
        """ Separates the date and time in timestamp metadata.
        
        Returns:
            metadata_dict (dict): An updated metadata dictionary with separated
            data and time measures.
        """
        
        metadata_dict = self.get_metadata_dict()
        date_and_time = metadata_dict[timestamp_label].split(" ")
        print("Would you like to save the date in a separate key?")
        user_choice = self.get_valid_yes_no_choice()
        if user_choice == "yes":
            label_name = input("Enter a date label name:")
            metadata_dict[label_name] = date_and_time[0]
            metadata_dict[timestamp_label] = date_and_time[1]
        return metadata_dict    
            


