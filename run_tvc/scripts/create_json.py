# down = the higher value is more relaxed
# up =  the lower value is more relaxed

torrent_variant_caller = {
"indel_strand_bias": [0.9, 1, "down"],
"indel_beta_bias": [10,1000, "down"],
"filter_unusual_predictions": [0.3, 1, "down"],
"filter_insertion_predictions": [0.2, 1, "down"],
"filter_deletion_predictions": [0.2, 1, "down"]
 }

long_indel_assembler = {
"kmer_len": [8, 19, "up"],
"relative_strand_bias": [0.8, 1, "down"]}


strand_bias = [["torrent_variant_caller","indel_strand_bias", [0.9, 1, "down"]],
                ["torrent_variant_caller","indel_beta_bias", [10,1000, "down"]],
                 ["long_indel_assembler","relative_strand_bias", [0.8, 1, "down"]]]
                 
predictionshift = [["torrent_variant_caller","filter_unusual_predictions", [0.3, 1, "down"]],
                   ["torrent_variant_caller","filter_insertion_predictions", [0.2, 1, "down"]],
                    ["torrent_variant_caller","filter_deletion_predictions", [0.2, 1, "down"]]]
                     
kmer = [["long_indel_assembler","kmer_len", [8, 19, "up"]],]


import json
from pprint import pprint
import collections
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.2f') # prevent floats from having too many digits
from numpy import arange

def get_range(start_stop, step_no):
    start = start_stop[0]
    stop = start_stop[1]
    direction = start_stop[2]
    
    step_size = (stop - start)/step_no    
    step_size = round(step_size,2)    
    
    result = arange(start, stop, step_size)
    
    if direction == "up":
        result = result[::-1]
    
    return result

def get_default():
    json_data=open('../data/chp2_somatic_lowstringency.json')
    default_data = json.load(json_data)
    json_data.close()
    return default_data

step_no = 10.0

############################################################################################
# create 10 jsons for each parameter

sections = ["strand_bias", "predictionshift", "kmer"]

for i in range(step_no):
    for j, tvc_section in enumerate([strand_bias, predictionshift, kmer]):
        output_name = "../data/custom_%s_%i.json" % (sections[j], i)
        
        data = get_default()
        
        for param_values in tvc_section:
            
            section_name = param_values[0]
            param_name = param_values[1]
            start_stop = param_values[2]
            
            new_value = get_range(start_stop, step_no)[i]
            
            if param_name == "kmer_len":
                new_value = int(new_value)
                
            data[section_name][param_name] = new_value
            
        with open(output_name, "w") as json_out:
            json.dump(data, json_out, indent=4, sort_keys=True)

# ############################################################################################
# # create 10 jsons for each section
# 
# sections = ["long_indel_assembler", "torrent_variant_caller"]
# 
# for i in range(step_no):
#     for j, tvc_section in enumerate([long_indel_assembler, torrent_variant_caller]):
#         output_name = "../data/custom_%s_%i.json" % (sections[j], i)
#         
#         data = get_default()
#         
#         for param, start_stop in tvc_section.items():
#             new_value = get_range(start_stop, step_no)[i]
#             
#             if param == "kmer_len":
#                 new_value = int(new_value)
#             data[sections[j]][param] = new_value
#             
#         with open(output_name, "w") as json_out:
#             json.dump(data, json_out, indent=4, sort_keys=True)
            
############################################################################################
# create combined json

sections = ["long_indel_assembler", "torrent_variant_caller"]

for i in range(step_no):
    
    output_name = "../data/custom_combined_%i.json" % (i)
    data = get_default()

    for j, tvc_section in enumerate([long_indel_assembler, torrent_variant_caller]):
        for param, start_stop in tvc_section.items():
            new_value = get_range(start_stop, step_no)[i]
        
            if param == "kmer_len":
                new_value = int(new_value)
            data[sections[j]][param] = new_value
            
        with open(output_name, "w") as json_out:
            json.dump(data, json_out, indent=4, sort_keys=True)
     