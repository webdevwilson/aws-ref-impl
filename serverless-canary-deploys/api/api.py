import json
import os

def handler(evt, ctx):
    version = os.environ.get('VERSION')
    return {
        "statusCode": 200,
        "body": json.dumps({
            "version": version
        })
    }

if __name__ == '__main__':
    resp = handler(None,None)
    assert resp['statusCode'] == 200
