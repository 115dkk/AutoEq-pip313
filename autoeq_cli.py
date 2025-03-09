#!/usr/bin/env python

"""
AutoEq 명령줄 진입점
"""

import sys
from autoeq.__main__ import batch_processing, cli_args

def entry_point():
    """명령줄에서 실행 시 진입점 함수"""
    args = cli_args()
    batch_processing(**args)

if __name__ == "__main__":
    entry_point() 