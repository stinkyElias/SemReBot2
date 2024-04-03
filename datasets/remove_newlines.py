#!/usr/bin/env python3

import sys

domain_pddl_path = sys.argv[1]

with open(domain_pddl_path, 'r') as file:
    data = file.read()

content_without_newlines = data.replace('\n', ' ').replace('\r', ' ')

# if there are more than two whitespaces in a row, replace them with a single whitespace
content_without_newlines = ' '.join(content_without_newlines.split())

print(content_without_newlines)