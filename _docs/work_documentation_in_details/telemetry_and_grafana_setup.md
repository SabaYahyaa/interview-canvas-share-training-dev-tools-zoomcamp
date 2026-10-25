# 📊 Production Observability, Grafana Cloud & Incident Response Setup

This guide documents how to instrument the FastAPI production service
([interview-canvas-prod](https://interview-canvas-prod.onrender.com)) with OpenTelemetry, send telemetry to
Grafana Cloud, build 9 dashboard panels, enable log-to-trace
correlation, and configure alert notifications to both email and the
Incident Responder webhook. The final Grafana dashboard is show below:

![grafana dashboard](./assets/grafana_dashboard.png)

> **Before you begin:** You need access to the Grafana Cloud stack and
> the Render production service. Keep API tokens and other credentials
> secret. Do not commit them to this repository. Replace any example
> values and placeholders with the values for your own Grafana Cloud
> stack.

## Step 1: Create a Grafana Cloud account and configure OTLP authentication

### 1.1 Create or open your Grafana Cloud stack

1.  Go to [Grafana Cloud](https://grafana.com/products/cloud/) and sign
    up (create a free account) or log in.
2.  Create a stack, or open your existing stack (e.g., whitecantaloupe3594).
3.  Note your stack URL, for example `https://<your-stack>.grafana.net`.

### 1.2 Retrieve OpenTelemetry credentials

1.  In Grafana Cloud, navigate to **Connections → Add new connection →
    OpenTelemetry (OTLP)**. The exact menu wording may change.
2.  Find the numeric instance ID / user value (e.g., 1023456) for your stack.
3.  Generate or retrieve the appropriate API token / service account
    token for sending telemetry, go to https://grafana.com/orgs/ -> stack instance (e.g., whitecantaloupe3594) -> find OpenTelemetry -> click Configuration -> get the ID and create a token.

Treat the token as a secret. Do not paste a real token into this file or
into source control.

### 1.3 Configure environment variables in Render

In the Render Dashboard, open the production web service (for example,
`interview-canvas-app`) and configure these environment variables:

  -----------------------------------------------------------------------------------------------
  Variable                            Value
  ----------------------------------- -----------------------------------------------------------
  `OTEL_EXPORTER_OTLP_ENDPOINT`       `https://otlp-gateway-prod-us-central-0.grafana.net/otlp`
                                      or the OTLP gateway endpoint for your Grafana Cloud region

  `OTEL_EXPORTER_OTLP_HEADERS_USER`   Your Grafana Cloud instance ID / user

  `OTEL_EXPORTER_OTLP_HEADERS_KEY`    Your Grafana Cloud API token

  `OTEL_SERVICE_NAME`                 `interview-canvas-backend-prod`
  -----------------------------------------------------------------------------------------------

Use the endpoint and credentials provided for your own Grafana Cloud
stack. The example endpoint above is regional and may not match your
stack.

## Step 2: Configure OpenTelemetry instrumentation

The project's telemetry setup is in `app/telemetry.py`. It configures
OTLP exporters for traces, metrics, and logs, and attaches trace context
(`trace_id` and `span_id`) to log records so that logs can be correlated
with traces.

The following illustrates the configuration pattern. Keep it aligned
with the implementation and dependency versions in your repository.



**Important implementation checks**

The project's OpenTelemetry instrumentation is implemented in [telemetry.py](/backend/app/telemetry.py).

This module configures telemetry export to Grafana Cloud for:

Traces: Track requests as they pass through the application.

Metrics: Monitor request rates, latency, and HTTP status codes.

Logs: Collect application logs and include trace context to help correlate logs with traces.

Implementation checks

Confirm that setup_telemetry() is called during application startup.

Configure the required Grafana Cloud environment variables in Render, as described in Step 1.

Verify that telemetry is successfully exported to Grafana Cloud.

Check that the OpenTelemetry dependencies in the project support the implementation.

## Step 3: Production Grafana dashboard

The production dashboard is named **Observability FastAPI interview-canvas-prod**.
It brings together request metrics, traces, and logs for
`interview-canvas-backend-prod`.

The dashboard screenshot shows these panels:

| Panel | Purpose | Visualization / data source |
|---|---|---|
| **Total Request Rate** | Shows request throughput over time | Stat with sparkline / Prometheus |
| **Total Requests Count** | Shows the total request count over the selected time range | Stat with sparkline / Prometheus |
| **Active HTTP Requests** | Shows requests currently in progress | Stat / Prometheus |
| **95th Percentile HTTP Request Duration (Last 5 Minutes)** | Shows p95 request latency | Time series / Prometheus |
| **Average request latency (Last 5 Minutes)** | Shows average request latency | Time series / Prometheus |
| **Request Traces** | Lists recent traces, including start time, service, operation, and duration | Traces / Tempo |
| **Logs Data** | Displays production application logs | Logs / Loki |
| **Percentage of 2xx Requests (Success Rate) - Last 5m** | Shows the success rate for HTTP 2xx responses | Time series / Prometheus |
| **Error Percentage (4xx / 5xx) Requests - Last 5m** | Shows the percentage of 4xx and 5xx responses | Time series / Prometheus |

### Graphs queries

These are example queries for the relevant panels. Keep the queries in
your Grafana dashboard aligned with the actual metric names and labels
exported by the application.

**Request Rate**

```promql
sum(rate(http_server_duration_milliseconds_count{service_name="interview-canvas-backend-prod"}[5m]))
```
**Total Request Count**

```promql
sum(http_server_duration_milliseconds_count{service_name="interview-canvas-backend-prod"})
```

**Active HTTP Requests**

```promql
sum(server_active_requests{
  service_name="interview-canvas-backend-prod"
})
```


It uses the in-progress request metric emitted
by the instrumentation. The exact metric name depends on the FastAPI /
OpenTelemetry instrumentation version, so use the query already
configured in your dashboard rather than assuming a metric nam


**95th Percentile HTTP Request Duration (Last 5 Minutes)**

```promql
histogram_quantile(0.95, sum(rate(http_server_duration_milliseconds_bucket{service_name="interview-canvas-backend-prod"}[5m])) by (le))
```

This estimates the 95th-percentile request duration from histogram
buckets. It requires the matching histogram bucket metric to exist.

**Average request latency (Last 5 Minutes)**

```promql
sum(rate(http_server_duration_milliseconds_sum{service_name="interview-canvas-backend-prod"}[5m]))
/
sum(rate(http_server_duration_milliseconds_count{service_name="interview-canvas-backend-prod"}[5m]))
```

This query assumes the corresponding `_sum` and `_count` metrics are
exported. Confirm the metric names in your Prometheus data source.


**Error percentage (4xx and 5xx)**

```promql
(
  sum(rate(http_server_duration_milliseconds_count{
    service_name="interview-canvas-backend-prod",
    http_status_code=~"4..|5.."
  }[5m]))
  /
  sum(rate(http_server_duration_milliseconds_count{
    service_name="interview-canvas-backend-prod"
  }[5m]))
) * 100
```

**Success percentage (2xx)**

```promql
(
  sum(rate(http_server_duration_milliseconds_count{
    service_name="interview-canvas-backend-prod",
    http_status_code=~"2.."
  }[5m]))
  /
  sum(rate(http_server_duration_milliseconds_count{
    service_name="interview-canvas-backend-prod"
  }[5m]))
) * 100
```

The success and error queries assume the status-code label is named
`http_status_code`. Metric names and labels can vary with instrumentation
versions, so check the actual exported series before changing a working
dashboard query.

**Logs Data**

```promql
{service_name="interview-canvas-backend-prod"} | logfmt
```
Panel uses Loki to inspect application logs. The exact
TraceQL and LogQL expressions should match the labels and log format in
your Grafana Cloud stack.

**Request Traces**
```promql
{ resource.service.name = "interview-canvas-backend-prod" }
```
Panel uses Tempo to inspect trace timelines.

### Dashboard data check

In the supplied screenshot, request count and traces/logs are visible,
but some metric panels show **No data** or appear empty. Before treating
the dashboard as fully verified, check each panel's query, selected data
source, time range, metric name, and label names. A panel can show no
data even when traces and logs are arriving successfully.

## Step 4: Enable log-to-trace correlation with Loki Derived Fields

Derived Fields allow you to open a related Tempo trace directly from a
log entry in Loki.

1.  In Grafana Cloud, open **Connections → Data sources**.
2.  Select the Loki data source.
3.  Find **Derived fields** and select **Add derived field**.
4.  Configure the field:

  Setting              Value
  -------------------- ---------------------------
  Name                 `TraceID`
  Regex                `"?trace_id"?[:=]"?(\w+)`
  Internal link        Enabled
  Target data source   Your Tempo data source

5.  Save the data source configuration.
6.  Open a log entry containing a `trace_id` value and check that the
    derived field link opens the matching trace in Tempo.

The regex must match the actual format of the trace ID in your logs. If
the link does not appear or opens the wrong trace, inspect a real log
entry and adjust the regex and target data source configuration.

## Step 5: Configure dual-routing alert notifications

Grafana is configured to send alert notifications to two destinations:
(1) the developer's email address and (2) the Render production application
through its `/alerts` webhook. This is a dual-destination notification flow.

### 5.1 Create contact points

In Grafana Cloud, navigate to **Alerts & IRM → Alerting → Notification configuration  → Add new Contact point**.

**Contact Point A --- Developer Email**

-   **Integration:** Email
-   **Address:** Your intended alert-recipient email address
-   **Purpose:** Receive notifications when an alert fires or changes
    state.

**Contact Point B --- Render Webhook**

-   **Integration:** Webhook
-   **URL:** `https://interview-canvas-prod.onrender.com/alerts`
-   **HTTP method:** `POST`

The webhook URL assumes the production service and `/alerts` route are
available. Confirm that this endpoint accepts Grafana's webhook payload
format.

### 5.2 Create the production server-error alert rule

1.  Navigate to **Alerts & IRM → Alerting → Alert rules** and create New alert rule for example production-alerts.
2.  Create a rule in the evaluation group `production-alerts`.
3.  Configure the query and condition:

3.1 Enter alert rule name: Prod-interviewer-canvas-app
3.2 Define query and alert condition:
Prometheus DataSource and PromQL:

``` promql
(
  rate(http_requests_total{service_name="interview-canvas-prod", status=~"^[45].*"}[5m]) > 0
)
or
(
  histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{service_name="interview-canvas-prod"}[5m])) by (le)) > 0.099
)
```
This condition fires when either the rate of HTTP 4xx or 5xx responses is greater than zero over the
  last 5 minutes or the 99th-percentile HTTP request duration exceeds 99 milliseconds
  over the last 5 minutes.

3.3 Add folder and labels:
Folder: production_alerts
Labels: add the following labels: environment=production, severity=critical, service_name=interview-canvas-prod

3.4 Set evaluation behavior for example 1h

3.5 Configure notifications: set the contact point, create a new contact points if you do not set it.

3.6 Configure notification message: set the Summary and the Description

### 5.3 Route notifications to both destinations

Configure Grafana's notification routing so the alert is delivered to
**both** the email contact point and the Render webhook contact point.

Depending on the Grafana notification-policy configuration, this may
require a parent policy with child policies, or a contact point that
includes both integrations. Verify the resulting routing behavior by
testing each destination.

### 5.4 Test the complete flow

-   Confirm that production telemetry is arriving in Prometheus, Loki,
    and Tempo.
-   Check that the five dashboard panels return data.
-   Confirm that a Loki log entry can link to its corresponding Tempo
    trace.
-   Use Grafana's contact-point test feature where available to test
    email and webhook delivery.
-   Verify that the Incident Responder receives and processes the
    webhook payload.
-   Confirm that alert notifications reach both destinations.


## Step 6: Inspecting Incident History & Logs on Render

To inspect previously received alerts, review saved JSON evidence payloads, or monitor webhook executions on your production Render instance (`interview-canvas-app`), use either of the following methods.

#### 6.1. Inspecting Saved Incident Payloads via Render Shell

The incident responder automatically saves incoming alert payloads as JSON evidence files in the running container's filesystem.

1. Open the **Render Dashboard**.
2. Select **`interview-canvas-app`**.
3. Click **Shell** in the left sidebar.
4. List the saved incident evidence files:

   ```bash
   ls -la incident_response/incidents/
   ```

5. View a specific alert payload:

   ```bash
   cat incident_response/incidents/inc_<alertname>.json
   ```

#### 6.2. Filtering Real-Time Logs via Render Logs Tab

To monitor alerts and track webhook executions as they arrive:

1. Open the **Render Dashboard**.
2. Select **`interview-canvas-app`**.
3. Click the **Logs** tab.
4. Search or filter for `[Responder]` in the log stream.

You should see execution records confirming alert reception and evidence storage, for example:

   ```text
   INFO: 10.x.x.x:xxxxx - "POST /alerts HTTP/1.1" 200 OK
   [Responder] Firing alert received: HighServerErrorRate
   [Responder] Evidence saved to: /app/incident_response/incidents/inc_highservererrorrate.json
   ```


------------------------------------------------------------------------

This guide describes the production observability configuration. Keep
secrets in Render environment variables or the relevant secret manager,
not in this documentation or in Git.
