# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# author : strangestring
# github : https://github.com/strangestring

import asyncio
import logging
# import multiprocessing
import random
import time
import traceback
from multiprocessing import Manager, Pool
import aiohttp
import headers_pool
import workflow_load_balance
import zhihu_APIs


# sys.path.append('./aiofetch')

# default args
PROCESS_NUM = 4
MAX_PROCESS_NUM = 8
FLOOD_DISCHARGE_RATIO = 0.3
FLOODPLAIN_RATIO = 0.1
HEADERS_POOL = headers_pool.HEADERS_POOL

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s   %(levelname)s   %(message)s')


async def _fetch(url: str, identifier: str or int, func: callable,
                 session: aiohttp.ClientSession, headers: dict,
                 **kwargs) -> dict:
    """
    :param url: url to access
    :param identifier: url_token/answer_id, etc.
    :param func: function that return url
    :param session: aiohttp.ClientSession
    :param headers: a random selection of headers
    :param kwargs: might contain 'offset' or 'limit', for raise_error positioning
    :return:
    """
    try:
        async with session.get(url, headers=headers, ssl=False) as resp:
            # verify_ssl is deprecated, use ssl=False instead
            status = resp.status
            if isinstance(func, zhihu_APIs.TextAPI):
                if status == 200:
                    return {'identifier': identifier, 'html': await resp.text()}
                else:
                    logging.warning(
                        f'{func.__init__.__name__}\t{identifier}\n{url} kwargs={kwargs}\nSTATUS CODE:{status}')
                    return {'identifier': identifier, 'html': None,
                            'status_code': status}
            else:
                if status == 200:
                    _json = await resp.json(encoding='utf-8')
                    if 'paging' in _json:  # list类API
                        _json['paging']['identifier'] = identifier
                    else:  # info类API
                        _json['identifier'] = identifier
                else:
                    # todo: record occasional errors and automatic retries
                    # mainly caused by human verification or '500'/'账号已停用'/'账号已注销'/'内容已被删除')
                    # just care about status code, _json is personalized
                    logging.warning(
                        f'{func.__init__.__name__}\t{identifier}\n{url} kwargs={kwargs}\nSTATUS CODE:{status}')
                    _json = {'paging': {'identifier': identifier,
                                        'status_code': status,
                                        'ret_json': await resp.json(
                                            encoding='utf-8')}, 'data': {
                        f'{func.__init__.__name__}\t{identifier} kwargs={kwargs}\tSTATUS CODE:{status}'}}
                    ...
                return _json
    except BaseException:
        logging.error(traceback.format_exc())


async def _gather_result(work_flow: dict, func: callable, headers_pool: list,
                         process_id: int):
    """
    :param work_flow: work flow dict
    :param func: function that return url
    :param headers_pool: headers pool for random selection
    :return: list that contain jsons from _fetch()
    """
    try:
        if 'limit' in func.__init__.__code__.co_varnames:
            func_limit = func.__init__.__defaults__[
                func.__init__.__code__.co_varnames.index(
                    'limit') - 2]  # self, url_token/answer_id is required
        else:
            func_limit = 1
        async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False)) as session:
            task_pool = []
            for task in work_flow['task_pool']:
                identifier = task['identifier']
                if 'query_args' in task:
                    query_args = task['query_args']
                else:
                    query_args = None
                if 'range' in task:  # list类API
                    step = limit = func_limit  # use default values
                    if len(task['range']) == 2:
                        start, end = task['range']
                    elif len(task['range']) == 3:
                        start, end, step = task['range']
                    else:
                        start, end, step, limit = task['range']
                        ...
                    remainder = end % step
                    for offset in range(start, end, step):
                        if offset + step > end:  # needs to be customized
                            offset = end - remainder
                            step = limit = remainder
                            ...
                        url = func(identifier, offset, limit=limit,
                                   query_args=query_args).url
                        task_pool.append(
                            _fetch(url, identifier, func, session,
                                   random.choice(headers_pool),
                                   offset=offset, step=step,
                                   limit=limit))
                        ...
                    ...
                else:  # info类API
                    url = func(identifier, query_args=query_args).url
                    task_pool.append(_fetch(url, identifier, func, session,
                                            random.choice(headers_pool)))
                    ...
                ...
            result = await asyncio.gather(*task_pool,
                                          return_exceptions=True)
            return result
    except BaseException:
        logging.error(traceback.format_exc())


def _sub_process(work_flow: dict, func: callable, headers_pool: list,
                 json_list: list, process_id: int) -> None:
    """

    :param work_flow: work flow dict
    :param func: function that return url
    :param headers_pool: headers pool for random selection
    :param json_list: multiprocessing.Manager.list
    :param process_id:
    :return:
    """
    __new_loop = asyncio.new_event_loop()
    # set 'new_loop' as event_loop for current subprocess
    asyncio.set_event_loop(__new_loop)
    __data = __new_loop.run_until_complete(
        _gather_result(work_flow, func, headers_pool, process_id))
    __new_loop.close()
    if isinstance(__data, list):
        json_list.extend(__data)


def get_data(fetch_body: list, func, process_num: int = 4,
             max_process_num: int = 8, flood_discharge_ratio: float = 0.3,
             floodplain_ratio: float = 0.1,
             headers_pool: list = HEADERS_POOL) -> dict:
    """
    :param fetch_body:
    :param func: function that return url
    :param process_num:
    :param max_process_num:
    :param flood_discharge_ratio:
    :param floodplain_ratio:
    :param headers_pool: headers pool for random selection
    :return:
    """
    return_list = Manager().list()
    pool = Pool(max_process_num)
    task_allocation = workflow_load_balance.load_balance(
        fetch_body,
        func,
        process_num,
        flood_discharge_ratio=flood_discharge_ratio,
        floodplain_ratio=floodplain_ratio)  # 负载均衡和range参数校验
    for process_id in range(process_num):
        if task_allocation[process_id]['task_count'] > 0:
            pool.apply_async(_sub_process,
                             [task_allocation[process_id], func, headers_pool,
                              return_list, process_id])
            ...
        ...
    pool.close()
    pool.join()

    # 合并同identifier的字典中的data
    res_dict = {}
    for each in return_list:
        if not isinstance(each, dict):
            print(each)
            continue
        if 'paging' in each:
            identifier = each['paging']['identifier']
        else:  # info类API
            identifier = each['identifier']
        if identifier in res_dict:
            # info类只返回一个dict,流向else
            # 若同时请求大量info,若请求时未做去重,重复结果将流入此
            if 'data' in res_dict[identifier]:
                if isinstance(each['data'], list):
                    res_dict[identifier]['data'].extend(each['data'])
                else:
                    logging.warning(f'each["data"] is not list{each["data"]}')
            else:  # 重复出现的相同对象的info应该忽略
                pass
        else:
            res_dict[identifier] = each
    '''
    res_dict:
    {
        "zhang-jia-wei":
        {
            "paging":
            {
                "totals": 2243453,
                "identifier": "zhang-jia-wei"
            },
            "data": [
            {
                "url_token": "1999nian-de-xia-tian",
                "id": "51651651",
            }]
        },
        "imike": {balabala}
    }
    '''
    return res_dict


if __name__ == '__main__':
    START = time.perf_counter()

    ZHI = zhihu_APIs.ZhiHu()
    FUNC = ZHI.members.followers

    FETCH_BODY = [{"identifier": 'imike', "query_args": ["following_count"],
                   "range": [0, 10]},
                  {"identifier": 'splitter', "range": [0, 10, 20, 2]}, ]
    RES = get_data(
        FETCH_BODY,
        FUNC,
        process_num=PROCESS_NUM,
        max_process_num=MAX_PROCESS_NUM,
        flood_discharge_ratio=FLOOD_DISCHARGE_RATIO,
        floodplain_ratio=FLOODPLAIN_RATIO,
        headers_pool=HEADERS_POOL)
    # print(RES)
    print(time.perf_counter() - START)
    ...
