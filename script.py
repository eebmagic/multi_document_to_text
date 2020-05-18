import os
import sys
import time
from PIL import Image
import pytesseract

# Check for input string
source = None
source_type = None
if "-i" in sys.argv:
    try:
        source = sys.argv[sys.argv.index("-i")+1]
        
        # Determine if input file or directory
        if os.path.isfile(source):
            source_type = "file"
        elif os.path.isdir(source):
            source_type = "directory"
            if source[-1] != "/":
                source += "/"
        else:
            quit(f'###ERROR: given input "{source}" is not a file or directory')


    except IndexError:
        quit("###ERROR: -i flag must be followed with a file or directory.")


# Check for output name preference
time_string = time.strftime("%x__%X").replace("/", "-").replace(":", ".")
output_name = f"generated_output_{time_string}.txt"
if "-o" in sys.argv:
    try:
        output_name = sys.argv[sys.argv.index("-o")+1]
    except IndexError:
        "###ERROR: -o flag must be followed with a output name"


add_file_headers = "-f" in sys.argv

if "-h" in sys.argv or "--help" in sys.argv:
    help_string = """Options:
    -i          input file or directory
    -o          prefered output name (defaults to "generated_output_\{time\}.txt" if not given)
    -f          add headers to text from each file with file path
    -h --help   show this page
    """
    quit(help_string)


print(f"given input file/dir: {source}")
print(f"given input type: {source_type}")
if source_type == "directory":
    print(os.listdir(source)[::-1])
print(f"output name: {output_name}")


### START ###

# Get input if none given
file_list = []
if source == None:
    source = ""
    print("\n\tNo input files were given.")
    given = None
    while given != "":
        given = input("\n\tDrag a file here and hit enter to add it to the source list (press enter to quit): ").strip()
        file_list.append(given)
    file_list = file_list[:-1]

# Set list from -i input flag
else:
    if source_type == "file":
        file_list = source
    else:
        for file in os.listdir(source)[::-1]:
            file = source+file
            if os.path.isfile(file):
                file_list.append(file)


# Allow user to remove from list
user_selection = "n"
while user_selection != "" and user_selection != "y":
    print("\nfile_list: ")
    for ind, file in enumerate(file_list):
        print(f'\t{ind} - "{file}"')

    user_selection = input("Is this list good?(Y/n): ").lower()

    if user_selection.startswith("n"):
        user_remove = int(input("\nChoose with file to remove: ").strip())
        try:
            removed_file = file_list[user_remove]
            file_list = file_list[:user_remove] + file_list[user_remove+1:]
            print(f"removed: {removed_file}")
        except IndexError:
            print("ERROR: must give a valid index in the list")



# Read all files and add to output
full_text = ""
file_list.sort()
for file in file_list:
    if not file.lower().endswith(".png") and not file.lower().endswith(".jpg") and not file.lower().endswith(".jpeg"):
        print(f"###ERROR: file {file} is not a supported image type (.png, .jpg, .jpeg)")
        print(f"skipping file: {file}")
    else:
        text = pytesseract.image_to_string(Image.open(file))
        if add_file_headers:
            # print(f"from: {file}")
            full_text += "##########################\n"
            full_text += f"from: {file}\n"
            full_text += "##########################\n"

        # print(text)
        full_text += text + "\n\n"


# Save to output file
with open(output_name, 'a+') as file:
    file.write(full_text)
    print(f"output written to: {output_name}")