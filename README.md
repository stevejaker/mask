# mask
Python CLI tool for checking for and masking confidential information from files.

## Recommended Setup (Linux/Unix)
```
$ git clone https://github.com/stevejaker/mask.git
$ cd mask/
$ bash setup.sh
```
## Usage Menu
```
$ mask -h

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

MASK SYNTAX -- #MASK: `mask_type'  [#O `assignment_operator' | #S | #X | #C comment]

#MASK: -- This is the keyword that triggers processing
    `mask_type' Options
        str    - string (Defaults to "")
        tstr   - triple string (Defaults to )
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
        Note: custom requires the use of `\n' characters to handle line spacing
        *** As of now, multiline masks are not enabled ***
#X -- Declares custom `mask_type' for the line
    Example: {\n"list": [\n\t]\n}
        variable_name = {
        "list": [
                ]
        }
#C -- Declares comment
    Comments are read from the end of `#C' through the next instance of '#' or
    the end of the line, whichever comes first. All comments will automatically
    be written with the preceeding comment character. NOTE: the comment CANNOT
    include '#' as it will trigger the end of the comment!
```

## Example
### Initial File
Filename: some_important_file.py
```python
#!/usr/bin/env python3

masked = "this is a masked string" #MASK: str #C This is a comment
not_masked = "this is not a masked string" # str #C This is a comment
triple_string = """this is a test triple string""" #MASK: tstr #C this is a messed up # comment
intvalue = 10 #MASK: int
floatval = 0.0 #MASK: float
dct = {  #MASK: dct
    "key1": "value1", #MASK: del
    "key2": "value2" #MASK: del
} #MASK: del
lst = ['value1', 'value2', 'value3'] #MASK: lst
s = "This should not appear in the code lol" #MASK: del

print(masked) # Standard Comment
print(not_masked)
```
### Running Initial File
```
$ python some_important_file.py
this is a masked string
this is not a masked string
```
### Checking Initial File
This reveals all unmasked lines in the file
```
$ mask check some_important_file.py
LINE: 3: masked = "this is a masked string" #MASK: str #C This is a comment
LINE: 5: triple_string = """this is a test triple string""" #MASK: tstr #C this is a messed up # comment
LINE: 6: intvalue = 10 #MASK: int
LINE: 7: floatval = 0.0 #MASK: float
LINE: 8: dct = {  #MASK: dct
LINE: 9: "key1": "value1", #MASK: del
LINE: 10: "key2": "value2" #MASK: del
LINE: 11: } #MASK: del
LINE: 12: lst = ['value1', 'value2', 'value3'] #MASK: lst
LINE: 13: s = "This should not appear in the code lol" #MASK: del
```
### Masking Initial File
```
$ mask some_important_file.py
```
### Masked File
Filename: MASKED_some_important_file.py
```python
#!/usr/bin/env python3

masked = "" # This is a comment
not_masked = "this is not a masked string" # str #C This is a comment
triple_string = """""" # this is a messed up# comment
intvalue = 0
floatval = 0.0
dct = {}
lst = []

print(masked) # Standard Comment
print(not_masked)
```
### Running Masked File
```
$ python MASKED_some_important_file.py

this is not a masked string
```
