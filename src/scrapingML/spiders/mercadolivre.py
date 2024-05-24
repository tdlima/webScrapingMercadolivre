import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]
    page_count = 1
    max_page = 10

    def parse(self, response):
        products = response.css('div.ui-search-result__content')
	
        for product in products:

            prices = product.css('span.andes-money-amount__fraction::text').getall()
            cents = product.css('span.andes-money-amount__cents::text').getall()

            yield{
	    	'marca': product.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get(),
                'descricao': product.css('h2.ui-search-item__title::text').get(),
                'valor_antigo': prices[0] if len(prices) > 0 else None,
                'centavos_ant': cents[0] if len(cents) > 0 else None,
                'valor_novo': prices[1] if len(prices) > 1 else None,
                'centavos_nv': cents[1] if len(cents) > 1 else None,
                'avaliacoes': product.css('span.ui-search-reviews__rating-number::text').get(),
                'qnt_avaliacoes': product.css('span.ui-search-reviews__amount::text').get()
	    }

        if self.page_count < self.max_page:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield scrapy.Request(url=next_page, callback=self.parse)
