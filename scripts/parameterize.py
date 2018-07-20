import argparse
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

def load_json(key, name, file_path):
    # Note we do not yet deal with directories, which
    # would require adding a sub-key for each level
    # of directory.
    file_name, ext = os.path.splitext(os.path.basename(file_path))
    with open(file_path) as jf:
        params[key] = json.load(jf)
        params[key]['name'] = name


def vprint(*pargs, **kwargs):
    if args.verbose:
        print(*pargs, **kwargs)


# Register environment and methods
env = Environment(
    loader=FileSystemLoader(".")
)

if __name__ == '__main__':
    params = {}

    parser = argparse.ArgumentParser()
    parser.add_argument('--net', action='store', required=True)
    parser.add_argument('--host', action='store', required=True)
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--config_dir', action='store', default="config", required=True)
    args = parser.parse_args()

    load_json('net', name=args.net, file_path=os.path.join("networks", args.net+".json"))
    load_json('host', args.host, file_path=os.path.join(args.config_dir, args.host, "config.json"))

    # Scan config and host directories, creating .py files
    # from .pyt files.
    common_files = glob(os.path.join(args.config_dir, "*.pyt"))
    host_files = glob(os.path.join(args.config_dir, args.host, "*.pyt"))
    for file_path in common_files+host_files:
        file_name, ext = os.path.splitext(os.path.basename(file_path))
        if ext == '.pyt':
            vprint(f"Rendering {file_name}.py")
            content = render(file_path, env_vars=params)
            with open(f'{file_name}.py', "w") as outf:
                outf.write(content)
        else:
            sys.exit(f"Cannot process file {file_path}: not a Python template (.pyt)")
