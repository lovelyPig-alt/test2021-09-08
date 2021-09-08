from selenium import webdriver
import datetime
import queue
import re
import threading
from openpyxl import Workbook


def generate_url_queue():
    url_queue = queue.Queue()
    with open("url.txt") as f:
        urls = f.readlines()
        for url in urls:
            url_queue.put(url.strip())

    return url_queue

def spider(url_queue):
    # 启动驱动获取url
    driver = webdriver.Chrome(executable_path="../web/chromedriver.exe")
    while not url_queue.empty():
        url  = url_queue.get()
        try:
            driver.get(url)
            stars = driver.find_element_by_id("acrCustomerReviewText").text
            appraise = driver.find_element_by_class_name('a-size-medium.a-color-base').text
            householdRanking = driver.find_element_by_xpath('//*[@id="productDetails_detailBullets_sections1"]/tbody/tr[3]/td/span/span[1]').text
            rangking = driver.find_element_by_xpath('//*[@id="productDetails_detailBullets_sections1"]/tbody/tr[3]/td/span/span[2]').text
            householdRanking1 = int(''.join(re.findall(r".*?(\d+).*?", householdRanking)))
            rangking1 = int(''.join(re.findall(r".*?(\d+).*?", rangking)))
            info  = "{} {} {} {} {}".format(url,stars,appraise,householdRanking1,rangking1)
            print("{}:{}".format(datetime.datetime.now(), householdRanking1))
            print("{}:{}".format(datetime.datetime.now(), rangking1))
            with open("articles.txt", "a+") as f:
                f.write("{} \n".format(info))
        except Exception as e:
            print("{} {}".format(url,e))
    # driver.close()


def main():
    url_queue = generate_url_queue()
    threadin_pool = []

    # 开启的线程数
    thread_number = 2
    for i in range(thread_number):
        thread = threading.Thread(target=spider,args=(url_queue,))
        threadin_pool.append(thread)

    for one in threadin_pool:
        one.start()

    for one in threadin_pool:
        one.join()

    # 新建对象
    wb = Workbook()
    # 激活Sheet
    sheet = wb.active
    # 给表格取名
    sheet.title = "商品评价及排行"
    sheet.append(['url', '星级', '评价星级', '一类排行', '二类排行'])
    sheet.append(())

if __name__ == '__main__':
    main()