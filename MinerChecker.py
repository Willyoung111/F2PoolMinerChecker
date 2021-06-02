# -*- coding: UTF-8 -*-
import re
from bs4 import BeautifulSoup
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
import pymysql
import time

def has_class_and_data_name(tag):
    return tag.has_attr('class') and tag.has_attr('data-name')


def save_data(minerName, power, conn):
    cursor = conn.cursor()

    # select if data
    date = time.strftime("%Y-%m-%d")
    cursor.execute('SELECT * from powerlog WHERE date = %s AND name = %s', (date, minerName))
    res = cursor.fetchall()
    if not res:
        cursor.execute('INSERT INTO powerlog (date, name, power) VALUES (%s, %s, %s)', (date, minerName, power))
        print("add log date ", date, " mineName:", minerName, " Power:", power)
    else:
        print(minerName ,"has add log today!")
    cursor.close()
    conn.commit()
    conn.close()

def main(urlHead, wallet, conn):
    req = requests.get(url=urlHead+wallet)
    html = req.text
    soup = BeautifulSoup(html, features="html.parser")
    for minerinfo in soup.find_all(has_class_and_data_name):
        minerName = minerinfo["data-name"]
        powerinfo = minerinfo.find('td', class_='hash-24h')
        pattern = re.compile(r'\d*\.\d*')
        power = float(pattern.findall(powerinfo.contents[0])[0])
        save_data(minerName, power, conn)


if __name__ == "__main__":
    # Schedule task


    urlHead = 'https://www.f2pool.com/eth/'
    # wallet = '0x9f8405F3E8997312A0575E61DAD28862cFe65bF5'
    wallet = '0xDb8f6cc0543F9b0f157956Cc72142ca30922949D'
    # main(urlHead, wallet)

    user = input("mysql username:")
    passwd = input("mysql passwd:")
    conn = pymysql.connect(user=user, passwd=passwd, db="MinerLog")
    
    hour = 7
    minute = 55
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'cron', args=[urlHead, wallet, conn], hour=hour, minute=minute)
    print('已启动定时矿工收益查询，每天 %02d:%02d 为您查询记录' % (int(hour), int(minute)))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
