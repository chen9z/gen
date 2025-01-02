import logging
import uuid
from asyncio import Lock
from concurrent.futures.thread import ThreadPoolExecutor
from dataclasses import dataclass
from inspect import signature
from queue import Queue
from typing import Optional, Any, List, Callable, Dict

from .context import Context
from .state import State

__ERROR__ = "__ERROR__"
__OUTPUT__ = "__OUTPUT__"
__HASH_SPLIT__ = "__HASH_SPLIT__"


@dataclass
class NextTask:
    id: str
    inputs: Optional[dict[str, Any]] = None
    spawn_another: bool = False


@dataclass
class TaskOutput:
    output: Any
    next_task: Optional[List[NextTask]] = None


@dataclass
class Task:
    id: str
    action: Callable[[Context], TaskOutput]


@dataclass
class StreamChunk:
    task_id: str
    value: Any


class Flow:
    def __init__(self, thread_pool_executor: ThreadPoolExecutor, context: Optional[Context] = None):
        self.tasks = {}
        self.active_tasks = set()
        self.context = context or Context()
        self.output_task_ids = set()
        self._executor = thread_pool_executor

        self.active_tasks_lock = Lock()
        self.output_ids_lock = Lock()
        self.logger = logging.getLogger(__name__)

    def add_task(self, name: str, action: Callable[[Context], TaskOutput]):
        self.context.set_state(name, State.empty())
        self.tasks[name] = Task(name, action)
        self.logger.info(f"Added task {name}")

    def run(self, start_task_id: str, inputs: Optional[dict[str, Any]] = None) -> Dict[str, Any]:
        self.logger.info(f"Starting task {start_task_id}")
        task_queue = Queue()
        futures = set()
        self.active_tasks.add(start_task_id)
        task_queue.put(NextTask(start_task_id, inputs))

        if inputs:
            for key, value in inputs.items():
                self.context.set(key, value)

        while True:
            next_task = task_queue.get()
            if next_task.id == __ERROR__:
                for f in futures:
                    f.cancel()

                err = self.context.get(__ERROR__)
                raise Exception(err)

            if next_task.id == __OUTPUT__:
                with self.active_tasks_lock:
                    if len(self.active_tasks) == 0:
                        break
                continue

            action = self.tasks[next_task.id.split(__HASH_SPLIT__)[0]].action
            future = self._executor.submit(self.execute_task, action, next_task, task_queue)
            futures.add(future)

        return {task_id: self.context.get(task_id) for task_id in self.active_tasks}

    def execute_task(self, action: Callable[[Context], TaskOutput], task: NextTask, task_queue: Queue,
                     stream_queue: Optional[Queue] = None):
        self.logger.info(f"Starting Executing task {task.id}")
        try:
            sig = signature(action)
            if "inputs" in sig.parameters:
                result: TaskOutput = action(self.context, inputs=task.inputs)
            else:
                result: TaskOutput = action(self.context)
            context.set(task.id, result.output)
            if stream_queue is not None:
                stream_queue.put(StreamChunk(task.id, result))

            with self.active_tasks_lock:
                self.active_tasks.remove(task.id)
                self.logger.info(f"Completed execution of task {task.id}")

                if not result.next_task or len(result.next_task) == 0:
                    self.logger.info(f"Task {task.id} completed as output node")
                    with self.output_ids_lock:
                        self.output_task_ids.add(task.id)
                        task_queue.put(NextTask(task.id, None))
                else:
                    self.logger.debug(
                        f"Task '{task.id}' scheduling next tasks: {result.next_tasks}"
                    )

                    for next_task in result.next_task:
                        if next_task.id.split(__HASH_SPLIT__)[0] in self.tasks:
                            if next_task.id not in self.active_tasks:
                                self.active_tasks.add(next_task.id)
                                task_queue.put(NextTask(next_task.id, next_task.inputs))
                            elif next_task.spawn_another:
                                self.logger.info(f"Spawning another instance of task '{next_task.id}'")
                                task_id_with_hash = next_task.id + __HASH_SPLIT__ + str(uuid.uuid4())[0:8]
                                self.active_tasks.add(task_id_with_hash)
                                task_queue.put(NextTask(task_id_with_hash, next_task.inputs))
                        else:
                            raise Exception(f"Task {next_task.id} not found")


        except Exception as e:
            import traceback
            self.context.set(__ERROR__, message={"error": str(e), "traceback": traceback.format_exc()})
            with self.active_tasks_lock:
                self.active_tasks.clear()
                task_queue.put(NextTask(__ERROR__, None))

    def stream(self, start_task_id: str, inputs: Optional[Dict[str, Any]] = None):

        task_queue = Queue()
        stream_queue = Queue()
        futures = set()

        self.active_tasks.add(start_task_id)
        task_queue.put(NextTask(start_task_id, inputs))

        if inputs:
            for key, value in inputs.items():
                self.context.set(key, value)

        self.context.set_stream(stream_queue)

        def run_engine():
            while True:
                next_task = task_queue.get()

                if next_task.id == __ERROR__:
                    for f in futures:
                        f.cancel()
                    stream_queue.put(StreamChunk(__ERROR__, None))  # Signal completion
                    break

                if next_task.id == __OUTPUT__:
                    with self.active_tasks_lock:
                        if len(self.active_tasks) == 0:
                            stream_queue.put(StreamChunk(__OUTPUT__, None))  # Signal completion
                            break
                    continue

                action = self.tasks[next_task.id.split(__HASH_SPLIT__)[0]].action

                future = self._executor.submit(
                    self.execute_task, action, next_task, task_queue, stream_queue
                )
                futures.add(future)

        self._executor.submit(run_engine)

        # Yield results from stream queue
        while True:
            stream_chunk: StreamChunk = stream_queue.get()
            if stream_chunk.task_id == __OUTPUT__ or stream_chunk.task_id == __ERROR__:  # Check for completion signal
                break
            yield stream_chunk


    def get_context(self) -> Context:
        return self.context
