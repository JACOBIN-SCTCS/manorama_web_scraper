import scrapy
import json




class NewsSpider(scrapy.Spider):
    name = "news"
    
    sites = ['astrology','news','sports']

    def gen_url(self):

        url = []
        for site in self.sites:
            url.append('https://www.manoramaonline.com/content/mm/mo/'+site+'/_jcr_content/mm-section-top-left/channelallstories.results.15.4.json')
        return url   


    def start_requests(self):

        urls = self.gen_url()

        for url in urls : 
            yield scrapy.Request(url,callback=self.parse)

   
   

    def parse(self,response):
        json_data = str(json.loads(response.text)['articleList'])
        json_format = json.loads(json_data)
        for i in range(len(json_format)):
            next_page = response.urljoin(json_format[i]['url'])
            yield scrapy.Request(next_page, callback=self.get_data)
                
    def get_data(self,response): 
        headline = response.css('div.story-header h1.story-headline::text').get()
        category = response.url.split("/")[3]
        text = '.'.join(response.css('div.rte-article p::text').getall())
        with open("res.txt","a") as f : 
            f.write('\n{\n \"category\" : ' + category + 
                '\n\"headline\" : ' + headline + 
                '\n\"text\" : ' + text +
                '\n} '
                
                )
            