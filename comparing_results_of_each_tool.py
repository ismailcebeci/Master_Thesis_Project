import subprocess
import os
import glob
import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations
data = []

test_smells = ["Magic Number", "Assertion Roulette", "Conditional Test Logic", "Constructor Initialization",
               "Default Test", "Empty Test", "Exception Catching Throwing", "General Fixture", "Mystery Guest",
               "Print Statement", "Redundant Assertion", "Sensitive Equality", "Verbose Test", "Sleepy Test",
               "Eager Test", "Lazy Test", "Duplicate Assert", "Unknown Test", "Ignored Test", "Resource Optimism",
               "Dependent Test"]
# Function to calculate co-occurrence matrix for a specific tool

def calculate_co_occurrence(test_smells):
    co_occurrence_matrix = np.zeros((len(test_smells), len(test_smells)))
    for pair in combinations(range(len(test_smells)), 2):
        index1, index2 = pair
        count_smell1 = test_smells[index1]
        count_smell2 = test_smells[index2]
        if count_smell1 > 0 and count_smell2 > 0:
            co_occurrence_ratio = min(count_smell1, count_smell2) / max(count_smell1, count_smell2)
        else:
            co_occurrence_ratio = 0.0
        co_occurrence_matrix[index1][index2] = co_occurrence_ratio
        co_occurrence_matrix[index2][index1] = co_occurrence_ratio
    return co_occurrence_matrix

# Function to plot heatmap with numerical annotations
def plot_heatmap_with_annotations(co_occurrence_matrix, test_smells, tool, save_dir):
    plt.figure(figsize=(25, 12))  # Set the figure size
    plt.imshow(co_occurrence_matrix, cmap='Blues', interpolation='nearest')
    plt.colorbar(label='Co-occurrences')
    plt.title(f'Co-occurrence Matrix for {tool}')
    plt.xlabel('Test Smells')
    plt.ylabel('Test Smells')

    # Add test smells names on x and y axes
    plt.xticks(np.arange(len(test_smells)), test_smells, rotation=90)
    plt.yticks(np.arange(len(test_smells)), test_smells)

    # Add numerical annotations
    for i in range(len(test_smells)):
        for j in range(len(test_smells)):
            plt.text(j, i, f'{co_occurrence_matrix[i][j]:.2f}', ha='center', va='center', color='black')

    plt.savefig(os.path.join(save_dir, f'Co-occurance_of_test_smells_with_{tool}.png'), bbox_inches='tight')
    plt.show()


# Read the data from the text file
file_path = "D:\Master_Thesis\Github_Projects\Results_for_JNose_Tool\Result_output_txt_file.txt"
with open(file_path, 'r') as file:
    current_file = ""
    for line in file:
        line = line.strip()
        if line.endswith(".java:"):
            current_file = line.replace(":", "")
        else:
            parts = [part.strip() for part in line.split(":")]
            if len(parts) == 3:
                tool, smell, count = parts
                count = int(count)
                data.append((current_file, tool, smell, count))
            else:
                print(f"Invalid line: {line}")
# Group the data by file name
grouped_data = {}

total_test_smell_for_jnose_tool_in_all_files = 0
total_test_smell_for_testsmelldetector_tool_in_all_files = 0
total_test_smell_in_all_files = 0

for item in data:
    file_name, tool_name, test_smell, count = item
    if file_name not in grouped_data:
        grouped_data[file_name] = []
    grouped_data[file_name].append((tool_name, test_smell, count))


# Initialize total counters for each test smells
total_magic_number_test_for_jnose_tool = total_magic_number_test_for_testsmelldetector_tool = total_assertion_roulette_for_jnose_tool = \
total_assertion_roulette_for_testsmelldetector_tool = total_conditional_test_logic_for_jnose_tool = total_conditional_test_logic_for_testsmelldetector_tool =  \
total_constructor_initialization_for_jnose_tool = total_constructor_initialization_for_testsmelldetector_tool = total_default_test_for_jnose_tool = \
total_default_test_for_testsmelldetector_tool =  total_empty_test_for_jnose_tool = total_empty_test_for_testsmelldetector_tool = \
total_exception_catching_throwing_for_jnose_tool = total_exception_catching_throwing_for_testsmelldetector_tool = total_general_fixture_for_jnose_tool = \
total_general_fixture_for_testsmelldetector_tool = total_mystery_guest_for_jnose_tool = total_mystery_guest_for_testsmelldetector_tool = total_print_statement_for_jnose_tool = \
total_print_statement_for_testsmelldetector_tool = total_redundant_assertion_for_jnose_tool = total_redundant_assertion_for_testsmelldetector_tool = \
total_sensitive_equality_for_jnose_tool =  total_sensitive_equality_for_testsmelldetector_tool = total_verbose_test_for_jnose_tool = \
total_verbose_test_for_testsmelldetector_tool = total_sleepy_test_for_jnose_tool = total_sleepy_test_for_testsmelldetector_tool = total_eager_test_for_jnose_tool = \
total_eager_test_for_testsmelldetector_tool = total_lazy_test_for_jnose_tool = total_lazy_test_for_testsmelldetector_tool = total_duplicate_assert_for_jnose_tool = \
total_duplicate_assert_for_testsmelldetector_tool = total_unknown_test_for_jnose_tool = total_unknown_test_for_testsmelldetector_tool = total_ignored_test_for_jnose_tool = \
total_ignored_test_for_testsmelldetector_tool = total_resource_optimism_for_jnose_tool = total_resource_optimism_for_testsmelldetector_tool = \
total_dependent_test_for_jnose_tool = total_dependent_test_for_testsmelldetector_tool = 0

# Initialize counters for each affected files
file_count_affected_by_magic_number_test_for_jnose_tool = file_count_affected_by_magic_number_test_for_testsmelldetector_tool = file_count_affected_by_assertion_roulette_for_jnose_tool = \
file_count_affected_by_assertion_roulette_for_testsmelldetector_tool = file_count_affected_by_conditional_test_logic_for_jnose_tool = file_count_affected_by_conditional_test_logic_for_testsmelldetector_tool =  \
file_count_affected_by_constructor_initialization_for_jnose_tool = file_count_affected_by_constructor_initialization_for_testsmelldetector_tool = file_count_affected_by_default_test_for_jnose_tool = \
file_count_affected_by_default_test_for_testsmelldetector_tool =  file_count_affected_by_empty_test_for_jnose_tool = file_count_affected_by_empty_test_for_testsmelldetector_tool = \
file_count_affected_by_exception_catching_throwing_for_jnose_tool = file_count_affected_by_exception_catching_throwing_for_testsmelldetector_tool = file_count_affected_by_general_fixture_for_jnose_tool = \
file_count_affected_by_general_fixture_for_testsmelldetector_tool = file_count_affected_by_mystery_guest_for_jnose_tool = file_count_affected_by_mystery_guest_for_testsmelldetector_tool = file_count_affected_by_print_statement_for_jnose_tool = \
file_count_affected_by_print_statement_for_testsmelldetector_tool = file_count_affected_by_redundant_assertion_for_jnose_tool = file_count_affected_by_redundant_assertion_for_testsmelldetector_tool = \
file_count_affected_by_sensitive_equality_for_jnose_tool = file_count_affected_by_sensitive_equality_for_testsmelldetector_tool = file_count_affected_by_verbose_test_for_jnose_tool = \
file_count_affected_by_verbose_test_for_testsmelldetector_tool = file_count_affected_by_sleepy_test_for_jnose_tool = file_count_affected_by_sleepy_test_for_testsmelldetector_tool = file_count_affected_by_eager_test_for_jnose_tool = \
file_count_affected_by_eager_test_for_testsmelldetector_tool = file_count_affected_by_lazy_test_for_jnose_tool = file_count_affected_by_lazy_test_for_testsmelldetector_tool = file_count_affected_by_duplicate_assert_for_jnose_tool = \
file_count_affected_by_duplicate_assert_for_testsmelldetector_tool = file_count_affected_by_unknown_test_for_jnose_tool = file_count_affected_by_unknown_test_for_testsmelldetector_tool = file_count_affected_by_ignored_test_for_jnose_tool = \
file_count_affected_by_ignored_test_for_testsmelldetector_tool = file_count_affected_by_resource_optimism_for_jnose_tool = file_count_affected_by_resource_optimism_for_testsmelldetector_tool = \
file_count_affected_by_dependent_test_for_jnose_tool = file_count_affected_by_dependent_test_for_testsmelldetector_tool = 0

# Initialize number_of_total files and total affected files
number_of_total_file = no_affected_files = no_affected_files_for_jnose_tool = no_affected_files_for_testsmelldetector_tool = no_affected_files_for_both_tool= 0

for file_name, file_data in grouped_data.items():
    # Extract unique test smells for the file
    unique_test_smells = set(test_smell for _, test_smell, _ in file_data)
    # Initialize lists to store counts for each tool
    jnose_tool_counts = []
    testsmelldetector_tool_counts = []
    test_smell_names_for_jnose_tool = []
    test_smell_names_for_testsmelldetector_tool = []
    
    # Initialize counters for each test smell in each file
    magic_number_test_for_jnose_tool = magic_number_test_for_testsmelldetector_tool = assertion_roulette_for_jnose_tool = assertion_roulette_for_testsmelldetector_tool = \
    conditional_test_logic_for_jnose_tool = conditional_test_logic_for_testsmelldetector_tool = constructor_initialization_for_jnose_tool = \
    constructor_initialization_for_testsmelldetector_tool = default_test_for_jnose_tool = default_test_for_testsmelldetector_tool = empty_test_for_jnose_tool = \
    empty_test_for_testsmelldetector_tool = exception_catching_throwing_for_jnose_tool = exception_catching_throwing_for_testsmelldetector_tool = \
    general_fixture_for_jnose_tool = general_fixture_for_testsmelldetector_tool = mystery_guest_for_jnose_tool = mystery_guest_for_testsmelldetector_tool = \
    print_statement_for_jnose_tool = print_statement_for_testsmelldetector_tool = redundant_assertion_for_jnose_tool = redundant_assertion_for_testsmelldetector_tool = \
    sensitive_equality_for_jnose_tool = sensitive_equality_for_testsmelldetector_tool = verbose_test_for_jnose_tool = verbose_test_for_testsmelldetector_tool = \
    sleepy_test_for_jnose_tool = sleepy_test_for_testsmelldetector_tool = eager_test_for_jnose_tool = eager_test_for_testsmelldetector_tool = lazy_test_for_jnose_tool = \
    lazy_test_for_testsmelldetector_tool = duplicate_assert_for_jnose_tool = duplicate_assert_for_testsmelldetector_tool = unknown_test_for_jnose_tool = \
    unknown_test_for_testsmelldetector_tool = ignored_test_for_jnose_tool = ignored_test_for_testsmelldetector_tool = resource_optimism_for_jnose_tool = \
    resource_optimism_for_testsmelldetector_tool = dependent_test_for_jnose_tool = dependent_test_for_testsmelldetector_tool = 0

    # Initialize total counters for each tool in each file
    total_test_smell_for_jnose_tool_in_file = total_test_smell_for_testsmelldetector_tool_in_file = total_test_smell_in_file = 0
    
    # Initialize ratio of each test smell to total number of test smells in each file
    ratio_of_magic_number_test_for_jnose_tool_to_total = ratio_of_magic_number_test_for_testsmelldetector_tool_to_total = \
    ratio_of_assertion_roulette_for_jnose_tool_to_total = ratio_of_assertion_roulette_for_testsmelldetector_tool_to_total = \
    ratio_of_conditional_test_logic_for_jnose_tool_to_total = ratio_of_conditional_test_logic_for_testsmelldetector_tool_to_total = \
    ratio_of_constructor_initialization_for_jnose_tool_to_total = ratio_of_constructor_initialization_for_testsmelldetector_tool_to_total = \
    ratio_of_default_test_for_jnose_tool_to_total = ratio_of_default_test_for_testsmelldetector_tool_to_total = \
    ratio_of_empty_test_for_jnose_tool_to_total = ratio_of_empty_test_for_testsmelldetector_tool_to_total = \
    ratio_of_exception_catching_throwing_for_jnose_tool_to_total = ratio_of_exception_catching_throwing_for_testsmelldetector_tool_to_total = \
    ratio_of_general_fixture_for_jnose_tool_to_total = ratio_of_general_fixture_for_testsmelldetector_tool_to_total = \
    ratio_of_mystery_guest_for_jnose_tool_to_total = mystery_guest_for_testsmelldetector_tool_to_total = \
    ratio_of_print_statement_for_jnose_tool = ratio_of_print_statement_for_testsmelldetector_tool = \
    ratio_of_redundant_assertion_for_jnose_tool_to_total = ratio_of_redundant_assertion_for_testsmelldetector_tool_to_total = \
    ratio_of_sensitive_equality_for_jnose_tool = ratio_of_sensitive_equality_for_testsmelldetector_tool = \
    ratio_of_verbose_test_for_jnose_tool_to_total = ratio_of_verbose_test_for_testsmelldetector_tool_to_total = \
    ratio_of_sleepy_test_for_jnose_tool_to_total = ratio_of_sleepy_test_for_testsmelldetector_tool_to_total = \
    ratio_of_eager_test_for_jnose_tool_to_total = ratio_of_eager_test_for_testsmelldetector_tool_to_total = \
    ratio_of_lazy_test_for_jnose_tool_to_total =  ratio_of_lazy_test_for_testsmelldetector_tool_to_total = \
    ratio_of_duplicate_assert_for_jnose_tool_to_total = ratio_of_duplicate_assert_for_testsmelldetector_tool_to_total = \
    ratio_of_unknown_test_for_jnose_tool_to_total = ratio_of_unknown_test_for_testsmelldetector_tool_to_total = \
    ratio_of_ratio_of_ignored_test_for_jnose_tool_to_total = ratio_of_ignored_test_for_testsmelldetector_tool_to_total = \
    ratio_of_resource_optimism_for_jnose_tool_to_total = ratio_of_resource_optimism_for_testsmelldetector_tool_to_total = \
    ratio_of_dependent_test_for_jnose_tool_to_total = ratio_of_dependent_test_for_testsmelldetector_tool_to_total = 0

    # Calculate the union of unique test smells for both tools
    all_unique_test_smells = set(test_smell for _, test_smell, _ in file_data)

    # Initialize counts for each tool
    jnose_tool_counts = []
    testsmelldetector_tool_counts = []

    for smell in unique_test_smells:
        # Get counts for each tool
        # Get count for JNoseTool
        jnose_count = sum(count for _, test_smell, count in file_data if test_smell == smell and _ == 'JNoseTool')
        jnose_tool_counts.append(jnose_count)
        
        # Get count for TestSmellDetectorTool
        detector_count = sum(count for _, test_smell, count in file_data if test_smell == smell and _ == 'TestSmellDetectorTool')
        testsmelldetector_tool_counts.append(detector_count)
        test_smell_name_for_jnose_tool = next(((test_smell for _, test_smell, count in file_data if test_smell == smell and _ == 'JNoseTool')), 0)

        test_smell_names_for_jnose_tool.append(test_smell_name_for_jnose_tool)

        test_smell_name_for_testsmelldetector_tool = next(((test_smell for _, test_smell, count in file_data if test_smell == smell \
                                                            and _ == 'TestSmellDetectorTool')), 0)

        test_smell_names_for_testsmelldetector_tool.append(test_smell_name_for_testsmelldetector_tool)

    #print(test_smell_names_for_jnose_tool,test_smell_names_for_testsmelldetector_tool)
    # Counting test smells for JNoseTool in each file and total number of each test smells type in all files for JNose Tool.
    for i in range(len(test_smell_names_for_jnose_tool)):
        if test_smell_names_for_jnose_tool[i] == 'Magic Number Test':
            magic_number_test_for_jnose_tool += jnose_tool_counts[i] 
            total_magic_number_test_for_jnose_tool += jnose_tool_counts[i]
            file_count_affected_by_magic_number_test_for_jnose_tool += 1
        elif test_smell_names_for_jnose_tool[i] == 'Assertion Roulette':
            assertion_roulette_for_jnose_tool += jnose_tool_counts[i] 
            total_assertion_roulette_for_jnose_tool += jnose_tool_counts[i]
            file_count_affected_by_assertion_roulette_for_jnose_tool += 1
        elif test_smell_names_for_jnose_tool[i] == 'Conditional Test Logic':
            conditional_test_logic_for_jnose_tool += jnose_tool_counts[i] 
            total_conditional_test_logic_for_jnose_tool += jnose_tool_counts[i]
            file_count_affected_by_conditional_test_logic_for_jnose_tool += 1
        elif test_smell_names_for_jnose_tool[i] == 'Constructor Initialization':
            constructor_initialization_for_jnose_tool += jnose_tool_counts[i] 
            total_constructor_initialization_for_jnose_tool += jnose_tool_counts[i]
            file_count_affected_by_constructor_initialization_for_jnose_tool += 1
        elif test_smell_names_for_jnose_tool[i] == 'Default Test':
            default_test_for_jnose_tool += jnose_tool_counts[i] 
            total_default_test_for_jnose_tool += jnose_tool_counts[i]
            file_count_affected_by_default_test_for_jnose_tool += 1
        elif test_smell_names_for_jnose_tool[i] == 'EmptyTest':
            empty_test_for_jnose_tool += jnose_tool_counts[i] 
            total_empty_test_for_jnose_tool += jnose_tool_counts[i]
            file_count_affected_by_empty_test_for_jnose_tool += 1
        elif test_smell_names_for_jnose_tool[i] == 'Exception Catching Throwing':
            exception_catching_throwing_for_jnose_tool += jnose_tool_counts[i] 
            total_exception_catching_throwing_for_jnose_tool += jnose_tool_counts[i]
            file_count_affected_by_exception_catching_throwing_for_jnose_tool += 1
        elif test_smell_names_for_jnose_tool[i] == 'General Fixture':
            general_fixture_for_jnose_tool += jnose_tool_counts[i] 
            total_general_fixture_for_jnose_tool += jnose_tool_counts[i]
            file_count_affected_by_general_fixture_for_jnose_tool += 1
        elif test_smell_names_for_jnose_tool[i] == 'Mystery Guest':
            mystery_guest_for_jnose_tool += jnose_tool_counts[i] 
            total_mystery_guest_for_jnose_tool += jnose_tool_counts[i]
            file_count_affected_by_mystery_guest_for_jnose_tool += 1
        elif test_smell_names_for_jnose_tool[i] == 'Print Statement':
            print_statement_for_jnose_tool += jnose_tool_counts[i] 
            total_print_statement_for_jnose_tool += jnose_tool_counts[i]
            file_count_affected_by_print_statement_for_jnose_tool += 1
        elif test_smell_names_for_jnose_tool[i] == 'Redundant Assertion':
            redundant_assertion_for_jnose_tool += jnose_tool_counts[i] 
            total_redundant_assertion_for_jnose_tool += jnose_tool_counts[i]
            file_count_affected_by_redundant_assertion_for_jnose_tool += 1
        elif test_smell_names_for_jnose_tool[i] == 'Sensitive Equality':
            sensitive_equality_for_jnose_tool += jnose_tool_counts[i] 
            total_sensitive_equality_for_jnose_tool += jnose_tool_counts[i]
            file_count_affected_by_sensitive_equality_for_jnose_tool += 1
        elif test_smell_names_for_jnose_tool[i] == 'Verbose Test':
            verbose_test_for_jnose_tool += jnose_tool_counts[i] 
            total_verbose_test_for_jnose_tool += jnose_tool_counts[i]
            file_count_affected_by_verbose_test_for_jnose_tool += 1
        elif test_smell_names_for_jnose_tool[i] == 'Sleepy Test':
            sleepy_test_for_jnose_tool += jnose_tool_counts[i] 
            total_sleepy_test_for_jnose_tool += jnose_tool_counts[i]
            file_count_affected_by_sleepy_test_for_jnose_tool += 1
        elif test_smell_names_for_jnose_tool[i] == 'Eager Test':
            eager_test_for_jnose_tool += jnose_tool_counts[i] 
            total_eager_test_for_jnose_tool += jnose_tool_counts[i]
            file_count_affected_by_eager_test_for_jnose_tool += 1
        elif test_smell_names_for_jnose_tool[i] == 'Lazy Test':
            lazy_test_for_jnose_tool += jnose_tool_counts[i] 
            total_lazy_test_for_jnose_tool += jnose_tool_counts[i]
            file_count_affected_by_lazy_test_for_jnose_tool += 1
        elif test_smell_names_for_jnose_tool[i] == 'Duplicate Assert':
            duplicate_assert_for_jnose_tool += jnose_tool_counts[i] 
            total_duplicate_assert_for_jnose_tool += jnose_tool_counts[i]
            file_count_affected_by_duplicate_assert_for_jnose_tool += 1
        elif test_smell_names_for_jnose_tool[i] == 'Unknown Test':
            unknown_test_for_jnose_tool += jnose_tool_counts[i] 
            total_unknown_test_for_jnose_tool += jnose_tool_counts[i]
            file_count_affected_by_unknown_test_for_jnose_tool += 1
        elif test_smell_names_for_jnose_tool[i] == 'IgnoredTest':
            ignored_test_for_jnose_tool += jnose_tool_counts[i] 
            total_ignored_test_for_jnose_tool += jnose_tool_counts[i]
            file_count_affected_by_ignored_test_for_jnose_tool += 1
        elif test_smell_names_for_jnose_tool[i] == 'Resource Optimism':
            resource_optimism_for_jnose_tool += jnose_tool_counts[i] 
            total_resource_optimism_for_jnose_tool += jnose_tool_counts[i]
            file_count_affected_by_resource_optimism_for_jnose_tool += 1
        elif test_smell_names_for_jnose_tool[i] == 'Dependent Test':
            dependent_test_for_jnose_tool += jnose_tool_counts[i] 
            total_dependent_test_for_jnose_tool += jnose_tool_counts[i]
            file_count_affected_by_dependent_test_for_jnose_tool += 1

    # Counting test smells for TestSmellDetector in each file and total number of each test smells type in all files for TestSmellDetector.
    for i in range(len(test_smell_names_for_testsmelldetector_tool)):
        if test_smell_names_for_testsmelldetector_tool[i] == 'Magic Number Test':
            magic_number_test_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            total_magic_number_test_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            file_count_affected_by_magic_number_test_for_testsmelldetector_tool += 1
        elif test_smell_names_for_testsmelldetector_tool[i] == 'Assertion Roulette':
            assertion_roulette_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            total_assertion_roulette_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            file_count_affected_by_assertion_roulette_for_testsmelldetector_tool += 1
        elif test_smell_names_for_testsmelldetector_tool[i] == 'Conditional Test Logic':
            conditional_test_logic_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            total_conditional_test_logic_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            file_count_affected_by_conditional_test_logic_for_testsmelldetector_tool += 1
        elif test_smell_names_for_testsmelldetector_tool[i] == 'Constructor Initialization':
            constructor_initialization_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            total_constructor_initialization_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            file_count_affected_by_constructor_initialization_for_testsmelldetector_tool += 1
        elif test_smell_names_for_testsmelldetector_tool[i] == 'Default Test':
            default_test_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            total_default_test_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            file_count_affected_by_default_test_for_testsmelldetector_tool += 1
        elif test_smell_names_for_testsmelldetector_tool[i] == 'EmptyTest':
            empty_test_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            total_empty_test_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            file_count_affected_by_empty_test_for_testsmelldetector_tool += 1
        elif test_smell_names_for_testsmelldetector_tool[i] == 'Exception Catching Throwing':
            exception_catching_throwing_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            total_exception_catching_throwing_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            file_count_affected_by_exception_catching_throwing_for_testsmelldetector_tool += 1
        elif test_smell_names_for_testsmelldetector_tool[i] == 'General Fixture':
            general_fixture_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            total_general_fixture_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            file_count_affected_by_general_fixture_for_testsmelldetector_tool += 1
        elif test_smell_names_for_testsmelldetector_tool[i] == 'Mystery Guest':
            mystery_guest_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            total_mystery_guest_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            file_count_affected_by_mystery_guest_for_testsmelldetector_tool += 1
        elif test_smell_names_for_testsmelldetector_tool[i] == 'Print Statement':
            print_statement_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            total_print_statement_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            file_count_affected_by_print_statement_for_testsmelldetector_tool += 1
        elif test_smell_names_for_testsmelldetector_tool[i] == 'Redundant Assertion':
            redundant_assertion_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            total_redundant_assertion_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            file_count_affected_by_redundant_assertion_for_testsmelldetector_tool += 1
        elif test_smell_names_for_testsmelldetector_tool[i] == 'Sensitive Equality':
            sensitive_equality_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            total_sensitive_equality_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            file_count_affected_by_sensitive_equality_for_testsmelldetector_tool += 1
        elif test_smell_names_for_testsmelldetector_tool[i] == 'Verbose Test':
            verbose_test_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            total_verbose_test_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            file_count_affected_by_verbose_test_for_testsmelldetector_tool += 1
        elif test_smell_names_for_testsmelldetector_tool[i] == 'Sleepy Test':
            sleepy_test_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            total_sleepy_test_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            file_count_affected_by_sleepy_test_for_testsmelldetector_tool += 1
        elif test_smell_names_for_testsmelldetector_tool[i] == 'Eager Test':
            eager_test_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            total_eager_test_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            file_count_affected_by_eager_test_for_testsmelldetector_tool += 1
        elif test_smell_names_for_testsmelldetector_tool[i] == 'Lazy Test':
            lazy_test_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            total_lazy_test_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            file_count_affected_by_lazy_test_for_testsmelldetector_tool += 1
        elif test_smell_names_for_testsmelldetector_tool[i] == 'Duplicate Assert':
            duplicate_assert_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            total_duplicate_assert_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            file_count_affected_by_duplicate_assert_for_testsmelldetector_tool += 1
        elif test_smell_names_for_testsmelldetector_tool[i] == 'Unknown Test':
            unknown_test_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            total_unknown_test_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            file_count_affected_by_unknown_test_for_testsmelldetector_tool += 1
        elif test_smell_names_for_testsmelldetector_tool[i] == 'IgnoredTest':
            ignored_test_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            total_ignored_test_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            file_count_affected_by_ignored_test_for_testsmelldetector_tool += 1
        elif test_smell_names_for_testsmelldetector_tool[i] == 'Resource Optimism':
            resource_optimism_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            total_resource_optimism_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            file_count_affected_by_resource_optimism_for_testsmelldetector_tool += 1
        elif test_smell_names_for_testsmelldetector_tool[i] == 'Dependent Test':
            dependent_test_for_testsmelldetector_tool += testsmelldetector_tool_counts[i]
            total_dependent_test_for_testsmelldetector_tool += testsmelldetector_tool_counts[i] 
            file_count_affected_by_dependent_test_for_testsmelldetector_tool += 1

    if (magic_number_test_for_jnose_tool == 0 and assertion_roulette_for_jnose_tool == 0 and conditional_test_logic_for_jnose_tool == 0 and \
        constructor_initialization_for_jnose_tool == 0 and default_test_for_jnose_tool == 0 and empty_test_for_jnose_tool == 0 and exception_catching_throwing_for_jnose_tool == 0 and \
        general_fixture_for_jnose_tool == 0 and  mystery_guest_for_jnose_tool == 0 and print_statement_for_jnose_tool == 0 and redundant_assertion_for_jnose_tool == 0 and \
        sensitive_equality_for_jnose_tool == 0 and verbose_test_for_jnose_tool == 0 and sleepy_test_for_jnose_tool == 0 and eager_test_for_jnose_tool == 0 and \
        lazy_test_for_jnose_tool == 0 and duplicate_assert_for_jnose_tool == 0 and unknown_test_for_jnose_tool == 0 and ignored_test_for_jnose_tool == 0 and \
        resource_optimism_for_jnose_tool == 0 and dependent_test_for_jnose_tool == 0):

        no_affected_files_for_jnose_tool += 1      
        
    elif(magic_number_test_for_testsmelldetector_tool == 0 and assertion_roulette_for_testsmelldetector_tool == 0 and conditional_test_logic_for_testsmelldetector_tool == 0 and \
            constructor_initialization_for_testsmelldetector_tool == 0 and default_test_for_testsmelldetector_tool == 0 and empty_test_for_testsmelldetector_tool == 0 and \
            exception_catching_throwing_for_testsmelldetector_tool == 0 and general_fixture_for_testsmelldetector_tool == 0 and mystery_guest_for_testsmelldetector_tool == 0 and \
            print_statement_for_testsmelldetector_tool == 0 and redundant_assertion_for_testsmelldetector_tool == 0 and sensitive_equality_for_testsmelldetector_tool == 0 and \
            verbose_test_for_testsmelldetector_tool == 0 and sleepy_test_for_testsmelldetector_tool == 0 and eager_test_for_testsmelldetector_tool == 0 and \
            lazy_test_for_testsmelldetector_tool == 0 and duplicate_assert_for_testsmelldetector_tool == 0 and unknown_test_for_testsmelldetector_tool == 0 and \
            ignored_test_for_testsmelldetector_tool == 0 and resource_optimism_for_testsmelldetector_tool == 0 and dependent_test_for_testsmelldetector_tool == 0):
        
        no_affected_files_for_testsmelldetector_tool += 1 

    elif(magic_number_test_for_jnose_tool == 0 and assertion_roulette_for_jnose_tool == 0 and conditional_test_logic_for_jnose_tool == 0 and \
        constructor_initialization_for_jnose_tool == 0 and default_test_for_jnose_tool == 0 and empty_test_for_jnose_tool == 0 and exception_catching_throwing_for_jnose_tool == 0 and \
        general_fixture_for_jnose_tool == 0 and  mystery_guest_for_jnose_tool == 0 and print_statement_for_jnose_tool == 0 and redundant_assertion_for_jnose_tool == 0 and \
        sensitive_equality_for_jnose_tool == 0 and verbose_test_for_jnose_tool == 0 and sleepy_test_for_jnose_tool == 0 and eager_test_for_jnose_tool == 0 and \
        lazy_test_for_jnose_tool == 0 and duplicate_assert_for_jnose_tool == 0 and unknown_test_for_jnose_tool == 0 and ignored_test_for_jnose_tool == 0 and \
        resource_optimism_for_jnose_tool == 0 and dependent_test_for_jnose_tool == 0 and magic_number_test_for_testsmelldetector_tool == 0 and assertion_roulette_for_testsmelldetector_tool == 0 and conditional_test_logic_for_testsmelldetector_tool == 0 and \
        constructor_initialization_for_testsmelldetector_tool == 0 and default_test_for_testsmelldetector_tool == 0 and empty_test_for_testsmelldetector_tool == 0 and \
        exception_catching_throwing_for_testsmelldetector_tool == 0 and general_fixture_for_testsmelldetector_tool == 0 and mystery_guest_for_testsmelldetector_tool == 0 and \
        print_statement_for_testsmelldetector_tool == 0 and redundant_assertion_for_testsmelldetector_tool == 0 and sensitive_equality_for_testsmelldetector_tool == 0 and \
        verbose_test_for_testsmelldetector_tool == 0 and sleepy_test_for_testsmelldetector_tool == 0 and eager_test_for_testsmelldetector_tool == 0 and \
        lazy_test_for_testsmelldetector_tool == 0 and duplicate_assert_for_testsmelldetector_tool == 0 and unknown_test_for_testsmelldetector_tool == 0 and \
        ignored_test_for_testsmelldetector_tool == 0 and resource_optimism_for_testsmelldetector_tool == 0 and dependent_test_for_testsmelldetector_tool == 0 ):
        
        no_affected_files_for_both_tool += 1

    # Count total test smells in each file for JNose Tool
    total_test_smell_for_jnose_tool_in_file = magic_number_test_for_jnose_tool + assertion_roulette_for_jnose_tool + \
    conditional_test_logic_for_jnose_tool + constructor_initialization_for_jnose_tool + default_test_for_jnose_tool + \
    empty_test_for_jnose_tool + exception_catching_throwing_for_jnose_tool + general_fixture_for_jnose_tool + \
    mystery_guest_for_jnose_tool + print_statement_for_jnose_tool + redundant_assertion_for_jnose_tool + sensitive_equality_for_jnose_tool + \
    verbose_test_for_jnose_tool + sleepy_test_for_jnose_tool + eager_test_for_jnose_tool + lazy_test_for_jnose_tool + \
    duplicate_assert_for_jnose_tool + unknown_test_for_jnose_tool + ignored_test_for_jnose_tool + resource_optimism_for_jnose_tool + \
    dependent_test_for_jnose_tool

    # Count total test smells in each file for TestSmellDetector Tool
    total_test_smell_for_testsmelldetector_tool_in_file = magic_number_test_for_testsmelldetector_tool + assertion_roulette_for_testsmelldetector_tool + \
    conditional_test_logic_for_testsmelldetector_tool + constructor_initialization_for_testsmelldetector_tool + default_test_for_testsmelldetector_tool + \
    empty_test_for_testsmelldetector_tool + exception_catching_throwing_for_testsmelldetector_tool + general_fixture_for_testsmelldetector_tool + \
    mystery_guest_for_testsmelldetector_tool + print_statement_for_testsmelldetector_tool + redundant_assertion_for_testsmelldetector_tool + \
    sensitive_equality_for_testsmelldetector_tool + verbose_test_for_testsmelldetector_tool + sleepy_test_for_testsmelldetector_tool + \
    eager_test_for_testsmelldetector_tool + lazy_test_for_testsmelldetector_tool + duplicate_assert_for_testsmelldetector_tool + \
    unknown_test_for_testsmelldetector_tool + ignored_test_for_testsmelldetector_tool + resource_optimism_for_testsmelldetector_tool + \
    dependent_test_for_testsmelldetector_tool
    
    '''
    # Calculate ratio for each test smell to total test smell in each file
    ratio_of_magic_number_test_for_jnose_tool_to_total_in_each_file = magic_number_test_for_jnose_tool/total_test_smell_for_jnose_tool_in_file*100
    ratio_of_magic_number_test_for_testsmelldetector_tool_to_total_in_each_file = magic_number_test_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_file*100
    ratio_of_assertion_roulette_for_jnose_tool_to_total_in_each_file = assertion_roulette_for_jnose_tool/total_test_smell_for_jnose_tool_in_file*100
    ratio_of_assertion_roulette_for_testsmelldetector_tool_to_total_in_each_file = assertion_roulette_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_file*100
    ratio_of_conditional_test_logic_for_jnose_tool_to_total_in_each_file = conditional_test_logic_for_jnose_tool/total_test_smell_for_jnose_tool_in_file*100
    ratio_of_conditional_test_logic_for_testsmelldetector_tool_to_total_in_each_file = conditional_test_logic_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_file*100
    ratio_of_constructor_initialization_for_jnose_tool_to_total_in_each_file = constructor_initialization_for_jnose_tool/total_test_smell_for_jnose_tool_in_file*100
    ratio_of_constructor_initialization_for_testsmelldetector_tool_to_total_in_each_file = constructor_initialization_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_file*100
    ratio_of_default_test_for_jnose_tool_to_total_in_each_file = default_test_for_jnose_tool/total_test_smell_for_jnose_tool_in_file*100
    ratio_of_default_test_for_testsmelldetector_tool_to_total_in_each_file = default_test_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_file*100
    ratio_of_empty_test_for_jnose_tool_to_total_in_each_file = empty_test_for_jnose_tool/total_test_smell_for_jnose_tool_in_file*100
    ratio_of_empty_test_for_testsmelldetector_tool_to_total_in_each_file = empty_test_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_file*100
    ratio_of_exception_catching_throwing_for_jnose_tool_to_total_in_each_file = exception_catching_throwing_for_jnose_tool/total_test_smell_for_jnose_tool_in_file*100
    ratio_of_exception_catching_throwing_for_testsmelldetector_tool_to_total_in_each_file = exception_catching_throwing_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_file*100
    ratio_of_general_fixture_for_jnose_tool_to_total_in_each_file = general_fixture_for_jnose_tool/total_test_smell_for_jnose_tool_in_file*100
    ratio_of_general_fixture_for_testsmelldetector_tool_to_total_in_each_file = general_fixture_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_file*100
    ratio_of_mystery_guest_for_jnose_tool_to_total_in_each_file = mystery_guest_for_jnose_tool/total_test_smell_for_jnose_tool_in_file*100
    ratio_of_mystery_guest_for_testsmelldetector_tool_to_total_in_each_file = mystery_guest_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_file*100
    ratio_of_print_statement_for_jnose_tool_in_each_file = print_statement_for_jnose_tool/total_test_smell_for_jnose_tool_in_file*100
    ratio_of_print_statement_for_testsmelldetector_tool_in_each_file = print_statement_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_file*100
    ratio_of_redundant_assertion_for_jnose_tool_to_total_in_each_file = redundant_assertion_for_jnose_tool/total_test_smell_for_jnose_tool_in_file*100
    ratio_of_redundant_assertion_for_testsmelldetector_tool_to_total_in_each_file = redundant_assertion_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_file*100
    ratio_of_sensitive_equality_for_jnose_tool_in_each_file = sensitive_equality_for_jnose_tool/total_test_smell_for_jnose_tool_in_file*100
    ratio_of_sensitive_equality_for_testsmelldetector_tool_in_each_file = sensitive_equality_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_file*100
    ratio_of_verbose_test_for_jnose_tool_to_total_in_each_file = verbose_test_for_jnose_tool/total_test_smell_for_jnose_tool_in_file*100
    ratio_of_verbose_test_for_testsmelldetector_tool_to_total_in_each_file = verbose_test_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_file*100
    ratio_of_sleepy_test_for_jnose_tool_to_total_in_each_file = sleepy_test_for_jnose_tool/total_test_smell_for_jnose_tool_in_file*100
    ratio_of_sleepy_test_for_testsmelldetector_tool_to_total_in_each_file = sleepy_test_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_file*100
    ratio_of_eager_test_for_jnose_tool_to_total_in_each_file = eager_test_for_jnose_tool/total_test_smell_for_jnose_tool_in_file*100
    ratio_of_eager_test_for_testsmelldetector_tool_to_total_in_each_file = eager_test_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_file*100
    ratio_of_lazy_test_for_jnose_tool_to_total_in_each_file = lazy_test_for_jnose_tool/total_test_smell_for_jnose_tool_in_file*100
    ratio_of_lazy_test_for_testsmelldetector_tool_to_total_in_each_file = lazy_test_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_file*100
    ratio_of_duplicate_assert_for_jnose_tool_to_total_in_each_file = duplicate_assert_for_jnose_tool/total_test_smell_for_jnose_tool_in_file*100
    ratio_of_duplicate_assert_for_testsmelldetector_tool_to_total_in_each_file = duplicate_assert_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_file*100
    ratio_of_unknown_test_for_jnose_tool_to_total_in_each_file = unknown_test_for_jnose_tool/total_test_smell_for_jnose_tool_in_file*100
    ratio_of_unknown_test_for_testsmelldetector_tool_to_total_in_each_file = unknown_test_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_file*100
    ratio_of_ignored_test_for_jnose_tool_to_total_in_each_file = ignored_test_for_jnose_tool/total_test_smell_for_jnose_tool_in_file*100
    ratio_of_ignored_test_for_testsmelldetector_tool_to_total_in_each_file = ignored_test_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_file*100
    ratio_of_resource_optimism_for_jnose_tool_to_total_in_each_file = resource_optimism_for_jnose_tool/total_test_smell_for_jnose_tool_in_file*100
    ratio_of_resource_optimism_for_testsmelldetector_tool_to_total_in_each_file = resource_optimism_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_file*100
    ratio_of_dependent_test_for_jnose_tool_to_total_in_each_file = dependent_test_for_jnose_tool/total_test_smell_for_jnose_tool_in_file*100
    ratio_of_dependent_test_for_testsmelldetector_tool_to_total_in_each_file = dependent_test_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_file*100
    '''  
 
    # Total number of test smell with using two tools in each file
    total_test_smell_in_file = total_test_smell_for_testsmelldetector_tool_in_file + total_test_smell_for_jnose_tool_in_file

    # Total number of test smells for each tools and calculate total number of test smell overall with using all files
    total_test_smell_for_jnose_tool_in_all_files += total_test_smell_for_jnose_tool_in_file
    total_test_smell_for_testsmelldetector_tool_in_all_files += total_test_smell_for_testsmelldetector_tool_in_file
    total_test_smell_in_all_files = total_test_smell_for_jnose_tool_in_all_files + total_test_smell_for_testsmelldetector_tool_in_all_files
    
    number_of_total_file += 1

    '''
    print(ratio_of_magic_number_test_for_jnose_tool_to_total,ratio_of_magic_number_test_for_testsmelldetector_tool_to_total)
    print(ratio_of_assertion_roulette_for_jnose_tool_to_total,ratio_of_assertion_roulette_for_testsmelldetector_tool_to_total)
    print(ratio_of_verbose_test_for_jnose_tool_to_total,ratio_of_verbose_test_for_testsmelldetector_tool_to_total)
    '''
    
    '''
    Plot number of test smells for each tool in each file
    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Define colors for each tool
    tool_colors = {'JNoseTool': 'blue', 'TestSmellDetectorTool': 'orange'}

    # Define the width of each bar
    bar_width = 0.35
    
    # Set the position of the bars on the x-axis
    x = np.arange(len(unique_test_smells))

    # Plot the bars for each tool with different colors
    ax.bar(x - 0.2, jnose_tool_counts, width=0.4, color=tool_colors['JNoseTool'], label='JNoseTool')
    ax.bar(x + 0.2, testsmelldetector_tool_counts, width=0.4, color=tool_colors['TestSmellDetectorTool'], label='TestSmellDetectorTool')
    # Write counts on top of each bar
    for i, (jnose_count, detector_count) in enumerate(zip(jnose_tool_counts, testsmelldetector_tool_counts)):
        ax.text(x[i] - 0.2, jnose_count + 0.1, str(jnose_count), ha='center', va='bottom', fontsize = 6)
        ax.text(x[i] + 0.2, detector_count + 0.1, str(detector_count), ha='center', va='bottom', fontsize = 6)
    
    # Add labels and title
    ax.set_xlabel('Test Smell')
    ax.set_ylabel('Count')
    ax.set_title(f'Test Smells in {file_name}')
    ax.set_xticks(x)
    ax.set_xticklabels(unique_test_smells, rotation=90, ha='center')
    ax.legend()
    # Set y-axis scale
    ax.set_ylim(0, max(max(jnose_tool_counts), max(testsmelldetector_tool_counts)) + 10)
    ax.set_yticks(np.arange(0, max(max(jnose_tool_counts), max(testsmelldetector_tool_counts)) + 10, 10))
    '''
    
    '''
    # Plot ratio of each test smell in each file by using each tool
    # Add other test smells as keys with their corresponding ratio values
    ratio_data = {
    'Magic Number Test': [ratio_of_magic_number_test_for_jnose_tool_to_total_in_each_file, ratio_of_magic_number_test_for_testsmelldetector_tool_to_total_in_each_file],
    'Assertion Roulette': [ratio_of_assertion_roulette_for_jnose_tool_to_total_in_each_file, ratio_of_assertion_roulette_for_testsmelldetector_tool_to_total_in_each_file],
    'Conditional Test Logic': [ratio_of_conditional_test_logic_for_jnose_tool_to_total_in_each_file, ratio_of_conditional_test_logic_for_testsmelldetector_tool_to_total_in_each_file],
    'Constructor Initialization': [ratio_of_constructor_initialization_for_jnose_tool_to_total_in_each_file, ratio_of_constructor_initialization_for_testsmelldetector_tool_to_total_in_each_file],
    'Default Test': [ratio_of_default_test_for_jnose_tool_to_total_in_each_file, ratio_of_default_test_for_testsmelldetector_tool_to_total_in_each_file],
    'EmptyTest': [ratio_of_empty_test_for_jnose_tool_to_total_in_each_file, ratio_of_empty_test_for_testsmelldetector_tool_to_total_in_each_file],
    'Exception Catching Throwing': [ratio_of_exception_catching_throwing_for_jnose_tool_to_total_in_each_file, ratio_of_exception_catching_throwing_for_testsmelldetector_tool_to_total_in_each_file],
    'General Fixture': [ratio_of_general_fixture_for_jnose_tool_to_total_in_each_file, ratio_of_general_fixture_for_testsmelldetector_tool_to_total_in_each_file],
    'Mystery Guest': [ratio_of_mystery_guest_for_jnose_tool_to_total_in_each_file, ratio_of_mystery_guest_for_testsmelldetector_tool_to_total_in_each_file],
    'Print Statement': [ratio_of_print_statement_for_jnose_tool_in_each_file, ratio_of_print_statement_for_testsmelldetector_tool_in_each_file],
    'Redundant Assertion': [ratio_of_redundant_assertion_for_jnose_tool_to_total_in_each_file, ratio_of_redundant_assertion_for_testsmelldetector_tool_to_total_in_each_file],
    'Sensitive Equality': [ratio_of_sensitive_equality_for_jnose_tool_in_each_file, ratio_of_sensitive_equality_for_testsmelldetector_tool_in_each_file],
    'Verbose Test': [ratio_of_verbose_test_for_jnose_tool_to_total_in_each_file, ratio_of_verbose_test_for_testsmelldetector_tool_to_total_in_each_file],
    'Sleepy Test': [ratio_of_sleepy_test_for_jnose_tool_to_total_in_each_file, ratio_of_sleepy_test_for_testsmelldetector_tool_to_total_in_each_file],
    'Eager Test': [ratio_of_eager_test_for_jnose_tool_to_total_in_each_file, ratio_of_eager_test_for_testsmelldetector_tool_to_total_in_each_file],
    'Lazy Test': [ratio_of_lazy_test_for_jnose_tool_to_total_in_each_file, ratio_of_lazy_test_for_testsmelldetector_tool_to_total_in_each_file],
    'Duplicate Assert': [ratio_of_duplicate_assert_for_jnose_tool_to_total_in_each_file, ratio_of_duplicate_assert_for_testsmelldetector_tool_to_total_in_each_file],
    'Unknown Test': [ratio_of_unknown_test_for_jnose_tool_to_total_in_each_file, ratio_of_unknown_test_for_testsmelldetector_tool_to_total_in_each_file],
    'IgnoredTest': [ratio_of_ignored_test_for_jnose_tool_to_total_in_each_file, ratio_of_ignored_test_for_testsmelldetector_tool_to_total_in_each_file],
    'Resource Optimism': [ratio_of_resource_optimism_for_jnose_tool_to_total_in_each_file, ratio_of_resource_optimism_for_testsmelldetector_tool_to_total_in_each_file],
    'Dependent Test': [ratio_of_dependent_test_for_jnose_tool_to_total_in_each_file, ratio_of_dependent_test_for_testsmelldetector_tool_to_total_in_each_file],
    }

    # Extract test smell names
    test_smells = list(ratio_data.keys())

    # Number of tools
    num_tools = len(next(iter(ratio_data.values())))

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Define the width of each bar
    bar_width = 0.35

    # Set the position of the bars on the x-axis
    x = np.arange(len(test_smells))

    # Plot bars for each tool
    for i in range(num_tools):
        tool_ratio_values = [ratio[i] for ratio in ratio_data.values()]
        bar_positions = x + bar_width * (i - num_tools / 2)
        if i == 0:
                label = 'JNose Tool'
        else:
                label = 'TestSmellDetectorTool'
        bars = ax.bar(bar_positions, tool_ratio_values, bar_width, label=label)

        # Write rounded values on top of each bar
        for j, val in enumerate(tool_ratio_values):
            if val == 0.00:
                continue
            else:
                ax.text(bar_positions[j]-0.015, val, f'{val:.2f}', ha='center', va='bottom', fontsize=6)  # Round to two decimal places
    
    # Add labels and title
    ax.set_xlabel('Test Smell')
    ax.set_ylabel('Ratio (%)')
    ax.set_title(f'Ratios of Test Smells in {file_name}')
    ax.set_xticks(x)
    ax.set_xticklabels(test_smells, rotation=90, ha='center')
    ax.legend()
    '''

no_affected_files = number_of_total_file - no_affected_files_for_both_tool

# Labels for the two tools
tools = ['JNose Tool', 'TestSmellDetectorTool']

# Ratios for each tool
affected_or_not_affected_files = [number_of_total_file, no_affected_files_for_jnose_tool, no_affected_files_for_testsmelldetector_tool, no_affected_files_for_both_tool]


# Categories
categories = ['Total Files', 'No Affected (JNose)', 'No Affected (TestSmellDetector)', 'No Affected (Both)']

# Plotting
plt.figure(figsize=(25, 12))
bars = plt.bar(categories, affected_or_not_affected_files, color='skyblue')

# Add numbers on top of the bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, height,
             ha='center', va='bottom')

plt.xlabel('Category')
plt.ylabel('Number of Files')
plt.title('Affected or Not Affected Files')

save_dir = 'D:\Master_Thesis\Github_Projects'
plt.savefig(os.path.join(save_dir, 'Number_of_Affected_and_not_Affected_Files.png'), bbox_inches='tight')

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

data_for_affected_files = {
'Magic Number Test': [file_count_affected_by_magic_number_test_for_jnose_tool, file_count_affected_by_magic_number_test_for_testsmelldetector_tool],
'Assertion Roulette': [file_count_affected_by_assertion_roulette_for_jnose_tool, file_count_affected_by_assertion_roulette_for_testsmelldetector_tool],
'Conditional Test Logic': [file_count_affected_by_conditional_test_logic_for_jnose_tool, file_count_affected_by_conditional_test_logic_for_testsmelldetector_tool],
'Constructor Initialization': [file_count_affected_by_constructor_initialization_for_jnose_tool, file_count_affected_by_constructor_initialization_for_testsmelldetector_tool],
'Default Test': [file_count_affected_by_default_test_for_jnose_tool, file_count_affected_by_default_test_for_testsmelldetector_tool],
'EmptyTest': [file_count_affected_by_empty_test_for_jnose_tool, file_count_affected_by_empty_test_for_testsmelldetector_tool],
'Exception Catching Throwing': [file_count_affected_by_exception_catching_throwing_for_jnose_tool, file_count_affected_by_exception_catching_throwing_for_testsmelldetector_tool],
'General Fixture': [file_count_affected_by_general_fixture_for_jnose_tool, file_count_affected_by_general_fixture_for_testsmelldetector_tool],
'Mystery Guest': [file_count_affected_by_mystery_guest_for_jnose_tool, file_count_affected_by_mystery_guest_for_testsmelldetector_tool],
'Print Statement': [file_count_affected_by_print_statement_for_jnose_tool, file_count_affected_by_print_statement_for_testsmelldetector_tool],
'Redundant Assertion': [file_count_affected_by_redundant_assertion_for_jnose_tool, file_count_affected_by_redundant_assertion_for_testsmelldetector_tool],
'Sensitive Equality': [file_count_affected_by_sensitive_equality_for_jnose_tool, file_count_affected_by_sensitive_equality_for_testsmelldetector_tool],
'Verbose Test': [file_count_affected_by_verbose_test_for_jnose_tool, file_count_affected_by_verbose_test_for_testsmelldetector_tool],
'Sleepy Test': [file_count_affected_by_sleepy_test_for_jnose_tool, file_count_affected_by_sleepy_test_for_testsmelldetector_tool],
'Eager Test': [file_count_affected_by_eager_test_for_jnose_tool, file_count_affected_by_eager_test_for_testsmelldetector_tool],
'Lazy Test': [file_count_affected_by_lazy_test_for_jnose_tool, file_count_affected_by_lazy_test_for_testsmelldetector_tool],
'Duplicate Assert': [file_count_affected_by_duplicate_assert_for_jnose_tool, file_count_affected_by_duplicate_assert_for_testsmelldetector_tool],
'Unknown Test': [file_count_affected_by_unknown_test_for_jnose_tool, file_count_affected_by_unknown_test_for_testsmelldetector_tool],
'IgnoredTest': [file_count_affected_by_ignored_test_for_jnose_tool, file_count_affected_by_ignored_test_for_testsmelldetector_tool],
'Resource Optimism': [file_count_affected_by_resource_optimism_for_jnose_tool, file_count_affected_by_resource_optimism_for_testsmelldetector_tool],
'Dependent Test': [file_count_affected_by_dependent_test_for_jnose_tool, file_count_affected_by_dependent_test_for_testsmelldetector_tool],
}

# Extract test smell names
test_smells = list(data_for_affected_files.keys())

# Number of tools
num_tools = len(next(iter(data_for_affected_files.values())))

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(25, 12))

# Define the width of each bar
bar_width = 0.35

# Set the position of the bars on the x-axis
x = np.arange(len(test_smells))

# Plot bars for each tool
for i in range(num_tools):
    tool_ratio_values = [ratio[i] for ratio in data_for_affected_files.values()]
    # Adjust the position of the bars
    if i == 0:
        bar_positions = x + bar_width - 0.1  # Shift bars to the left for the first tool
        label = 'JNose Tool'
    elif i == 1:
        bar_positions = x - 0.1  # No shift for the second tool
        label = 'TestSmellDetectorTool'
        
    bars = ax.bar(bar_positions, tool_ratio_values, bar_width, label=label)

    # Write rounded values on top of each bar
    for j, val in enumerate(tool_ratio_values):
        if val == 0.00:
            continue
        else:
            ax.text(bar_positions[j]-0.015, val, f'{val}', ha='center', va='bottom', fontsize=6)  # Round to two decimal places

# Add labels and title
ax.set_xlabel('Test Smells')
ax.set_ylabel('Number of Affected Test Files')
ax.set_title(f'Number of Affected Files by Each Test Smells')
ax.set_xticks(x)
ax.set_xticklabels(test_smells, rotation=90, ha='center')
ax.legend()

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

plt.savefig(os.path.join(save_dir, 'Number_of_Affected_Files_by_Each_Test_Smells.png'), bbox_inches='tight')
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
total_magic_number_test_for_both_tool = total_magic_number_test_for_jnose_tool + total_magic_number_test_for_testsmelldetector_tool
total_assertion_roulette_for_both_tool = total_assertion_roulette_for_jnose_tool + total_assertion_roulette_for_testsmelldetector_tool
total_conditional_test_logic_for_both_tool = total_conditional_test_logic_for_jnose_tool + total_conditional_test_logic_for_testsmelldetector_tool
total_constructor_initialization_for_both_tool = total_constructor_initialization_for_jnose_tool + total_constructor_initialization_for_testsmelldetector_tool
total_default_test_for_both_tool = total_default_test_for_jnose_tool + total_default_test_for_testsmelldetector_tool
total_empty_test_for_both_tool = total_empty_test_for_jnose_tool + total_empty_test_for_testsmelldetector_tool
total_exception_catching_throwing_for_both_tool = total_exception_catching_throwing_for_jnose_tool + total_exception_catching_throwing_for_testsmelldetector_tool
total_general_fixture_for_both_tool = total_general_fixture_for_jnose_tool + total_general_fixture_for_testsmelldetector_tool
total_mystery_guest_for_both_tool = total_mystery_guest_for_jnose_tool + total_mystery_guest_for_testsmelldetector_tool
total_print_statement_for_both_tool = total_print_statement_for_jnose_tool + total_print_statement_for_testsmelldetector_tool
total_redundant_assertion_for_both_tool = total_redundant_assertion_for_jnose_tool + total_redundant_assertion_for_testsmelldetector_tool
total_sensitive_equality_for_both = total_sensitive_equality_for_jnose_tool + total_sensitive_equality_for_testsmelldetector_tool
total_verbose_test_for_both_tool = total_verbose_test_for_jnose_tool + total_verbose_test_for_testsmelldetector_tool
total_sleepy_test_for_both_tool = total_sleepy_test_for_jnose_tool + total_sleepy_test_for_testsmelldetector_tool
total_eager_test_for_both_tool = total_eager_test_for_jnose_tool + total_eager_test_for_testsmelldetector_tool
total_lazy_test_for_both_tool = total_lazy_test_for_jnose_tool + total_lazy_test_for_testsmelldetector_tool
total_duplicate_assert_for_both_tool = total_duplicate_assert_for_jnose_tool + total_duplicate_assert_for_testsmelldetector_tool
total_unknown_test_for_both_tool = total_unknown_test_for_jnose_tool + total_unknown_test_for_testsmelldetector_tool
total_ignored_test_for_both_tool = total_ignored_test_for_jnose_tool + total_ignored_test_for_testsmelldetector_tool
total_resource_optimism_for_both_tool = total_resource_optimism_for_jnose_tool + total_resource_optimism_for_testsmelldetector_tool
total_dependent_test_for_both_tool = total_dependent_test_for_jnose_tool + total_dependent_test_for_testsmelldetector_tool

data_for_total_test_smells = {
'Magic Number Test': [total_magic_number_test_for_jnose_tool, total_magic_number_test_for_testsmelldetector_tool,total_magic_number_test_for_both_tool],
'Assertion Roulette': [total_assertion_roulette_for_jnose_tool, total_assertion_roulette_for_testsmelldetector_tool,total_assertion_roulette_for_both_tool],
'Conditional Test Logic': [total_conditional_test_logic_for_jnose_tool, total_conditional_test_logic_for_testsmelldetector_tool,total_conditional_test_logic_for_both_tool],
'Constructor Initialization': [total_constructor_initialization_for_jnose_tool, total_constructor_initialization_for_testsmelldetector_tool,total_constructor_initialization_for_both_tool],
'Default Test': [total_default_test_for_jnose_tool, total_default_test_for_testsmelldetector_tool,total_default_test_for_both_tool],
'EmptyTest': [total_empty_test_for_jnose_tool, total_empty_test_for_testsmelldetector_tool,total_empty_test_for_both_tool],
'Exception Catching Throwing': [total_exception_catching_throwing_for_jnose_tool, total_exception_catching_throwing_for_testsmelldetector_tool,total_exception_catching_throwing_for_both_tool],
'General Fixture': [total_general_fixture_for_jnose_tool, total_general_fixture_for_testsmelldetector_tool,total_general_fixture_for_both_tool],
'Mystery Guest': [total_mystery_guest_for_jnose_tool, total_mystery_guest_for_testsmelldetector_tool,total_mystery_guest_for_both_tool],
'Print Statement': [total_print_statement_for_jnose_tool, total_print_statement_for_testsmelldetector_tool,total_print_statement_for_both_tool],
'Redundant Assertion': [total_redundant_assertion_for_jnose_tool, total_redundant_assertion_for_testsmelldetector_tool, total_redundant_assertion_for_both_tool],
'Sensitive Equality': [total_sensitive_equality_for_jnose_tool, total_sensitive_equality_for_testsmelldetector_tool,total_sensitive_equality_for_both],
'Verbose Test': [total_verbose_test_for_jnose_tool, total_verbose_test_for_testsmelldetector_tool,total_verbose_test_for_both_tool],
'Sleepy Test': [total_sleepy_test_for_jnose_tool, total_sleepy_test_for_testsmelldetector_tool,total_sleepy_test_for_both_tool],
'Eager Test': [total_eager_test_for_jnose_tool, total_eager_test_for_testsmelldetector_tool,total_eager_test_for_both_tool],
'Lazy Test': [total_lazy_test_for_jnose_tool, total_lazy_test_for_testsmelldetector_tool,total_lazy_test_for_both_tool],
'Duplicate Assert': [total_duplicate_assert_for_jnose_tool, total_duplicate_assert_for_testsmelldetector_tool,total_duplicate_assert_for_both_tool],
'Unknown Test': [total_unknown_test_for_jnose_tool, total_unknown_test_for_testsmelldetector_tool,total_unknown_test_for_both_tool],
'IgnoredTest': [total_ignored_test_for_jnose_tool, total_ignored_test_for_testsmelldetector_tool,total_ignored_test_for_both_tool],
'Resource Optimism': [total_resource_optimism_for_jnose_tool, total_resource_optimism_for_testsmelldetector_tool,total_resource_optimism_for_both_tool],
'Dependent Test': [total_dependent_test_for_jnose_tool, total_dependent_test_for_testsmelldetector_tool,total_dependent_test_for_both_tool],
}

# Extract test smell names
test_smells = list(data_for_total_test_smells.keys())

# Number of tools
num_tools = len(next(iter(data_for_total_test_smells.values())))

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(25, 12))

# Define the width of each bar
bar_width = 0.25  

# Set the position of the bars on the x-axis
x = np.arange(len(test_smells))

# Plot bars for each tool
for i in range(num_tools):
    tool_ratio_values = [ratio[i] for ratio in data_for_total_test_smells.values()]
    # Adjust the position of the bars
    if i == 0:
        bar_positions = x - bar_width  # Shift bars to the left for the first tool
        label = 'JNose Tool'
    elif i == 1:
        bar_positions = x  # No shift for the second tool
        label = 'TestSmellDetectorTool'
    else: 
        bar_positions = x + bar_width  # Shift bars to the right for the third tool
        label = 'BothTools'
        
    bars = ax.bar(bar_positions, tool_ratio_values, bar_width, label=label)

    # Write rounded values on top of each bar
    for j, val in enumerate(tool_ratio_values):
        if val == 0.00:
            continue
        else:
            ax.text(bar_positions[j], val, f'{val}', ha='center', va='bottom', fontsize=6)  # Round to two decimal places

# Add labels and title
ax.set_xlabel('Test Smells')
ax.set_ylabel('Number of Test Smell')
ax.set_title('Total Number of Test Smells in all files')
ax.set_xticks(x)
ax.set_xticklabels(test_smells, rotation=90, ha='center')
ax.legend()

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

plt.savefig(os.path.join(save_dir, 'Total_Number_of_Test_Smells_in_all_files.png'), bbox_inches='tight')
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Calculate ratio for each test smell to total test smell with using all files
ratio_of_magic_number_test_for_jnose_tool_to_total = total_magic_number_test_for_jnose_tool/total_test_smell_for_jnose_tool_in_all_files*100
ratio_of_magic_number_test_for_testsmelldetector_tool_to_total = total_magic_number_test_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_all_files*100
ratio_of_magic_number_test_for_both_tools = (total_magic_number_test_for_jnose_tool+total_magic_number_test_for_testsmelldetector_tool)/total_test_smell_in_all_files*100
ratio_of_assertion_roulette_for_jnose_tool_to_total = total_assertion_roulette_for_jnose_tool/total_test_smell_for_jnose_tool_in_all_files*100
ratio_of_assertion_roulette_for_testsmelldetector_tool_to_total = total_assertion_roulette_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_all_files*100
ratio_of_assertion_roulette_for_both_tools = (total_assertion_roulette_for_jnose_tool+total_assertion_roulette_for_testsmelldetector_tool)/total_test_smell_in_all_files*100
ratio_of_conditional_test_logic_for_jnose_tool_to_total = total_conditional_test_logic_for_jnose_tool/total_test_smell_for_jnose_tool_in_all_files*100
ratio_of_conditional_test_logic_for_testsmelldetector_tool_to_total = total_conditional_test_logic_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_all_files*100
ratio_of_conditional_test_logic_for_both_tools = (total_conditional_test_logic_for_jnose_tool+total_conditional_test_logic_for_testsmelldetector_tool)/total_test_smell_in_all_files*100
ratio_of_constructor_initialization_for_jnose_tool_to_total = total_constructor_initialization_for_jnose_tool/total_test_smell_for_jnose_tool_in_all_files*100
ratio_of_constructor_initialization_for_testsmelldetector_tool_to_total = total_constructor_initialization_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_all_files*100
ratio_of_constructor_initialization_for_both_tools = (total_constructor_initialization_for_jnose_tool+total_constructor_initialization_for_testsmelldetector_tool)/total_test_smell_in_all_files*100
ratio_of_default_test_for_jnose_tool_to_total = total_default_test_for_jnose_tool/total_test_smell_for_jnose_tool_in_all_files*100
ratio_of_default_test_for_testsmelldetector_tool_to_total = total_default_test_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_all_files*100
ratio_of_default_test_for_both_tools = (total_default_test_for_jnose_tool+total_default_test_for_testsmelldetector_tool)/total_test_smell_in_all_files*100
ratio_of_empty_test_for_jnose_tool_to_total = total_empty_test_for_jnose_tool/total_test_smell_for_jnose_tool_in_all_files*100
ratio_of_empty_test_for_testsmelldetector_tool_to_total = total_empty_test_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_all_files*100
ratio_of_empty_test_for_both_tools = (total_empty_test_for_jnose_tool+total_empty_test_for_testsmelldetector_tool)/total_test_smell_in_all_files*100
ratio_of_exception_catching_throwing_for_jnose_tool_to_total = total_exception_catching_throwing_for_jnose_tool/total_test_smell_for_jnose_tool_in_all_files*100
ratio_of_exception_catching_throwing_for_testsmelldetector_tool_to_total = total_exception_catching_throwing_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_all_files*100
ratio_of_exception_catching_throwing_for_both_tools = (total_exception_catching_throwing_for_jnose_tool+total_exception_catching_throwing_for_testsmelldetector_tool)/total_test_smell_in_all_files*100
ratio_of_general_fixture_for_jnose_tool_to_total = total_general_fixture_for_jnose_tool/total_test_smell_for_jnose_tool_in_all_files*100
ratio_of_general_fixture_for_testsmelldetector_tool_to_total = total_general_fixture_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_all_files*100
ratio_of_general_fixture_for_both_tools = (total_general_fixture_for_jnose_tool+total_general_fixture_for_testsmelldetector_tool)/total_test_smell_in_all_files*100
ratio_of_mystery_guest_for_jnose_tool_to_total = total_mystery_guest_for_jnose_tool/total_test_smell_for_jnose_tool_in_all_files*100
ratio_of_mystery_guest_for_testsmelldetector_tool_to_total = total_mystery_guest_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_all_files*100
ratio_of_mystery_guest_for_both_tools = (total_mystery_guest_for_jnose_tool+total_mystery_guest_for_testsmelldetector_tool)/total_test_smell_in_all_files*100
ratio_of_print_statement_for_jnose_tool = total_print_statement_for_jnose_tool/total_test_smell_for_jnose_tool_in_all_files*100
ratio_of_print_statement_for_testsmelldetector_tool = total_print_statement_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_all_files*100
ratio_of_print_statement_for_both_tools = (total_print_statement_for_jnose_tool+total_print_statement_for_testsmelldetector_tool)/total_test_smell_in_all_files*100
ratio_of_redundant_assertion_for_jnose_tool_to_total = total_redundant_assertion_for_jnose_tool/total_test_smell_for_jnose_tool_in_all_files*100
ratio_of_redundant_assertion_for_testsmelldetector_tool_to_total = total_redundant_assertion_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_all_files*100
ratio_of_redundant_assertion_for_both_tools = (total_redundant_assertion_for_jnose_tool+total_redundant_assertion_for_testsmelldetector_tool)/total_test_smell_in_all_files*100
ratio_of_sensitive_equality_for_jnose_tool = total_sensitive_equality_for_jnose_tool/total_test_smell_for_jnose_tool_in_all_files*100
ratio_of_sensitive_equality_for_testsmelldetector_tool = total_sensitive_equality_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_all_files*100
ratio_of_sensitive_equality_for_both_tools = (total_sensitive_equality_for_jnose_tool+total_sensitive_equality_for_testsmelldetector_tool)/total_test_smell_in_all_files*100
ratio_of_verbose_test_for_jnose_tool_to_total = total_verbose_test_for_jnose_tool/total_test_smell_for_jnose_tool_in_all_files*100
ratio_of_verbose_test_for_testsmelldetector_tool_to_total = total_verbose_test_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_all_files*100
ratio_of_verbose_test_for_both_tools = (total_verbose_test_for_jnose_tool+total_verbose_test_for_testsmelldetector_tool)/total_test_smell_in_all_files*100
ratio_of_sleepy_test_for_jnose_tool_to_total = total_sleepy_test_for_jnose_tool/total_test_smell_for_jnose_tool_in_all_files*100
ratio_of_sleepy_test_for_testsmelldetector_tool_to_total = total_sleepy_test_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_all_files*100
ratio_of_sleepy_test_for_both_tools = (total_sleepy_test_for_jnose_tool+total_sleepy_test_for_testsmelldetector_tool)/total_test_smell_in_all_files*100
ratio_of_eager_test_for_jnose_tool_to_total = total_eager_test_for_jnose_tool/total_test_smell_for_jnose_tool_in_all_files*100
ratio_of_eager_test_for_testsmelldetector_tool_to_total = total_eager_test_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_all_files*100
ratio_of_eager_test_for_both_tools = (total_eager_test_for_jnose_tool+total_eager_test_for_testsmelldetector_tool)/total_test_smell_in_all_files*100
ratio_of_lazy_test_for_jnose_tool_to_total = total_lazy_test_for_jnose_tool/total_test_smell_for_jnose_tool_in_all_files*100
ratio_of_lazy_test_for_testsmelldetector_tool_to_total = total_lazy_test_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_all_files*100
ratio_of_lazy_test_for_both_tools = (total_lazy_test_for_jnose_tool+total_lazy_test_for_testsmelldetector_tool)/total_test_smell_in_all_files*100
ratio_of_duplicate_assert_for_jnose_tool_to_total = total_duplicate_assert_for_jnose_tool/total_test_smell_for_jnose_tool_in_all_files*100
ratio_of_duplicate_assert_for_testsmelldetector_tool_to_total = total_duplicate_assert_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_all_files*100
ratio_of_duplicate_assert_for_both_tools = (total_duplicate_assert_for_jnose_tool+total_duplicate_assert_for_testsmelldetector_tool)/total_test_smell_in_all_files*100
ratio_of_unknown_test_for_jnose_tool_to_total = total_unknown_test_for_jnose_tool/total_test_smell_for_jnose_tool_in_all_files*100
ratio_of_unknown_test_for_testsmelldetector_tool_to_total = total_unknown_test_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_all_files*100
ratio_of_unknown_test_for_both_tools = (total_unknown_test_for_jnose_tool+total_unknown_test_for_testsmelldetector_tool)/total_test_smell_in_all_files*100
ratio_of_ignored_test_for_jnose_tool_to_total = total_ignored_test_for_jnose_tool/total_test_smell_for_jnose_tool_in_all_files*100
ratio_of_ignored_test_for_testsmelldetector_tool_to_total = total_ignored_test_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_all_files*100
ratio_of_ignored_test_for_both_tools = (total_ignored_test_for_jnose_tool+total_ignored_test_for_testsmelldetector_tool)/total_test_smell_in_all_files*100
ratio_of_resource_optimism_for_jnose_tool_to_total = total_resource_optimism_for_jnose_tool/total_test_smell_for_jnose_tool_in_all_files*100
ratio_of_resource_optimism_for_testsmelldetector_tool_to_total = total_resource_optimism_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_all_files*100
ratio_of_resource_optimism_for_both_tools = (total_resource_optimism_for_jnose_tool+total_resource_optimism_for_testsmelldetector_tool)/total_test_smell_in_all_files*100
ratio_of_dependent_test_for_jnose_tool_to_total = total_dependent_test_for_jnose_tool/total_test_smell_for_jnose_tool_in_all_files*100
ratio_of_dependent_test_for_testsmelldetector_tool_to_total = total_dependent_test_for_testsmelldetector_tool/total_test_smell_for_testsmelldetector_tool_in_all_files*100
ratio_of_dependent_test_for_both_tools = (total_dependent_test_for_jnose_tool+total_dependent_test_for_testsmelldetector_tool)/total_test_smell_in_all_files*100

print(total_test_smell_for_jnose_tool_in_all_files,total_test_smell_for_testsmelldetector_tool_in_all_files,total_test_smell_in_all_files)
print(total_magic_number_test_for_jnose_tool,total_magic_number_test_for_testsmelldetector_tool)
print(total_assertion_roulette_for_jnose_tool, total_assertion_roulette_for_testsmelldetector_tool)

print(number_of_total_file, no_affected_files, no_affected_files_for_jnose_tool, no_affected_files_for_testsmelldetector_tool, no_affected_files_for_both_tool)
print(file_count_affected_by_assertion_roulette_for_jnose_tool, file_count_affected_by_assertion_roulette_for_testsmelldetector_tool)
print(file_count_affected_by_magic_number_test_for_jnose_tool, file_count_affected_by_magic_number_test_for_testsmelldetector_tool)

# Add other test smells as keys with their corresponding ratio values
ratio_data2 = {
'Magic Number Test': [ratio_of_magic_number_test_for_jnose_tool_to_total, ratio_of_magic_number_test_for_testsmelldetector_tool_to_total,ratio_of_magic_number_test_for_both_tools],
'Assertion Roulette': [ratio_of_assertion_roulette_for_jnose_tool_to_total, ratio_of_assertion_roulette_for_testsmelldetector_tool_to_total,ratio_of_assertion_roulette_for_both_tools],
'Conditional Test Logic': [ratio_of_conditional_test_logic_for_jnose_tool_to_total, ratio_of_conditional_test_logic_for_testsmelldetector_tool_to_total,ratio_of_conditional_test_logic_for_both_tools],
'Constructor Initialization': [ratio_of_constructor_initialization_for_jnose_tool_to_total, ratio_of_constructor_initialization_for_testsmelldetector_tool_to_total,ratio_of_constructor_initialization_for_both_tools],
'Default Test': [ratio_of_default_test_for_jnose_tool_to_total, ratio_of_default_test_for_testsmelldetector_tool_to_total,ratio_of_default_test_for_both_tools],
'EmptyTest': [ratio_of_empty_test_for_jnose_tool_to_total, ratio_of_empty_test_for_testsmelldetector_tool_to_total,ratio_of_empty_test_for_both_tools],
'Exception Catching Throwing': [ratio_of_exception_catching_throwing_for_jnose_tool_to_total, ratio_of_exception_catching_throwing_for_testsmelldetector_tool_to_total,ratio_of_exception_catching_throwing_for_both_tools],
'General Fixture': [ratio_of_general_fixture_for_jnose_tool_to_total, ratio_of_general_fixture_for_testsmelldetector_tool_to_total,ratio_of_general_fixture_for_both_tools],
'Mystery Guest': [ratio_of_mystery_guest_for_jnose_tool_to_total, ratio_of_mystery_guest_for_testsmelldetector_tool_to_total,ratio_of_mystery_guest_for_both_tools],
'Print Statement': [ratio_of_print_statement_for_jnose_tool, ratio_of_print_statement_for_testsmelldetector_tool,ratio_of_print_statement_for_both_tools],
'Redundant Assertion': [ratio_of_redundant_assertion_for_jnose_tool_to_total, ratio_of_redundant_assertion_for_testsmelldetector_tool_to_total,ratio_of_redundant_assertion_for_both_tools],
'Sensitive Equality': [ratio_of_sensitive_equality_for_jnose_tool, ratio_of_sensitive_equality_for_testsmelldetector_tool,ratio_of_sensitive_equality_for_both_tools],
'Verbose Test': [ratio_of_verbose_test_for_jnose_tool_to_total, ratio_of_verbose_test_for_testsmelldetector_tool_to_total,ratio_of_verbose_test_for_both_tools],
'Sleepy Test': [ratio_of_sleepy_test_for_jnose_tool_to_total, ratio_of_sleepy_test_for_testsmelldetector_tool_to_total,ratio_of_sleepy_test_for_both_tools],
'Eager Test': [ratio_of_eager_test_for_jnose_tool_to_total, ratio_of_eager_test_for_testsmelldetector_tool_to_total,ratio_of_eager_test_for_both_tools],
'Lazy Test': [ratio_of_lazy_test_for_jnose_tool_to_total, ratio_of_lazy_test_for_testsmelldetector_tool_to_total,ratio_of_lazy_test_for_both_tools],
'Duplicate Assert': [ratio_of_duplicate_assert_for_jnose_tool_to_total, ratio_of_duplicate_assert_for_testsmelldetector_tool_to_total,ratio_of_duplicate_assert_for_both_tools],
'Unknown Test': [ratio_of_unknown_test_for_jnose_tool_to_total, ratio_of_unknown_test_for_testsmelldetector_tool_to_total,ratio_of_unknown_test_for_both_tools],
'IgnoredTest': [ratio_of_ignored_test_for_jnose_tool_to_total, ratio_of_ignored_test_for_testsmelldetector_tool_to_total,ratio_of_ignored_test_for_both_tools],
'Resource Optimism': [ratio_of_resource_optimism_for_jnose_tool_to_total, ratio_of_resource_optimism_for_testsmelldetector_tool_to_total,ratio_of_resource_optimism_for_both_tools],
'Dependent Test': [ratio_of_dependent_test_for_jnose_tool_to_total, ratio_of_dependent_test_for_testsmelldetector_tool_to_total,ratio_of_dependent_test_for_both_tools],
}

# Extract test smell names
test_smells = list(ratio_data2.keys())

# Number of tools
num_tools = len(next(iter(ratio_data2.values())))

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(25, 12))

# Define the width of each bar
bar_width = 0.25  # Decrease the width of each bar

# Set the position of the bars on the x-axis
x = np.arange(len(test_smells))

# Plot bars for each tool
for i in range(num_tools):
    tool_ratio_values = [ratio[i] for ratio in ratio_data2.values()]
    # Adjust the position of the bars
    if i == 0:
        bar_positions = x - bar_width  # Shift bars to the left for the first tool
        label = 'JNose Tool'
    elif i == 1:
        bar_positions = x  # No shift for the second tool
        label = 'TestSmellDetectorTool'
    else: 
        bar_positions = x + bar_width  # Shift bars to the right for the third tool
        label = 'BothTools'
        
    bars = ax.bar(bar_positions, tool_ratio_values, bar_width, label=label)

    # Write rounded values on top of each bar
    for j, val in enumerate(tool_ratio_values):
        if val == 0.00:
            continue
        else:
            ax.text(bar_positions[j], val, f'{val:.2f}', ha='center', va='bottom', fontsize=6)  # Round to two decimal places

# Add labels and title
ax.set_xlabel('Test Smell')
ax.set_ylabel('Ratio (%)')
ax.set_title('Ratios of Test Smells by using each tools and both in all files')
ax.set_xticks(x)
ax.set_xticklabels(test_smells, rotation=90, ha='center')
ax.legend()

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

plt.savefig(os.path.join(save_dir, 'Ratios_of_Test_Smells_by_using_each_tools_and_both_in_all_files.png'), bbox_inches='tight')
#------------------------------------------------------------------------------------------------------------------------------

ratio_of_total_test_smell_for_jnose_tool_to_total_test_smell_in_all_files = total_test_smell_for_jnose_tool_in_all_files/total_test_smell_in_all_files*100
ratio_of_total_test_smell_for_testsmelldetector_tool_to__total_test_smell_in_all_files = total_test_smell_for_testsmelldetector_tool_in_all_files/total_test_smell_in_all_files*100

# Ratios for each tool
ratios_for_each_tool = [ratio_of_total_test_smell_for_jnose_tool_to_total_test_smell_in_all_files,
          ratio_of_total_test_smell_for_testsmelldetector_tool_to__total_test_smell_in_all_files]

# Plotting the graph
plt.figure(figsize=(10, 6))
plt.bar(tools, ratios_for_each_tool, color=['blue', 'green'])

# Adding labels and title
plt.xlabel('Tool')
plt.ylabel('Ratio of Total Test Smell (%)')
plt.title('Ratio of Total Test Smell for Each Tool')

# Displaying the values on each bar
for i, ratio in enumerate(ratios_for_each_tool):
    plt.text(i, ratio + 0.01, f'{ratio:.2f}', ha='center')

plt.savefig(os.path.join(save_dir, 'Ratio_of_Total_Test_Smell_for_Each_Tool'), bbox_inches='tight')

#--------------------------------------------------------------------------------------------------------------------------------------

# Calculate ratio for each test smell to total test smell with using all files
ratio_of_file_count_affected_by_magic_number_test_for_jnose_tool = file_count_affected_by_magic_number_test_for_jnose_tool/number_of_total_file*100
ratio_of_file_count_affected_by_magic_number_test_for_testsmelldetector_tool = file_count_affected_by_magic_number_test_for_testsmelldetector_tool/number_of_total_file*100
ratio_of_file_count_affected_by_assertion_roulette_for_jnose_tool = file_count_affected_by_assertion_roulette_for_jnose_tool/number_of_total_file*100
ratio_of_file_count_affected_by_assertion_roulette_for_testsmelldetector_tool = file_count_affected_by_assertion_roulette_for_testsmelldetector_tool/number_of_total_file*100
ratio_of_file_count_affected_by_conditional_test_logic_for_jnose_tool = file_count_affected_by_conditional_test_logic_for_jnose_tool/number_of_total_file*100
ratio_of_file_count_affected_by_conditional_test_logic_for_testsmelldetector_tool = file_count_affected_by_conditional_test_logic_for_testsmelldetector_tool/number_of_total_file*100
ratio_of_file_count_affected_by_constructor_initialization_for_jnose_tool = file_count_affected_by_constructor_initialization_for_jnose_tool/number_of_total_file*100
ratio_of_file_count_affected_by_constructor_initialization_for_testsmelldetector_tool = file_count_affected_by_constructor_initialization_for_testsmelldetector_tool/number_of_total_file*100
ratio_of_file_count_affected_by_default_test_for_jnose_tool = file_count_affected_by_default_test_for_jnose_tool/number_of_total_file*100
ratio_of_file_count_affected_by_default_test_for_testsmelldetector_tool = file_count_affected_by_default_test_for_testsmelldetector_tool/number_of_total_file*100
ratio_of_file_count_affected_by_empty_test_for_jnose_tool = file_count_affected_by_empty_test_for_jnose_tool/number_of_total_file*100
ratio_of_file_count_affected_by_empty_test_for_testsmelldetector_tool = file_count_affected_by_empty_test_for_testsmelldetector_tool/number_of_total_file*100
ratio_of_file_count_affected_by_exception_catching_throwing_for_jnose_tool = file_count_affected_by_exception_catching_throwing_for_jnose_tool/number_of_total_file*100
ratio_of_file_count_affected_by_exception_catching_throwing_for_testsmelldetector_tool = file_count_affected_by_exception_catching_throwing_for_testsmelldetector_tool/number_of_total_file*100
ratio_of_file_count_affected_by_general_fixture_for_jnose_tool = file_count_affected_by_general_fixture_for_jnose_tool/number_of_total_file*100
ratio_of_file_count_affected_by_general_fixture_for_testsmelldetector_tool = file_count_affected_by_general_fixture_for_testsmelldetector_tool/number_of_total_file*100
ratio_of_file_count_affected_by_mystery_guest_for_jnose_tool = file_count_affected_by_mystery_guest_for_jnose_tool/number_of_total_file*100
ratio_of_file_count_affected_by_mystery_guest_for_testsmelldetector_tool = file_count_affected_by_mystery_guest_for_testsmelldetector_tool/number_of_total_file*100
ratio_of_file_count_affected_by_print_statement_for_jnose_tool = file_count_affected_by_print_statement_for_jnose_tool/number_of_total_file*100
ratio_of_file_count_affected_by_print_statement_for_testsmelldetector_tool = file_count_affected_by_print_statement_for_testsmelldetector_tool/number_of_total_file*100
ratio_of_file_count_affected_by_redundant_assertion_for_jnose_tool = file_count_affected_by_redundant_assertion_for_jnose_tool/number_of_total_file*100
ratio_of_file_count_affected_by_redundant_assertion_for_testsmelldetector_tool = file_count_affected_by_redundant_assertion_for_testsmelldetector_tool/number_of_total_file*100
ratio_of_file_count_affected_by_sensitive_equality_for_jnose_tool = file_count_affected_by_sensitive_equality_for_jnose_tool/number_of_total_file*100
ratio_of_file_count_affected_by_sensitive_equality_for_testsmelldetector_tool = file_count_affected_by_sensitive_equality_for_testsmelldetector_tool/number_of_total_file*100
ratio_of_file_count_affected_by_verbose_test_for_jnose_tool = file_count_affected_by_verbose_test_for_jnose_tool/number_of_total_file*100
ratio_of_file_count_affected_by_verbose_test_for_testsmelldetector_tool = file_count_affected_by_verbose_test_for_testsmelldetector_tool/number_of_total_file*100
ratio_of_file_count_affected_by_sleepy_test_for_jnose_tool = file_count_affected_by_sleepy_test_for_jnose_tool/number_of_total_file*100
ratio_of_file_count_affected_by_sleepy_test_for_testsmelldetector_tool = file_count_affected_by_sleepy_test_for_testsmelldetector_tool/number_of_total_file*100
ratio_of_file_count_affected_by_eager_test_for_jnose_tool = file_count_affected_by_eager_test_for_jnose_tool/number_of_total_file*100
ratio_of_file_count_affected_by_eager_test_for_testsmelldetector_tool = file_count_affected_by_eager_test_for_testsmelldetector_tool/number_of_total_file*100
ratio_of_file_count_affected_by_lazy_test_for_jnose_tool = file_count_affected_by_lazy_test_for_jnose_tool/number_of_total_file*100
ratio_of_file_count_affected_by_lazy_test_for_testsmelldetector_tool = file_count_affected_by_lazy_test_for_testsmelldetector_tool/number_of_total_file*100
ratio_of_file_count_affected_by_duplicate_assert_for_jnose_tool = file_count_affected_by_duplicate_assert_for_jnose_tool/number_of_total_file*100
ratio_of_file_count_affected_by_duplicate_assert_for_testsmelldetector_tool = file_count_affected_by_duplicate_assert_for_testsmelldetector_tool/number_of_total_file*100
ratio_of_file_count_affected_by_unknown_test_for_jnose_tool = file_count_affected_by_unknown_test_for_jnose_tool/number_of_total_file*100
ratio_of_file_count_affected_by_unknown_test_for_testsmelldetector_tool = file_count_affected_by_unknown_test_for_testsmelldetector_tool/number_of_total_file*100
ratio_of_file_count_affected_by_ignored_test_for_jnose_tool = file_count_affected_by_ignored_test_for_jnose_tool/number_of_total_file*100
ratio_of_file_count_affected_by_ignored_test_for_testsmelldetector_tool = file_count_affected_by_ignored_test_for_testsmelldetector_tool/number_of_total_file*100
ratio_of_file_count_affected_by_resource_optimism_for_jnose_tool = file_count_affected_by_resource_optimism_for_jnose_tool/number_of_total_file*100
ratio_of_file_count_affected_by_resource_optimism_for_testsmelldetector_tool = file_count_affected_by_resource_optimism_for_testsmelldetector_tool/number_of_total_file*100
ratio_of_file_count_affected_by_dependent_test_for_jnose_tool = file_count_affected_by_dependent_test_for_jnose_tool/number_of_total_file*100
ratio_of_file_count_affected_by_dependent_test_for_testsmelldetector_tool = file_count_affected_by_dependent_test_for_testsmelldetector_tool/number_of_total_file*100

# Add other test smells as keys with their corresponding ratio values
ratio_data3 = {
'Magic Number Test': [ratio_of_file_count_affected_by_magic_number_test_for_jnose_tool, ratio_of_file_count_affected_by_magic_number_test_for_testsmelldetector_tool],
'Assertion Roulette': [ratio_of_file_count_affected_by_assertion_roulette_for_jnose_tool, ratio_of_file_count_affected_by_assertion_roulette_for_testsmelldetector_tool],
'Conditional Test Logic': [ratio_of_file_count_affected_by_conditional_test_logic_for_jnose_tool, ratio_of_file_count_affected_by_conditional_test_logic_for_testsmelldetector_tool],
'Constructor Initialization': [ratio_of_file_count_affected_by_constructor_initialization_for_jnose_tool, ratio_of_file_count_affected_by_constructor_initialization_for_testsmelldetector_tool],
'Default Test': [ratio_of_file_count_affected_by_default_test_for_jnose_tool, ratio_of_file_count_affected_by_default_test_for_testsmelldetector_tool],
'EmptyTest': [ratio_of_file_count_affected_by_empty_test_for_jnose_tool, ratio_of_file_count_affected_by_empty_test_for_testsmelldetector_tool],
'Exception Catching Throwing': [ratio_of_file_count_affected_by_exception_catching_throwing_for_jnose_tool, ratio_of_file_count_affected_by_exception_catching_throwing_for_testsmelldetector_tool],
'General Fixture': [ratio_of_file_count_affected_by_general_fixture_for_jnose_tool, ratio_of_file_count_affected_by_general_fixture_for_testsmelldetector_tool],
'Mystery Guest': [ratio_of_file_count_affected_by_mystery_guest_for_jnose_tool, ratio_of_file_count_affected_by_mystery_guest_for_testsmelldetector_tool],
'Print Statement': [ratio_of_file_count_affected_by_print_statement_for_jnose_tool, ratio_of_file_count_affected_by_print_statement_for_testsmelldetector_tool],
'Redundant Assertion': [ratio_of_file_count_affected_by_redundant_assertion_for_jnose_tool, ratio_of_file_count_affected_by_redundant_assertion_for_testsmelldetector_tool],
'Sensitive Equality': [ratio_of_file_count_affected_by_sensitive_equality_for_jnose_tool, ratio_of_file_count_affected_by_sensitive_equality_for_testsmelldetector_tool],
'Verbose Test': [ratio_of_file_count_affected_by_verbose_test_for_jnose_tool, ratio_of_file_count_affected_by_verbose_test_for_testsmelldetector_tool],
'Sleepy Test': [ratio_of_file_count_affected_by_sleepy_test_for_jnose_tool, ratio_of_file_count_affected_by_sleepy_test_for_testsmelldetector_tool],
'Eager Test': [ratio_of_file_count_affected_by_eager_test_for_jnose_tool, ratio_of_file_count_affected_by_eager_test_for_testsmelldetector_tool],
'Lazy Test': [ratio_of_file_count_affected_by_lazy_test_for_jnose_tool, ratio_of_file_count_affected_by_lazy_test_for_testsmelldetector_tool],
'Duplicate Assert': [ratio_of_file_count_affected_by_duplicate_assert_for_jnose_tool, ratio_of_file_count_affected_by_duplicate_assert_for_testsmelldetector_tool],
'Unknown Test': [ratio_of_file_count_affected_by_unknown_test_for_jnose_tool, ratio_of_file_count_affected_by_unknown_test_for_testsmelldetector_tool],
'IgnoredTest': [ratio_of_file_count_affected_by_ignored_test_for_jnose_tool, ratio_of_file_count_affected_by_ignored_test_for_testsmelldetector_tool],
'Resource Optimism': [ratio_of_file_count_affected_by_resource_optimism_for_jnose_tool, ratio_of_file_count_affected_by_resource_optimism_for_testsmelldetector_tool],
'Dependent Test': [ratio_of_file_count_affected_by_dependent_test_for_jnose_tool, ratio_of_file_count_affected_by_dependent_test_for_testsmelldetector_tool],
}

print(ratio_of_file_count_affected_by_default_test_for_jnose_tool, ratio_of_file_count_affected_by_default_test_for_testsmelldetector_tool)
print(file_count_affected_by_default_test_for_jnose_tool, file_count_affected_by_default_test_for_testsmelldetector_tool)

# Extract test smell names
test_smells = list(ratio_data3.keys())

# Number of tools
num_tools = len(next(iter(ratio_data3.values())))

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(25, 12))

# Define the width of each bar
bar_width = 0.25 # Decrease the width of each bar

# Set the position of the bars on the x-axis
x = np.arange(len(test_smells))

# Plot bars for each tool
for i in range(num_tools):
    tool_ratio_values = [ratio[i] for ratio in ratio_data3.values()]
    # Adjust the position of the bars
    if i == 0:
        bar_positions = x + bar_width - 0.1  # Shift bars to the left for the first tool
        label = 'JNose Tool'
    elif i == 1:
        bar_positions = x - 0.1  # No shift for the second tool
        label = 'TestSmellDetectorTool'
        
    bars = ax.bar(bar_positions, tool_ratio_values, bar_width, label=label)

    # Write rounded values on top of each bar
    for j, val in enumerate(tool_ratio_values):
        if val == 0.00:
            continue
        else:
            ax.text(bar_positions[j], val, f'{val:.2f}', ha='center', va='bottom', fontsize=6)  # Round to two decimal places

# Add labels and title
ax.set_xlabel('Test Smell')
ax.set_ylabel('Ratio (%)')
ax.set_title('Ratios of Affected Files by Each Test Smells')
ax.set_xticks(x)
ax.set_xticklabels(test_smells, rotation=90, ha='center')
ax.legend()

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

plt.savefig(os.path.join(save_dir, 'Ratios_of_Affected_Files_by_Test_Smells.png'), bbox_inches='tight')

plt.tight_layout()
plt.show()


co_occurrence_list_both = [total_magic_number_test_for_both_tool,
                            total_assertion_roulette_for_both_tool,
                            total_conditional_test_logic_for_both_tool,
                            total_constructor_initialization_for_both_tool,
                            total_default_test_for_both_tool,
                            total_empty_test_for_both_tool,
                            total_exception_catching_throwing_for_both_tool,
                            total_general_fixture_for_both_tool,
                            total_mystery_guest_for_both_tool,
                            total_print_statement_for_both_tool,
                            total_redundant_assertion_for_both_tool,
                            total_sensitive_equality_for_both,
                            total_verbose_test_for_both_tool,
                            total_sleepy_test_for_both_tool,
                            total_eager_test_for_both_tool,
                            total_lazy_test_for_both_tool,
                            total_duplicate_assert_for_both_tool,
                            total_unknown_test_for_both_tool,
                            total_ignored_test_for_both_tool,
                            total_resource_optimism_for_both_tool,
                            total_dependent_test_for_both_tool]

co_occurrence_list_jnose = [total_magic_number_test_for_jnose_tool, 
                            total_assertion_roulette_for_jnose_tool,
                            total_conditional_test_logic_for_jnose_tool,
                            total_constructor_initialization_for_jnose_tool,
                            total_default_test_for_jnose_tool,
                            total_empty_test_for_jnose_tool,
                            total_exception_catching_throwing_for_jnose_tool,
                            total_general_fixture_for_jnose_tool,
                            total_mystery_guest_for_jnose_tool,
                            total_print_statement_for_jnose_tool,
                            total_redundant_assertion_for_jnose_tool,
                            total_sensitive_equality_for_jnose_tool,
                            total_verbose_test_for_jnose_tool,
                            total_sleepy_test_for_jnose_tool,
                            total_eager_test_for_jnose_tool, 
                            total_lazy_test_for_jnose_tool, 
                            total_duplicate_assert_for_jnose_tool, 
                            total_unknown_test_for_jnose_tool, 
                            total_ignored_test_for_jnose_tool, 
                            total_resource_optimism_for_jnose_tool, 
                            total_dependent_test_for_jnose_tool]

co_occurrence_list_testsmelldetector = [total_magic_number_test_for_testsmelldetector_tool,
                        total_assertion_roulette_for_testsmelldetector_tool,
                        total_conditional_test_logic_for_testsmelldetector_tool,
                        total_constructor_initialization_for_testsmelldetector_tool,
                        total_default_test_for_testsmelldetector_tool,
                        total_empty_test_for_testsmelldetector_tool,
                        total_exception_catching_throwing_for_testsmelldetector_tool,
                        total_general_fixture_for_testsmelldetector_tool,
                        total_mystery_guest_for_testsmelldetector_tool,
                        total_print_statement_for_testsmelldetector_tool,
                        total_redundant_assertion_for_testsmelldetector_tool,
                        total_sensitive_equality_for_testsmelldetector_tool,
                        total_verbose_test_for_testsmelldetector_tool,
                        total_sleepy_test_for_testsmelldetector_tool,
                        total_eager_test_for_testsmelldetector_tool,
                        total_lazy_test_for_testsmelldetector_tool,
                        total_duplicate_assert_for_testsmelldetector_tool,
                        total_unknown_test_for_testsmelldetector_tool,
                        total_ignored_test_for_testsmelldetector_tool,
                        total_resource_optimism_for_testsmelldetector_tool,
                        total_dependent_test_for_testsmelldetector_tool]


# Plot co-occurrence matrix for each tool separately
plot_heatmap_with_annotations(calculate_co_occurrence(co_occurrence_list_both), test_smells, 'Both Tools', save_dir)
plot_heatmap_with_annotations(calculate_co_occurrence(co_occurrence_list_jnose), test_smells, 'JNose Tool', save_dir)
plot_heatmap_with_annotations(calculate_co_occurrence(co_occurrence_list_testsmelldetector), test_smells, 'TestSmellDetector Tool',save_dir)

