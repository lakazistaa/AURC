import requests
import json

BASE_URL = ' https://engine.theses-algerie.com/api/as/v1/engines/theses-dz/'
API_SEARCH= 'search.json'
API_DETAILS = 'documents'

url=BASE_URL+API_SEARCH

data = {
  "query": '',
  "facets": {
    "type": {
      "type": "value",
      "size": 100
    },
    "authors": {
      "type": "value",
      "size": 250
    },
    "field": {
      "type": "value",
      "size": 100
    },
    "keywords": {
      "type": "value",
      "size": 100
    },
    "publisher": {
      "type": "value",
      "size": 100
    },
    "language": {
      "type": "value",
      "size": 250
    }
  },
  "filters": {
    "all": [
      {
        "any": [
          {
            "publisher": "Université Hamma Lakhdar - Eloued"
          },
          {
            "publisher": "Université Mohamed Khider - Biskra"
          },
          {
            "publisher": "Université Abdelhamid Ibn Badis - Mostaganem"
          },
          {
            "publisher": "Université Abou Bekr Belkaid - Tlemcen"
          },
          {
            "publisher": "Université Mohamed Boudiaf - M'sila"
          },
          {
            "publisher": "Université Frères Mentouri - Constantine 1"
          },
          {
            "publisher": "Université M'Hamed Bougara - Boumerdes"
          },
          {
            "publisher": "Université des Sciences et de la Technologie Houari-Boumédièn - Alger"
          },
          {
            "publisher": "Université Hassiba Ben Bouali - Chlef"
          },
          {
            "publisher": "Université Benyoucef Benkhedda - Alger 1"
          },
          {
            "publisher": "Université Akli Mohand Oulhadj - Bouira"
          },
          {
            "publisher": "Université Abdelhamid Mehri - Constantine 2"
          },
          {
            "publisher": "Université Ferhat Abbas - Sétif 1"
          },
          {
            "publisher": "Université Abou EL Kacem Saâdallah - Alger 2"
          }
        ]
      },
      
      
    ]
  },
  "search_fields": {
    "title": {},
    "keywords": {},
    "abstract": {},
    "body": {},
    "authors": {}
  },
  "result_fields": {
    "id": {
      "raw": {}
    },
    "type": {
      "raw": {}
    },
    "field": {
      "raw": {}
    },
    "publication_date": {
      "raw": {}
    },
    "publisher": {
      "raw": {}
    },
    "title": {
      "snippet": {
        "size": 175,
        "fallback": True
      }
    },
    "abstract": {
      "snippet": {
        "size": 700,
        "fallback": True
      }
    },
    "body": {
      "snippet": {
        "size": 350,
        "fallback": True
      }
    },
    "keywords": {
      "raw": {}
    },
    "source_details": {
      "raw": {}
    },
    "url": {
      "raw": {}
    },
    "language": {
      "raw": {}
    },
    "authors": {
      "raw": {}
    }
  },
  "page": {
    "size": 10,
    "current": 1
  }
}
params = {"ids[]":1801903693855250}





headers = {
    "Authorization": "Bearer private-vq7y3ap5tkax1r7wouo2xzfm",
    "Content-Type": "application/json"
}







response = requests.post(url,json=data,headers=headers)
#response = requests.get(url,params=params,headers=headers)

if response.status_code == 200:
    print(response)
    results = response.json()
    facets = results.get('results', [])
    
    formatted_results = json.dumps(facets, indent=4, ensure_ascii=True)

    
    # Replace non-ASCII characters with escape codes
    formatted_results = formatted_results.encode('ascii', 'backslashreplace').decode('ascii')
    
    # with open('ff.txt','x') as f :
    #     f.write(formatted_results)
    print(formatted_results)
else:
    print("Request failed with status code:", response.status_code)
    print(response.text)
    


















