import re

from taskcardmaker.renderer import Renderer
from taskcardmaker.parser import TaskCardParser
from taskcardmaker.cli import main

def parse_version (version_string):
    match = re.match(r'^([0-9]+)\.([0-9]+)\.([0-9]+)(-(.+))?$', version_string)
    if match:
        return (match.group(1), match.group(2), match.group(3), match.group(5) if match.group(4) else None)
    else:
        return ("0", "0", "0", "n/a")


version = "0.4.6"
version_info = parse_version(version)
