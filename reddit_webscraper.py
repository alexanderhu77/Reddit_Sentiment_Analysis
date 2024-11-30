import time
import httpx
import pandas as pd

def scrape_subreddit(base_url, endpoint, category):

    url = base_url + endpoint + category + '.json'
    after_post_id = None
    dataset = []

    for t in range (10):
        params = {
            'limit' : 100,
            't' : 'year' ,
            'after' : after_post_id
        }

        response = httpx.get (url, params=params, follow_redirects=True)
        print(f'fetching  {response.url}')
        if response.status_code !=200:
            print (response.status_code)
            raise Exception('Failed')

        json_data = response.json()

        dataset.extend([rec['data'] for rec in json_data['data']['children']])

        after_post_id = json_data['data']['after']
        time.sleep(0.5)

    df = pd.DataFrame(dataset)
    df.to_csv(f'C:\\Tian-Starter-Task\\reddit_scrape_{endpoint[3:]}.csv', index=False)

    
scrape_subreddit('https://www.reddit.com/','/r/DigitalPrivacy' , '/new')
scrape_subreddit('https://www.reddit.com/', '/r/ComputerSecurity', '/new')