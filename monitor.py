#!/usr/bin/env python


from settings import MAX_TICKS_SECS, DUR_TICK_SECS, \
    MAX_CPU_PERCENT, MAX_MEM_PERCENT
from helpers.notifications import send_hogging_email, send_hogging_slack
from helpers.utils import convert_bytes
from helpers.database import save_hog_alerts
import psutil
from collections import defaultdict
import time
import logging
logging.basicConfig(level=logging.DEBUG)


def get_hog_processes(
    max_cpu_pc=MAX_CPU_PERCENT, max_mem_pc=MAX_MEM_PERCENT,
        max_ticks=MAX_TICKS_SECS):

    cpu_exceed_counts = defaultdict(lambda: 0)
    mem_exceed_counts = defaultdict(lambda: 0)
    while True:
        hog_procs = []
        for p in psutil.process_iter():
            with p.oneshot():
                try:
                    proc_pid = p.pid
                    proc_name = p.name()
                    proc_cpu_percent = p.cpu_percent(interval=None)
                    proc_mem_percent = p.memory_percent()
                    proc_mem_used = convert_bytes(p.memory_info().rss)
                    proc_command = ' '.join(p.cmdline())
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
                        'command': '...' + proc_command[-64:] if len(proc_command) > 64 else proc_command,
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
            save_hog_alerts(hog_procs=hog_procs)
        time.sleep(DUR_TICK_SECS)


if __name__ == '__main__':
    get_hog_processes()