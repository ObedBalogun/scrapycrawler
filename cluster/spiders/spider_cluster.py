import scrapy


class LinkedinProfileCrawler(scrapy.Spider):
    name = 'linkedin_profile_crawler'
    custom_settings = {
        'FEEDS': {'scraped_data/%(name)s_%(time)s.jsonl': {'format': 'jsonlines', }}
    }

    @classmethod
    def start_requests(cls):
        profile_list = ['olamidecoker']
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, sdch, br",
            "accept-language": "en-US,en;q=0.8,ms;q=0.6",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        }
        for profile in profile_list:
            linkedin_people_url = f'https://www.linkedin.com/in/{profile}/'
            yield scrapy.Request(url=linkedin_people_url, callback=cls.parse_profile, headers=headers,
                                 meta={'profile': profile, 'linkedin_url': linkedin_people_url})

    @classmethod
    def parse_profile(cls, request):
        item = {
            'profile': request.meta['profile'],
            'url': request.meta['linkedin_url'],
        }
        """
            SUMMARY SECTION
        """
        summary_box = request.css("section.top-card-layout")
        print(summary_box, 'summary_box')
        item['name'] = summary_box.css("h1::text").get().strip()
        item['description'] = summary_box.css("h2::text").get().strip()

        ## Location
        try:
            item['location'] = summary_box.css('div.top-card__subline-item::text').get()
        except Exception as e:
            item['location'] = summary_box.css('span.top-card__subline-item::text').get().strip()
            if 'followers' in item['location'] or 'connections' in item['location']:
                item['location'] = ''

        item['followers'] = ''
        item['connections'] = ''

        for span_text in summary_box.css('span.top-card__subline-item::text').getall():
            if 'followers' in span_text:
                item['followers'] = span_text.replace(' followers', '').strip()
            if 'connections' in span_text:
                item['connections'] = span_text.replace(' connections', '').strip()

        """
            ABOUT SECTION
        """
        item['about'] = request.css('section.summary div.core-section-container__content p::text').get(default='')

        """
            EXPERIENCE SECTION
        """
        item['experience'] = []
        experience_box = request.css('section.experience-section')
        for experience in experience_box.css('li.experience-section__list-item'):
            experience_item = {'title': experience.css('h3::text').get().strip(),
                               'company': experience.css('h4::text').get().strip(),
                               'date_range': experience.css('h5::text').get().strip(),
                               'description': experience.css('p::text').get(default='').strip()}
            item['experience'].append(experience_item)

        """
            EDUCATION SECTION
        """
        item['education'] = []
        education_box = request.css('section.education-section')
        for education in education_box.css('li.education-section__list-item'):
            education_item = {'school': education.css('h3::text').get().strip}
        yield item
