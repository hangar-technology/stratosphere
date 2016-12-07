import os

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


def get_google_auth(service, version='v2'):
    credentials = GoogleCredentials.get_application_default()
    service_conn = discovery.build(service, version, credentials=credentials)
    return service_conn


def get_latest_image(project, name):
    '''
    This attempts to return the latest image based on an search string.
    '''
    g = get_google_auth('compute', 'v1')

    # Google puts public images in different projects.
    newest_image = None
    for _project in ['centos-cloud', 'coreos-cloud', 'debian-cloud', 'ubuntu-os-cloud', project]:
        result = g.images().list(project=_project).execute()
        for image in result.get('items', []):
            if image['name'].find(name) != -1:
                if not newest_image:
                    newest_image = image
                else:
                    if image['creationTimestamp'] > newest_image['creationTimestamp']:
                        newest_image = image

    if not newest_image:
        raise KeyError("No images found for {}/{}".format(project, name))

    return newest_image['selfLink']


def load_startup_script(path, replacements=None):
    """
    Loads a startup-script from disk

    path (str): A path to the script file
    replacements (tuple): A tuple of string replacements to run on the file, if supplied.
                          Formatted like: ((string1, string2, count), (string3, string4, count)) where
                          count is the number of replacements to make for that pattern
    """
    path = os.path.abspath(path)
    if os.path.isfile(path):
        with open(path) as f:
            script = f.read()
    else:
        raise ValueError('Startup-script file not found: {}'.format(path))
    if replacements is not None:
        for replacement in replacements:
            if not isinstance(replacement, tuple):
                raise ValueError('Replacements must be a tuple of tuples to replace')
            from_string = str(replacement[0])
            to_string = str(replacement[1])
            if len(replacement) == 3:
                max = replacement[2]
                script = script.replace(from_string, to_string, max)
            else:
                script = script.replace(from_string, to_string)

    return script
