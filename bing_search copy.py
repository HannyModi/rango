import json
import urllib.parse
import urllib.request
import urllib.response
import certifi

def read_bing_key():
    """
    Reads the BING API key from a file called 'bing.key'.
    returns: a string which is either None, i.e. no key found, or with a key.
    Remember: put bing.key in your .gitignore file to avoid committing it!
    """
    bing_api_key = None

    try:
        with open('bing.key', 'r') as f:
            bing_api_key = f.readline()
    except:
        raise IOError('bing.key file not found')

    return bing_api_key


def run_query(search_terms):
    """
    Given a string containing search terms (query),
    returns a list of results from the Bing search engine.
    """
    bing_api_key = read_bing_key()
    #read_bing_key()

    if not bing_api_key:
        raise KeyError("Bing Key Not Found!!!")

    root_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"

    # 'https://api.cognitive.microsoft.com/bing/v7.0'
    service = 'Web'

    results_per_page = 10
    offset = 0

    query = "'{0}'".format(search_terms)
    query = urllib.parse.quote(query)

    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
        root_url, service, results_per_page, offset, query)
    #"{0}{1}?$format=json&$top={2}&$skip={3}&$Query={4}".format(root_url, service, results_per_page, offset, query)

    username = ''
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()

    password_mgr.add_password(None, search_url, username, bing_api_key)

    results = []

    try:
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)

        response = urllib.request.urlopen(search_url).read()
        response = response.decode('utf-8')

        json_response = json.loads(response)

        for result in json_response['d']['results']:
            results.append({'title': result['Title'],
                            'link': ['Url'],
                            'summery': ['Description']})
    except Exception as e:
        print(e)
        print("Error when querying the Bing API")

    return results


def main():
    item = input("Enter the item you want to search from Bing:")
    print(run_query(item))


if __name__ == '__main__':
    main()
