import csv
from bs4 import BeautifulSoup
from selenium import webdriver

def get_url(search):
    #Generating a url from the search term
    template='https://www.amazon.in/s?k={}&ref=nb_sb_noss_2'
    #if we have any spaces in search term we are appending it
    search=search.replace(' ','+')
    #adding the search term to the url
    url = template.format(search)
    url += '&page{}'
    return url


def extraction(item):
    #for extracting all the data
    #extracting the anchor tag
    atag=item.h2.a
    #extracting the name of the product, price, reviews,url,ratings
    desc = atag.text.strip()
    url1='https://www.amazon.com'+atag.get('href')
    try:
        price_main=item.find('span','a-price')
        price=price_main.find('span','a-offscreen').text
    except AttributeError:
        return
    try:
        rating = item.i.text
        review_count = item.find('span',{'class':'a-size-base'}).text
    except AttributeError:
        rating=''
        review_count=''
    result = (desc,price,rating,review_count,url1)
    return result

def main(search):
    #starting the webdriver
    driver= webdriver. Chrome(executable_path="D:/WebScraping/chromedriver.exe")
    records=[]
    url = get_url(search)
    for page in range(1,21):
        driver.get(url.format(page))
        soup = BeautifulSoup (driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        for item in results:
            r=extraction(item)
            if r:
                records.append(r)
    driver.close()

    #saving data to csv file
    with open('amazon_results.csv','w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f)
        writer.writerow(['Description','Price','Rating','Review Count'])
        writer.writerows(records)
    
search = input()
main(search)
