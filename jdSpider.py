# coding = utf-8
import string
from bs4 import BeautifulSoup
import re  # 正则匹配
import urllib.request, urllib.error  # 指定URL，获取网页数据
from urllib.parse import quote
import xlwt
import ssl

# 全局取消证书验证（https）
ssl._create_default_https_context = ssl._create_unverified_context


def main():
    keywords = input("请输入关键字：")
    datalist = []
    baseUrl = "https://search.jd.com/Search?keyword=" + keywords + "&page="
    datalist = getData(baseUrl)

    print(datalist)

findImgSrc = re.compile(r'<img.*data-lazy-img="(.*?)"', re.S)
findPrice = re.compile(r'<i>(.*?)</i>', re.S)
findInfo = re.compile(r'<div class="p-name p-name-type-2">(.*?)<em>(.*?)</em>', re.S)
findStore = re.compile(r'<span class="J_im_icon"><a.*?>(.*?)</a>', re.S)



def getUrl(askUrl):
    head = {}
    head[
        "User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    s = quote(askUrl, safe=string.printable)  # urllib.request.urlopen不支持中英文混合的字符串，方法quote的参数safe表示可以忽略的字符
    request = urllib.request.Request(s, headers=head)

    html = ""

    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except Exception as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html


def getData(baseUrl):
    datalist = []
    url = baseUrl + str(1)
    html = getUrl(url)
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all("li", class_="gl-item"):
        data = []
        item = str(item)
        imgSrc = re.findall(findImgSrc, item)[0]
        imgSrc = imgSrc[2:]  # 去掉前面多余的/
        price = re.findall(findPrice, item)[0]
        data.append(imgSrc)
        data.append(price)
        info = re.findall(findInfo, item)[0]
        store = re.findall(findStore, item)[0]
        data.append(store)
        datalist.append(data)

    return datalist



if __name__ == '__main__':
    main()
