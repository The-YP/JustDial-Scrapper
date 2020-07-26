import scrapy


class jdscrap(scrapy.Spider):
    name = "justdial"

    allowed_domains = ["justdial.com"]

    start_urls = [
        "https://www.justdial.com/Delhi/House-On-Rent/nct-10192844/page-%s" % i for i in range(1, 51)
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def getphone(self, ph_arr):

        digit = {"dc": "+", "fe": "(", "hg": ")", "ba": "-", "acb": "0", "yz": "1",
                 "wx": "2", "vu": "3", "ts": "4", "rq": "5", "po": "6", "nm": "7",
                 "lk": "8", "ji": "9"}
        ph = []

        for i in ph_arr:
            ph.append(digit.get(
                i.replace('mobilesv', '').replace('icon-', '').replace(' ', '')))

        return ''.join(ph)

    def parse(self, response):
        for post in response.css("li.cntanr "):
            yield {

                'Name': post.css("span.lng_cont_name ::text").get(),
                'Rating': post.css("span.exrt_count  ::text").get(),
                'Phone': self.getphone(post.css("p.contact-info span::attr(class)").getall()),
                'Address': post.css("span.cont_sw_addr ::text").get().replace('\t', '').replace('\n', '')

            }
