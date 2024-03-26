from utils import parse_bulleted_list, parse_org_boolean, parse_org_date

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
        self.set_summary(   )
        self.set_skills()
        self.set_jobs()
        self.set_education_history()
        self.set_awards()

    def set_meta(self):
        self.meta = {}
        lines = self.root.body.split('\n')
        for line in lines:
            if line.startswith("#+"):
                key_value_pair = line.lstrip("#+").split(":", 1)
                if len(key_value_pair) == 2:
                    key, value = key_value_pair
                    self.meta[key.strip().upper()] = value.strip()

    def set_summary(self):
        self.summary = self.get_node_by_heading('summary').body
        
    def set_awards(self):
        pass

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

    def set_jobs(self):
        self.jobs = list()
        jobs = self.get_node_by_heading('Experience').children
        for job in jobs:
            self.jobs.append(Job(job))

    def set_awards(self):
        self.awards = list()
        awards = self.get_node_by_heading('Awards').children
        for award in awards:
            self.awards.append(Award(award))

    def set_education_history(self):
        self.education_history = list()
        educations = self.get_node_by_heading('Education').children
        for edu in educations:
            self.education_history.append(Education(edu))

class Job(Node, dict):
    properties = (
        'id',
        'company',
        'start_date',
        'end_date',
        'location',
        'remote',
        'contract',
    )
    boolean_properties = (
        'contract',
        'remote'
    )
    sections = (
        'details',
        'summary'
    )
    def __init__(self, node):
        super().__init__(node)
        self.title = node.heading
        for property in self.properties:
            self[property] = node.get_property(property.upper())
            if property in self.boolean_properties:
                self[property] = parse_org_boolean(self[property])
        self.details = parse_bulleted_list(
            self.get_node_by_heading('details').body
        )
        self.summary = self.get_node_by_heading('summary').body
        for org_date in ('start_date', 'end_date'):
            self[org_date] = parse_org_date(self[org_date])

class Award(Node, dict):
    properties = (
        'id',
        'iss',
        'year'
    )
    def __init__(self, node):
        super().__init__(node)
        self.title = node.heading
        for property in self.properties:
            self[property] = node.get_property(property.upper())

class Education(Node, dict):
    properties = (
        'id',
        'iss',
        'year',
        'location',
    )
    def __init__(self, node):
        super().__init__(node)
        self.title = node.heading
        for property in self.properties:
            self[property] = node.get_property(property.upper())