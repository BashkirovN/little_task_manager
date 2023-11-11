# Task Manager

The Little Task Manager takes the number of workers and a task list as input, and outputs a list of tasks for each worker while honoring prerequisites and minimizing the time.

**Note:** This implementation is not particularly efficient but was sufficient for completing a CS61C assignment. Future improvements and explorations may be considered.

## Ideas for Future Enhancements

- Assign task priority using weights applied to task occurrence in prerequisites, required time, task ID, and prerequisites' length.
- Experiment with different weights using random values and choose the combination that yields the best results.

## Input File Format
6   # num tasks. Not parsed, set THREADS = 'this number' manually :)
0 10 0  
1 5 0
2 3 2 0 1   # task id, task duration, num of prerecs, list of prerecs
3 2 1 2
4 10 0
5 5 2 3 4
