#!/bin/bash

set +x +e

cf set-health-check demo-bot http
cf push demo-bot
