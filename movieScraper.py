from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from unidecode import unidecode
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

        if(soup.find('span', string='Ano de produção')):
            infos.append(str(soup.find('span', string='Ano de produção').next_sibling.next_sibling.string))
        if(soup.find('span', string='Tipo de filme')):
            infos.append(str(soup.find('span', string='Tipo de filme').next_sibling.next_sibling.string))
        if(soup.find('span', string='Orçamento')):
            infos.append(str(soup.find('span', string='Orçamento').nextSibling.nextSibling.string))
        if(soup.find('span', string='Idiomas')):
            infos.append(str(soup.find('span', string='Idiomas').nextSibling.nextSibling.string))
        if(soup.find('span', class_='stareval-note')):
            infos.append(str(soup.find('span', class_='stareval-note').string))

        return infos
        
    def query_url_link_creator(self, query):
        return self.LINK + query
    
    def searcher_movie_page(self):
        movie_url = None
        link = self.query_url_link_creator(self.movie_name)

        driver.get(link)
    
        tags = driver.find_elements_by_class_name('meta-title-link')

        for i in tags:
            tag_string = WordFormater(str(i.text))
            if(tag_string.formater() == self.movie_name):
                if(str(i.get_attribute('href'))[27:33] == 'filmes'):
                    movie_url = str(i.get_attribute('href'))

        driver.quit()
        
        return movie_url

class WordFormater(object):
    def __init__(self, word):
        self.word = word

    def upper_word(self):
        self.word = self.word.upper()
        return self

    def normalize(self):
        self.word = unidecode(self.word)
        return self

    def query_format(self):
        self.word = self.word.replace(' ', '+')
        return self

    def formater(self):
        self.upper_word().normalize().query_format()
        return self.word
        


if __name__ == '__main__':
    name = WordFormater(sys.argv[1]) 
    crawler = AdoroCinema(name.formater())
    movie_stats = crawler.movie_page_parser()

    if(type(movie_stats) is list):
        for i in movie_stats:
            print(i)
    else:
        print(movie_stats)