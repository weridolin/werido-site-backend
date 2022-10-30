
a1=["10:26","11:55"]
a2=["10:52","11:19"]
a3=["11:08","12:30"]
a4=["11:32","12:08"]


task_list = [a1,a2,a3,a4]

import datetime
def to_seconds(start:str,end:str):
    hour,second = start.split(":")
    start_ = int(hour)*60+int(second)
    hour,second = end.split(":")
    end_ = int(hour)*60+int(second)
    return [start_,end_]

def get_concurrency_time(task_list):
    min_start= min(task_list)[0]
    max_end = max(task_list,key=lambda task:task[1])[1]
    running_task = list()
    running_task.append(task_list[0])
    result=dict() # 每分钟对应的运行的所有任务数量
    for t in range(min_start,max_end):
        for task in task_list:
            if task[0]<=t<=task[1]:
                if task not in running_task:
                    running_task.append(task)
            else:
                if task in running_task:
                    running_task.remove(task)
    
        result.update({t:running_task.copy()})
    print(result)

    # new_result=dict()
    # for k,v in result.items():
    #     if len(v)>1:
    #         if str(v) in new_result:
    #             new_result.update({
    #                 str(v):[new_result[str(v)][0],k]
    #             })
    #         else:
    #             new_result.update({
    #                 str(v):[k,0]
    #             })
    # print(new_result)

task_list = [to_seconds(*t) for t in task_list]

get_concurrency_time(task_list)