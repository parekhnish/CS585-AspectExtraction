# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++                             +++++++++++++++++++++++++
# +++++++++++++++++++++++ AUTHOR: NISHIT UMESH PAREKH +++++++++++++++++++++++++
# +++++++++++++++++++++++                             +++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import numpy as np
import re
import json

# Define the Input and Output Filenames
input_filename_list = ["Apex AD2600 Progressive-scan DVD player.txt" , "Canon G3.txt" , "Creative Labs Nomad Jukebox Zen Xtra 40GB.txt" , "Nikon coolpix 4300.txt" , "Nokia 6610.txt"]
output_filename_list = ["d%d.json"%i for i in range(5)]

# Compile the Regex Pattern to be used for Parsing Data
title_regex_str = r"\[t\]"
label_regex_str = r"\[[+-][1-3]\]"

title_regex_obj = re.compile(title_regex_str)
label_regex_obj = re.compile(label_regex_str)

# For Every Raw Data File ---
for file_index in range(5):

    # --- Get their fileames
    input_filename  = "../Dataset/customer review data/" + input_filename_list[file_index]
    output_filename = "../Dataset/" + output_filename_list[file_index]

    # Read in the data
    with open(input_filename,'r') as fp:
        raw_text = fp.read()

    # Split the data into individual lines
    raw_lines = str.splitlines(raw_text)
    num_lines = len(raw_lines)


    # Get the  indices of the first line of every review in the Raw Data
    start_indices = []

    for i in range(num_lines):
        if (not (re.search(title_regex_obj, raw_lines[i]) == None)):
            start_indices.append(i)

    num_reviews = len(start_indices)

    end_indices = [ind-1 for ind in start_indices[1:]]
    end_indices.append(num_lines-1)

    
    # The whole data is going to be a list of dicts (each dict constitutes a review).
    # Initialise that list.
    processed_data = []

    # For each review ---
    for k in range(num_reviews):

        # Initialise the dict for that review
        review_dict = {}
        review_dict['sentences'] = []

        # Get the indices of the first and last line for the review in the raw data
        start_ind = start_indices[k]
        end_ind   = end_indices[k]

        # For every line belonging to the review in the Raw Data ---
        for i in range(start_ind,end_ind):

            # If it is the first line, it has to be the title. Parse and store that.
            if i==start_ind:
                review_dict['title'] = (raw_lines[i][re.search(title_regex_obj , raw_lines[i]).end():]).strip()
                continue

            # All the other lines are the actual review and the labels.
            # First, separate the text from the labels
            temp_split = raw_lines[i].split("##")
            label_str = temp_split[0]
            sent_str = temp_split[1]

            # Initialise the dict for the Sentence, and add the text to it
            sent_dict = {}
            sent_dict['text'] = sent_str.strip()

            # Initialise the dict for the labels
            sent_dict['labels'] = {}

            # Split the labels section of the line into individual labels
            for label in label_str.split(","):

                # See if it is actually a label (or an empty string)
                temp_match = re.search(label_regex_obj , label)

                # If it is a label ---
                if(not(temp_match == None)):

                    # Extract the key ('aspect') and value ('rating')
                    key = (label[:temp_match.start()]).strip()
                    val = int(label[temp_match.start()+1:temp_match.end()-1])

                    # Store the labels
                    sent_dict['labels'][key] = val

            # Add the sentence dict to the list
            review_dict['sentences'].append(sent_dict)


        # Add the review dict to the list
        processed_data.append(review_dict)


    # Write the Processed Data to a JSON file
    with open(output_filename,'w') as fp:
        json.dump(processed_data,fp,indent="\t")