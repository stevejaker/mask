#!/usr/bin/env python3

import os
import sys

################################################################################
#                                    Help Menus                                #
################################################################################

def help():
    print("""
`mask' is a command-line tool for masking confidential information within python
scripts. It is allows you to safely upload files while masking critical information.

`mask' is not a replacement for best coding practices.

Command Line Usage:
    mask <filename>        Masks <filename>
    mask <file_directory>  Masks all files in <file_directory>
    mask check <filename>  Checks <filename> for data that should be masked

Command Line Help:
    -h,  --help        Prints this message and exits
    -e,  --examples    Prints examples and exits
         --open        Opens the masked files once complete
""")

def help_detailed():
    print("""MASK SYNTAX -- #MASK: `mask_type'  [#O `assignment_operator' | #S | #X | #C comment]

#MASK: -- This is the keyword that triggers processing
    `mask_type' Options
        str    - string (Defaults to "")
        tstr   - triple string (Defaults to """""")
        lst    - list (Defaults to [])
        dct    - dictionary (Defaults to {})
        int    - integer (Defaults to 0)
        float  - floating point number (Defaults to 0.0)
        del    - deletes the entire line from the masked code
        custom - leaves custom masking (Requires #X argument)
#O -- Declares an `assignment_operator' which the character used to split the
    variable names from the mask. This is not a required argument and defaults
    to '='. The `assignment_operator' would typically be changed when dealing
    with a dictionary or other sort of multiline mask.
    Note: Be careful using non '=' `assignment_operator' characters as the entire
    line will be split using this character! If there are more than one of these
    characters in the line, the FIRST instance of it will be used!
#S -- Declares the start/stop of of multiline mask
    Applicable `mask_type' Options:
        tstr, lst, dct, custom
        Note: custom requires the use of `\\n' characters to handle line spacing
        *** As of now, multiline masks are not enabled ***
#X -- Declares custom `mask_type' for the line
    Example: {\\n"list": [\\n\\t]\\n}
        variable_name = {
        "list": [
                ]
        }
#C -- Declares comment
    Comments are read from the end of `#C' through the next instance of '#' or
    the end of the line, whichever comes first. All comments will automatically
    be written with the preceeding comment character. NOTE: the comment CANNOT
    include '#' as it will trigger the end of the comment!
""")

def examples():
    print("""Examples:
    #MASK: lst #S #C some comment here
        #MASK: lst -- Declares type 'lst'
        #S -- Declares the start/stop of of multiline mask
        #C -- Declares comment 'some comment here'

    #MASK: dct #O : #C This is a part of a multiline dictionary
        #MASK: dct -- Declares type 'dct'
        #O : -- Declares `assignment_operator' to be ':'
        #C -- Declares comment 'This is a part of a multiline dictionary'
""")
################################################################################
#                               Class Declaration                              #
################################################################################
class Mask(object):
    """
    """
    def __init__(self):
        self.Batch_Mode = False
        self.File_is_Written = False

        self.file_list = file_list

        self.infile  = open(infile, 'r')  # Read Only File Object
        self.outfile = open(outfile, 'w') # Write Only File Object
        self.outfile_content = [] # Content to eventually write to outfile

    def setup(self):
        if self.Batch_Mode:
            pass
        else:
            self.file_list = [  ]

    def configure_filenames(self):
        self.infile_name = filename
        self.outfile_name = outfile_name or f"MAKSED_{filename}"


    def close(self):
        if not self.File_is_Written:
            # self.prompt('')
            self.write()
        self.infile.close()
        self.outfile.close()


    def write(self):
        for line in self.outfile_content:
            pass




def get_file_list(filename):
    if os.path.isdir(filename):
        os.chdir(filename)
        return [x for x in os.listdir() if not os.path.isdir(x)]
    else:
        return [ filename ]

def handle_mask(mask):
    if mask == "str":
        return '\"\"'
    elif mask == "tstr":
        return '\"\"\"\"\"\"'
    elif mask == "lst":
        return '[]'
    elif mask == "dct":
        return '{}'
    elif mask == "int":
        return '0'
    elif mask == "float":
        return '0.0'
    elif mask == "del":
        return False
    elif mask == "custom":
        return ""
    else:
        return ""

def parse_args(args):
    if args[0] == '#MASK:':
        # mask_type = args[1]
        return handle_mask(args[1]), False
    elif args[0] == '#S':
        #Not functional
        return "", True
    elif args[0] == '#O':
        # Returns `assignment_operator'
        return f"ACODE: {args[1]}", False
    elif args[0] == '#C':
        # Returns full comment
        return " # " + " ".join(args[1:]), False
    else:
        # Handles unknown arguments and comments
        return " ".join(args), False

def findall(s, char="#"):
    # Returns the index values of all occurences `char'
    return [x for x in range(len(s)) if s[x] == char]

def process(line, line_number):
    mask_idx = line.find("#MASK:")
    if mask_idx == -1:
        return line
    elif CHECK_ONLY:
        print(f"LINE: {line_number}: {line}", end="")
    mask_args = line[mask_idx:]
    assignment_operator = '='
    out = ""
    cont = False # Not sure how to handle this
    arg_index = findall(mask_args)
    # argc = len(arg_index) - 1
    for i, idx in enumerate(arg_index):
        if i == len(arg_index) - 1:
            args = mask_args[idx:].strip().split()
        else:
            args = mask_args[idx:arg_index[i + 1]].strip().split()
        mask, cont = parse_args(args)
        if mask and "ACODE: " not in mask:
            # Handles if there is an `assignment_operator'
            # Will be replaced by a class variable once converted to class
            out += mask
        elif isinstance(mask, str) and "ACODE: " in mask:
            assignment_operator = mask.replace('ACODE: ', '').strip()
        else:
            # return False
            return "REMOVE"
    assignment_idx = line.find(assignment_operator) + 1
    var = line[:assignment_idx]
    return f"{var} {out}\n"

def main(file, OPEN=False):
    """
    Maybe include 2 options:
        Fast Process: Reads, writes file simultaneously.
            This would be a lot faster, but it could cause issues if there are
            unmatched #S args. Unmatched #S args would be caught; however, we
            would have already written part of the file by the time we found the
            error. This 'could' be remedied by deleting files if an error is
            detected at the cost of efficiency.
        Regular Process: Save outfile_content and write once processing is done.
            This would be a lot slower. We would make sure there are no
            mismatched #S args. The tradeoff for speed would ensure issues are
            ignored and prevent part of a file from being written in the event
            of an error.
    """
    with open(file, 'r') as infile:
        outfile_content = []
        line_number = 1
        if not CHECK_ONLY:
            outfile = open(f"MASKED_{file}", 'w')
        for line in infile:
            outfile_content.append(process(line, line_number))
            line_number += 1 
        # outfile_content = [process(line) for line in infile]
        for line in outfile_content:
            if line != 'REMOVE' and not CHECK_ONLY:
                outfile.write(f"{line}")
        if not CHECK_ONLY:
            outfile.close()
    if OPEN and not CHECK_ONLY:
        os.system(f'subl MASKED_{file}')


if __name__ == '__main__':
    global CHECK_ONLY
    OPEN = False
    CHECK_ONLY = False
    file_position = 1
    if len(sys.argv) < 2:
        # print("ERROR: Not enough CLIsubl validate arguments")
        help()
        sys.exit()
    elif sys.argv[1] == "check":
        CHECK_ONLY= True
        file_position = 2
    if '-h' in sys.argv or '--help' in sys.argv:
        help()
        help_detailed()
        sys.exit()
    elif '-e' in sys.argv or '--examples' in sys.argv:
        examples()
        sys.exit()
    else:
        file_list = get_file_list(sys.argv[file_position])
        for file in file_list:
            if not file.endswith('.py'):
                inp = input("This file does not appear to be a .py file.\nWould you like to continue? ")
            if '--open' in sys.argv:
                OPEN = True
            main(file, OPEN=OPEN)

