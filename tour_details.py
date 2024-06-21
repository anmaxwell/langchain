import requests
from bs4 import BeautifulSoup

def get_tour_details(tour_urls):

    contents = []
    tours = []
    for index, url in enumerate(tour_urls):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')

        # store the title of each tour in a list
        tours.append(soup.title.get_text().replace('\n', ' ').replace('\t', ''))
        
        tour_info = []  # a list to store the info of each tour
        header_info = soup.find_all('p', class_='wyg-text-info')
        for header in header_info:
            tour_info.append(header.get_text(strip=True))

        detailed_info = soup.find_all('li', class_='wyg-intro-list-item')
        for detail in detailed_info:
            tour_info.append(detail.get_text(strip=True))

        contents.append(tour_info)

    corpus_of_documents = []
    for item in contents:
        full_details = ' '.join(item)
        corpus_of_documents.append(full_details)
    
    return tours, corpus_of_documents