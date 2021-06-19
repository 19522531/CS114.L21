from bs4 import BeautifulSoup
import urllib.request
# import csv
import json

#2018 8400

dic = {
    "uknews": [2000, 10],
    "worldnews": [1000, 10]
}

ls = list(dic.keys())

def crawl_thesuncouk():
    count = 0
    url = 'https://www.thesun.co.uk/news/'
    # with open("thesuncouk_0.csv", "w", newline='') as csv_file:
    #     writer = csv.writer(csv_file)

    # Mở file json để ghi
    # with open("thesuncouk_0.json", "w") as json_file:
    with open("sarcasm_headlines_dataset.json", "a") as json_file:
        for type in ls:
            for page in range(2, dic[type][0], dic[type][1]):

                #Url có dạng https://www.thesun.co.uk/news/[type]/page/[page]/
                url_ = url + type + '/page/'+ str(page) + '/'
                print(url_)
                try:

                    # Request và Fix lỗi HTTPError
                    req = urllib.request.Request(url_, headers={'User-Agent': 'Mozilla/5.0'})
                    html = urllib.request.urlopen(req)
                    html_ = html.read().decode('utf-8')
                    soup = BeautifulSoup(html_, 'html.parser')

                    # Tìm các tag
                    find_a = soup.find_all('a', class_='text-anchor-wrap')
                    for find in find_a:
                        try:

                            # Định dạng dữ liệu ghi vào file json
                            out = {
                                "article_link": find.get('href'),
                                "headline": (find.find('p', class_='teaser__subdeck').get_text()).strip("\n\t"),
                                "is_sarcastic": 0
                            }

                            # Ghi vào file
                            json.dump(out, json_file)
                            json_file.write('\n')
                            count += 1

                        # writer.writerow([find.get('href'), (find.find('p', class_='teaser__subdeck').get_text()).strip("\n\t"), 0])
                        except:
                            print("*")
                        continue
                except:
                    print("**")
                    continue
        return count

if __name__=="__main__":
    crawl_thesuncouk()