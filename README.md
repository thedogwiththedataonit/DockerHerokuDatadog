# Adding Datadog to Docker on Heroku

The Datadog agent requires a explicit hostname value when starting up the agent or there will be a missing token file making the agent unable to send telemetry.

### Option 1 (Recommended) - Heroku Metadata
https://devcenter.heroku.com/articles/dyno-metadata

### Option 2 - hostname_trust_uts_namespace: true
When enabled, the Agent will trust the value retrieved from non-root UTS namespace instead of failing.