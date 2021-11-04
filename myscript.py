import argparse
import boto3
import random
import time
from elasticsearch import Elasticsearch
from datetime import datetime
import pytz
from pytz import timezone

LUT_IP_TO_COUNTRY_CODE = {
    "192.0.2.3": 1000,
    "10.0.0.0": 2000,
    "1.2.3.4": 5000,
}

s3 = boto3.client('s3')
es = None

try:
    es = Elasticsearch(["<Enter Elastic Search url>"], http_auth=('<username>','<password>'))
except Exception as e:
    print("An exception occurred while creating ES context")
    print("{}".format(str(e)))

def get_country_from_ip(ipaddress):
    try:
        return LUT_IP_TO_COUNTRY_CODE[ipaddress]
    except Exception as e:
        # unknown IP address, map to random integer
        return random.randint(10000, 50000)

def http_status_class_one_hot_encoding(http_status):
    # returns one hot encoding based on http response status class
    # classes are: 1xx, 2xx, 3xx, 4xx, 5xx
    if 100 <= http_status <= 199: # informational responses
        return (1, 0, 0, 0, 0)
    elif 200 <= http_status < 299: # successful responses
        return (0, 1, 0, 0, 0)
    elif 300 <= http_status < 399: # redirects
        return (0, 0, 1, 0, 0)
    elif 400 <= http_status < 499: # client errors
        return (0, 0, 0, 1, 0)
    elif 500 <= http_status < 599: # server errors
        return (0, 0, 0, 0, 1)

def main():
    try:
        arg_parser = argparse.ArgumentParser()
        sub_arg_parser = arg_parser.add_subparsers(help='Available commands',
                                                   dest='command')
        setup_parser = sub_arg_parser.add_parser('normal', help='generate normal logs')
        clean_parser = sub_arg_parser.add_parser('anomaly', help='generate anomalies')
        args = arg_parser.parse_args()
        if args.command == 'normal':
            MODE = "NORMAL"
        elif args.command == 'anomaly':
            print("Generating anomalies...")
            MODE = "ANOMALY"
        else:
            print("Mode not specified, defaulting to normal")
            MODE = "NORMAL"

        while True:
            timestamp = datetime.now()
            tz = timezone("Australia/Melbourne")
            timestamp = timestamp.astimezone(tz)
            remote_ip = random.choice(list(LUT_IP_TO_COUNTRY_CODE.keys()))
            remote_ip = random.choices(list(LUT_IP_TO_COUNTRY_CODE.keys()), weights=(1000,1000,1000))
            remote_ip = remote_ip[0]
            if MODE == "ANOMALY":
                # Let's go berserk with country codes
                country_code = random.randint(1000, 5000)
                # Some 200 OK with a significant number of other really bad error responses thrown in
                status = random.choices(list([200, 400, 401, 403, 405, 429, 500, 502, 503, 511]))
                status = status[0]
            else:
                # Limit to the list of predefined country codes
                country_code = get_country_from_ip(remote_ip)
                # Mostly 200 OK with occasional 404 Not Found
                status = random.choices(list([200, 404]), weights=(1000,5))
                status = status[0]

            http_1xx, http_2xx, http_3xx, http_4xx, http_5xx = http_status_class_one_hot_encoding(status)

            log_entry = {
                'es_timestamp': timestamp,
                's3_timestamp': timestamp,
                'day_of_week': timestamp.weekday(),
                'hour_of_day': timestamp.hour,
                'remote_ip': remote_ip,
                'country_code': country_code,
                'requester': "79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be",
                'bucket': "somebucket",
                'key': "somekey",
                'operation': "REST.GET.VERSIONING",
                'request_uri': "GET /awsexamplebucket1?versioning HTTP/1.1",
                'status_code': status,
                'http_1xx': http_1xx,
                'http_2xx': http_2xx,
                'http_3xx': http_3xx,
                'http_4xx': http_4xx,
                'http_5xx': http_5xx,
                'error_code': "-",
                'bytes_sent': 113,
                'object_size': 0,
                'user_agent': "S3Console/0.4"
            }
            res = es.index(index="fake-logs-entries", body=log_entry)
            #print(res['result'])
            #print(log_entry['es_timestamp'])

            if MODE == "ANOMALY":
                continue
            else:
                # play with the minute on the clock to generate a temporal pattern
                m = timestamp.time().minute
                m = m % 10
                if m:
                    time.sleep(1/m)
                else:
                    continue
    except Exception as e:
        print(e)
        raise e
        #making changes

while True:
    main()
