"""Python Class that Provides Data Extraction From Org to Jinja"""

class Resume:
    def __init__(self, root):
        self.root = root
        self.set_meta()
        self.set_header()
        self.set_email()
        self.set_location()
        self.set_linkedin()

    def set_meta(self):
        self.meta = {}
        lines = self.root.body.split('\n')
        for line in lines:
            if line.startswith("#+"):
                key_value_pair = line.lstrip("#+").split(":", 1)
                if len(key_value_pair) == 2:
                    key, value = key_value_pair
                    self.meta[key.strip().upper()] = value.strip()
    
    def _get_node_by_heading(self, heading=""):
        return next((node for node in self.root if node.heading.upper() == heading.upper()), None)
    
    def _get_node_properties(self, node, *properties):
        return {
            prop.upper(): node.get_property(prop.upper())
            for prop in properties
        }
        
    
    def set_header(self):
        node = self._get_node_by_heading('contact')
        self.header = self._get_node_properties(node, 'name_last', 'name_first')

    def set_email(self):
        self.email = self._get_node_properties(
            self._get_node_by_heading('contact'),
            'email'
        )['EMAIL']

    def set_location(self):
        self.location = self._get_node_properties(
            self._get_node_by_heading('contact'),
            'city', 'state'
        )
    
    def set_linkedin(self):
        self.linkedin = self._get_node_properties(
            self._get_node_by_heading('contact'),
            'linkedin'
        )['LINKEDIN']