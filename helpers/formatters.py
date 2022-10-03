"""
    Formatter functions for this project.
"""

# pylint: disable=consider-using-f-string
def format_proc_details(hog_procs):
    """ Returns a list of hogging processes information. """
    proc_details = []
    for proc in hog_procs:
        proc_details.append(
            "---------------PID {} Start---------------\n".format(proc['pid']) +
            "Process Name: {}\n".format(proc['name']) +
            "CPU Consumed: {}%\n".format(round(proc['cpu_percent'], 2)) +
            "Memory Consumed: {} ({}%)\n".format(
                proc['mem_used'], round(proc['mem_percent'], 2)) +
            "Command: {}\n".format(proc['command']) +
            "CPU Overload Duration: {} sec\n".format(proc['num_ticks_cpu']) +
            "Memory Overload Duration: {} sec\n".format(proc['num_ticks_mem']) +
            "----------------PID {} End----------------\n\n".format(
                proc['pid'])
        )
    return proc_details
