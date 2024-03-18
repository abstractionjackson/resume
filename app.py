from Resume import Resume
from dotenv import load_dotenv
from os import environ, path
from orgparse import load as load_org
from jinja2 import Environment, FileSystemLoader

load_dotenv()

def render_template(template_name, resume):
    # Set up Jinja environment
    template_dir = path.join(path.dirname(path.abspath(__file__)), 'templates')  # Change 'templates' to your template directory
    env = Environment(loader=FileSystemLoader(template_dir))

    # Load the template
    template = env.get_template(template_name)

    # Render the template with data
    return template.render(resume=resume)

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
    resume = Resume(data)
    template = render_template(environ.get("TEMPLATE"), resume)
    
    with open(path.join("public", environ.get("OUTPUT")), 'w') as f:
        f.write(template)

if __name__ == "__main__":
    main()