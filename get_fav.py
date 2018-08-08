import urllib.request
import re

# https://stackoverflow.com/questions/28982850/twitter-api-getting-list-of-users-who-favorited-a-status

def get_favoritters(post_id):
    try:
        json_data = urllib.request.urlopen('https://twitter.com/i/activity/favorited_popup?id=' + str(post_id)).read()
        json_data=json_data.decode("utf-8")
        found_ids = re.findall(r'data-user-id=\\"+\d+', json_data)
        unique_ids = list(set([re.findall(r'\d+', match)[0] for match in found_ids]))
        return unique_ids
    except urllib.request.HTTPError:
        return False
        
if __name__ == "__main__":
    print(get_favoritters())