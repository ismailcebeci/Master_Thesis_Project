import csv
import os
import subprocess


def read_csv_and_extract_info(file_path):
    """
    Read a CSV file and extract information from specific columns.

    Parameters:
    - file_path: The path to the CSV file.

    Returns:
    - Tuple of lists containing information extracted from the CSV.
    """

    git_clone_url = []
    git_project_full_name = []
    git_project_modified_name = []

    global_git_clone_url = []
    global_git_project_full_name = [] 
    global_git_project_modified_name = []

    try:
        with open(file_path, 'r') as csvfile:
            # Create a CSV DictReader object
            csv_reader = csv.DictReader(csvfile, delimiter=';')

            # Read and extract information from specific columns
            for row in csv_reader:
                if "clone_url" in row:
                    git_clone_url.append(row['clone_url'])
                    global_git_clone_url.append(row['clone_url'])
                if "Full_name" in row:
                    git_project_full_name.append(row['Full_name'])
                    global_git_project_full_name.append(row['Full_name'])

        for element in git_project_full_name:
            git_project_modified_name.append(element.split('/')[-1])
            global_git_project_modified_name.append(element.split('/')[-1])
        return git_clone_url, git_project_full_name, git_project_modified_name

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return [], [], []
    except Exception as e:
        print(f"An error occurred: {e}")
        return [], [], []

def create_folders(base_path, folder_names):
    """
    Create folders in the specified base path. 
    Call read_csv_and_extract_info function before using this function.

    Parameters:
    - base_path: The base path where new folders will be created.
    - folder_names: List of folder names.

    Returns:
    - List of paths to the created folders.
    """
    new_folders = []

    try:
        # Create folders
        for folder_name in folder_names:
            new_folder_path = os.path.join(base_path, folder_name)

            # Check if the folder already exists before creating
            if not os.path.exists(new_folder_path):
                os.mkdir(new_folder_path)
                print(f"Folder '{new_folder_path}' created successfully.")
                new_folders.append(new_folder_path)
            else:
                print(f"Folder '{new_folder_path}' already exists.")

        return new_folders

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def clone_git_projects(base_path, git_clone_url, git_project_modified_name):
    """
    Clone git projects into specified local paths.

    Parameters:
    - base_path: The base path where repositories will be cloned.
    - git_clone_url: List of git clone URLs.
    - git_project_full_name: List of full project names.

    Returns:
    - List of paths to the cloned repositories.
    """
    try:
        for elem in git_clone_url:
            for filename in os.listdir(base_path):
                for elem2 in git_project_modified_name:
                    if elem2 in filename and elem2 in elem:
                        full_path = os.path.join(base_path, elem2)
                        if len(os.listdir(full_path)) == 0:
                            subprocess.run(['git', 'clone', elem, full_path], check=True)
                            print(f"Repository cloned successfully to '{full_path}'.")
                        else:
                            print(f"Folder is not empty. Git cloning aborted")
                    else:
                        continue

    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def find_files_for_test_and_source_codes_by_partial_name(folder_path, partial_name):
    """
    Find files in a folder based on a partial match of their names.

    Parameters:
    - folder_path: The path to the folder to search in.
    - partial_name: The partial name to match against file names.

    Returns:
    - List of file paths matching the partial name.
    """
    matching_files_for_test_code = []
    updated_matching_files_for_test_code = []
    matching_files_for_source_code = []
    updated_matching_files_for_source_code = []
    temp_list = []
    source_file_name = []

    try:
        # Iterate through all files in the folder
        #Finding all test file in specific folder
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                if partial_name in file_name:
                    file_path = os.path.join(root, file_name)
                    matching_files_for_test_code.append(file_path)

        # Changing name of files which contains Test.java to .java file to find source files
        for variable in matching_files_for_test_code:
            temp_list = variable.replace('Test.java', '.java').split('\\')
            source_file_name.append(temp_list[-1])
        
        # Finding all source files of found test files
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                for elem in (source_file_name):
                    if elem in file_name:
                        file_path = os.path.join(root, file_name)
                        if file_path not in matching_files_for_source_code:
                            matching_files_for_source_code.append(file_path)
                        else:
                            continue
        
        #Arranging files according to assosiation between files
        ''' Some found files for test and source can be irrelavent 
        For example some found source file do not have test file which are found. 
        Therefore, whichever source file has a test file, it is saved them to the list.
        '''
        for item in matching_files_for_source_code:
            temp_item = item.split('\\')[-1]
            temp_item2 = temp_item.split('.')[0]
            for element in matching_files_for_test_code:
                if (temp_item2 + 'Test.java') in element \
                    and (temp_item2 + 'Test.java') not in updated_matching_files_for_test_code \
                    and item not in updated_matching_files_for_source_code\
                    and element not in updated_matching_files_for_test_code :
                    updated_matching_files_for_test_code.append(element) #for test code
                    updated_matching_files_for_source_code.append(item) #for source code
                else:
                    continue

        return updated_matching_files_for_test_code, updated_matching_files_for_source_code

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def write_lists_to_csv(constant_name,list1, list2, output_folder, file_name):
    """
    Write pairs of items from two lists to a CSV file.

    Parameters:
    - list1: The first list of items.
    - list2: The second list of items.
    - output_folder: The path to the folder where the CSV file will be saved.
    - file_name: The name of the CSV file.

    Returns:
    - None
    """
    # Combine the folder and file path
    file_path = os.path.join(output_folder, file_name)

    # Writing to CSV file with zip and a for loop
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Writing each pair of items in the same row using a for loop and zip
        for item1, item2 in zip(list1, list2):
            csv_writer.writerow([constant_name,item1, item2])

    print(f'Data written to {file_path} successfully.')

def remove_java_test_and_source_files_from_list(test_file_paths,source_file_paths):
    
    """
    Remove test and source files which contains just comment lines in list.

    Parameters:
    - test_file_paths: The path for test files.
    - source_file_paths: The path for source names.

    Returns:
    - List of file paths after removing irrelavent files from list.
    """
    result_paths_for_test_code = []
    updated_results_paths_for_test_code = []
    updated_results_paths_for_source_code = []
    
    # Finding test files which contains only comments lines and remove them from list
    for element in test_file_paths:
        try:
            with open(element, 'r') as file:
                result = []
                for line in file:
                    # Check if the line is a comment or empty
                    if '/*' in line or ' * ' in line or '*/' in line:
                        result.append(True)
                    else:
                        result.append(False)

        except FileNotFoundError:
            print(f"File not found: {element}")

        except Exception as e:
            print(f"An error occurred: {e}")

        if all(result):
            continue
        else:
            result_paths_for_test_code.append(element)
    
    #Removing irrelavent source files to remove from list according to result of removing test files process
    
    for item in source_file_paths:
        temp_item = item.split('\\')[-1]
        temp_item2 = temp_item.split('.')[0]
        for element in result_paths_for_test_code:
            if (temp_item2 + 'Test.java') in element \
                and (temp_item2 + 'Test.java') not in updated_results_paths_for_test_code \
                and item not in updated_results_paths_for_source_code\
                and element not in updated_results_paths_for_test_code :
                updated_results_paths_for_test_code.append(element) #for test code
                updated_results_paths_for_source_code.append(item) #for source code

            else:
                continue
    
    return updated_results_paths_for_test_code, updated_results_paths_for_source_code


#--------------------------------------------------------------------------------------------------------------------------------------

#Calling read_csv_and_extract_info function
file_path = 'D:\Master_Thesis\Github_Projects\projects.csv'
base_path = 'D:\Master_Thesis\Github_Projects'
git_clone_url, git_project_full_name, git_project_modified_name = read_csv_and_extract_info(file_path)

# Now you can use the extracted information as needed
print("Git Clone URLs:", git_clone_url)
print("Git Project Full Names:", git_project_full_name)
print("Git Project Modified Names:", git_project_modified_name)

#--------------------------------------------------------------------------------------------------------------------------------------

#Calling create_folders function
create_folders(base_path, git_project_modified_name)

#--------------------------------------------------------------------------------------------------------------------------------------

#Calling clone_git_projects function
clone_git_projects(base_path, git_clone_url, git_project_modified_name)

#--------------------------------------------------------------------------------------------------------------------------------------

#Calling find_files_for_test_and_source_codes_by_partial_name
partial_name_for_test_codes = 'Test.java'
path_for_test_files, path_for_source_files = find_files_for_test_and_source_codes_by_partial_name(base_path, partial_name_for_test_codes)

if path_for_test_files:
    print(f"Found {len(path_for_test_files)} files:")
    for file_path in path_for_test_files:
        print(file_path)
else:
    print(f"No files found with partial name '{partial_name_for_test_codes}'.")

if path_for_source_files:
    print(f"Found {len(path_for_source_files)} files:")
    for file_path in path_for_source_files:
        print(file_path)
else:
    print(f"No files found.")

#--------------------------------------------------------------------------------------------------------------------------------------

#Calling process_java_test_files to remove files which contains just comment lines from list

proper_java_test_code_paths, proper_java_source_test_code_paths = remove_java_test_and_source_files_from_list(path_for_test_files,path_for_source_files)

if proper_java_test_code_paths:
    print(f"Found {len(proper_java_test_code_paths)} files:")
    for file_path in proper_java_test_code_paths:
        print(file_path)
else:
    print(f"No files found.")

if proper_java_source_test_code_paths:
    print(f"Found {len(proper_java_source_test_code_paths)} files:")
    for file_path in proper_java_source_test_code_paths:
        print(file_path)
else:
    print(f"No files found.")

#--------------------------------------------------------------------------------------------------------------------------------------

#Calling write_lists_to_csv function to write values into cvs file to use for TestSmellDetector Project

output_folder = 'D:\Master_Thesis\TestSmellDetector'  # TestSmellDetector project path
file_name = 'output.csv'
app_name = 'TestSmellDetector'
write_lists_to_csv(app_name,proper_java_test_code_paths, proper_java_source_test_code_paths, output_folder, file_name)
