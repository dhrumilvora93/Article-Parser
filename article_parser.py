import requests
from bs4 import BeautifulSoup
import csv


def trade_spyder(max_pages):
    header_flag = True
    page = 20170701
    while page <= max_pages:
        url = "http://www.dailymail.co.uk/home/sitemaparchive/day_"+ str(page) +".html"
        source_code =  requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text,'html.parser')
        # print(soup.prettify())
        for link in soup.find_all('a'):
            add= link.get('href')

            if add is not None and "index.html" not in add:
                if "http://www.dailymail.co.uk" not in str(add):
                    news_url = "http://www.dailymail.co.uk" + add

                else:
                    news_url = add
            print("URL: "+news_url)
            get_single_item_data(news_url,header_flag)
            header_flag = False
        page += 1


def get_single_item_data(item_url,header_flag):
    news_author = ""
    news_desc = ""
    news_title = ""
    date_pub = ""
    date_up = ""
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')

    for link in soup.find_all('h1'):
        news_title = link.string
        print('Title: ' + news_title)

    for link in soup.find_all('a',{'class':'author'}):
        if len(news_author) > 1:
            news_author += "," + link.string
        else:
            news_author = link.string
        #write(item_url,news_title,news_author,header_flag)

    if len(news_author) > 1:
        print('Author: ' + news_author)

    for link in soup.find_all('p', {'class': 'byline-section'}):
        for link_in in link.find_all('span',{'class': 'article-timestamp article-timestamp-published'}):
            date_pub = link_in.contents[2]
            date_pub = date_pub.strip(' \t\n\r')
            print("Published: "+date_pub)

    for link in soup.find_all('p', {'class': 'byline-section'}):
        for link_in in link.find_all('span',{'class': 'article-timestamp article-timestamp-updated'}):
            date_up = link_in.contents[2]
            date_up = date_pub.strip(' \t\n\r')
            print("Updated: "+date_up)

    for link in soup.find_all('div', {'itemprop': 'articleBody'}):
        # if link is not None:
            for link_in in link.find_all('p',{'class': 'mol-para-with-font'}):
                if link_in.string is not None:

                    news_desc += "\n"+str(link_in.string).strip()

    if len(news_desc) > 1:
        print("Description: "+news_desc)

    write(item_url, news_title, news_author, date_pub, date_up, news_desc,header_flag)

def write(news_url, news_title, news_author, date_pub, date_up, news_desc,header_flag):
    with open('names.csv', 'a+') as csvfile:
        fieldnames = ['news_url','news_title','news_author','date_pub','date_up','news_desc']
        data_list = {'news_url': news_url,'news_title': news_title,'news_author': news_author,'date_pub': date_pub,'date_up': date_up,'news_desc': news_desc}
        #data_list = [str(news_url),str(news_title),str(news_author),str(date_pub),str(date_up),str(news_desc)]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if header_flag is True:
            writer.writeheader()
        if '' not in data_list.values():
            print(data_list.values())

            writer.writerow(data_list.values())
            print('Written')
            header_flag = False





"""
def init_for_xls():
    row = 1
    workbook = xlsxwriter.Workbook('Articles.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': 1})
    worksheet.write('A1', 'News URL', bold)
    worksheet.write('B1', 'News Title', bold)
    worksheet.write('C1', 'News Author', bold)
    worksheet.write('D1', 'Published Date', bold)
    worksheet.write('E1', 'Description', bold)
    return row

def write(news_url, news_title, news_author, date_pub, date_up, news_desc):
    row = init_for_xls()
    # actual write function
    worksheet.write_url(row, column, news_url)
    worksheet.write(row, column + 1, news_title)
    worksheet.write(row, column + 2, news_author)
    worksheet.write(row, column + 3, date_pub)
    worksheet.write(row, column + 4, news_desc)
    row += 1
    column = 0
"""
# Main
# Range of Pages to be extracted
trade_spyder(20170701)
