import requests
from bs4 import BeautifulSoup 
import json
import re
baseurl = "https://www.hepsiburada.com/bebelac-gold-3-cocuk-devam-sutu-1250-gr-900-gr-350-gr-1-yasindan-itibaren-p-HBV00000HE7CW"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"}
# HTTP status code 403 Forbidden. The server understood the request, but is refusing to fulfill it. 

def price_scrapper(baseurl,headers):
    respond = requests.get(baseurl,headers=headers)#auth=("kullanicisadi@gmail.com","şifre"))
    result = BeautifulSoup(respond.content,"html.parser")
    #print(respond.status_code) # if it returns 202 so its oke.
    # Current price and product name 
    product_price = result.find_all("span",class_="price")
    product_price = BeautifulSoup(str(product_price).replace("[","").replace("]",""),"html.parser")
    price = product_price.span["content"] 
    product_name = result.title.text
    print(f"Product name is : {product_name}")
    print(f"Product price is : {price}")
    # Other sellers information
    json_objects = result.find_all("script")
    list1 = []
    for json_object in json_objects:
        new_json = BeautifulSoup(str(json_object),"html.parser")
        for json in new_json:
            data = str(json).split(";")
            for element in data:
                match = re.findall(r"[{][^}]*.*[}]",element)
                list1.append(match)
    list2 = []
    for element in list1:
        if element:
            match = element[0].find("merchantName")
            if match!=-1:
                list2.append(element[0])
    list3 = []
    for element in list2:
        new_element = element.split(",")
        list3.append(new_element)
    list4 = []
    for element in list3:
        for element1 in element:
            if element1.find("merchantName")!=-1:
                list4.append(element1)
    list5 = list(set(list4))

    for i in range(0,len(list5)):
        list5[i] = list5[i].replace("\\","")
        list5[i] = "{"+list5[i]+"}"

    list5 = list(set(list5))
    list6 = []
    import json 
    for item in list5:
        list6.append(json.loads(item))
    print("Merchants except the current one are in the below \n")

    for merchant in list6:
        if merchant["merchantName"]: # If its not empty than return it 
            if merchant!=None:
                print(merchant["merchantName"])
                
price_scrapper(baseurl,headers)
