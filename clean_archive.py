#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os

from boto.s3.connection import OrdinaryCallingFormat, S3Connection

ARCHIVE = os.environ['ARCHIVE']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']


def main():
    conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
                        calling_format=OrdinaryCallingFormat())
    bucket = conn.get_bucket('melpa.emacs.pe')
    print('Deleting packages from %s... ' % ARCHIVE)
    for key in bucket.list(prefix=ARCHIVE):
        key.delete()


if __name__ == '__main__':
    main()
