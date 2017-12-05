#!/usr/bin/env python

import sys
import time
import socket
import boto3
import requests

RECORD = 'box'
DOMAIN = 'dot-cloud.de.'


def get_zone(client, domain):
    zones = client.list_hosted_zones()
    for zone in zones['HostedZones']:
        if zone['Name'] == domain:
            return zone
    return None


def get_current_record():
    try:
        return socket.gethostbyname(RECORD + '.' + DOMAIN)
    except:
        return ''


def get_current_ip():
    return requests.get('http://ipinfo.io/ip').text.strip()


def update_record_set(client, zone, ip):
    client = boto3.client('route53')

    res = client.change_resource_record_sets(
            HostedZoneId=zone['Id'],
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': RECORD + '.' + DOMAIN,
                            'Type': 'A',
                            'TTL': 0,
                            'ResourceRecords': [
                                {
                                    'Value': ip
                                    }
                                ]
                            },
                        }
                    ]
                }
            )
    return res


def log(message):
    print time.strftime('%d/%m/%y %H:%M:%S') + ': ' + message


if __name__ == '__main__':
    ip = get_current_ip()
    if ip != get_current_record():
        client = boto3.client('route53')
        zone = get_zone(client, DOMAIN)
        if zone == None:
            log('ERROR: zone is None')
            sys.exit(2)
        update_record_set(client, zone, ip)
        log('record updated. New IP: ' + ip)
