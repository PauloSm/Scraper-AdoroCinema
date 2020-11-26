from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import sys

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)


class AdoroCinema(object):

    LINK = 'http://www.adorocinema.com/busca/?q='

    def __init__(self, movie_name):
        self.movie_name = movie_name

    def movie_page_parser(self):
        url = self.searcher_movie_page()

        if(url == None): 
            return 'Filme não encontrado.'
        
        try:
            res = requests.get(url)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        
        soup = BeautifulSoup(res.content, 'html.parser')
        
        infos = []
        infos.append(str(soup.find('span', string='Ano de produção').next_sibling.next_sibling.string))
        infos.append(str(soup.find('span', string='Tipo de filme').next_sibling.next_sibling.string))
        infos.append(str(soup.find('span', string='Orçamento').nextSibling.nextSibling.string))
        infos.append(str(soup.find('span', string='Idiomas').nextSibling.nextSibling.string))
        infos.append(str(soup.find('span', class_='stareval-note').string))

        return infos
    
    def formater_name_to_query_string(self, name):
        name = name.upper()
        name = name.replace(' ', '+')

        return name
        
    def query_url_link_creator(self, query):
        return self.LINK + query
    
    def searcher_movie_page(self):
        movie_url = None
        name = self.formater_name_to_query_string(self.movie_name)
        link = self.query_url_link_creator(name)

        driver.get(link)
    
        tags = driver.find_elements_by_class_name('meta-title-link')

        for i in tags:
            if(str(i.text).upper() == self.movie_name.upper()):
                movie_url = str(i.get_attribute('href'))

        driver.quit()
        
        return movie_url
        


if __name__ == '__main__':
    crawler = AdoroCinema(sys.argv[1])
    movie_stats = crawler.movie_page_parser()

    if(type(movie_stats) is list):
        for i in movie_stats:
            print(i)
    else:
        print(movie_stats)