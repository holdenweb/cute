import argparse
import base64
import json
import os
import sys

from glob import glob
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = "templates"
OUTPUT_DIR = "server"

# Funcs
def render(template_name, env_vars=os.environ):
    return env.get_template(template_name).render(env_vars)


# Register environment and methods
env = Environment(
    loader=FileSystemLoader("templates")
)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("template_file", nargs='+')
    args = parser.parse_args()
    
    params = {}
    
    # Scan all local json files, accumulating data
    # Note we do not yet deal with directories, which
    # would require adding a sub-key for each level
    # of directory.
    for j_file_name in glob('*.json'):
        with open(j_file_name) as jf:
            params[j_file_name[:-5]] = json.load(jf)

    for template_file in args.template_file:
        if not template_file.endswith('.pyt'):
            sys.exit('Sorry, we only process .pyt files')
        file_name = template_file[:-1]
        print(f"Rendering {file_name}")
        content = render(template_file, env_vars=params)
        with open(file_name, "w") as outf:
            outf.write(content)
