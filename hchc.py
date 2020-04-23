import os
import sys
import time
import json
import requests
import logging

logging.basicConfig()
log = logging.getLogger(__file__[:-3])
log.setLevel(logging.INFO)

hcio_sleep = int(os.environ["HCIO_SLEEP"])

http_user = os.environ["HTTP_USER"]
http_pass = os.environ["HTTP_PASS"]

local_healthcheck_guid = os.environ["LOCAL_CHECK_GUID"]
local_api_key = os.environ["LOCAL_API_KEY"]
local_hc_name = os.environ["LOCAL_HC_NAME"]
local_url = os.environ["LOCAL_URL"]
if local_url.endswith("/"):
    local_url = local_url[:-1]

remote_healthcheck_url = os.environ["REMOTE_HEALTHCHECK_URL"]

https_auth = requests.auth.HTTPBasicAuth(http_user, http_pass)

while True:
    try:
        start = time.time()
        requests.get(f"{local_url}/ping/{local_healthcheck_guid}", auth=https_auth)
        r = requests.get(f"{local_url}/api/v1/checks/",
                         headers={"X-Api-Key": local_api_key},
                         auth=https_auth)
    
        data = json.loads(r.content.decode())
        for entry in data["checks"]:
            if entry["name"] != local_hc_name:
                continue
            if entry["status"] == "up":
                log.info("Local service is up. Sending healthchecks.io ping")
                requests.get(remote_healthcheck_url)
            else:
                log.warning("Local service is DOWN, NOT sending remote ping")
        
        end = time.time()
        execution_time = end - start
        
    
        if execution_time < hcio_sleep:
            log.debug(f"Sleeping for {hcio_sleep - execution_time} seconds")
            time.sleep(hcio_sleep - execution_time)
    except Exception as e:
        log.exception("message")
        time.sleep(5)
