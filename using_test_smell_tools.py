import subprocess
import os
import glob
import csv
from collections import defaultdict
'''
def execute_tool(tool_path, file_name):
    try:
        # Change to the desired directory
        working_directory = os.path.dirname(tool_path)
        os.chdir(working_directory)

        # Command to execute
        execution_command = f'java -jar {tool_path} {file_name}'

        # Execute the command
        result = subprocess.run(execution_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Print the result
        print(result.stdout)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Print the current working directory after execution
        current_path = os.getcwd()
        print(f"Current working directory: {current_path}")
'''
def delete_files_by_pattern(folder_path, filename_pattern):
    try:
        # Use glob to find all files matching the pattern in the specified folder
        matching_files = glob.glob(os.path.join(folder_path, filename_pattern))

        # Delete each matching file
        for file_path in matching_files:
            try:
                os.remove(file_path)
                print(f"File deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

def read_csv_files_by_pattern(folder_path,filename_pattern):
    """
    Read a CSV file and extract information from specific columns.

    Parameters:
    - folder_path: The path to the CSV file.
    - filename_pattern: Desired pattern to find proper csv files

    Returns:
    - Tuple of lists containing information extracted from the CSV.
    """

    columns_to_read = ['TestClass', 'TestFilePath', 'ProductionFilePath', 'Assertion Roulette', 'Conditional Test Logic', 'Constructor Initialization', \
                       'Default Test', 'EmptyTest', 'Exception Catching Throwing', 'General Fixture', 'Mystery Guest', 'Print Statement', 'Redundant Assertion',\
                       'Sensitive Equality', 'Verbose Test', 'Sleepy Test', 'Eager Test', 'Lazy Test', 'Duplicate Assert', 'Unknown Test', 'IgnoredTest', \
                       'Resource Optimism', 'Magic Number Test', 'Dependent Test']
    column_data_test_class=[]
    column_data_test_file_path=[]
    column_data_production_file_path=[]
    column_data_Assertion_Roulette=[]
    column_data_Conditional_Test_Logic=[]
    column_data_Constructor_Initialization=[]
    column_data_Default_Test=[]
    column_data_Empty_Test=[]
    column_data_Exception_Catching_Throwing=[]
    column_data_General_Fixture=[]
    column_data_Mystery_Guest=[]
    column_data_Print_Statement=[]
    column_data_Redundant_Assertion=[]
    column_data_Sensitive_Equality=[]
    column_data_Verbose_Test=[]
    column_data_Sleepy_Test=[]
    column_data_Eager_Test=[]
    column_data_Lazy_Test=[]
    column_data_Duplicate_Assert=[]
    column_data_Unknown_Test=[]
    column_data_Ignored_Test=[]
    column_data_Resource_Optimism=[]
    column_data_Magic_Number_Test=[]
    column_data_Dependent_Test=[]
    
    try:
        matching_files = glob.glob(f'{folder_path}/{filename_pattern}')
        for file_path in matching_files:
            print(f"Reading data from: {matching_files}")
            with open(file_path, 'r') as csvfile:
                # Create a CSV Reader object
                csv_reader = csv.DictReader(csvfile)
                # Read and extract information from specific columns
                # Process each row in the CSV file
                for row in csv_reader:
                    # Extract data for each specified column and append to the list
                    column_data_test_class.extend(row[col] for col in columns_to_read if col == 'TestClass')
                    column_data_test_file_path.extend(row[col] for col in columns_to_read if col == 'TestFilePath')
                    column_data_production_file_path.extend(row[col] for col in columns_to_read if col == 'ProductionFilePath')
                    column_data_Assertion_Roulette.extend(row[col] for col in columns_to_read if col == 'Assertion Roulette')
                    column_data_Conditional_Test_Logic.extend(row[col] for col in columns_to_read if col == 'Conditional Test Logic')
                    column_data_Constructor_Initialization.extend(row[col] for col in columns_to_read if col == 'Constructor Initialization')
                    column_data_Default_Test.extend(row[col] for col in columns_to_read if col == 'Default Test')
                    column_data_Empty_Test.extend(row[col] for col in columns_to_read if col == 'EmptyTest')
                    column_data_Exception_Catching_Throwing.extend(row[col] for col in columns_to_read if col == 'Exception Catching Throwing')
                    column_data_General_Fixture.extend(row[col] for col in columns_to_read if col == 'General Fixture')
                    column_data_Mystery_Guest.extend(row[col] for col in columns_to_read if col == 'Mystery Guest')
                    column_data_Print_Statement.extend(row[col] for col in columns_to_read if col == 'Print Statement')
                    column_data_Redundant_Assertion.extend(row[col] for col in columns_to_read if col == 'Redundant Assertion')
                    column_data_Sensitive_Equality.extend(row[col] for col in columns_to_read if col == 'Sensitive Equality')
                    column_data_Verbose_Test.extend(row[col] for col in columns_to_read if col == 'Verbose Test')
                    column_data_Sleepy_Test.extend(row[col] for col in columns_to_read if col == 'Sleepy Test')
                    column_data_Eager_Test.extend(row[col] for col in columns_to_read if col == 'Eager Test')
                    column_data_Lazy_Test.extend(row[col] for col in columns_to_read if col == 'Lazy Test')
                    column_data_Duplicate_Assert.extend(row[col] for col in columns_to_read if col == 'Duplicate Assert')
                    column_data_Unknown_Test.extend(row[col] for col in columns_to_read if col == 'Unknown Test')
                    column_data_Ignored_Test.extend(row[col] for col in columns_to_read if col == 'IgnoredTest')
                    column_data_Resource_Optimism.extend(row[col] for col in columns_to_read if col == 'Resource Optimism')
                    column_data_Magic_Number_Test.extend(row[col] for col in columns_to_read if col == 'Magic Number Test')
                    column_data_Dependent_Test.extend(row[col] for col in columns_to_read if col == 'Dependent Test')

        file_path = 'D:\Master_Thesis\TestSmellDetector\Output_of_TestSmellDetector_Tool.txt'
        zipped_file = zip(column_data_test_class, column_data_Assertion_Roulette, 
                          column_data_Conditional_Test_Logic, column_data_Constructor_Initialization, column_data_Default_Test, column_data_Empty_Test, \
                           column_data_Exception_Catching_Throwing, column_data_General_Fixture, column_data_Mystery_Guest, column_data_Print_Statement, \
                             column_data_Redundant_Assertion, column_data_Sensitive_Equality, column_data_Verbose_Test, column_data_Sleepy_Test, \
                                column_data_Eager_Test, column_data_Lazy_Test, column_data_Duplicate_Assert, column_data_Unknown_Test,  column_data_Ignored_Test, \
                                    column_data_Resource_Optimism, column_data_Magic_Number_Test, column_data_Dependent_Test)
        # Open the file in write mode
        with open(file_path, 'w') as file:
            # Iterate over the lists simultaneously using zip
            for item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11 ,item12,item13,\
                 item14, item15, item16, item17, item18, item19, item20, item21, item22 in zipped_file:
                # Write the elements from each list into the file
                file.write(f"{item1}:\n")
                file.write(f"  TestSmellDetectorTool: Assertion Roulette: {item2}\n")
                file.write(f"  TestSmellDetectorTool: Conditional Test Logic: {item3}\n")
                file.write(f"  TestSmellDetectorTool: Constructor_Initialization: {item4}\n")
                file.write(f"  TestSmellDetectorTool: Default Test: {item5}\n")
                file.write(f"  TestSmellDetectorTool: EmptyTest: {item6}\n")
                file.write(f"  TestSmellDetectorTool: Exception Catching Throwing: {item7}\n")
                file.write(f"  TestSmellDetectorTool: General Fixture: {item8}\n")
                file.write(f"  TestSmellDetectorTool: Mystery Guest: {item9}\n")
                file.write(f"  TestSmellDetectorTool: Print Statement: {item10}\n")
                file.write(f"  TestSmellDetectorTool: Redundant Assertion: {item11}\n")
                file.write(f"  TestSmellDetectorTool: Sensitive Equality: {item12}\n")
                file.write(f"  TestSmellDetectorTool: Verbose Test: {item13}\n")
                file.write(f"  TestSmellDetectorTool: Sleepy Test: {item14}\n")
                file.write(f"  TestSmellDetectorTool: Eager Test: {item15}\n")
                file.write(f"  TestSmellDetectorTool: Lazy Test: {item16}\n")
                file.write(f"  TestSmellDetectorTool: Duplicate Assert: {item17}\n")
                file.write(f"  TestSmellDetectorTool: Unknown Test: {item18}\n")
                file.write(f"  TestSmellDetectorTool: IgnoredTest: {item19}\n")
                file.write(f"  TestSmellDetectorTool: Resource Optimism: {item20}\n")
                file.write(f"  TestSmellDetectorTool: Magic Number Test: {item21}\n")
                file.write(f"  TestSmellDetectorTool: Dependent Test: {item22}\n")

    except FileNotFoundError:
        print(f"File not found: {matching_files}")
        return [], [], []
    except Exception as e:
        print(f"An error occurred: {e}")
        return [], [], []

def read_csv_for_Jnose_tool(input_folder_path, output_folder_path):
    """
    Read a CSV file and extract information from specific columns.

    Parameters:
    - input_folder_path: The path to the CSV file.
    - output_folder_path: The path to write data into txt file from found csv files

    Returns:
    - Tuple of lists containing information extracted from the CSV.
    """
    global_git_clone_url = []
    global_git_project_full_name = [] 
    global_git_project_modified_name = []
    file_path = 'D:\Master_Thesis\Github_Projects\projects.csv'
    try:
        with open(file_path, 'r') as csvfile:
            # Create a CSV DictReader object
            csv_reader = csv.DictReader(csvfile, delimiter=';')

            # Read and extract information from specific columns
            for row in csv_reader:
                if "clone_url" in row:
                    global_git_clone_url.append(row['clone_url'])
                if "Full_name" in row:
                    global_git_project_full_name.append(row['Full_name'])

        for element in global_git_project_full_name:
            global_git_project_modified_name.append(element.split('/')[-1])  
    
    
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return [], [], []
    except Exception as e:
        print(f"An error occurred: {e}")
        return [], [], []
    
    column_data_test_file_name_for_Jnose_tool=[]
    test_smell_types = []
    columns_to_read = ['name', 'testSmellName']                
    try:
        for elem in (global_git_project_modified_name):
            print(f"Reading data from: {elem}" + "_result_byclasstest_testsmells.csv")
            for filename in os.listdir(input_folder_path):
                # Check if the partial name is in the filename
                if elem in filename:
                    # Construct the full file path
                    file_path = os.path.join(input_folder_path, filename)
                    if '.csv' in file_path:
                        with open(file_path, 'r') as csvfile:
                            # Create a CSV Reader object
                            csv_reader = csv.DictReader(csvfile, delimiter = ';')
                            # Read and extract information from specific columns
                            # Process each row in the CSV file  
                            for row in csv_reader:
                                    column_data_test_file_name_for_Jnose_tool.extend(row[col] for col in columns_to_read if col == 'name')
                                    test_smell_types.extend(row[col] for col in columns_to_read if col == 'testSmellName')       
                            
                            test_files = []
                            test_smells = []
                            smell_counts = []

                            # Iterate over the zipped list to populate test_files and test_smells lists
                            for test_file, test_smell in zip(column_data_test_file_name_for_Jnose_tool,test_smell_types):
                                if test_file not in test_files:
                                    test_files.append(test_file)
                                if test_smell not in test_smells:
                                    test_smells.append(test_smell)

                            # Initialize a counter list for each test file
                            for _ in test_files:
                                smell_counts.append([0] * len(test_smells))

                            # Iterate over the zipped list again to count occurrences
                            for test_file, test_smell in zip(column_data_test_file_name_for_Jnose_tool,test_smell_types):
                                file_index = test_files.index(test_file)
                                smell_index = test_smells.index(test_smell)
                                smell_counts[file_index][smell_index] += 1
            # Open a file in write mode
            os.chdir(output_folder_path)
            with open(elem +"_Jnose_Tool_Output.txt", "w") as file:
                # Write the counts of each test smell type for each test file to the file
                for i, test_file in enumerate(test_files):
                    file.write(f"{test_file}" + ".java:\n")
                    for j, test_smell in enumerate(test_smells):
                        count = smell_counts[i][j]
                        if count > 0:
                            file.write(f"  JNoseTool: {test_smell}: {count}\n")
            os.chdir(output_folder_path)
            column_data_test_file_name_for_Jnose_tool = []
            test_smell_types = []
                                           
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return [], [], []
    except Exception as e:
        print(f"An error occurred: {e}")
        return [], [], []


        # Iterate over each file path
        for file_path in file_paths:
            # Check if the file has already been processed
            if file_path in processed_files:
                continue  # Skip the file if already processed

            # Add the file to the set of processed files
            processed_files.add(file_path)

            # Open the input file in read mode
            with open(file_path, 'r') as infile:
                # Read the content of the input file
                content = infile.read()
                # Write the content to the output file
                outfile.write(content)

def merge_text_files(file_paths, output_file_path):
    """
    Merge the contents of multiple text files into a single text file.

    Args:
        file_paths (list): List of file paths to be merged.
        output_file_path (str): Path to the output merged file.
    """
    # Open the output file in append mode
    with open(output_file_path, 'a') as outfile:
        # Iterate over each file path
        for file_path in file_paths:
            # Open each input file in read mode
            with open(file_path, 'r') as infile:
                # Read the content of the input file
                content = infile.read()
                # Write the content to the output file
                outfile.write(content)
            
def updated_merge_txt_files(input_file_path, output_file_path):
    """
    After merging, update merged files according to test files.

    Parameters:
    - input_file_path: Path for output of the (merge_txt_files) function.
    - output_file_path: The path to write data after updating
    """    
    data = {}

    # Read the input file and organize data into a dictionary
    with open(input_file_path, 'r') as input_file:
        current_key = None
        for line in input_file:
            line = line.strip()
            if line.endswith(':'):
                current_key = line
                if current_key not in data:
                    data[current_key] = []
            elif current_key:
                data[current_key].append(line)

    # Write the organized data to the output file
    with open(output_file_path, 'w') as output_file:
        for key, values in data.items():
            output_file.write(key + '\n')
            for value in values:
                output_file.write('  ' + value + '\n')

def remove_empty_lines(input_file_path, output_file_path):
    
    with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
    # Iterate over each line in the input file
        for line in input_file:
            if not len(line.strip()) == 0:
                output_file.write(line)
            else:
                continue
      
def remove_lines_with_zero(input_file_path,output_file_path):
    # Read the content of the file
    with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
        # Iterate over each line in the input file
        for line in input_file:
            # Check if the line ends with ': 0'
            if not line.strip().endswith(': 0'):
                # Write the line to the output file if it doesn't end with ': 0'
                output_file.write(line)

# Execution path for TestSmellDetector Tool
tool_path = 'D:\\Master_Thesis\\TestSmellDetector\\TestSmellDetector.jar'
file_name_path = 'D:\\Master_Thesis\\TestSmellDetector\\output.csv'

# Replace 'filename_pattern' with the pattern you know (e.g., 'Output_TestSmellDetection_*.csv')
filename_pattern = 'Output_TestSmellDetection_*.csv'

# Replace 'folder_path' with the path to the specific folder to delete files which have specific pattern
folder_path = 'D:\\Master_Thesis\\TestSmellDetector'

# Call the function
#delete_files_by_pattern(folder_path, filename_pattern)

# Folder path to delete existing files with specific patterns
output_txt_file = "D:\Master_Thesis\Github_Projects\Results_for_JNose_Tool\Merged_output_txt_file.txt"
updated_txt_output = "D:\Master_Thesis\Github_Projects\Results_for_JNose_Tool\Merged_output_txt_file_updated.txt"
removed_empty_line_txt_output = "D:\Master_Thesis\Github_Projects\Results_for_JNose_Tool\Removed_empty_line_output_txt_file.txt"
final_txt_output = "D:\Master_Thesis\Github_Projects\Results_for_JNose_Tool\Result_output_txt_file.txt"
folder_path_for_merged_data = "D:\Master_Thesis\Github_Projects\Results_for_JNose_Tool"
# Replace 'filename_pattern' with the pattern you know (e.g., 'merged_output_txt__*.csv')
filename_pattern_for_merged_data = "merged_output_txt_*"
filename_pattern_for_TestSmellDetector_output_txt = "Output_*.txt"
# Call the function
delete_files_by_pattern(folder_path_for_merged_data, filename_pattern_for_merged_data)
delete_files_by_pattern(folder_path, filename_pattern_for_TestSmellDetector_output_txt)
delete_files_by_pattern(folder_path_for_merged_data,removed_empty_line_txt_output)
delete_files_by_pattern(folder_path_for_merged_data,final_txt_output)
# Call the function
# execute_tool(tool_path, file_name_path)

# Call the function
read_csv_files_by_pattern(folder_path, filename_pattern)

input_csv_files_path = 'D:\Master_Thesis\Github_Projects\JNose_Output'
output_txt_files_path = 'D:\Master_Thesis\Github_Projects\Results_for_JNose_Tool'

# Call the function
read_csv_for_Jnose_tool(input_csv_files_path,output_txt_files_path)

output_csv_files_for_JNose_path = "D:\Master_Thesis\Github_Projects\Results_for_JNose_Tool"
output_csv_files_for_TestSmellDetector = "D:\Master_Thesis\TestSmellDetector"
matching_csv_files_for_JNose = glob.glob(f'{output_csv_files_for_JNose_path}/*.txt')
matching_csv_files_for_TestSmellDetector = glob.glob(f'{output_csv_files_for_TestSmellDetector}/*.txt')
file_paths = []  # Add all file paths here

for path in matching_csv_files_for_TestSmellDetector:
    for path2 in matching_csv_files_for_JNose:
        file_paths.append(path2)
    file_paths.append(path)

# Call the function

delete_files_by_pattern(folder_path_for_merged_data, filename_pattern_for_merged_data)

merge_text_files(file_paths, output_txt_file)

updated_merge_txt_files(output_txt_file, updated_txt_output)

remove_empty_lines(updated_txt_output, removed_empty_line_txt_output)

remove_lines_with_zero(removed_empty_line_txt_output,final_txt_output)
