# contributors_formatter.py
def format_contributors(website_data, config):
    contributors_key = website_data.get('Contributor')
    contributors = website_data.get('Contributor', 'Anonymous')

    if contributors_key in config.get('contributors', {}):
        contributor_value = config['contributors'][contributors_key]
        if isinstance(contributor_value, list):
            contributors = ', '.join(contributor_value)
        else:
            contributors = contributor_value
    return contributors or 'Anonymous'
