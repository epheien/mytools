#!/usr/bin/env python3
'''alfred sdcv workflow 包装器'''

import sys
import subprocess
import json

def main(argv):
    word = argv[1]
    p = subprocess.Popen(['/usr/bin/env', 'sdcv', '-nj', word],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = p.communicate()

    d = json.loads(out)

    result = {'items': []}

    for one in d:
        item = {
            #"uid": "desktop",
            #"type": "file",
            "title": one['word'],
            "subtitle": one['definition'].replace('\n', ' '),
            "arg": word,
            #"autocomplete": "Desktop",
            "icon": {
                "type": "dictionary",
            }
        }
        result['items'].append(item)

    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main(sys.argv)
