# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# author : strangestring
# github : https://github.com/strangestring


import copy


def load_balance(fetch_body: list, func: callable, work_flow_num: int,
                 flood_discharge_ratio: float = 0.3,
                 floodplain_ratio: float = 0.1) -> list:
    """
    :param fetch_body:
    :param func: function that return url
    :param work_flow_num: process_num
    :param flood_discharge_ratio: the ratio of the single maximum allowable increase to floodplain_size when allowing a little overflow
    :param floodplain_ratio: the percentage of work_flow_capacity when allowing a small overflow of the work_flow task
    :return: {'task_count': task_total_count:int, 'task_pool': [{},{},]}
    """
    # print(func.__defaults__)

    if 'limit' in func.__init__.__code__.co_varnames:
        func_limit = func.__init__.__defaults__[
            func.__init__.__code__.co_varnames.index(
                'limit') - 2]  # self, url_token/answer_id is required
    else:
        func_limit = 1
        ...
    
    # print(func_limit)
    
    task_total_count = 0
    for task in fetch_body:
        if 'range' in task:
            task_range = task['range']
            assert len(
                    task_range) >= 2, f'\n\n\'Range\' must contain \'start\' and \'end\'.'
            step = limit = func_limit
            if len(task_range) == 2:
                pass
            elif len(task_range) == 3:
                step = task_range[2]
            else:
                step, limit = task_range[2:]
                ...
            # 'start' and 'end'
            assert 0 <= task_range[0] < task_range[
                1], f'\n\n\'Start\' and \'end\' must satisfy 0 <= \'start\' < \'end\' in task:\n{task}\n.'
            # 'limit' and 'step'
            assert 0 < limit <= step, f'\n\n\'Limit\' and step must satisfy 0 < \'limit\' <= \'step\' in task:\n{task}\n.'
            span = task_range[1] - task_range[0]
            task_count = span // step * limit + min(limit, span % step)
            # for unexpected occasions
            assert task_count > 0, f'\n\n\'Task_count\' <= 0 in task:\n{task}\nPlease check start,end[,step[,limit]].'
        else:
            task_count = 1
            ...
        task['task_count'] = task_count
        task_total_count += task_count
        ...
    
    if work_flow_num == 1:
        # '_gather_result()' focus on 'task_count'
        return [{'task_count': task_total_count, 'task_pool': fetch_body}]
    
    work_flow_capacity = task_total_count // work_flow_num  # type:float
    work_flow_task_count = [0 for x in range(work_flow_num)]
    work_flows = [{'task_count': 0, 'task_pool': []} for x in
                  range(work_flow_num)]
    
    min_flood_discharge = 1 if floodplain_ratio > 0 else 0
    floodplain_size = max(0,
                          int(min(1., floodplain_ratio) * work_flow_capacity))
    flood_discharge = max(min_flood_discharge,
                          int(min(1., flood_discharge_ratio) * floodplain_size))
    
    pos = 0
    while fetch_body:
        if pos == len(fetch_body) - 1:  # 已遍历1次
            fetch_body = sorted(fetch_body, key=lambda x: x['task_count'],
                                reverse=True)
            pos = 0
            cur_task = fetch_body[0]
        else:
            cur_task = fetch_body[pos]
            ...
        min_work_flow_index = work_flow_task_count.index(
                min(work_flow_task_count))
        min_work_flow = work_flows[min_work_flow_index]
        if (cur_task['task_count'] > 100) and (
                cur_task['task_count'] + work_flow_task_count[
            min_work_flow_index] > work_flow_capacity + floodplain_size):
            # For 'task_count'>100 that exceeds the buffer size
            # when allocated directly
            # Circumvent the case where the 'task_count'+1 of
            # the smallest 'work_flow' will also exceed capacity
            # when 'work_flow_capacity' is not an integer.
            # Divide strictly from front to back by multiples of 'step'
            
            if len(cur_task['range']) == 3:
                step = cur_task['range'][2]
            elif len(cur_task['range']) == 4:
                step = cur_task['range'][2]
            else:
                step = func_limit
                ...
            # calculate task_count
            raw_allocate_task_num = (work_flow_capacity - work_flow_task_count[
                min_work_flow_index] + flood_discharge)
            # flood_discharge == 0 when floodplain_ratio == 0
            allocate_task_num = raw_allocate_task_num - raw_allocate_task_num % step
            
            start, end = cur_task['range'][:2]
            new_end = start + allocate_task_num
            
            new_task = copy.deepcopy(cur_task)
            new_task['task_count'] = allocate_task_num
            cur_task['task_count'] -= allocate_task_num
            
            new_task['range'][1] = new_end
            cur_task['range'][0] += allocate_task_num
            work_flow_task_count[min_work_flow_index] += allocate_task_num
            
            min_work_flow['task_count'] += allocate_task_num
            min_work_flow['task_pool'].append(new_task)
        
        else:  # allocate directly
            min_work_flow['task_count'] += cur_task['task_count']
            min_work_flow['task_pool'].append(copy.deepcopy(cur_task))
            work_flow_task_count[min_work_flow_index] += cur_task['task_count']
            
            cur_task_index = fetch_body.index(cur_task)
            fetch_body.pop(cur_task_index)  # pop'cur_task' whenever
            ...
        ...
    return work_flows


if __name__ == '__main__':
    import zhihu_APIs
    
    
    # performance: 250k in 10s, 500k in 33s
    # if len(fetch_body) is much more than 250k,consider rewrite
    
    # args for unit test
    STEP = 20
    LIMIT = 20
    TASK_COUNT_LIST = [5000 + x for x in range(100000, 0, -1)] + [3, 2, 1]
    
    print(f'len(task_count_list)\t{len(TASK_COUNT_LIST)}')
    FETCH_BODY = [{"identifier": "url_token",
                   "query_args": ["voteup_count", "answer_count",
                                  "article_count"],
                   "range": [0, x, STEP, LIMIT]} for x in TASK_COUNT_LIST]
    
    FUNC = zhihu_APIs.ZhiHu().members.followers
    # print(FUNC)
    # print(FUNC.__init__.__defaults__)
    # print(FUNC.__init__.__code__.co_varnames)
    # print(type(FUNC))
    RES = load_balance(FETCH_BODY, FUNC, 2, flood_discharge_ratio=0.3,
                       floodplain_ratio=0.1)
    
    print(RES)
