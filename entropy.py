import csv
import math
import operator

def main():

    # Frequency dictionary for each value in the netflow record
    src_address = dict()
    dst_address = dict()
    src_port = dict()
    dst_port = dict()

    # list of paths, as records can be spread across multiple csv files
    paths = []
    
    print("type 'done' to execute'\n")
    print("Target output csv: ", end="")
    target_path = input()

    # Erase the target file
    target = open(target_path, 'w')
    target.truncate()
    target.close()

    # ask for multiple csv's, breaks on 'done'
    while(True):
        print("Filepath: ", end="")
        filepath = input()
        if filepath == "done":
            break
        paths.append(filepath);

    # Show that this step has been started
    print("working")

    # iterate through each file
    for path in paths:
        with open(path, 'r') as es_data_file:

            # iterate through each line in the csv, breaking apart the columns and calling
            # dict_add to incremenet the count of each occurrance of each type
            for line in es_data_file:
                cols = line.split(",")
        
                # increase the count of cols[x] in the dictionary y.
                # If the current item doesn't exist in the dictionary, add it, and increase its count by one
                dict_add(cols[0], src_address)
                dict_add(cols[1], dst_address)
                dict_add(cols[2], src_port)
                dict_add(cols[3], dst_port)

    target = open(target_path, 'w')

    calcfreq("Destination Address", dst_address, target)
    calcfreq("Source Address", src_address, target)
    calcfreq("Destination Port", dst_port, target)
    calcfreq("Source Port", src_port, target)

    target.close()
    print("done")


def calcfreq(dict_name, count_dict, file_target):

    file_target.write("\n\n" + dict_name +"\n");

    # Get a sorted list of the dictionary elements by the # of record occurrences
    sorted_dict = sorted(count_dict.items(), key=operator.itemgetter(1))

    # sort from large to small
    sorted_dict = sorted_dict[::-1]

    
    probability = {}
    number_of_records = 0

    #Count the total number of records
    for element in count_dict:
        number_of_records = number_of_records + count_dict[element]
    
    # Write the number of records
    file_target.write("Total number of records: " + str(number_of_records) + "\n")
    
    # Count how many lines, to never exceed 500 lines
    i = 0
    file_target.write("Key,# Records,Probability (count/totalcount),Entropy (-log_2(probability)))\n")
    for element in sorted_dict:
        if i > 500:
            break
        probability[element[0]] = count_dict[element[0]] / number_of_records
        data = element[0] + "," + str(count_dict[element[0]]) + "," + str(probability[element[0]]) + "," + str((math.log(probability[element[0]], 2.0)* -1)) + "\n"
        file_target.write(data)
        i += 1


    # Increase count in dictionary arg, if it doesn't exist, set count to 1
def dict_add(in_string, in_dictionary):
    if in_string in in_dictionary:
        in_dictionary[in_string] += 1   
    else:
        in_dictionary[in_string] = 1



main()