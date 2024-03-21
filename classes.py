from utils import parse_bulleted_list, parse_org_date

class Node:
    def __init__(self, root):
        self.root = root

    def get_node_by_heading(self, heading=""):
        return next((node for node in self.root if node.heading.upper() == heading.upper()), None)
    

class Resume(Node):
    def __init__(self, root):
        super().__init__(root)
        self.set_meta()
        self.set_header()
        self.set_email()
        self.set_location()
        self.set_linkedin()
        self.set_skills()
        self.set_experience()

    def set_meta(self):
        self.meta = {}
        lines = self.root.body.split('\n')
        for line in lines:
            if line.startswith("#+"):
                key_value_pair = line.lstrip("#+").split(":", 1)
                if len(key_value_pair) == 2:
                    key, value = key_value_pair
                    self.meta[key.strip().upper()] = value.strip()

    
    def _get_node_properties(self, node, *properties):
        return {
            prop.upper(): node.get_property(prop.upper())
            for prop in properties
        }

    def set_header(self):
        node = self.get_node_by_heading('contact')
        self.header = self._get_node_properties(node, 'name_last', 'name_first')

    def set_email(self):
        self.email = self._get_node_properties(
            self.get_node_by_heading('contact'),
            'email'
        )['EMAIL']

    def set_location(self):
        self.location = self._get_node_properties(
            self.get_node_by_heading('contact'),
            'city', 'state'
        )
    
    def set_linkedin(self):
        self.linkedin = self._get_node_properties(
            self.get_node_by_heading('contact'),
            'linkedin'
        )['LINKEDIN']

    def set_skills(self):
        self.skills = parse_bulleted_list(
            self.get_node_by_heading('skills').body
        )

    def set_experience(self):
        self.experience = list()
        jobs = self.get_node_by_heading('Experience').children
        for job in jobs:
            self.experience.append(Job(job))
        pass

class Job(Node, dict):
    properties = (
        'id',
        'company',
        'start_date',
        'end_date',
        'location',
        'remote'
    )
    def __init__(self, node):
        super().__init__(node)
        self.title = node.heading
        for property in self.properties:
            self[property] = node.get_property(property.upper())
        self.details = parse_bulleted_list(
            self.get_node_by_heading('details').body
        )
        for org_date in ('start_date', 'end_date'):
            self[org_date] = parse_org_date(self[org_date])