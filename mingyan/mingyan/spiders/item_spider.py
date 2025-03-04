import scrapy

class itemSpider( scrapy.Spider ):
	name = "itemSpider"
	
	def parse( self, response ):
		config = self.get_config
		print("@@@@itemSpider is parse")
