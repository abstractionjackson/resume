from dotenv import load_dotenv
from os import environ
from orgparse import load as load_org

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

def main():
    print("App")
    mode = environ.get('MODE')
    data = None
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

if __name__ == "__main__":
    main()