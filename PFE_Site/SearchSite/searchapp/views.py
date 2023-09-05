import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

universities = [
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




def search_view(request):
    if request.method == 'POST':
        query = request.POST.get('query')  # Get the query from the form
        if query:
            BASE_URL = ' https://engine.theses-algerie.com'
            API_SEARCH= '/api/as/v1/engines/theses-dz/search.json'
            url=BASE_URL+API_SEARCH

            current =int(request.POST.get('current')) if request.POST.get('current') else 1
            
            data = {
                "query": query,
                "facets": {
                "type": {
                  "type": "value",
                  "size": 100
                },
                "authors": {
                  "type": "value",
                  "size": 100
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
                  "size": 10
                }
                },
                "filters": {
                "all": [
                  {
                    "any": universities
                  }
                ]
                },
                "search_fields": {
                "title": {},
                "keywords": {},
                "abstract": {},
                "body": {},
                "authors": {},

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
                "current": current
                }
              }
            headers = {
                "Authorization": "Bearer search-tcwftsrg9j5xyaqpgtt2oqqk",
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                resp = response.json()
                
                results = resp.get('results', [])
                meta = resp.get('meta')
                
                return render(request, 'search_results.html', {'results': results,'query':query,'meta':meta})
                
    
    return render(request, 'index.html')
