# -*- coding: utf-8 -*-
import scrapy, logging

"""
https://www.klimaundenergiemodellregionen.at/modellregionen/liste-der-regionen/
"""


class GetcontactsSpider(scrapy.Spider):
    name = 'getcontacts'
    allowed_domains = ['www.klimaundenergiemodellregionen.at']
    start_urls = ['https://www.klimaundenergiemodellregionen.at/modellregionen/liste-der-regionen/']
    template_regionURL = 'https://www.klimaundenergiemodellregionen.at/modellregionen/liste-der-regionen/getregion/{regionID}'
    # xpath_state = '//table[@id="datatable"]/tbody/tr/td[1]/text()'
    xpath_state = '//table[@id="datatable"]/tbody/tr/td[2]/a/@href'
    # xpath_state = '//table[@id="datatable"]/tbody/tr/td[1]/a'
    xpath_region_mode = '//img[@alt="Inaktive Region"]'
    xpath_region_area = '/html/body/div/div/div/i[has-class("fa","fa-map-marker","blue","bigger","text-center")]/following-sibling::span[has-class("fakt")][1]/text()'
    xpath_region_date = '/html/body/div/div/div/i[has-class("fa","fa-calendar","blue","big","text-center")]/following-sibling::span[has-class("fakt")][1]/text()'
    xpath_region_phase = '/html/body/div/div/div/i[has-class("fa","fa-list-ol","blue","big","text-center")]/following-sibling::span[has-class("fakt")][1]/text()'
    xpath_region_size = '/html/body/div/div/div/i[has-class("fa","fa-arrows","blue","big","text-center")]/following-sibling::span[has-class("fakt")][1]/text()'
    xpath_region_population = '/html/body/div/div/div/i[has-class("fa","fa-user","blue","big","text-center")]/following-sibling::span[has-class("fakt")][1]/text()'
    xpath_region_website = '/html/body/div/div/div/i[has-class("fa","fa-globe","blue","big","text-center")]/following-sibling::a[1]/@href'
    xpath_region_contactName = '/html/body/div/div/div/i[has-class("fa","fa-envelope","blue","big","text-center")]/following-sibling::span[has-class("fakt")][1]/a/text()'
    xpath_contact_type = '//div[@id="manager"]/div[has-class("row")]/div[@class]/h4[1]/text()'
    xpath_contact_institution = '//div[@id="manager"]/div/div[@class="large-5 medium-5 small-8 columns"]/text()[2]'
    # xpath_contact_name = '//div[@id="manager"]/div/div[@class="large-5 medium-5 small-8 columns"]/text()[1]'
    xpath_contact_name = '//div[@id="manager"]/div[has-class("row")][2]/div[@class]/text()[1]'
    # xpath_contact_phone = '//div[@id="manager"]/div/div[@class="large-5 medium-5 small-8 columns"]/i[@class="fa fa-phone"]/following-sibling::text()'
    xpath_contact_phone = '//div[@id="manager"]/div[has-class("row")][2]/div[@class]/i[has-class("fa","fa-phone")]/following-sibling::text()'
    # xpath_contact_mobile = '//div[@id="manager"]/div/div[@class="large-5 medium-5 small-8 columns"]/a[@class="blue mobile"]/i/following-sibling::text()'
    xpath_contact_mobile = '//div[@id="manager"]/div[has-class("row")][2]/div[@class]/a[has-class("blue","mobile")]/i[has-class("fa","fa-phone")]/following-sibling::text()[1]'
    # xpath_contact_mail = '//div[@id="manager"]/div/div[@class="large-5 medium-5 small-8 columns"]/a[@class="blue"]/i[@class="fa fa-envelope"]/following-sibling::text()'
    xpath_contact_mail = '//div[@id="manager"]/div[has-class("row")][2]/div[@class]/a[has-class("blue")]/i[has-class("fa","fa-envelope")]/following-sibling::text()[1]'
    # xpath_contact_address = '//div[@id="manager"]/div/div[@class="large-5 medium-5 small-8 columns"]/strong[text()="Ort"]/following-sibling::text()[1]'
    xpath_contact_address = '//div[@id="manager"]/div[has-class("row")][2]/div[@class]/strong[text()="Ort"]/following-sibling::text()[1]'

    def start_requests(self):
        logging.debug(self.settings.get('BOT_NAME'))
        yield scrapy.Request(self.start_urls[0])
        for regionID in range(0, 501):
            yield scrapy.Request(self.template_regionURL.format(regionID=regionID), callback=self.parseKEM)

    def parse(self, response):
        logging.debug('Got regions: %s', response.xpath(self.xpath_state).getall())
        for kem in response.xpath(self.xpath_state).getall():
            logging.debug('Yielding KEM region: %s', kem)
            yield scrapy.Request(response.urljoin(kem), callback=self.parseKEM)

    def parseKEM(self, response):
        # TODO check empty fields
        # TODO sanitize data (phone, mail, split name)
        logging.debug('#########################')
        hasData = False
        resultData = {
            'Page': response.url,
            'Region Mode': '',
            'Region Area': '',
            'Region Date': '',
            'Region Phase': '',
            'Region Size': '',
            'Region Population': '',
            'Region Website': '',
            'Region Contactname': '',
            'Contact Type': '',
            'Contact Name': '',
            'Contact Phone': '',
            'Contact Mobile': '',
            'Contact Mail': '',
            'Contact Address': '',
            'Contact Institution': ''
        }

        raw_region_mode = response.xpath(self.xpath_region_mode).get()
        if raw_region_mode == None:
            resultData['Region Mode'] = 'Active'
        else:
            resultData['Region Mode'] = 'Inactive'
        logging.debug('Region Mode: %s', resultData['Region Mode'])

        raw_region_area = response.xpath(self.xpath_region_area).get()
        if raw_region_area != None:
            hasData = True
            region_area = raw_region_area.strip()
            resultData['Region Area'] = region_area
            logging.debug('Region Area: %s', region_area)

        raw_region_date = response.xpath(self.xpath_region_date).get()
        if raw_region_date != None:
            hasData = True
            region_date = raw_region_date.strip()
            resultData['Region Date'] = region_date
            logging.debug('Region Date: %s', region_date)

        raw_region_phase = response.xpath(self.xpath_region_phase).get()
        if raw_region_phase != None:
            hasData = True
            region_phase = raw_region_phase.strip()
            resultData['Region Phase'] = region_phase
            logging.debug('Region Phase: %s', region_phase)

        raw_region_size = response.xpath(self.xpath_region_size).get()
        if raw_region_size != None:
            hasData = True
            region_size = raw_region_size.strip()
            resultData['Region Size'] = region_size
            logging.debug('Region Size: %s', region_size)

        raw_region_population = response.xpath(self.xpath_region_population).get()
        if raw_region_population != None:
            hasData = True
            region_population = raw_region_population.strip()
            resultData['Region Population'] = region_population
            logging.debug('Region Population: %s', region_population)

        raw_region_website = response.xpath(self.xpath_region_website).get()
        if raw_region_website != None:
            hasData = True
            region_website = raw_region_website.strip()
            resultData['Region Website'] = region_website
            logging.debug('Region Website: %s', region_website)

        raw_region_contactName = response.xpath(self.xpath_region_contactName).get()
        if raw_region_contactName != None:
            region_contactName = raw_region_contactName.strip()
            resultData['Region Contactname'] = region_contactName
            logging.debug('Region Contactname: %s', region_contactName)

        raw_contactType = response.xpath(self.xpath_contact_type).get()
        if raw_contactType != None:
            contactType = raw_contactType.strip()
            resultData['Contact Type'] = contactType
            logging.debug('Contact Type: %s', contactType)

        raw_contactName = response.xpath(self.xpath_contact_name).get()
        if raw_contactName != None:
            contactName = raw_contactName.strip()
            resultData['Contact Name'] = contactName
            logging.debug('Contact Name: %s', contactName)

        raw_contactPhone = response.xpath(self.xpath_contact_phone).get()
        if raw_contactPhone != None:
            hasData = True
            contactPhone = raw_contactPhone.strip()
            resultData['Contact Phone'] = contactPhone
            logging.debug('Contact Phone: %s', contactPhone)

        raw_contactMobile = response.xpath(self.xpath_contact_mobile).get()
        if raw_contactMobile != None:
            hasData = True
            contactMobile = raw_contactMobile.strip()
            resultData['Contact Mobile'] = contactMobile
            logging.debug('Contact Mobile: %s', contactMobile)

        raw_contactMail = response.xpath(self.xpath_contact_mail).get()
        if raw_contactMail != None:
            hasData = True
            contactMail = raw_contactMail.strip()
            resultData['Contact Mail'] = contactMail
            logging.debug('Contact Mail: %s', contactMail)

        raw_contactAddress = response.xpath(self.xpath_contact_address).get()
        if raw_contactAddress != None:
            hasData = True
            contactAddress = raw_contactAddress.strip()
            resultData['Contact Address'] = contactAddress
            logging.debug('Contact Address: %s', contactAddress)

        raw_ContactInstitution = response.xpath(self.xpath_contact_institution).get()
        if raw_ContactInstitution != None:
            hasData = True
            contactInstitution = raw_ContactInstitution.strip()
            resultData['Contact Institution'] = contactInstitution
            logging.debug('Contact Institution: %s', contactInstitution)

        if hasData:
            yield resultData
