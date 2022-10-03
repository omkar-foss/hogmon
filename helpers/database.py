"""
    Database modules (PostgreSQL).
"""

import traceback
import logging
import psycopg2
from settings import DB_HOST, DB_USER, DB_PASSWORD, \
    DB_PORT, DB_NAME, DB_TABLE_NAME, DB_TABLE_COLS, PERSIST_ALERTS_ENABLED
logging.basicConfig(level=logging.DEBUG)


# pylint: disable=consider-using-f-string
def save_hog_alerts(hog_procs):
    """ Persists the hogging processes alert to the database table. """
    if not PERSIST_ALERTS_ENABLED:
        return False

    dsn = "dbname={} user={} password={} host={} port={}".format(
        DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT,
    )
    try:
        with psycopg2.connect(dsn) as conn:
            with conn.cursor() as curs:
                curs.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS {} (
                        id integer generated always as identity primary key,
                        pid integer not null,
                        process_name varchar(100) not null,
                        command varchar(100) not null,
                        cpu_percent numeric not null,
                        memory_percent numeric not null,
                        cpu_overload_dur_secs integer not null,
                        mem_overload_dur_secs integer not null,
                        created_at timestamp not null
                    )
                    '''.format(DB_TABLE_NAME)
                )
                for proc in hog_procs:
                    query = 'INSERT INTO {} ({}) VALUES '\
                        .format(DB_TABLE_NAME, ','.join(DB_TABLE_COLS)) +\
                        "({}, '{}', '{}', {}, {}, {}, {}, NOW())".format(
                            proc['pid'], proc['name'], proc['command'],
                            proc['cpu_percent'], proc['mem_percent'],
                            proc['num_ticks_cpu'], proc['num_ticks_mem'],
                        )
                    logging.info('Executing Query: %s', query)
                    curs.execute(query)
        return True
    # pylint: disable=bare-except
    except:
        logging.error(
            'Something went wrong while saving the alerts. Traceback: %s',
            traceback.format_exc(),
        )
        return False
