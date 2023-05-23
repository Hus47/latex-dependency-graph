tables = {'Customers': {'columns': ['CustomerID', 'CustomerName', 'ContactName', 'Country', 'City', 'PostalCode'], 'primary keys': ['CustomerID'], 'unique keys': ['CustomerName', 'ContactName']}, 'Orders': {'columns': ['OrderID', 'CustomerID', 'OrderDate'], 'primary keys': ['OrderID'], 'unique keys': ['CustomerID']}, 'Orders2': {'columns': ['OrderID', 'CustomerID', 'OrderDate', 'test'], 'primary keys': ['OrderID'], 'unique keys': ['test', ['CustomerID', 'OrderDate']]}, 'Orders3': {'columns': ['OrderID', 'productID', 'OrderDate'], 'primary keys': [['OrderID', 'productID']], 'unique keys': []}, 'Orders4': {'columns': ['OrderID', 'productID', 'OrderDate'], 'primary keys': [['OrderID', 'productID']], 'unique keys': ['OrderDate']}, 'Orders5': {'columns': ['OrderID', 'productID'], 'primary keys': [['OrderID', 'productID']], 'unique keys': []}}

from num2words import num2words

def draw_latex_arrows(from_cols, to_cols, direction, offset):
    if direction == 'north':
        latex_template = "\\draw[-latex, very thick, black!70!black] (dedi.{} north) -- ++(0,{}) -| (dedi.{} north);\n".format(num2words(from_cols), offset, num2words(to_cols))
    else: # south
        latex_template = "\\draw[-latex, very thick, black!70!black] (dedi.{} south) -- ++(0,-{}) -| (dedi.{} south);\n".format(num2words(from_cols), offset, num2words(to_cols))
    return latex_template


def generate_latex_for_table(table, name):
    cols = table["columns"]
    num_cols = len(cols)
    
    # Making LaTeX for nodes
    latex_nodes = "{"
    for i, col in enumerate(cols):
        latex_nodes += "\\nodepart{{{}}}  ".format(num2words(i+1))
        if any(col in pk for pk in table['primary keys']):
            latex_nodes += "\\underline{{{}}}\n".format(col)
        else:
            latex_nodes += "{{{}}}\n".format(col)
    latex_nodes += "};\n"

    # Get primary key indices
    primary_key_indices = [i+1 for i, col in enumerate(cols) if any(col in pk for pk in table['primary keys'])]

    # Making LaTeX for arrows
    latex_arrows = ""
    unique_key_counter = 0
    for i, col in enumerate(cols):
        # Draw arrows from primary keys to other non-primary key columns
        if any(col in pk for pk in table['primary keys']):
            for j in range(i+1, num_cols):
                if not any(cols[j] in pk for pk in table['primary keys']):  # don't draw arrow to other primary keys
                    latex_arrows += draw_latex_arrows(i+1, j+1, 'south', 0.5)
        # Draw arrows from unique keys to primary keys
        elif col in table['unique keys']:
            for pk_index in primary_key_indices:
                latex_arrows += draw_latex_arrows(i+1, pk_index, 'north', 0.5+0.1*(cols.index(col)+1))

    # Handling combination unique keys
    for unique_key in table['unique keys']:
        if isinstance(unique_key, list):  # If this unique key is a combination of columns
            for i in range(len(unique_key)):
                height = cols.index(unique_key[0])+1
                for pk_index in primary_key_indices:
                    latex_arrows += draw_latex_arrows(cols.index(unique_key[i])+1, pk_index, 'north', 0.5+0.1*height)
            unique_key_counter += 1

    # Combining everything
    latex_front = "\n\\textbf{" + name + "}\n\\par" + """\n\\begin{tikzpicture}[my shape/.style={
    rectangle split, rectangle split parts=#1, draw, anchor=center}]
    \\node (start) {};"""
    
    latex_col_count = """\\node [my shape={}, rectangle split horizontal,name=dedi]""".format(num_cols)
    
    latex_back = """\\end{tikzpicture}\n"""
    
    latex = latex_front + "\n" + latex_col_count + "\n" + latex_nodes + "\n" + latex_arrows + "\n" + latex_back
    return latex



def generate_latex_from_dict(tables):
    max_cols = max(len(table['columns']) for table in tables.values())
    num_tables = len(tables)
    print(max_cols)

    width = max_cols * 3  # adjust scaling factor as needed
    height = num_tables * 3.5  # adjust scaling factor as needed

    latex_header = """\\documentclass[parskip]{scrartcl}
    \\usepackage[margin=1mm,landscape,paperwidth={""" + str(height) + """cm},paperheight={""" + str(width) + """cm}]{geometry}
    \\usepackage{tikz}
    \\usetikzlibrary{shapes.multipart, calc}

    \\begin{document}"""

    __latex = latex_header

    
    for name, table in tables.items():
        __latex += generate_latex_for_table(table, name)
        __latex += "\\par" + "\\par"
    
    __latex += """\\end{document}"""
    print(__latex)

    with open("output.txt", "w") as f:
        f.write(__latex)


generate_latex_from_dict(tables)
