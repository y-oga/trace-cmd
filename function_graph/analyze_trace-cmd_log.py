# Tool to analyze a trace-cmd file (function_graph)
# Display duration of each functions and sort these durations
# Usage: python .\kernelshark_analyze.py trace.dat

import sys
import queue

def main():
    trace_data = sys.argv[1]
    trace_lines = []
    all_list = []
    func_q = queue.LifoQueue()

    try:
        with open(trace_data, 'r') as f:
            trace_lines = f.readlines()
    except Exception as e:
        print(e)
        return 1

    for line in trace_lines:
        func_name = 'none'
        duration = -1

        check_str = line[0:3]
        if check_str == 'cpu' or check_str == 'CPU':
            continue
        
        word_list = line.split('|')

        tmp = word_list[0].split()
        if len(tmp) == 6:
            duration = float(tmp[4])
        elif len(tmp) == 7:
            duration = float(tmp[5])

        func_list = word_list[1].split()
        if len(func_list) == 1:
            if func_list[0] == '}':
                func_name = func_q.get()

                data = [duration, func_name]
                all_list.append(data)
            else:
                func_name = func_list[0][:(len(func_list[0]) - 1)]

                data = [duration, func_name]
                all_list.append(data)
        elif len(func_list) == 2:
            func_name = func_list[0]
            func_q.put(func_name)

    all_list.sort()
    for l in all_list:
        print(l[0], l[1])

    return 0

if __name__ == '__main__':
    sys.exit(main())