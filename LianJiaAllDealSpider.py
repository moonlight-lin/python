# -*- coding:utf-8 -*-
import scrapy
import re
import psycopg2

from scrapy.selector import HtmlXPathSelector

## 1. install scrapy
##    sudo pip install Scrapy

## 2. create project
##    scrapy startproject LianJia

## 3. check project org
##    tree ScrapyLianJia/

## 4. Don't obey robots.txt rules
##      vi ScrapyLianJia/ScrapyLianJia/settings.py
##      ROBOTSTXT_OBEY = False

## 5. add spider
##    vi ScrapyLianJia/ScrapyLianJia/spiders/LianJiaSpider.py

## 6. run
##    cd ScrapyLianJia
##    scrapy crawl lianjia



class LianJiaSpider(scrapy.spiders.Spider):
    name = "lianjia"
    allowed_domains = ["lianjia.com"]
    
    ## 在售
    start_urls_tianhe    = ["https://gz.lianjia.com/chengjiao/tianhe/pg" + str(i) + "ep400"    for i in range(1,96)]
    start_urls_yuexiu    = ["https://gz.lianjia.com/chengjiao/yuexiu/pg" + str(i) + "ep400"    for i in range(1,50)]
    start_urls_liwan     = ["https://gz.lianjia.com/chengjiao/liwan/pg"  + str(i) + "ep400"    for i in range(1,84)]
    start_urls_haizhu    = ["https://gz.lianjia.com/chengjiao/haizhu/pg" + str(i) + "ep200"    for i in range(1,90)]
    start_urls_panyu     = ["https://gz.lianjia.com/chengjiao/panyu/pg"  + str(i) + "ep200"    for i in range(1,98)]
    start_urls_baiyun    = ["https://gz.lianjia.com/chengjiao/baiyun/pg" + str(i) + "ep150"    for i in range(1,86)]
    start_urls_huangpugz = ["https://gz.lianjia.com/chengjiao/huangpugz/pg" + str(i) + "ep400" for i in range(1,50)]
    start_urls_huadou    = ["https://gz.lianjia.com/chengjiao/huadou/pg" + str(i) + "ep400"    for i in range(1,11)]
    
    start_urls_tianhe_2    = ["https://gz.lianjia.com/chengjiao/tianhe/pg" + str(i) + "bp400ep10000"    for i in range(1,35)]
    start_urls_yuexiu_2    = ["https://gz.lianjia.com/chengjiao/yuexiu/pg" + str(i) + "bp400ep10000"    for i in range(1,9)]
    start_urls_liwan_2     = ["https://gz.lianjia.com/chengjiao/liwan/pg"  + str(i) + "bp400ep10000"    for i in range(1,5)]
    start_urls_haizhu_2    = ["https://gz.lianjia.com/chengjiao/haizhu/pg" + str(i) + "bp200ep10000"    for i in range(1,67)]
    start_urls_panyu_2     = ["https://gz.lianjia.com/chengjiao/panyu/pg"  + str(i) + "bp200ep10000"    for i in range(1,40)]
    start_urls_baiyun_2    = ["https://gz.lianjia.com/chengjiao/baiyun/pg" + str(i) + "bp150ep10000"    for i in range(1,80)]
    start_urls_huangpugz_2 = ["https://gz.lianjia.com/chengjiao/huangpugz/pg" + str(i) + "bp400ep10000" for i in range(1,2)]
    
    start_urls = []
    
    start_urls.extend(start_urls_tianhe)
    start_urls.extend(start_urls_yuexiu)
    start_urls.extend(start_urls_liwan)
    start_urls.extend(start_urls_haizhu)
    start_urls.extend(start_urls_panyu)
    start_urls.extend(start_urls_baiyun)
    start_urls.extend(start_urls_huangpugz)
    start_urls.extend(start_urls_huadou)
    
    start_urls.extend(start_urls_tianhe_2)
    start_urls.extend(start_urls_yuexiu_2)
    start_urls.extend(start_urls_liwan_2)
    start_urls.extend(start_urls_haizhu_2)
    start_urls.extend(start_urls_panyu_2)
    start_urls.extend(start_urls_baiyun_2)
    start_urls.extend(start_urls_huangpugz_2)

    def parse(self, response):
        current_url = response.url
        body = response.body
        unicode_body = response.body_as_unicode()

        print "\n\n=============\n" + response.url + "\n================\n\n"

        hxs = HtmlXPathSelector(response)

        if re.match('https://gz.lianjia.com/chengjiao/.*', response.url):
            items = hxs.select('//ul[@class="listContent"]/li')     ## // 查询所有后代, / 查询下一代
            print "Match? Yes\n"
            print "Items: " + str(len(items))
            
            district = "无信息"
            if re.match('.*tianhe.*', response.url):
                district = "天河"
            elif re.match('.*yuexiu.*', response.url):
                district = "越秀"
            elif re.match('.*liwan.*', response.url):
                district = "荔湾"
            elif re.match('.*haizhu.*', response.url):
                district = "海珠"
            elif re.match('.*panyu.*', response.url):
                district = "番禺"
            elif re.match('.*baiyun.*', response.url):
                district = "白云"
            elif re.match('.*huangpugz.*', response.url):
                district = "黄埔"
            elif re.match('.*huadou.*', response.url):
                district = "花都"

            result = []

            for i in range(len(items)):
                #e = items[i].extract()
                #print type(e)
                #print str(i) + " =====\n" + e + "\n"
                
                title = hxs.select('//ul[@class="listContent"]/li['+str(i+1)+']//div[@class="title"]/a/text()').extract()[0].split()
                
                if len(title) < 3:
                    ## 可能是车位, 跳过
                    continue

                address = title[0].strip()
                room = title[1].strip()
                size = title[2].strip()[0:-2]
                
                info = hxs.select('//ul[@class="listContent"]/li['+str(i+1)+']//div[@class="houseInfo"]/text()').extract()[0].split("|")
                direct = info[0].strip()
                
                if len(info) >= 3:
                    lift = info[2].strip()
                else:
                    lift = "无信息"
                
                totalPrice = hxs.select('//ul[@class="listContent"]/li['+str(i+1)+']//div[@class="totalPrice"]/span[@class="number"]/text()')
                if len(totalPrice) != 0:
                    totalPrice = totalPrice.extract()[0]
                else:
                    continue
                    
                dealDate  = hxs.select('//ul[@class="listContent"]/li['+str(i+1)+']//div[@class="dealDate"]/text()').extract()[0][0:-3]
                
                unitPrice = hxs.select('//ul[@class="listContent"]/li['+str(i+1)+']//div[@class="unitPrice"]/span[@class="number"]/text()').extract()[0]
                initPrice = hxs.select('//ul[@class="listContent"]/li['+str(i+1)+']//span[@class="dealCycleTxt"]/span[1]/text()').extract()[0][2:-1]
                
                period = hxs.select('//ul[@class="listContent"]/li['+str(i+1)+']//span[@class="dealCycleTxt"]/span[2]/text()')
                if len(period) != 0:
                    period = period.extract()[0][4:-1]
                else:
                    period = '0'
                
                #print district, address, room, size, totalPrice, unitPrice, initPrice, period, dealDate, direct, lift
                result.append([district, address, room, size, totalPrice, unitPrice, initPrice, period, dealDate, direct, lift])

            try:
                '''
                psql -h localhost -p 5432 -U ed -d db_test

                drop table house_deal;
                truncate house_deal;
                
                CREATE TABLE house_deal (
                    district     CHARACTER VARYING(10),
                    address      CHARACTER VARYING(30),
                    room         CHARACTER VARYING(10),
                    size         NUMERIC(20,5) NOT NULL,
                    totalPrice   NUMERIC(20,5) NOT NULL,
                    unitPrice    NUMERIC(20,5) NOT NULL,
                    initPrice    NUMERIC(20,5) NOT NULL,
                    period       INTEGER,
                    dealDate     CHARACTER VARYING(20),
                    direct       CHARACTER VARYING(10),
                    lift         CHARACTER VARYING(10)
                ) WITH (
                    OIDS=FALSE
                );
                
                select * from house_deal;
                select count(*) from house_deal;
                
                select address as address_2017, count(*) as total, round(avg(totalPrice),2) as avg_total, round(avg(unitPrice),2) as avg_unit, round(avg(period),2) as avg_period, round(avg(size),2) as avg_size 
                       from house_deal where dealDate >= '2017.01' and dealDate <= '2017.12' group by address order by total desc;
                       
                create view deal_2017 as 
                    select address as address_2017, count(*) as total, 
                           round(avg(totalPrice),2) as avg_total, round(avg(unitPrice),2) as avg_unit, round(avg(period),2) as avg_period, round(avg(size),2) as avg_size 
                    from house_deal 
                    where dealDate >= '2017.01' and dealDate <= '2017.12' 
                    group by address 
                    order by total desc;
                                
                select t1.address_2017 as address_2017_2018, 
                       t1.total, t1.avg_total, t1.avg_unit, t1.avg_period, t1.avg_size,
                       t2.total, t2.avg_total, t2.avg_unit, t2.avg_period, t2.avg_size,
                       t1.total - t2.total as diff, cast(cast(t2.total as float)/cast(t1.total as float) as numeric(10,2)) as "18/17",
                       cast((t2.avg_unit - t1.avg_unit)/t1.avg_unit as numeric(10,2)) as diff_unit
                from deal_2017 t1
                join deal_2018 t2 on t1.address_2017 = t2.address_2018
                where t1.total >= 5
                order by diff_unit desc;

                select ROW_NUMBER() over(order by cast((t2.avg_unit - t1.avg_unit)/t1.avg_unit as numeric(10,2)) desc) as id,
                       t1.address_2017 as address_2017_2018, 
                       t1.total, t1.avg_total, t1.avg_unit, t1.avg_period, t1.avg_size,
                       t2.total, t2.avg_total, t2.avg_unit, t2.avg_period, t2.avg_size,
                       t1.total - t2.total as diff, cast(cast(t2.total as float)/cast(t1.total as float) as numeric(10,2)) as "18/17",
                       cast((t2.avg_unit - t1.avg_unit)/t1.avg_unit as numeric(10,2)) as diff_unit
                from deal_2017 t1
                join deal_2018 t2 on t1.address_2017 = t2.address_2018
                where t1.total >= 5;
                
                select ROW_NUMBER() over(order by t2.avg_unit desc) as id,
                       t1.address_2017 as address_2017_2018, 
                       t1.total, t1.avg_total, t1.avg_unit, t1.avg_period, t1.avg_size,
                       t2.total, t2.avg_total, t2.avg_unit, t2.avg_period, t2.avg_size,
                       t1.total - t2.total as diff, cast(cast(t2.total as float)/cast(t1.total as float) as numeric(10,2)) as "18/17",
                       cast((t2.avg_unit - t1.avg_unit)/t1.avg_unit as numeric(10,2)) as diff_unit
                from deal_2017 t1
                join deal_2018 t2 on t1.address_2017 = t2.address_2018
                where t1.total >= 5;
                
                select ROW_NUMBER() over(order by cast((t2.avg_unit - t1.avg_unit)/t1.avg_unit as numeric(10,2)) desc) as id,
                       t1.address_2017 as address_2017_2018, 
                       t1.total, t1.avg_total, t1.avg_unit, t1.avg_period, t1.avg_size,
                       t2.total, t2.avg_total, t2.avg_unit, t2.avg_period, t2.avg_size,
                       t1.total - t2.total as diff, cast(cast(t2.total as float)/cast(t1.total as float) as numeric(10,2)) as "18/17",
                       cast((t2.avg_unit - t1.avg_unit)/t1.avg_unit as numeric(10,2)) as diff_unit
                from 
                    (select address as address_2017, count(*) as total, 
                           round(avg(totalPrice),2) as avg_total, round(avg(unitPrice),2) as avg_unit, round(avg(period),2) as avg_period, round(avg(size),2) as avg_size
                    from house_deal 
                    where dealDate >= '2017.01' and dealDate <= '2017.12' and lift != '无电梯'
                    group by address) t1
                join
                    (select address as address_2018, count(*) as total, 
                           round(avg(totalPrice),2) as avg_total, round(avg(unitPrice),2) as avg_unit, round(avg(period),2) as avg_period, round(avg(size),2) as avg_size
                    from house_deal 
                    where dealDate >= '2018.01' and dealDate <= '2018.12' and lift != '无电梯'
                    group by address) t2
                on t1.address_2017 = t2.address_2018
                where t1.total >= 5;
                       
				select ROW_NUMBER() over(order by cast((t2.avg_unit - t1.avg_unit)/t1.avg_unit as numeric(10,2)) desc) as id,
                       t1.address_2018_01_to_06 as address, 
                       t1.total, t1.avg_total, t1.avg_unit, t1.avg_period, t1.avg_size,
                       t2.total, t2.avg_total, t2.avg_unit, t2.avg_period, t2.avg_size,
                       t1.total - t2.total as diff, cast(cast(t2.total as float)/cast(t1.total as float) as numeric(10,2)) as "18_2/18_1",
                       cast((t2.avg_unit - t1.avg_unit)/t1.avg_unit as numeric(10,2)) as diff_unit
                from 
                    (select address as address_2018_01_to_06, count(*) as total, 
                           round(avg(totalPrice),2) as avg_total, round(avg(unitPrice),2) as avg_unit, round(avg(period),2) as avg_period, round(avg(size),2) as avg_size
                    from house_deal 
                    where dealDate >= '2018.01' and dealDate <= '2018.06' and lift != '无电梯' and size >= 50 and size <= 120
                    group by address) t1
                join
                    (select address as address_2018_07_to_now, count(*) as total, 
                           round(avg(totalPrice),2) as avg_total, round(avg(unitPrice),2) as avg_unit, round(avg(period),2) as avg_period, round(avg(size),2) as avg_size
                    from house_deal 
                    where dealDate >= '2018.07' and lift != '无电梯' and size >= 50 and size <= 120
                    group by address) t2
                on 
                    t1.address_2018_01_to_06 = t2.address_2018_07_to_now
                where 
                    t1.total >= 2 and t2.total >= 2 and t1.total + t2.total >= 5
                order by
                    t2.avg_total;
				
                select * from house_deal where address = '亚运城媒体南村' and dealDate >= '2018.01' order by dealDate desc;
                
                select * from house_deal where address like '丽江%' and dealDate >= '2018.01' order by dealDate desc;
                select address, count(*) from house_deal where address like '丽江%' and dealDate >= '2018.01' group by address;
                select ROW_NUMBER() over(order by count(*)) as id, address, count(*) from house_deal where dealDate >= '2018.01' group by address;
                '''
                
                conn = psycopg2.connect(database = "db_test", \
                                        host = "localhost", \
                                        port = "5432", \
                                        user = "ed", \
                                        password = "123456")
                cur = conn.cursor()

                sql = 'insert into house_deal values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                cur.executemany(sql, result)
                conn.commit()
            except Exception,e:
                print "\n\nERROR:  " + str(e) + "\n\n\n"
                exit(1)
                
    def is_number(self, s):
        try:
            float(s)
            return True
        except:
            pass
        
        try:
            int(s)
            return True
        except:
            pass
     
        return False



