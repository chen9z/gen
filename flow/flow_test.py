
from concurrent.futures import ThreadPoolExecutor

from flow.context import Context
from flow.flow import Flow, TaskOutput, NextTask

flow = Flow(thread_pool_executor=ThreadPoolExecutor(max_workers=4))


def task1(context: Context) -> TaskOutput:
    return TaskOutput(output="result1", next_task=[NextTask("task2")])


def task2(context: Context) -> TaskOutput:
    result1 = context.get("task1")
    return TaskOutput(output="result2")


flow.add_task("task1", task1)
flow.add_task("task2", task2)

result = flow.run("task1")
print(result)
