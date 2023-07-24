# Simple SQL to ERD CLI Tool

This project is a simple command-line interface (CLI) tool that generates Entity Relationship Diagrams (ERD) from `.sql` files using the Graphviz library. Currently, it only supports Microsoft SQL Server / Azure SQL (T-SQL), but more dialects can be added over time.

## Features

The current version of the tool generates ERDs with the following features:

- Table names
- Columns for each table
- Data types of each column
- Foreign key relationships between tables

## Usage

python sql2erd_cli.py <folder of .sql files> -f output_format

## Output Formats

Output always includes a .gv file, and can also output as pdf, png, etc, via the -f parameter

## Contributing

Feel free to fork this project and modify it as needed. If you add support for additional SQL dialects or other features, please consider submitting a pull request to share your improvements with the community.

