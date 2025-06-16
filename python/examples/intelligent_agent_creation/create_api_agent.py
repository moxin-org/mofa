

from openai import OpenAI
import json
if __name__ == "__main__":
    client = OpenAI(base_url="http://127.0.0.1:8000/v1", api_key="***REMOVED***jsha-1234567890")

    # user_input = """"endpoint": "https://api.ipify.org?format=json","description": "Get the public IP address in IPv4 format.","documentation_url": "https://www.ipify.org/?ref=freepublicapis.com","request_type": "GET","request_parameter": "None","error": false    """
    user_input = """"{"endpoint": "https://randomuser.me/api/","description": "API for generating random user data like names, emails, addresses, and more.","documentation_url": "https://randomuser.me/","request_type": "GET","request_parameter": "None","error": false}"""
    api_datas = [
    {
        "endpoint": "http://ccdb.hemiola.com/characters/radicals/85",
        "description": "This API is designed to help developers manage and respond to 404 errors on their websites. It provides insights into potential causes and offers solutions for correcting broken links and missing files to improve user experience.",
        "documentation_url": "http://ccdb.hemiola.com/?ref=freepublicapis.com",
        "request_type": "GET",
        "request_parameter": "None",
        "error": False
    },
        {
            "endpoint": "https://a.4cdn.org/po/catalog.json",
            "description": "Catalog from Origami",
            "documentation_url": "https://github.com/4chan/4chan-API?ref=freepublicapis.com",
            "request_type": "GET",
            "request_parameter": "",
            "error": False
        },
    {
        "endpoint": "https://a.4cdn.org/3/catalog.json",
        "description": "Catalog from 3D",
        "documentation_url": "https://github.com/4chan/4chan-API?ref=freepublicapis.com",
        "request_type": "GET",
        "request_parameter": "",
        "error": False
    },
    {
        "endpoint": "https://a.4cdn.org/boards.json",
        "description": "Boards",
        "documentation_url": "https://github.com/4chan/4chan-API?ref=freepublicapis.com",
        "request_type": "GET",
        "request_parameter": "",
        "error": False
    },
    {
        "endpoint": "https://abhi-api.vercel.app/api/logo/glitch?text=Abhi+Api",
        "description": "Generate glitch effect text effect logo",
        "documentation_url": "https://abhi-api.vercel.app/api/logo/glitch?text=?ref=freepublicapis.com",
        "request_type": "GET",
        "request_parameter": "text",
        "error": False
    },
    {
        "endpoint": "https://api.apitools.workers.dev/api/ai/chatgpt4?text=hi",
        "description": "ChatGPT 4 Endpoint",
        "documentation_url": "https://api.apitools.workers.dev/?ref=freepublicapis.com",
        "request_type": "GET",
        "request_parameter": "text",
        "error": False
    },
    {
        "endpoint": "https://endpoint.api2.news/",
        "description": "The API2NEWS Endpoint provides access to the latest news stories from various sources, including BBC, TechCrunch, and CNN. Users can retrieve articles by making GET requests to specific endpoints for each publication, including filtering by query parameters for specific articles.",
        "documentation_url": "https://documenter.getpostman.com/view/13902582/2sA3rxrZcC?ref=producthunt?ref=freepublicapis.com",
        "request_type": "GET",
        "request_parameter": "Not specified",
        "error": False
    },
    {
        "endpoint": "https://api.apicagent.com/?ua=Mozilla/5.0%20(Macintosh;%20Intel%20Mac%20OS%20X%2010_15_5)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/89.0.4389.114%20Safari/537.36",
        "description": "Free REST API to detect browser, OS, device from user agent string. Provides easy-to-use API to avoid user-agent parsing libraries.",
        "documentation_url": "https://www.apicagent.com/docs?ref=freepublicapis.com",
        "request_type": "GET",
        "request_parameter": "ua",
        "error": False
    },
    {
        "endpoint": "https://aareguru.existenz.ch/v2018/today?city=bern",
        "description": "Current Temperature in Bern",
        "documentation_url": "https://aareguru.existenz.ch/?ref=freepublicapis.com",
        "request_type": "GET",
        "request_parameter": "city",
        "error": False
    },
    {
        "endpoint": "https://aareguru.existenz.ch/v2018/current?city=bern",
        "description": "All Data for a specific City",
        "documentation_url": "https://aareguru.existenz.ch/?ref=freepublicapis.com",
        "request_type": "GET",
        "request_parameter": "city",
        "error": False
    },
    {
        "endpoint": "https://aareguru.existenz.ch/v2018/widget",
        "description": "All Data for all Cities all at once",
        "documentation_url": "https://aareguru.existenz.ch/?ref=freepublicapis.com",
        "request_type": "GET",
        "request_parameter": "None",
        "error": False
    },
    {
        "endpoint": "https://aareguru.existenz.ch/v2018/cities",
        "description": "List of all Cities in the API",
        "documentation_url": "https://aareguru.existenz.ch/?ref=freepublicapis.com",
        "request_type": "GET",
        "request_parameter": "None",
        "error": False
    },
    {
        "endpoint": "https://musicbrainz.org/ws/2/recording/?query=recording:%22Billie%20Jean%22+AND+artist:%22Michael%20Jackson%22&fmt=json",
        "description": "Find valid MBID (in musicbrainz)",
        "documentation_url": "https://acousticbrainz.org/data?ref=freepublicapis.com",
        "request_type": "GET",
        "request_parameter": "query, fmt",
        "error": False
    },
    {
        "endpoint": "https://acousticbrainz.org/98567252-2622-4e0f-b7bd-6ab93ef2f678/low-level",
        "description": "Find low-level data for this MBID",
        "documentation_url": "https://acousticbrainz.org/data?ref=freepublicapis.com",
        "request_type": "GET",
        "request_parameter": "None",
        "error": False
    },
    {
        "endpoint": "https://acousticbrainz.org/98567252-2622-4e0f-b7bd-6ab93ef2f678/high-level",
        "description": "Find high level data (more detailed)",
        "documentation_url": "https://acousticbrainz.org/data?ref=freepublicapis.com",
        "request_type": "GET",
        "request_parameter": "None",
        "error": False
    }
]
    for data in api_datas:
        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content":' '.join(f'{k}={v}' for k, v in data.items())},
        ],
        )
        print(response)