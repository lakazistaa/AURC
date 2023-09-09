import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse, HttpResponse
import json
import ast

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


BASE_URL = ' https://engine.theses-algerie.com/api/as/v1/engines/theses-dz/'
API_SEARCH= 'search.json'
API_DETAILS='documents'
SEARCH_TOKEN = "Bearer search-tcwftsrg9j5xyaqpgtt2oqqk"
DETAILS_TOKEN = "Bearer private-vq7y3ap5tkax1r7wouo2xzfm"



def search_view(request):
    if request.method == 'POST':
        query = request.POST.get('query')  # Get the query from the form
        if query:
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
                "Authorization": SEARCH_TOKEN,
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                resp = response.json()                
                results = resp.get('results', [])
                meta = resp.get('meta')               
                return render(request, 'search_results.html', {'results': results,'query':query,'meta':meta,'full_data':data})
                
    
    return render(request, 'index.html')

def about(request):
    return render(request,'about.html')

def stores(request):
    return render(request,'stores.html')

def ressources(request):
    return render(request,'ressources.html')

def advanced_search_view(request):
    # Initialize variables
    search_fields = []
    from_year = None
    to_year = None
    authors_list = []  
    keywords_list = [] 

    years_filter = {}
    specialities_filter = {}
    universities_filter = {}
    types_filter = {}
    langue_filter = {}
    search_fieldss={}
    query = []
    if request.method == 'POST':
        # Extract form data
        title = request.POST.get('title')
        authors = request.POST.get('authors')
        keywords = request.POST.get('keywords')

        # Check if fields are filled and add them to search_fields
        if title:
            search_fields.append('title')
            query.append(f'{title}')
        if authors:
            search_fields.append('authors')
            authors_list = [author.strip() for author in authors.split(';') if author.strip()]
            query.append(' OR '.join([f'"{author}"' for author in authors_list]))
        if keywords:
            search_fields.append('keywords')
            keywords_list = [keyword.strip() for keyword in keywords.split(';') if keyword.strip()]
            query.append(' OR '.join([f'"{keyword}"' for keyword in keywords_list]))

        
        # Get values of other fields
        depots_universite = request.POST.getlist('depots_universite[]')
        specialite = request.POST.getlist('specialite[]')
        type = request.POST.getlist('type[]')
        langue = request.POST.getlist('langue[]')

        # Get values for the year fields
        from_year = request.POST.get('from')
        to_year = request.POST.get('to')
       #########################################################################################
        if from_year or to_year:
            years_filter["all"] = [{"publication_date": {"from": int(from_year), "to": int(to_year)}}]

        if specialite:
            specialities_filter["any"] = [{"field": s} for s in specialite]

        
        if depots_universite:
            universities_filter["any"] = [universities[int(index) - 1] for index in depots_universite]
        elif universities:
            universities_filter["any"] = universities

        if type:
            types_filter["any"] = [{"type": t} for t in type]

        if langue:
            langue_filter["any"] = [{"language": l} for l in langue]

        for field in search_fields:
            search_fieldss[field] = {}

        combined_query = ' AND '.join(query)
        #######################################################################################
        url = BASE_URL + API_SEARCH
        data = {
            "query": combined_query,
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
              years_filter,
              universities_filter,
              types_filter,
              langue_filter,
              specialities_filter,

            ]
            },
            "search_fields": search_fieldss,
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
        headers = {
            "Authorization": SEARCH_TOKEN,
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            resp = response.json()               
            results = resp.get('results', [])
            meta = resp.get('meta')               
            return render(request, 'search_results.html', {'results': results,'query':combined_query,'meta':meta,"full_data":data})

        else:
            print("Request failed with status code:", response.status_code)
            print(response.text)
      
    return render(request,'advanced_search.html')

def more_details(request):
    id = request.GET.get('id')
    url = BASE_URL + API_DETAILS
    headers={
        "Authorization": DETAILS_TOKEN,
        "Content-Type": "application/json"
    }
    params = {"ids[]": id}

    try:
        response = requests.get(url, params=params,headers=headers)

        if response.status_code == 200:
            data = response.json()
            return JsonResponse({'details': data})

        else:
            # Handle other status codes as needed
            return HttpResponse("Failed to fetch data: {}".format(response.status_code), status=response.status_code)

    except requests.exceptions.RequestException as e:
        # Handle connection errors or exceptions
        return HttpResponse("Request failed: {}".format(str(e)), status=500)
    

def pagination_view(request):
    if request.method == 'POST':
        full_data = request.POST.get('full_data')
        print(type(full_data))
        if full_data :
            url=BASE_URL+API_SEARCH
            current =int(request.POST.get('current'))
            print(current)
            full_data = ast.literal_eval(full_data) 
            full_data['page']['current'] = current
            headers = {
                "Authorization": SEARCH_TOKEN,
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=full_data, headers=headers)
            
            if response.status_code == 200:
                resp = response.json()                
                results = resp.get('results', [])
                meta = resp.get('meta')               
                return render(request, 'search_results.html', {'results': results,'query':full_data['query'],'meta':meta,'full_data':full_data})
            else:
              print("Request failed with status code:", response.status_code)
              print(response.text)
        