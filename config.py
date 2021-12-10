#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "9ca5a737-bf42-4941-8e38-43787f301602")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "^#md=TrdFiYGj-TRoFMxkEJNyv?_v2fJ")
