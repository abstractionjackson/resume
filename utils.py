from datetime import datetime

def parse_bulleted_list(body):
    '''Takes a plaintext string of newline-separated bullet ("-") items, and returns a list'''
    # Split the input string into individual lines and remove leading/trailing whitespace
    lines = [line.strip() for line in body.split('\n')]
    
    # Extract items starting with a bullet ("-")
    bullet_list = [line[1:].strip() for line in lines if line.startswith('-')]
    
    return bullet_list

def parse_org_date(org_date):
    '''Takes an org-mode date string and returns a datetime object'''
    def remove_brackets(org_date):
        '''Remove square and angle brackets from an org-mode date string'''
        return org_date.strip('<>').strip('[]')
    def remove_day(org_date):
        '''Remove the day of the week from an org-mode date string'''
        return org_date.split(' ', 1)[0]
    # remove brackets, then day
    return datetime.strptime(remove_day(remove_brackets(org_date)), '%Y-%m-%d')

def parse_org_boolean(org_boolean):
    '''Takes an org-mode boolean string and returns a Python boolean'''
    return org_boolean == 't'