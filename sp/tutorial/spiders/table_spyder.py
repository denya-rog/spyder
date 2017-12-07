
import scrapy
import re

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from items import DataItem


class TableSpider(scrapy.Spider):
    name = "table"

    
    def start_requests(self):
        """takes urls and go thru them, calling parse fun"""
        
        urls = ['http://proxylist.hidemyass.com/',
    
        ]
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

            
    def parse(self, response):
        """function for persing. also creates DB wuth 3 columns"""
   
        port = response.xpath("//tbody/tr//td[3]/ text()").extract() # td[3]-column for port
        span = response.xpath('//tbody/tr/td[2]/span').extract()
        
        ip = []     #will collect ip-adress

        for i in span:            
            bad = re.findall(r'\.(\S{3,5}){display:none}',i) # find invisible classes     
            spans = re.findall(r'(<span .*?>.*?</span>)',i) #find all tags span
            divs = re.findall(r'(<div .*?>.*?</div>)',i)    #find all tags div
            tags = spans+divs
            
            style = '"display:none"'# for detecting invisible styles
            
            for j in bad:
                for k in tags:
                    if j in k or style in k:
                        i = i.replace(k,"")     #delete from string invisible data
                        
            i = re.findall(r'>(.*?)<',i)    #gathering all remain data
            i = "".join(i)
            ip.append(i)        
                  

        for i in range (len(ip)):
            Item = DataItem()
            Item['ip_adress'] = ip[i]
            Item['ip_adress'] = port[i]
            yield Item
            
          
