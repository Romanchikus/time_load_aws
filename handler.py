import json
import time
import aiohttp
import asyncio


def hello(event, context):
    body={}
    try:
        urls = event['website']
    except:
        body = {
            "Error": 'Please choose needed websites'
        }
    else:
        body =asyncio.run(get_dict_timeurl(urls))
    
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
    

async def site_response(url="https://www.youtube.com/"):
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

async def get_dict_timeurl(urls):
    start = time.time()
    tasks = [asyncio.create_task(
        site_response(url)) for url in urls]
    time_task = await asyncio.wait(tasks)
    dict_of_response = get_time_response(urls, time_task[0])

    return dict_of_response
    

def get_time_response(url,time_task):
    dict_of_response= {}
    for i in time_task:
        time_response,url = i.result()
        dict_of_response[url]=time_response
    return dict_of_response