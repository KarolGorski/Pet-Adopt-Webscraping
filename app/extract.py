# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import csv
import re

class Extraction():

    def has_class(self,tag):
        return tag.has_attr('class')


    def get_info_dict(self,url):
        
        r = requests.get(url)
        r.encoding = 'utf-8'
        data = r.text

        soup = BeautifulSoup(data, "html.parser")

        info_dict = {'url' : '',
                     'title' : '',
                     'author' : '',
                     'description' : '',
                     'charset' : '',
                     'lang' : ''
        }

        
        info_dict['url']= url
        
        title_object = soup.find("title")
        if title_object is not None:
            info_dict['title'] = title_object.string.encode('utf-8')
        
       
        author_object = soup.find("meta",{"name" : "author"})
        if author_object is not None:
            info_dict['author'] = author_object['content'].encode('utf-8')
       
        
        description_object = soup.find("meta",{"name" : "description"})
        if description_object is not None:
            info_dict['description'] = description_object['content'].encode('utf-8')
       
               
        charset_object = soup.find("meta", charset = re.compile('\d'))
        if charset_object is not None:
            info_dict['charset'] = charset_object['charset'].encode('utf-8')
       
        
        lang_object = soup.find("html", lang = re.compile('\d'))
        if lang_object is not None:
            info_dict['lang'] = lang_object['lang'].encode('utf-8')
        
       
        return info_dict


    def run(self,urls):

        urls = [ url.strip() for url in urls.strip().splitlines() if url]
        
        print(urls)
        with open('app/static/sites_metadata.csv', 'w') as csvfile:
            fieldnames = ['url', 'title', 'author', 'description', 'charset', 'lang']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
            writer.writeheader()
            
            
            for url in urls:
                url='http://'+url if not url[:4].lower() == 'http' else url
                
                row = self.get_info_dict(url)
                print("ROW: ",row)
                writer.writerow(row)
            
            
        print("Data extraction successful.")


    
