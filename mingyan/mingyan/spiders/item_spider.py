import scrapy

class itemSpider( scrapy.Spider ):
	name = "itemSpider"
	
	def parse( self, response ):
		print("@@@@itemSpider is parse")
