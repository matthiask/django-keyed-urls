#!/bin/sh
coverage run --branch --include="*keyed_urls/*" --omit="*tests*" ./manage.py test testapp
coverage html
