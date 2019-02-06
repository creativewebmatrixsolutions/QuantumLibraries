#!/bin/env python
# -*- coding: utf-8 -*-
##
# __init__.py: Logic for launching and configuring Q# clients.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##


import os
import sys
import time
import logging
from distutils.util import strtobool

def _start_client():
    logger = logging.getLogger(__name__)
    import qsharp.clients.iqsharp
    client = qsharp.clients.iqsharp.IQSharpClient()

    # When the module is imported, start the Q# server (unless --skipQSS is specified in the command line):
    if not strtobool(os.getenv("QSHARP_SKIP_CLIENT", "False")):
        client.check_installed()
        client.start()

    # Check if the server is up and running:
    server_ready = False
    for idx_attempt in range(1,20):
        try:
            server_ready = client.is_ready()
            if server_ready:
                break
        except Exception as ex:
            logger.debug('Exception while checking Q# environment.', exc_info=ex)
            if idx_attempt == 1:
                print("Preparing Q# environment...")
            time.sleep(1)
    if not server_ready:
        raise Exception("Q# environment was not available in allocated time.")

    return client
