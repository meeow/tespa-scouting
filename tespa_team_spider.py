from scrapy import Request
from scrapy.spiders import Spider

class CollectTeams(Spider):
    name = 's2'

    #allowed_domains
    name = "s2"
    allowed_domains = ["tespa.org"]
    start_urls = ["https://compete.tespa.org/tournament/111/registrants?page={}".format(i) for i in range(1,27)]
    custom_settings = {
            'DOWNLOAD_DELAY': 0.1,
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'FEED_FORMAT': 'csv',
            'FEED_URI': './db/tespa_teams.csv'
           }

    def parse(self, response):
        names = response.xpath('//table/tbody/tr')
        ans=[]
        for name in names:
            item = {}
            item['team_name'] = name.xpath('td/a/text()').extract()
            item['team_school'] = name.xpath("td[4]/text()").extract()
            item['team_link_url'] = name.xpath("td/a/@href").extract()
            item['team_rank'] = name.xpath("td[@class='registrant-ranks']/text()").extract()
            if item['team_link_url']:
                req = Request((str(item['team_link_url'][0])), callback=self.parse_2)
                req.meta['foo'] = item
                ans.append(req)
        return ans

    def parse_2(self, response):
        it = response.meta['foo']
        btag = response.xpath('//div/table/tbody/tr/td[3]/text()').extract()
        it['btag'] = btag
        return it       

