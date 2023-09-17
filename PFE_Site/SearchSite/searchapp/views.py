import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse, HttpResponse
import json
import ast
import threading
from pyquery import PyQuery as pq



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
                  },
                  {'any': [{'type': 'Mémoire de Master'}, {'type': 'Thèse de Doctorat'}, {'type': 'Mémoire de Magister'}, {'type': 'Autre'}, {'type': 'Mémoire de Licence'}, {'type': 'Non identifié'}, {'type': 'Rapport de Stage Médical'}, {'type': "Mémoire de Fin d'Étude"}, {'type': "Mémoire d'Ingéniorat"}, {'type': 'Article'}]}
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
            current =int(request.POST.get('current')) if request.POST.get('current') else 1
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



#-------------------------- core --------------------------------------------------#

def url_creator_g1(base_url, query):
    return f"{base_url}?query={query}&submit=Go"
    
def url_creator_g2(base_url,query):
    return f"{base_url}/discover?scope=%2F&query={query}&submit=Go"

def url_creator_g3(base_url,query):
    return f"{base_url}/simple-search?query={query.replace(' ', '+')}"
    
def url_creator_g4(base_url,query):
    return f"{base_url}/cgi/search/simple?q={query}&_action_search=Search&_order=bytitle&basic_srchtype=ALL&_satisfyall=ALL"

site_to_function = {
    "http://biblio.univ-alger.dz/jspui/": url_creator_g1,
    "http://dspace.univ-setif.dz:8888/jspui/": url_creator_g1,
    "https://repository.usthb.dz/": url_creator_g2,
    "http://dspace.univ-msila.dz:8080/xmlui/": url_creator_g2,
    "http://dlibrary.univ-boumerdes.dz:8080/jspui": url_creator_g2,
    "http://depot.umc.edu.dz/": url_creator_g2,
    "http://193.194.83.152:8080/xmlui/": url_creator_g2,
    "http://dspace.univ-chlef.dz:8080/jspui/": url_creator_g2,
    "http://dspace.univ-constantine2.dz/": url_creator_g2,
    "http://e-biblio.univ-mosta.dz/": url_creator_g2,
    "http://dspace.univ-eloued.dz/": url_creator_g3,
    "http://archives.univ-biskra.dz/": url_creator_g3,
    "http://dspace.univ-tlemcen.dz/": url_creator_g3,
    "http://dspace.univ-bouira.dz:8080/jspui/": url_creator_g3,
    "http://thesis.univ-biskra.dz/": url_creator_g4,
}

sites = [
    "http://dspace.univ-eloued.dz/",
    "http://archives.univ-biskra.dz/",
    "http://thesis.univ-biskra.dz/",
    "http://dspace.univ-setif.dz:8888/jspui/",
    "https://repository.usthb.dz/",
    "http://dspace.univ-msila.dz:8080/xmlui/",
    "http://193.194.83.152:8080/xmlui/",
    "http://dspace.univ-tlemcen.dz/",
    "http://depot.umc.edu.dz/",
    "http://dlibrary.univ-boumerdes.dz:8080/jspui",
    "http://dspace.univ-chlef.dz:8080/jspui/",
    "http://biblio.univ-alger.dz/jspui/",
    "http://dspace.univ-bouira.dz:8080/jspui/",
    "http://dspace.univ-constantine2.dz/",
    "http://e-biblio.univ-mosta.dz/"
]

def handler_g1(response, results,university):
    
    doc = pq(response)
    result_list = []
    type = doc('p:contains("collection")').text()
    item_rows = doc('table.miscTable tr:has(td.headers)')
    for item_row in item_rows:
        item_doc = pq(item_row)
        title = item_doc('td.headers').eq(1).text()
        author = item_doc('td.headers').eq(2).text()
        publication_date = item_doc('td.headers').eq(0).text()
        keywords = item_doc('td.headers').eq(3).text()
        abstract = item_doc('td.headers').eq(4).text()  
        result = {
            'title': title,
            'author': author,
            'publication_date': publication_date,
            'keywords': keywords,
            'abstract': abstract,
            'type':type,
            'university':university
        }
        result_list.append(result)

    results.append(result_list) 
    #get all results 
    next_page_link = doc('p:contains("next") a')
    if next_page_link:
        next_page_url = next_page_link.attr('href')
        next_page_response = requests.get(next_page_url)  
        if next_page_response:
            handler_g1(next_page_response, results)

def handler_g2(url, response_text,university):
    # Process the response for group 2 URLs here
    university +=1 
    response_text +=5
    print(f"Handling group 2 response for URL: {url}")
    # Add your processing logic here

def handler_g3(url, response_text):
    # Process the response for group 3 URLs here
    print(f"Handling group 3 response for URL: {url}")
    # Add your processing logic here

def handler_g4(url, response_text):
    # Process the response for group 4 URLs here
    print(f"Handling group 4 response for URL: {url}")
    # Add your processing logic here

site_to_handler = {
    "http://dspace.univ-eloued.dz/": handler_g2,  
    "http://archives.univ-biskra.dz/": handler_g2,  
    "http://thesis.univ-biskra.dz/": handler_g4,  
    "http://dspace.univ-setif.dz:8888/jspui/": handler_g3,  
    "https://repository.usthb.dz/": handler_g1,  
    "http://dspace.univ-msila.dz:8080/xmlui/": handler_g1,  
    "http://193.194.83.152:8080/xmlui/": handler_g1,  
    "http://dspace.univ-tlemcen.dz/": handler_g2,  
    "http://depot.umc.edu.dz/": handler_g1,  
    "http://dlibrary.univ-boumerdes.dz:8080/jspui": handler_g2,  
    "http://dspace.univ-chlef.dz:8080/jspui/": handler_g2,  
    "http://biblio.univ-alger.dz/jspui/": handler_g1,  
    "http://dspace.univ-bouira.dz:8080/jspui/": handler_g2,  
    "http://dspace.univ-constantine2.dz/": handler_g2,  
    "http://e-biblio.univ-mosta.dz/": handler_g1,  
}

def data_collector(url, results):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response_text = response.text

            if url in site_to_handler:
                handler_function = site_to_handler[url]
                handler_function(url, response_text, results)
            else:
                print(f"Aucun handler for this url: {url}")
        else:
            print(f"Request to URL {url} failed with status code {response.status_code}")
    except Exception as e:
        print(f"Error while processing URL {url}: {str(e)}")

def simple_search_requester(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        if query :
            threads = []
            results = {}
            for site in sites :
                url = site_to_function[site](site,query)
                thread = threading.Thread(target=data_collector,args=(url,results))
                thread.start()
                threads.append(thread)
            # wait for all threads to finish
            for thread in threads:
                thread.join()

            return render(request, 'search_results.html', {'results': results,'query':query})

