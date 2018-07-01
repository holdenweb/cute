import argparse
import base64
import json
import os
from jinja2 import Environment, FileSystemLoader

PROJECT_FOLDER = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
kubernetes_folder = os.path.join(PROJECT_FOLDER, 'kubernetes')
felix_conductor_folder = os.path.join(PROJECT_FOLDER, 'felix_conductor')


# Funcs
def b64encode(s):
    return base64.b64encode(s.encode('ascii')).decode('ascii')


def render(template_name, env_vars=os.environ):
    if not template_name.endswith('.pyt'):
        sys.exit('We only process .pyt files')
    contents = env.get_template(template_name).render(env_vars)

    file_name = template_name[:-1]

    print(f"Rendering {file_name}")
    with open(file_name, "w") as outf:
        outf.write(contents)
    return


# Register environment and methods
env = Environment(
    loader=FileSystemLoader(".")
)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("template_file", nargs='+')
    args = parser.parse_args()
    
    params = {}
    params['net'] = json.load(open('network.json'))
    params['host'] = json.load(open('system.json'))

    for template_file in args.template_file:
        render(template_file, env_vars=params)
