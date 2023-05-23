from num2words import num2words

def generate_latex_code(left_cols, right_cols):
    latex_template = "{"
    for i in range(len(left_cols)):
        latex_template += "\\nodepart{{{}}}  \\underline{{{}}}\n".format(num2words(i+1), left_cols[i])
    for i in range(len(right_cols)):
        latex_template += "\\nodepart{{{}}}  {{{}}}\n".format(num2words(i+len(left_cols)+1), right_cols[i])
    latex_template += "};\n"
    return latex_template

def generate_latex_arrows(left_cols, right_cols):
    latex_template = ""
    if len(left_cols) > 1:
        for i in range(2, len(left_cols)+1):
            latex_template += "\\draw[very thick, black!70!black] (dedi.one south) -- ++(0,-0.5) -| (dedi.{} south);\n".format(num2words(i))
    
    for i in range(1, len(right_cols)+1):
        latex_template += "\\draw[-latex, very thick, black!70!black] (dedi.one south) -- ++(0,-0.5) -| (dedi.{} south);\n".format(num2words(i+len(left_cols)))
    return latex_template

def draw_latex_arrows(from_cols, to_cols):
    latex_template = "\\draw[-latex, very thick, black!70!black] (dedi.{} north) -- ++(0,0.5) -| (dedi.{} north);\n".format(num2words(from_cols), num2words(to_cols))
    return latex_template

def generate_latex(all_cols, name):
    left_cols = []
    right_cols = []
    for i in range(len(all_cols)):
        left_cols.append(all_cols[i][0])
        right_cols.append(all_cols[i][1])


    latex = ""
    latex_front = "\n\\textbf{" + name + "}\n\\par" + """\n\\begin{tikzpicture}[my shape/.style={
rectangle split, rectangle split parts=#1, draw, anchor=center}]
\\node (start) {};"""

    cols = []
    for col in left_cols[0]:
        cols.append(col)
    for col in right_cols[0]:
        cols.append(col)
    num_cols = len(cols)

    latex_col_count = """\\node [my shape={}, rectangle split horizontal,name=dedi]""".format(num_cols)

    latex_code = generate_latex_code(left_cols[0], right_cols[0])
    latex_arrows = generate_latex_arrows(left_cols[0], right_cols[0])

    if len(right_cols[0]) == 0:
        latex_arrows = ""
    elif len(left_cols) > 1:
        for i in range(1, len(left_cols)):
            for k in range(len(left_cols[i])):
                comp = left_cols[i][k]
                from_cols = cols.index(comp)+1
                for j in range(len(right_cols[i])):
                    comp = right_cols[i][j]
                    print(comp)
                    to_cols = cols.index(comp)+1
                    print(from_cols)
                    print(to_cols)
                    latex_arrows += draw_latex_arrows(from_cols, to_cols)
    
    latex_back = """\\end{tikzpicture}\n"""

    latex = latex_front + "\n" + latex_col_count + "\n" + latex_code + "\n" + latex_arrows + "\n" + latex_back
    return latex


def get_user_input():
    all_cols = []
    name = input("Enter name of the table: ")
    while True:
        user_input = input("Enter columns in the format 'Column,Column,...->Column,Column,...' (or 0 to exit): ")
        if user_input == "0":
            break
        else:
            input_parts = user_input.split("->")
            left_cols = input_parts[0].split(",")
            if len(input_parts) == 1:
                right_cols = []
            else:
                right_cols = input_parts[1].split(",")
            all_cols.append([left_cols, right_cols])
            # latex = generate_latex(left_cols, right_cols)
            # print(latex)

    # print("All columns:", all_cols)

    latex = generate_latex(all_cols, name)
    return latex


__latex = """\\documentclass[parskip]{scrartcl}
\\usepackage[margin=15mm,landscape]{geometry}
\\usepackage{tikz}
\\usetikzlibrary{shapes.multipart, calc}

\\begin{document}"""

while True:
    user_input = input("Add table? (y/n): ")
    if user_input == "n":
        break
    txt = get_user_input()
    __latex += txt
    __latex += "\\par" + "\\par"


__latex += """\\end{document}"""

print(__latex)

with open("output.txt", "w") as f:
    f.write(__latex)