from dotenv import load_dotenv
from os import environ, path
from orgparse import load as load_org
from jinja2 import Environment, FileSystemLoader

load_dotenv()

def get_meta_data(org_string):
    metadata = {}
    lines = org_string.split('\n')
    for line in lines:
        if line.startswith("#+"):
            key_value_pair = line.lstrip("#+").split(":", 1)
            if len(key_value_pair) == 2:
                key, value = key_value_pair
                metadata[key.strip().lower()] = value.strip()
    return metadata

def get_title(node):
    meta_data = get_meta_data(node.body)
    return meta_data["title"]

def get_properties_dict(root, heading="", properties=[]):
    '''Get a dict of the properties under heading'''
    for node in root:
        if node.heading.upper() == heading.upper():
            return {
                k.lower(): node.get_property(k.upper())
                for k in properties
            }
def render_template(template_name, data):
    # Set up Jinja environment
    template_dir = path.join(path.dirname(path.abspath(__file__)), 'templates')  # Change 'templates' to your template directory
    env = Environment(loader=FileSystemLoader(template_dir))

    # Load the template
    template = env.get_template(template_name)

    # Render the template with data
    return template.render(data)

def main():
    print("App")
    mode = environ.get('MODE')
    data = None
    template = environ.get("TEMPLATE")
    if mode.lower() == "example":
        # load the sample resume
        print("Loading the sample resume...")
        data = load_org("resume.sample.org")
        pass
    else:
        # load the actual resume
        pass
    if not data:
        raise Exception()
    title = get_title(data)
    print("Title: ", title)
    template = render_template(environ.get("TEMPLATE"), {"title": title, "header": get_properties_dict(data, heading="Contact", properties=["NAME_LAST", "NAME_FIRST"]), "contact": get_properties_dict(data, heading="Contact", properties=["email"])})
    
    with open(path.join("public", environ.get("OUTPUT")), 'w') as f:
        f.write(template)

if __name__ == "__main__":
    main()