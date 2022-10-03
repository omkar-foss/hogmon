# hogmon

A simple monitoring tool to alert about processes hogging CPU and Memory.
Supports emails as well as Slack alerts (via [webhooks](https://api.slack.com/messaging/webhooks)). Also supports persisting the alerts
to a PostgreSQL database.

## Usage

1. Clone this project:

    ```shell
    git clone https://github.com/omkar-foss/hogmon.git
    ```

2. Copy `settings.py.sample` to `settings.py` and configure it as per your needs.
3. To start the monitor, run `python monitor.py`

## Examples


### With STDOUT Logging:
```shell
---------------PID 125 Start---------------
Process Name: brave
CPU Consumed: 60.5%
Memory Consumed: 332.7M (4.23%)
Command: /opt/brave.com/brave/brave --enable-crashpad
CPU Overload Duration: 30 sec
Memory Overload Duration: 10 sec
----------------PID 174870 End----------------
```

### In Slack Notifications:
```shell
I am under heavy load for more than 30 seconds from processes as below:

---------------PID 125 Start---------------
Process Name: brave
CPU Consumed: 60.5%
Memory Consumed: 332.7M (4.23%)
Command: /opt/brave.com/brave/brave --enable-crashpad
CPU Overload Duration: 30 sec
Memory Overload Duration: 10 sec
----------------PID 174870 End----------------
```

### In Email Notifications:
**Subject:** `High Resource Consumption Detected`

```shell
High Consumption Processes as below:

---------------PID 125 Start---------------
Process Name: brave
CPU Consumed: 60.5%
Memory Consumed: 332.7M (4.23%)
Command: /opt/brave.com/brave/brave --enable-crashpad
CPU Overload Duration: 30 sec
Memory Overload Duration: 10 sec
----------------PID 174870 End----------------
```