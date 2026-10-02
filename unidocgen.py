from enum import Enum
from wcwidth import wcswidth
import shlex

class UNIDOCGEN_CODEBOX_LINE_TYPE(list, Enum):
    SINGLE_LIGHT = ["┌", "┐", "└", "┘", "─", "│", "├", "┤", "┬", "┴", "┼"]
    SINGLE_LIGHT_DOUBLE_CORNERS = ["╔", "╗", "╚", "╝", "─", "│", "├", "┤", "┬", "┴", "┼"]
    SINGLE_HEAVY = ["┏", "┓", "┗", "┛", "━", "┃", "┣", "┫", "┳", "┻", "╋"]
    DOUBLE_LIGHT = ["╔", "╗", "╚", "╝", "═", "║", "╠", "╣", "╦", "╩", "╬"]

class UNIDOCGEN_COMPACT_TITLE_TYPE(str, Enum):
    LIGHT = "░"
    MEDIUM = "▒"
    HEAVY = "▓"
    FULL = "█"

class UNIDOCGEN_LINE_TYPE(list, Enum):
    SINGLE_LIGHT_SQUARE = ["[","─","]"]
    SINGLE_HEAVY_SQUARE = ["[","━","]"]
    DOUBLE_LIGHT_SQUARE = ["[","═","]"]
    SINGLE_LIGHT_ARROW = ["<","─",">"]
    SINGLE_HEAVY_ARROW = ["<","━",">"]
    DOUBLE_LIGHT_ARROW = ["<","═",">"]

global_variables = {}

def display_width_for_box(string: str, tab_size: int = 4) -> int: return wcswidth(string.expandtabs(tab_size))

def box_for_code(content: str, width: int, line_type: UNIDOCGEN_CODEBOX_LINE_TYPE, string_tab: str, line_number: int, tab_size: int = 4):
    if(width < 0):
        width = max(display_width_for_box(line, tab_size) for line in content.split('\n'))
    
    content = content.expandtabs(tab_size)
    lines = content.split('\n')
    
    num_width = len(str(line_number + len(lines) - 1)) + 3 if line_number >= 0 else 0

    if string_tab != "":
        actual_tab_width = display_width_for_box(string_tab, tab_size) + 2
        total_top_width = width + num_width
        if actual_tab_width + 2 >= total_top_width:
            total_top_width = actual_tab_width + 2
            width = total_top_width - num_width
        shift = total_top_width - actual_tab_width + 2
        final =  line_type[0] + line_type[4] * actual_tab_width + line_type[1] + ' ' * shift + '\n'
        final += line_type[5] + ' ' + string_tab + ' ' + line_type[5] + ' ' * shift + '\n'
        final += line_type[5] + ' ' * actual_tab_width + line_type[2] + line_type[4] * (shift - 1) + line_type[1]  + '\n'
    else:
        total_inner_width = width + num_width + 2
        final = line_type[0] + line_type[4] * total_inner_width + line_type[1] + '\n'

    total_inner_width = width + num_width + 2
    current_num = line_number

    for line in lines:
        chunks = [line[i:i + width] for i in range(0, len(line) or 1, width)]
        for idx, chunk in enumerate(chunks):
            if line_number >= 0:
                if idx == 0:
                    prefix = f"{current_num}".ljust(num_width - 3) + " ┊ "
                    current_num += 1
                else:
                    prefix = " " * (num_width - 3) + " ┊ "
            else:
                prefix = ""
                
            written_content = ' ' + prefix + chunk
            padding = max(0, total_inner_width - display_width_for_box(written_content, tab_size))
            final += line_type[5] + written_content + ' ' * padding + line_type[5] + '\n'

    return final + line_type[2] + line_type[4] * total_inner_width + line_type[3] + '\n'

def compact_title(lines, width, title_type):
    lines = lines.split('\n')
    max_line = max(len(line) for line in lines)
    min_width = max_line + 6
    width = max(width, min_width)

    border = title_type.value * width
    final = border + '\n'

    for line in lines:
        text = f"[ {line} ]"
        final += text.center(width, title_type.value) + '\n'
        final += border + '\n'

    return final


def parse_box_of_code(params, code_block):
    line_number = -1
    try:
        line_number = int(params["LINE_NUMBER"])
        if(line_number <= 0):
            line_number = -1
    except:
        pass
    line_type = UNIDOCGEN_CODEBOX_LINE_TYPE.SINGLE_LIGHT
    try:
        line_choice = params["LINE_TYPE"]
        if(line_choice == "SINGLE"):
            line_type = UNIDOCGEN_CODEBOX_LINE_TYPE.SINGLE_LIGHT
        elif(line_choice == "DOUBLE"):
            line_type = UNIDOCGEN_CODEBOX_LINE_TYPE.DOUBLE_LIGHT
        elif(line_choice == "SINGLE_HEAVY"):
            line_type = UNIDOCGEN_CODEBOX_LINE_TYPE.SINGLE_HEAVY
        elif(line_choice == "SINGLE_CORNERS"):
            line_type = UNIDOCGEN_CODEBOX_LINE_TYPE.SINGLE_LIGHT_DOUBLE_CORNERS
    except:
        pass  
    tab = ""
    try:
        tab = params["TAB"]
    except:
        pass
    width = -1
    try:
        width = int(params["WIDTH"])
    except:
        pass

    return box_for_code(code_block[:-1],width,line_type,tab,line_number)

def parse_title(params, title_block):
    title_type = UNIDOCGEN_COMPACT_TITLE_TYPE.LIGHT
    try:
        type_choice = params["TITLE_TYPE"]
        if(type_choice == "LIGHT"):
            title_type = UNIDOCGEN_COMPACT_TITLE_TYPE.LIGHT
        elif(type_choice == "MEDIUM"):
            title_type = UNIDOCGEN_COMPACT_TITLE_TYPE.MEDIUM
        elif(type_choice == "HEAVY"):
            title_type = UNIDOCGEN_COMPACT_TITLE_TYPE.HEAVY
        elif(type_choice == "FULL"):
            title_type = UNIDOCGEN_COMPACT_TITLE_TYPE.FULL
    except:
        pass
    width = -1
    try:
        width = int(params["WIDTH"])
    except:
        pass
    
    return compact_title(title_block[:-1], width, title_type)

def parse_params(line):
    tokens = shlex.split(line)
    d = dict(token.split("=", 1) for token in tokens if "=" in token)
    for key, value in d.items():
        try:
            d[key] = global_variables[value]
        except:
            pass
    return d

def add_global_variable(params):
    global global_variables
    global_variables = global_variables | params

def generate_doc(x, y):
    try:
        with open(x,"r") as file:
            content = file.read().split('\n')
    except:
        print(f"[ERROR] Can't find file {x}")

    final = ""
    i = 0

    while i < len(content):
        line = content[i]
        if "^UNIDOCGEN_BOX_CODE_START^" in line:
            params = parse_params(content[i])
            code_block = ""
            i += 1
            while i < len(content):
                if "^UNIDOCGEN_BOX_CODE_END^" in content[i]:
                    break
                code_block += content[i] + "\n"
                i += 1

            final += parse_box_of_code(params, code_block)
        elif "^UNIDOCGEN_COMPACT_TITLE_START^" in line:
            params = parse_params(content[i])
            title_block = ""
            i += 1
            while i < len(content):
                if "^UNIDOCGEN_COMPACT_TITLE_END^" in content[i]:
                    break
                title_block += content[i] + "\n"
                i += 1
            final += parse_title(params, title_block)
        elif "^UNIDOCGEN_GLOBAL_VARIABLE" in line:
            params = parse_params(content[i])
            add_global_variable(params)
        else:
            final += line + '\n'
        i += 1

    with open(y,"w") as file:
        file.write(final)
