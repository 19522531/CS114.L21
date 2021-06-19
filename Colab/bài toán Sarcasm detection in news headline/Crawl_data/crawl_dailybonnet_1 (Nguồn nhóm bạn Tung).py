from bs4 import BeautifulSoup
import urllib.request
# import csv
import json
#2016
#1754

def crawl_dailybonnet_1():
    count = 0
    url = "https://dailybonnet.com/"
    # with open('dailybonnet_1.csv', 'w', newline='') as csv_file:
    #     writer = csv.writer(csv_file)

    # Mở file json để ghi
    # with open("dailybonnet_1.json", "w") as json_file:
    with open("sarcasm_headlines_dataset.json", "a") as json_file:
        for year in range(2017, 2022):
            for month in range(1, 13):
                if (year == 2021 and month == 7):
                    return
                for page in range(1, 8):
                    # Url có dạng https://dailybonnet.com/[year]/[month]/page/[page]/
                    if page == 1:
                        url_ = url + str(year) + '/' + str(month) + '/'
                    else:
                        url_ = url_ = url + str(year) + '/' + str(month) + '/page/' + str(page) + '/'
                    print(url_)
                    try:

                        # Request
                        html = urllib.request.urlopen(url_)
                        html_=html.read().decode('utf-8')
                        soup = BeautifulSoup(html_, 'html.parser')

                        # Tìm các tag
                        find_div = soup.find_all('h3', class_='entry-title mh-posts-list-title')
                        for x in find_div:
                            try:
                                find_a = x.find('a')

                                # Định dạng dữ liệu ghi vào file json
                                out = {
                                    "article_link": find_a.get('href'),
                                    "headline": find_a.get('title'),
                                    "is_sarcastic": 1
                                }

                                # Ghi vào file
                                count += 1
                                json.dump(out, json_file)
                                json_file.write('\n')
                                # writer.writerow([find_a.get('href'), find_a.get('title'), 1])
                            except:
                                print("*")
                                continue
                    except:
                        print("**")
                        continue
        return count
if __name__ == "__main__":
    crawl_dailybonnet_1()



