import requests

BASE_URL = ' https://engine.theses-algerie.com'
API_SEARCH= '/api/as/v1/engines/theses-dz/search.json'

url=BASE_URL+API_SEARCH

data={"query":"lorawan"}



{"query":"lorawan",
 "facets":{
           
           "search_fields":
           {
                "title":{},
                "keywords":{},
                "abstract":{},
                "body":{},
                "authors":{}
            },
            
            "sort":
            {
                "publication_date":"desc"
            },
            "page":
            {
                "size":10,"current":84
            }
    }
}


headers = {
    "Authorization": "Bearer search-tcwftsrg9j5xyaqpgtt2oqqk",
    "Content-Type": "application/json"
}







resp = requests.post(url,json=data,headers=headers)


resp_json=resp.json()
print(len(resp_json['results']))
# for r in resp_json['results']:
#     print("="*100)
#     print("Title :",r['title']['raw'])
#     print("Field :",r['field']['raw'])
#     print("Keywords :",r['keywords']['raw'])
#     print("Original_url :",r['original_url']['raw'])
#     print("Publisher :",r['publisher']['raw'])
#     print("Authors :",r['authors']['raw'])
#     print("Type :",r['type']['raw'])
#     print("Language :",r['language']['raw'])
#     print("Abstract :",r['abstract']['raw'])
#     print("Url :",r['url']['raw'])


