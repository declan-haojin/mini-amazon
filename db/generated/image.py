import asyncio
import catapi

def get_random_image_urls(n):
    # Create the event loop where the code executes
    loop = asyncio.new_event_loop()
    # Initialize the api
    api = catapi.CatApi(api_key="live_sdXRJIntQaSKXlZgQ24qAUgL1RHXTcLvRAI0wkJyE8bG2Vvxt7pOWEz5DeLVXuNd")
    def run_coro(coroutine):
        return loop.run_until_complete(coroutine)
    results = run_coro(api.search_images(limit=n))
    ret = []
    for cat in results:
        ret.append(cat.url)
    return ret
