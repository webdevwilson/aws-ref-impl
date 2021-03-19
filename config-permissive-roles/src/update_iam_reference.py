import sys
from os import path
import glob
import json
import re

REGEX = re.compile('^\[([a-zA-Z0-9:]+)\]')

def scrape(dir):
    files = glob.glob(dir + '*.md')
    actions = []
    for f in files:
        with open(f) as fp:
            for _, line in enumerate(fp):
                sa = line.split('|')
                if len(sa) > 1:
                    action = sa[1].strip()
                    match = REGEX.match(action)
                    if match:
                        actions.append(match[1])
    print(json.dumps(actions))

if __name__ == '__main__':
    config_dir = sys.argv[1]
    scrape(config_dir)