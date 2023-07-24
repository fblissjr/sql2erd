import os
import argparse
from graphviz import Digraph
import re


def parse_sql_file(file_path):
    # Read file
    with open(file_path, "r") as file:
        data = file.read()

    # Extract table name
    table_name = re.search(
        "CREATE TABLE \[dbo\]\.\[(\w+)\]", data, re.IGNORECASE
    ).group(1)

    # Extract columns and data types
    columns = re.findall("\[(\w+)\] (\w+\(\d+(,\d+)?\))", data)

    # Try to extract foreign key constraints
    fk_constraints_search = re.findall(
        "FOREIGN KEY \(\[(\w+)\]\) REFERENCES \[dbo\]\.\[(\w+)\] \(\[(\w+)\]\)",
        data,
        re.IGNORECASE,
    )

    # If we found foreign key constraints, return them, otherwise return an empty list
    fk_constraints = fk_constraints_search if fk_constraints_search else []

    return table_name, columns, fk_constraints


def parse_sql_string(data):
    # Extract table name
    table_name = re.search(
        "CREATE TABLE \[dbo\]\.\[(\w+)\]", data, re.IGNORECASE
    ).group(1)

    # Extract columns and data types
    columns = re.findall("\[(\w+)\] (\w+\(\d+(,\d+)?\))", data)

    return table_name, columns


def generate_graph(tables, output_format="pdf"):
    # Create Digraph object
    g = Digraph("G", filename="erd.gv", node_attr={"shape": "record"})

    # Add nodes
    for table, data in tables.items():
        # Create label with table name and column names
        label = "{" + table + "|"
        for column in data[0]:
            # Join the elements of the data type tuple into a string
            column_name, *data_type = column
            data_type = " ".join(data_type)
            label += column_name + ": " + data_type + "\\l"
        label += "}"
        g.node(table, label)

    # Add edges
    for table, data in tables.items():
        for constraint in data[1]:
            if constraint:  # Only if there are foreign keys
                fk_column, ref_table, _ = constraint
                g.edge(table, ref_table, label=fk_column)

    # Render graph
    g.render(filename="erd", format=output_format, cleanup=True)


def main(folder_path, output_format):
    # List all .sql files in the directory
    sql_files = [f for f in os.listdir(folder_path) if f.endswith(".sql")]

    tables = {}
    # Parse each SQL file
    for sql_file in sql_files:
        file_path = os.path.join(folder_path, sql_file)
        table_name, columns, fk_constraints = parse_sql_file(file_path)
        tables[table_name] = (columns, fk_constraints)

    # Generate ERD diagram for the tables
    generate_graph(tables, output_format)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate ERD from SQL files.")
    parser.add_argument("folder", type=str, help="Folder containing SQL files.")
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        default="pdf",
        help="Output format (e.g., 'pdf', 'png').",
    )
    args = parser.parse_args()
    main(args.folder, args.format)
