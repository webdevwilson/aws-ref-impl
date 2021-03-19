import json
import re

def handler(event, context):
    print("Event: %s" % json.dumps(event))
    request = event['Records'][0]['cf']['request']
    request['uri'] = rewrite_request_uri(request['uri'])
    print('Request URI: \'{}\''.format(request['uri']))
    return request

def rewrite_request_uri(uri):
    if uri[-1] == '/':
        print('Rewriting request \'{}\''.format(uri))
        return uri + 'index.html'
    else:
        print('Skipping request \'{}\''.format(uri))
        return uri

if __name__ == '__main__':
    def test(uri, expected):
        result = rewrite_request_uri(uri)
        if result != expected:
            raise Exception('Expected: {0}, Got: {1}'.format(expected, result))
    
    test('/foo/bar/', '/foo/bar/index.html')
    test('/foo/bar/index.html', '/foo/bar/index.html')