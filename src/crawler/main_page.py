import requests
import yaml
from field_page import Field
from bs4 import BeautifulSoup
import os
import csv

'''
    Crawl each field url from main page.
    Create Field object for each field exist in requested fields in parameters.
'''


class Main:
    def __init__(self, parameters=None):
        self.baseURL = None
        self.fields_name = None
        self.fields = []
        self.load_variables(parameters)
        self.crawl_fields()

    def load_variables(self, parameters):
        if parameters is None:
            with open('../config') as conf_file:
                configs = yaml.full_load(conf_file)['Crawl']
                self.fields_name = configs['FIELDS']
                self.baseURL = configs['BASEURL']
                self.max_page = configs['MAXPAGE']
        else:
            self.fields_name = parameters.fields
            self.baseURL = parameters.baseURL

    def crawl_fields(self):
        fields = {}
        article = requests.get(self.baseURL + '/persian')
        soup = BeautifulSoup(article.content, 'html.parser')
        type_list = soup.find(role='navigation')
        type_list = type_list.find_all('ul')[0]
        for a in type_list.find_all('a'):
            url = a.get('href')
            text = a.get_text()
            if text in self.fields_name:
                max_page = self.max_page[self.fields_name.index(text)]
                self.fields.append(Field(text, url, self.baseURL, max_page))

if not os.path.exists('../data/dataset.csv'):
    with open('../data/dataset.csv', 'w', newline='') as csvfile:
        fieldnames = ['url', 'title', 'headline', 'body']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
Main()