#!/usr/bin/env python2.6

from boto.s3.connection import S3Connection

conn = S3Connection()
bucket = conn.get_bucket('js-logs-backup')
for key in bucket.list():
    print key.name.encode('utf-8')
