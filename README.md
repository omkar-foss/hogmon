# hogmon

A simple monitoring tool to alert about processes hogging CPU and Memory.
Supports emails as well as Slack alerts (via [webhooks](https://api.slack.com/messaging/webhooks)). Also supports persisting the alerts
to a PostgreSQL database.

## Usage

1. Clone this project:

    ```shell
    git clone https://github.com/<username>/hogmon.git
    ```

2. Copy `settings.py.sample` to `settings.py` and configure it as per your needs.
3. To start the monitor, run `python monitor.py`
