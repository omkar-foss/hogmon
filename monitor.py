#!/usr/bin/env python
"""
    Entrypoint for hogmon.
"""


from collections import defaultdict
import time
import logging
import psutil
from helpers.database import save_hog_alerts
from helpers.utils import convert_bytes
from helpers.notifications import format_hogging_procs, send_hogging_email, send_hogging_slack
from settings import MAX_TICKS_SECS, DUR_TICK_SECS, \
    MAX_CPU_PERCENT, MAX_MEM_PERCENT, LOG_TO_STDOUT
logging.basicConfig(level=logging.DEBUG)


def get_hog_processes(
    max_cpu_pc=MAX_CPU_PERCENT, max_mem_pc=MAX_MEM_PERCENT,
        max_ticks=MAX_TICKS_SECS):
    """ Main ticker function that monitors for hogging processes. """

    cpu_exceed_counts = defaultdict(lambda: 0)
    mem_exceed_counts = defaultdict(lambda: 0)
    while True:
        hog_procs = []
        for proc in psutil.process_iter():
            with proc.oneshot():
                try:
                    proc_pid = proc.pid
                    proc_name = proc.name()
                    proc_cpu_percent = proc.cpu_percent(interval=None)
                    proc_mem_percent = proc.memory_percent()
                    proc_mem_used = convert_bytes(proc.memory_info().rss)
                    proc_command = ' '.join(proc.cmdline())

                # pylint: disable=bare-except
                # We're using a bare except here so that the ticker does not
                # fail due to any kind of exceptions whatsoever.
                except:
                    continue

                if proc_cpu_percent > max_cpu_pc:
                    cpu_exceed_counts[proc_pid] += 1

                if proc_mem_percent > max_mem_pc:
                    mem_exceed_counts[proc_pid] += 1

                if any([
                    cpu_exceed_counts[proc_pid] >= max_ticks,
                    mem_exceed_counts[proc_pid] >= max_ticks
                ]):
                    hog_procs.append({
                        'pid': proc_pid,
                        'name': proc_name,
                        'command': '...' + proc_command[-64:]
                        if len(proc_command) > 64 else proc_command,
                        'cpu_percent': proc_cpu_percent,
                        'mem_percent': proc_mem_percent,
                        'mem_used': proc_mem_used,
                        'num_ticks_cpu': cpu_exceed_counts[proc_pid] * DUR_TICK_SECS,
                        'num_ticks_mem': mem_exceed_counts[proc_pid] * DUR_TICK_SECS,
                    })
                    cpu_exceed_counts[proc_pid] = 0
                    mem_exceed_counts[proc_pid] = 0
        if hog_procs:
            is_slack_sent = send_hogging_slack(hog_procs)
            if not is_slack_sent:
                send_hogging_email(hog_procs)
            save_hog_alerts(hog_procs)
            if LOG_TO_STDOUT:
                print(format_hogging_procs(hog_procs))
        time.sleep(DUR_TICK_SECS)


if __name__ == '__main__':
    get_hog_processes()
