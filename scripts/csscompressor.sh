#!/usr/bin/env bash
tr -d '\n' < static/css/styles.css | tr -d ' ' > static/css/styles.min.css;sed -i 's/\#1c6585/\{\{ main_color \}\}/g' static/css/styles.min.css
