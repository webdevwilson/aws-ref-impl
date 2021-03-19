import json

def handler(evt, _):
    print(json.dumps(evt))

if __name__ == '__main__':
    handler({}, None)