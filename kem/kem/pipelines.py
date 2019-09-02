# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy, logging, datetime
import databaseSchema as dbs

class DBPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        temp = cls()
        crawler.signals.connect(temp.spider_closed, signal=scrapy.signals.spider_closed)
        return temp

    def open_spider(self, spider):
        projectName = spider.settings.get('BOTNAME')
        spiderName = spider.name
        self.s = dbs.init_session('results.db')
        spider = self.s.query(dbs.Spider).filter(dbs.Spider.project==projectName).filter(dbs.Spider.name==spiderName).first()
        if not spider:
            spider = dbs.Spider(project=projectName, name=spiderName)
            self.s.add(spider)
        self.db_job = dbs.Job(timeStart=datetime.datetime.now(), spider=spider)
        logging.warning('Job ID is: %d', self.db_job.id)
        self.s.add(self.db_job)
        self.s.commit()

    def process_item(self, item, spider):
        dbItem = dbs.Item(job=self.db_job)
        self.s.add(dbItem)
        for fieldName in sorted(item.keys()):
            dbField = dbs.Data(
                name = fieldName,
                value = item[fieldName],
                item = dbItem
            )
            self.s.add(dbField)
        self.s.commit()
        return item

    def spider_closed(self, reason):
        self.db_job.timeEnd = datetime.datetime.now()
        finishingReason = self.session.query(dbs.FinishReason).filter(dbs.FinishReason.name==reason)
        if not finishingReason:
            finishingReason = dbs.FinishReason(
                name=reason
            )
            self.s.add(finishingReason)
        self.db_job.finishingReason = finishingReason
        self.s.commit()
        self.s.close()


