import os
import base64
from fastapi import FastAPI
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor


def setup_telemetry(app: FastAPI, db_engine=None):
    """
    Configures OpenTelemetry for FastAPI and SQLAlchemy, exporting directly
    to Grafana Cloud over OTLP/HTTP.
    """
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    user_id = os.getenv("OTEL_EXPORTER_OTLP_HEADERS_USER")
    api_key = os.getenv("OTEL_EXPORTER_OTLP_HEADERS_KEY")
    service_name = os.getenv("OTEL_SERVICE_NAME", "interviewer-canvas-backend")

    # If Grafana Cloud credentials are missing, telemetry runs locally without remote exporting
    if not endpoint or not user_id or not api_key:
        print("[Telemetry] No Grafana Cloud keys found. Skipping remote export.")
        return

    # Build Basic Auth header required by Grafana Cloud OTLP HTTP endpoint
    auth_bytes = f"{user_id}:{api_key}".encode("utf-8")
    auth_header = base64.b64encode(auth_bytes).decode("utf-8")
    headers = {"Authorization": f"Basic {auth_header}"}

    # Identify your service in Grafana
    resource = Resource.create({"service.name": service_name})

    # 1. Traces Configuration (Sends to Grafana Tempo)
    tracer_provider = TracerProvider(resource=resource)
    trace_exporter = OTLPSpanExporter(
        endpoint=f"{endpoint.rstrip('/')}/v1/traces", headers=headers
    )
    tracer_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
    trace.set_tracer_provider(tracer_provider)

    # 2. Metrics Configuration (Sends to Grafana Prometheus)
    metric_exporter = OTLPMetricExporter(
        endpoint=f"{endpoint.rstrip('/')}/v1/metrics", headers=headers
    )
    metric_reader = PeriodicExportingMetricReader(
        metric_exporter, export_interval_millis=15000  # Send metrics every 15 seconds
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)

    # 3. Automatic FastAPI Instrumentation
    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)

    # 4. Automatic SQLAlchemy DB Instrumentation (if engine provided)
    if db_engine:
        SQLAlchemyInstrumentor().instrument(engine=db_engine)

    print(
        f"[Telemetry] Successfully configured OTLP export to Grafana Cloud for '{service_name}'."
    )
