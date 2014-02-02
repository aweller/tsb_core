
import json
import re


def parse_json_cutoffs():
    filename = "/home/ionadmin/andreas/core/general/data/chp2_somatic_lowstringency.json"
    
    return  json.load(open(filename))
    
def parse_hotspot_bed():
#     filename = "chp2_hotspots.bed"
    filename = "/home/ionadmin/andreas/core/general/data/CHP1.HSMv12.1_reqions_NO_JAK2_NODUP.bed"
    
    hotspots = {}
    
    with open(filename) as bed:
        for row in bed:
            if row[0] != "c": continue
            fields = row[:-1].split("\t")
                        
            chrom = fields[0]
            start = int(fields[1])
            stop = int(fields[2])
#             exon = fields[3]
#             gene = fields[5].split("=")[1]
            
            if not hotspots.get(chrom):
                hotspots[chrom] = []
            
            hotspots[chrom].append([start, stop])
            
    return hotspots
            

def parse_blacklist():
    filename = "/home/ionadmin/andreas/core/general/data/blacklist.txt"
    blacklist_chromposes = []
    
    with open(filename) as blacklist:
        for row in blacklist:
            chrompos = row.split()[:2] 
            blacklist_chromposes.append("\t".join(chrompos))
            
    return blacklist_chromposes

def parse_annotation(annotation_file):
    
#     filename = "G153312W_v2.tsv"
    
    filename = annotation_file
    annotations = {}
    
#     print "opening", filename
    with open(filename) as annotation_file:
        for row in annotation_file:
            if len(row) < 2 or row[0] == "#": continue
            
            if row[0] == "c": # version 14
                fields = row.split()
                chrom = fields[0].split(":")[0]
                posfield = fields[0].split(":")[1]
                pos_regex = re.search("(\d+)", posfield)
                
                pos = "?"
                if pos_regex != None:
                    pos = pos_regex.groups()[0]
                chrompos = chrom +"\t"+ pos
                
                for field in fields[2:]:
                    if not "=" in field: continue
                    
                    key = field.split("=")[0]
                    value = field.split("=")[1]
                    
                    if key in ["func", "cds", "loc", "Minor_Allele_Frequency", "gid"]:                    
                        if not annotations.get(chrompos):
                            annotations[chrompos] = {}
                            
                        annotations[chrompos][key] = value
            
            elif row.split()[2] in ["INDEL", "NOCALL", "REF", "SNV", "type"]: # version 40 full
                fields = row.split()
                chrom = "chr" + fields[0]
                pos = fields[1]
                chrompos = chrom +"\t"+ pos
                
                if not annotations.get(chrompos):
                    annotations[chrompos] = {}

                annotations[chrompos]["ref"] = fields[3]
                annotations[chrompos]["alt"] = fields[5]
                
#                 print fields
                
                try:
                    annotations[chrompos]["gid"] = fields[6].split(":")[0]
                    annotations[chrompos]["loc"] = fields[8]
                    annotations[chrompos]["func"] = fields[9].split(":")[0].strip("[]")
                    infofield = fields[11]    
                except:
                    pass                                       
                    
                        
            else: # version 16
                fields = row.split()
                chrom = "chr" + fields[0]
                pos = fields[1]
                chrompos = chrom +"\t"+ pos
                
                if not annotations.get(chrompos):
                    annotations[chrompos] = {}
                
                annotations[chrompos]["ref"] = fields[2]
                annotations[chrompos]["alt"] = fields[3]
                
                try:
                    annotations[chrompos]["gid"] = fields[4]
                    annotations[chrompos]["loc"] = fields[6]
                    annotations[chrompos]["func"] = fields[7]
                    infofield = fields[11]    
                except:
                    pass           
        
        return annotations

def parse_run_database():
    filename = "run_database.tsv"
    
    runs = {}
    
    with open(filename) as runfile:
        for row in runfile:
            fields = row.strip().split("\t")
            
            runfile = fields[0]            
            sample = fields[1]
            chp = fields[2]
            ir = fields[3]
                        
            runs[runfile] = {}
            runs[runfile]["sample"] = sample
            runs[runfile]["chp"] = chp
            runs[runfile]["ir"] = ir
            
    return runs

def parse_poly_database():
    poly_covered = {} # proper variant with a NHS QC coverage
    
    with open("/home/ionadmin/CallValidation/all_nhs_datasets/all_covered_variants_stats.tsv") as polyfile:
        for row in polyfile:
            f = row.split("\t")
            chrompos = f[0] +"\t"+ f[1]
            total_count = f[2]
            
            poly_covered[chrompos] = total_count
    
    poly_variant = {} # any variant that shows an alt allele
    
    with open("/home/ionadmin/CallValidation/all_nhs_datasets/all_variants_stats.tsv") as polyfile:
        for row in polyfile:
            f = row.split("\t")
            chrompos = f[0] +"\t"+ f[1]
            total_count = f[2]
            
            poly_variant[chrompos] = total_count
    
    return poly_covered, poly_variant
    
    

#############################################################################            

# json_cutoff = parse_json_cutoffs()
hotspot_bed = parse_hotspot_bed()
blacklist = parse_blacklist()
# runs = parse_run_database()
poly_covered, poly_variant = parse_poly_database()

# parse_annotation("all_datasets/G152973G_v1_IR16.tsv")

def parse_datafiles(annotation_file):
    
    datasets = {}
    
#     datasets["json_cutoff"] = parse_json_cutoffs()
#     datasets["hotspot_bed"] = parse_hotspot_bed()
#     datasets["blacklist"] = parse_blacklist()
    datasets["annotations"] = parse_annotation(annotation_file)
    
    return datasets
    
    
