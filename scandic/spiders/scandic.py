import scrapy
import pendulum
from scrapy import Request


class ScandicSpider(scrapy.Spider):
    name = 'scandic'
    allowed_domains = ['scandic.se']

    def start_requests(self):
        start = pendulum.now().add(weeks=1).start_of('week')
        end = start.add(months=1)

        period = end - start

        print(period)

        date_ranges = [(day.to_date_string(), day.add(days=2).to_date_string()) for day in period.range('days')] # if day.day_of_week in [pendulum.THURSDAY, pendulum.FRIDAY, pendulum.SATURDAY] #pendulum.SUNDAY

        for date_range in date_ranges:
            for code in ['FG2', 'ICA', '']: #SUMMER
                url = f'https://www.scandichotels.se/hotelreservation/select-hotel?city=STOCKHOLM&fromDate={date_range[0]}&toDate={date_range[1]}&room[0].adults=1'
                if code != '':
                    url += '&bookingCode=' + code

                yield Request(url, callback=self.parse, meta={'date_range': date_range, 'booking_code': code})

    def parse(self, response):
        for e in response.css('div[data-js-sortable-hotel-list__hotel]'):
            data = {key[len('data-'):]: value for (key, value) in
                    e.attrib.items() if key.startswith('data-')}

            data['date_range'] = response.meta['date_range']
            data['booking_code'] = response.meta['booking_code']

            yield data
