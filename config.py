#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
# import sys
# import environ
# from pathlib import Path




def get_root():
    return os.path.dirname(os.path.abspath(__file__))

def tracking_path():
    return os.path.join(get_root(), 'tracking')



