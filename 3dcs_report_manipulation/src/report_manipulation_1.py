import os
import re
import shutil


# Helper/Misc
def debug_decorator(func):
    """ Debug decorator for displaying the output of a function, disable in the constants"""
    def wrapper(*args, **kwargs):
        output = func(*args, **kwargs)
        if debug:
            print(f"Debug {func.__name__}, return value: {output}")
            try:
                print(f"Debug len(): {len(output)}")
            except Exception:
                pass
        return output
    return wrapper


def match_str(pattern, string):
    """ Match pattern in string
    Out: True if match is found, false if not"""
    return re.match(pattern, string) is not None


def to_float(j):
    """ Try to convert to float, returns the string unchanged if fail """
    try:
        return float(j)
    except Exception:
        return j


# File operations
@debug_decorator
def get_active_folder():
    """ Get the folder of the simulation result, return path to latest created folder"""
    p = 'C:\\Users\\' + str(os.getlogin()) + '\\Documents\\DCS\\DCS_V5\\reports\\'
    active_dir = os.path.dirname(p)
    subfolders = [f for f in os.scandir(active_dir) if f.is_dir()]

    sorted_folder = sorted(subfolders, key=lambda x: x.stat().st_ctime)
    newest_created_folder = sorted_folder[-1]
    return newest_created_folder


@debug_decorator
def find_file(folder, pattern):
    """ Find file from regex pattern
    Out: First path of file found fullfilling pattern, if none is found returns None """
    subfiles = [f.path for f in os.scandir(folder) if f.is_file()]
    for i in subfiles:
        if match_str(pattern, i):
            return i
    return None


def get_file_content(path):
    with open(path, "r") as f:
        return f.read()


def save_content(path, content):
    with open(path, "w") as f:
        f.write(content)


# Data extraction
@debug_decorator
def create_data_dict(original_str):
    """ Returns the data in a dictionary"""

    def create(content, headers):
        node_html_removed = re.split("<.*?>", original_str)
        node_cleaned = [i for index, i in enumerate(node_html_removed) if index in headers.values()]
        node_comma_to_dot = [i.replace(',', '.') for i in node_cleaned]

        keys = [i for i in headers]

        data_dict = {keys[i]: to_float(node_comma_to_dot[i]) for i in range(len(headers))}

        return data_dict

    # sometimes min and max is included, need to establish when
    # Test for the longer, if error, test for the shorter one
    try:
        headers = {
            '#': 2, 'Name': 5, 'Parent': 8, 'TypeInfo': 10,
            'Description': 12, 'Nominal': 14, 'Mean': 16,
            'Std': 18, '10 Std Rng': 20, 'Min': 22, 'Max': 24,
            'LSL': 26, 'USL': 28,
            'L-OUT': 30, 'H-OUT': 32, 'Tot-OUT': 34,
            'Est.Type': 36, 'Est.Low': 38, 'Est.High': 40, 'Est.Range': 42}

        return create(original_str, headers=headers)

    except Exception:
        headers = {
            '#': 2, 'Name': 5, 'Parent': 8, 'TypeInfo': 10,
            'Description': 12, 'Nominal': 14, 'Mean': 16,
            'Std': 18, '10 Std Rng': 20, 'LSL': 22, 'USL': 24,
            'L-OUT': 26, 'H-OUT': 28, 'Tot-OUT': 30,
            'Est.Type': 32, 'Est.Low': 34, 'Est.High': 36, 'Est.Range': 38}

        return create(original_str, headers=headers)


# Measurement name tag verification
@debug_decorator
def is_val(original_str):
    """ Returns True if row is a validation [VAL] """
    return match_str(".*\[VAL\].*", original_str)


@debug_decorator
def is_sub(original_str):
    """ Returns True if row is a submeasurement [SUB] """
    return match_str(".*\[SUB\].*", original_str)


@debug_decorator
def is_sub_header(original_str):
    """ Returns True if row is a sub heading """
    return match_str(".*\[HEADER\].*", original_str)


# Html modification
@debug_decorator
def format_sub_header(data):
    """Create the string for the header html"""
    name = data["Name"]
    split = name.split("[HEADER]")[-1]
    header_html = f"<tr><td colspan = 99 style ='text-align: center; font-weight: 900; font-height: 14pt; background-color: grey;'> {split} </td></tr>"

    return header_html


def format_row(original_str, data, std_limit):
    """ Returns the formated html string """
    min_std_factor = 0
    max_std_factor = 0

    lsl, usl, mean, std = data["LSL"], data["USL"], data["Mean"], data["Std"]

    sigma = ""
    if std != 0:
        # Only write out actual value if the value is reasonable, avoids printing out if LSL/USL is set to a large/small value
        min_std_factor = (lsl - mean) / std
        if abs(min_std_factor) < std_limit * 2:
            sigma += f"<br/>LSL(&sigma;): { min_std_factor:.2f}"

        max_std_factor = (usl - mean) / std

        if abs(max_std_factor) < std_limit * 2:
            sigma += f"<br/>USL(&sigma;):{max_std_factor:.2f}"

    sub = ""
    if mean - std * std_limit < lsl or mean + std * std_limit > usl:
        sub = f"</A></TD> <TD NOWRAP style='text-align:center; background-color: red;'>Outside {std_limit}&sigma; limits{sigma}</TD>"
    else:
        sub = f"</A></TD> <TD NOWRAP style='text-align:center; background-color: green;'>Inside {std_limit}&sigma; limits{sigma}</TD>"

    new_str = re.sub("</A></TD> <TD.*?</TD>", sub, original_str)
    return new_str


def find_simulation_page(path):
    html_folder = path + "\\html\\"

    # get path to simulation file
    # if backup exist, use this file, else create backup
    sim_results_original_path = find_file(html_folder, ".*Results[.]html")
    sim_results_bak_path = find_file(html_folder, ".*Results.*backup.html")

    if sim_results_bak_path is None:
        # Copy original as backup befor doing any changes, name *.bak
        shutil.copyfile(sim_results_original_path, sim_results_original_path + ".backup.html")
        print("Backup created as *report_Simulation_Results.html.backup.html")
        return sim_results_original_path, sim_results_original_path
    else:
        return sim_results_original_path, sim_results_bak_path


def adjust_content(content):
    table_rows_unformated = re.findall("<TR>.*</TR>", content)

    # Replace the old string in the original context
    for i in table_rows_unformated[1:]:
        row = ""
        data = create_data_dict(i)

        if is_sub(i) or is_val(i):
            row = ""  # Remove row if VAL or SUB
        elif is_sub_header(i):
            row = format_sub_header(data)
        else:
            row = format_row(i, data, std_limit)

        content = content.replace(i, row)
    return content


# Main program
# -----
# Constants
std_limit = 5
debug = False

print("\n----------- New Run ------------")
# Get path to folder, latest created in default folder is used
folder = get_active_folder()
path = folder.path
print(f"Active dir: {path}")

output_sim_results_path, sim_results_path = find_simulation_page(path)
print(f"Simulation page: {sim_results_path}")

# Get file content
file_content = get_file_content(sim_results_path)

new_content = adjust_content(file_content)

save_content(output_sim_results_path, new_content)

print("---------- Run complete -------------")
