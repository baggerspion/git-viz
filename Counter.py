#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dateutil.parser
import LogParse, sys

if __name__ == '__main__':
    # Read the log data and sort it
    parser = LogParse.LogParse(sys.argv[1])
    log = parser.get_log()
    log.sort(key=lambda item:item['date'])

    # Parse the dates
    dates = {}
    for commit in log:
        commit['date'] = str(dateutil.parser.parse(commit['date']).date())
        if not commit['date'] in dates:
            dates[commit['date']] = 1
        else:
            dates[commit['date']] += 1

    for date in dates:
        print(date, dates[date])
