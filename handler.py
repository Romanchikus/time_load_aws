import json
import time
import aiohttp
import asyncio


def hello(event, context):
    response={}
    try:
        urls = event['website']
    except:
        response = {
            "Error": 'Please choose needed websites'
        }
    else:
        response =asyncio.run(get_time_for_urls(urls))
    
    return response

async def get_time_for_urls(urls):
    
    start = time.time()
    tasks = [asyncio.create_task(
        response_from_site(url)) for url in urls]
    time_from_tasks = await asyncio.wait(tasks)

    return get_time_response(urls, time_from_tasks[0])    

async def response_from_site(url="https://www.youtube.com/"):
    t1 = time.time()
    timeout = aiohttp.ClientTimeout(total=3)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, timeout=timeout) as resp:
                resp.close()
        except aiohttp.client_exceptions.ClientConnectorError as e:
            return getattr(e, 'message', 'Name of the server not known'),url
        except asyncio.TimeoutError as e:
            return getattr(e, 'message', 'Server not available'),url
    return round((time.time()-t1),2),url

    

def get_time_response(url,time_from_tasks):
    dict_of_response= {}
    
    for time_task in time_from_tasks:
        time_response,url = time_task.result()
        dict_of_response[url]=time_response
        
    return dict_of_response