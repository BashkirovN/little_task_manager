import time
from queue import PriorityQueue

THREADS = 100


def parsetestfile(file):
    testfile = open(file)
    data = testfile.readlines()[1:]
    result = []
    for i in data:
        element = [int(j) for j in i.strip().split(" ")]
        task = Task(element[0], element[1], element[3:])
        task.priority = get_priority(task)
        result.append(task)
    testfile.close()
    return result


def get_priority(task):
    return len(task.prerecs)


def clear_a_prereq(tasks: PriorityQueue, prereq: int):
    result = PriorityQueue()
    while tasks.qsize() > 0:
        task = tasks.get()[1]
        if prereq in task.prerecs:
            task.prerecs.remove(prereq)
            task.priority = get_priority(task)
        result.put((task.priority, task))
    return result


class Manager:

    def __init__(self, tasks, workers):
        self.tasks = PriorityQueue()
        for task in tasks:
            self.tasks.put((task.priority, task))
        self.workers = workers
        self.time = 0

    def assign_task(self, worker):
        # assign the next task from the PQ
        if self.tasks.qsize() > 0:
            task = self.tasks.get()[1]
            if len(task.prerecs) == 0:
                worker.tasks.append(task.id)
                worker.busytime = task.runtime
                worker.idle = False
            else:
                # need to pass more time to clear prerecs
                self.tasks.put((task.priority, task))

    def pass_time(self):
        self.time += 1
        for worker in self.workers:
            worker.pass_time()
            report = worker.report()
            if report is not None:
                self.tasks = clear_a_prereq(self.tasks, report)
            if worker.idle:
                self.assign_task(worker)


class Worker:
    def __init__(self):
        self.idle = True
        self.tasks = []
        self.busytime = 0

    def pass_time(self):
        if self.busytime > 0:
            self.busytime -= 1

    def report(self):
        #   returns the completed task if just done, else = None
        if not self.idle and self.busytime == 0:
            self.idle = True
            return self.tasks[-1]
        return None


class Task:
    def __init__(self, id, runtime, prerecs: []):
        self.id = id
        self.runtime = runtime
        self.prerecs = list(prerecs)
        self.priority = 0

    def __eq__(self, other):
        if isinstance(other, Task):
            return self.id == other.id
        return False

    def __lt__(self, other):
        if isinstance(other, Task):
            return self.id < other.id
        return NotImplemented


print('Starting...')
start_time = time.time()

task_list = parsetestfile('/Users/nikolai/Desktop/startercode/data.txt')
workers = []
for w in range(THREADS):
    workers.append(Worker())

mngr = Manager(task_list, workers)

while mngr.tasks.qsize() > 0:

    mngr.pass_time()

    new_tasks_len = mngr.tasks.qsize()

    # print('time:', mngr.time, ' |  tasks: ', new_tasks_len)


result_list = []
for w in mngr.workers:
    task_ids = [str(t) for t in w.tasks]
    result_list.append(','.join(task_ids) + ';')
result = ''.join(result_list)

output_file_path = '/Users/nikolai/Desktop/startercode/out.txt'
with open(output_file_path, 'w') as output_file:
    output_file.write(result)

print(f"Result written to: {output_file_path}")


end_time = time.time()
elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time} seconds")
