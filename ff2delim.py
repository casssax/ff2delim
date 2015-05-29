"""
Converts a fixed length file to a delimited file. 
call by typing: python ff2del_hd.PY <filename> <layout> <delimiter> <header> <quote>
layout syntax = <field length>,<field_name>...
(i.e. 30,LAST,20,FIRST,10,TITLE,10,SUFFIX...)
delimiter sytax: -c = comma, -p = pipe, -t = tab
(defaults to comma delimited if no option selected)
add -q for quote qualified output
"""
def find_last(field):  #returns last populated position in field
    pos = 0
    last = 0
    for e in field:
        if e != ' ':
            last = pos
            pos = pos + 1
        else:
            pos = pos + 1
    return last
    
def all_blank(field):  #returns True if empty field
    test = True
    for e in field:
        if e != ' ':
            test = False
    return test

def parse_layout_header(layout,delim): #converts layout file to list with headers
    fields = []
    new_fields = []
    pos = 0
    while pos != -1:
        pos = layout.find(',')
        if pos != -1:
            fields.append(layout[0:pos])
            layout = layout[pos + 1:]
        else:
            fields.append(layout)
    headers = fields[1::2]  #strips headers out of list
    #headers = delim.join(headers)
    out_fields = fields[::2]
    for e in out_fields:  #strips field lengths out of list
        new_fields.append(int(e))  #convert field lengths to int
    return new_fields,headers

def parse_layout(layout): #converts layout file to list
    fields = []
    pos = 0
    while pos != -1:
        pos = layout.find(',')
        if pos != -1:
            fields.append(int(layout[0:pos]))
            layout = layout[pos + 1:]
        else:
            fields.append(int(layout))
    return fields 

import sys
import os
# ---------------------------------------------------------------
# get script path
script_path = os.path.dirname(os.path.abspath(__file__))

# get delimiter
delims = {'-p':'|','-P':'|','-c':',','-C':',','-t':'\t','-T':'\t'}  #dictionary of delimiters
delim_def = {'-p':'pipe','-P':'pipe','-c':'comma','-C':'comma','-t':'tab','-T':'tab'}  #dictionary of delimiters

# set defaults for quotes and header
qqual = False
header = False
# accepted values for quotes and header
quotes = ['-q','-Q']
head = ['-h','-H']
# default to comma delimited
delim = ','

# parse input parameters
if len(sys.argv) > 3:
    args = sys.argv[3:]
    for arg in args:
        # select delimiter type
        if arg in delims:
            delim = delims[arg]
            print("using ", delim_def[arg], " delimited: ")
            print("delim: ", delim)
        # check for quote qualified
        if arg in quotes:
            qqual = True
            print("quote qualified: ")
        # check for header record
        if arg in head:
            header = True
            print("layout contains header names: ")

# ---------------------------------------------------------------
# import layout
# imput format i.e 30,20,1,10,10,60,60,30,2,5,4,3,4,5,9,80
try:  #test for layout file
    layout_name = sys.argv[2]
except:
    sys.exit("Error: Input format should be: ff2del_hd.PY <filename> <layout> [-t,-p,-c] [-h,-q]")
layout_path = script_path + '\\' + layout_name
layout = open(layout_path,"r")
for line in layout:
    if header == True:
        fields,headers = parse_layout_header(line,delim)
    else:
        fields = parse_layout(line)
layout.close()
print('fields: ', fields)
if header == True:
    print('headers: ', headers)
# ---------------------------------------------------------------
# import file
try:  #test for input file
    file_name = sys.argv[1]
except:
    sys.exit("Error: Input format should be: ff2del_hd.PY <filename> <layout> <layout> [-t,-p,-c] [-h,-q]")
file_path = script_path + '\\' + file_name
file = open(file_path,"r")
# ---------------------------------------------------------------
# create output file
out_file_path = script_path + '\\' + file_name[:-4] + '.out.txt' 
out_file = open(out_file_path,"w")
# ---------------------------------------------------------------
# process file
fields_list = []
first = 0
end = len(fields)
for f in fields:  #create list of lists:[start,end] positions for each field
    fields_list.append([first,first + f])
    first = first + f  

# set qualifier value
if qqual == True:
    qq = '\"'
else:
    qq = ''

# write out header record
if header == True:
    #out_file.write(headers + '\n')  #write headers as first line in file
    out_header = ''
    for h in headers:
        out_header = out_header + qq + h + qq + delim
    out_file.write(out_header[:-1] + '\n')
    # need to add functionality for header with quotes!!!!


# write lines in file
for line in file:
    count = 0    
    for field in fields_list:
        count = count + 1
        if all_blank(line[field[0]:field[1]]):  #check for empty field
            if count == end:
                out_file.write('\n') #carrage return if last field
            else:
                out_file.write(delim)  #write delimiter if empty field
        else:
            last = find_last(line[field[0]:field[1]]) + 1  #find last populated position in field
            if count == end:
                out_file.write(qq + line[field[0]:field[0] + last] + qq + '\n') #carrage return if last field
            else:
                out_file.write(qq + line[field[0]:field[0] + last] + qq + delim) #delimiter if not last field
out_file.close()
file.close()
