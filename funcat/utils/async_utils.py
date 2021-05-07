# -*- coding: utf-8 -*-
import os
from concurrent.futures import ThreadPoolExecutor
import asyncio


async def get_async_response(func, param):
    loop = asyncio.get_running_loop()

    # "None" will use all cores
    threads = ThreadPoolExecutor(max_workers=None)
    # send tasks to each worker
    blocking_tasks = [loop.run_in_executor(threads, func, x) for x in param]
    results = await asyncio.gather(*blocking_tasks)
    results = [x for x in results if x]
    return results


def check_ping(hostname):
    """async def get_async_response使用示例：
    async def main():
        filename = "082_pingHosts.txt"
        hostnames = open(filename).readlines()
        #  print(hostnames)

        result = await get_async_response(check_ping, hostnames)
        return result

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

"""
    response = os.system("ping -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        pingstatus = "Network Active"
    else:
        pingstatus = "Network Error"

    return pingstatus
