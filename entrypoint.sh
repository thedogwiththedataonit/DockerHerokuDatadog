#!/bin/bash

# Grab the Heroku environment variables and inject them into the Datadog Agent configuration
echo "hostname: $HEROKU_APP_DEFAULT_DOMAIN_NAME" >> /etc/datadog-agent/datadog.yaml
echo "tags: [\"app_name:$HEROKU_APP_NAME\", \"version:$HEROKU_RELEASE_VERSION\"]" >> /etc/datadog-agent/datadog.yaml

# Additional Heroku Tags -> HEROKU_RELEASE_CREATED_AT, HEROKU_APP_ID

datadog-agent run &
/opt/datadog-agent/embedded/bin/trace-agent --config=/etc/datadog-agent/datadog.yaml &
/opt/datadog-agent/embedded/bin/process-agent --config=/etc/datadog-agent/datadog.yaml &
python3 application.py



