# Healthchecks-Healthchecker

## Problem

I run a local healthchecks.io server to monitor various services to 
determine if they're down. Problem is: Who's watching the watcher?

Enter Healthcheck-Healthchecker.

Healthcheck-Healthchecker pings a local service and asserts the toggle
updates (and that the server responds). If it doesn't it won't notify
healthchecks.io. This should account for:

- Healthchecks service dies completely
- Healthchecks service stops recording pings
- Network connectivity issues

My upstream has been configured to use push notifications to notify 
me in the event of an outage.

## Setup

I'm the sole audience for this script, but if you're interested it
can be executed via BASH:

```bash
HCIO_SLEEP="58" \  # Time between polls
HTTP_USER="admin" \  # HTTP Basic Authentication details
HTTP_PASS="redacted" \  # HTTP Basic Authentication details
LOCAL_URL="https://example.com" \
LOCAL_HC_NAME="hchc" \  # Name of the HC polled
LOCAL_CHECK_GUID="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa" \  # Guid of HC POLLED
LOCAL_API_KEY="aaaaaa-aa-aaaaaaaaaaaaaaaaaaaaaa" \  # Local API auth token
REMOTE_HEALTHCHECK_URL="https://hc-ping.com/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa" \  # Remote service endpoint to poll
python3 hchc.py
```

A docker container also exists and can be run with:

```bash
docker run \
    -e HCIO_SLEEP="58" \
    -e HTTP_USER="admin" \
    -e HTTP_PASS="redacted" \
    -e LOCAL_URL="https://example.com" \
    -e LOCAL_HC_NAME="hchc" \
    -e LOCAL_CHECK_GUID="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa" \
    -e LOCAL_API_KEY="aaaaaa-aa-aaaaaaaaaaaaaaaaaaaaaa" \
    -e REMOTE_HEALTHCHECK_URL="https://hc-ping.com/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa" \
    --rm --name hchc yoloclin/healthchecks-healthchecker
```
