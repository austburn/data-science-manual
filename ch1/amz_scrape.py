import re

import requests
from bs4 import BeautifulSoup


rank_rxp = '#\d{,3}(,\d{,3})*'
books = [
    ('algo_design_manual', 'https://www.amazon.com/Algorithm-Design-Manual-Steven-Skiena/dp/1849967202'),
    ('data_science_manual', 'https://www.amazon.com/Science-Design-Manual-Texts-Computer/dp/3319554433'),
    ('programming_challenges', 'https://www.amazon.com/Programming-Challenges-Contest-Training-Computer-ebook/dp/B008AFF2ZU')
]

def convert_to_int(match):
    rank = match.group()
    return int(rank[1:].replace(',', ''))


if __name__ == '__main__':
    for b in books:
        key = b[0]
        url = b[1]

        r = requests.get(url, headers={'Referer': 'https://amazon.com'})

        if not r.ok:
            print('non-200 code: {}'.format(r.status_code))
            exit(1)

        soup = BeautifulSoup(r.content, 'html.parser')
        best_seller_info = soup.find('li', id='SalesRank')

        overall_best_seller = re.search(rank_rxp, best_seller_info.text)
        print(key, convert_to_int(overall_best_seller))

        categorical_rankings = best_seller_info.findAll('li', 'zg_hrsr_item')
        for category in categorical_rankings:
            ranking = re.search(rank_rxp, category.text)
            category_name = category.text.split(' > ')[-1].replace('\n', '')
            print(category_name, convert_to_int(ranking))

