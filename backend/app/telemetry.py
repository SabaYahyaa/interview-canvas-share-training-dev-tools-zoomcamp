import base64
import logging
import os
from fastapi import FastAPI
from opentelemetry import metrics, trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def setup_telemetry(app: FastAPI, db_engine=None):
    """Configures OpenTelemetry for FastAPI, sending Traces (Tempo), Metrics

    (Prometheus), and Logs (Loki) directly to Grafana Cloud over OTLP/HTTP.
    """
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    user_id = os.getenv("OTEL_EXPORTER_OTLP_HEADERS_USER")
    api_key = os.getenv("OTEL_EXPORTER_OTLP_HEADERS_KEY")
    service_name = os.getenv("OTEL_SERVICE_NAME", "interview-canvas-backend-dev")

    if not endpoint or not user_id or not api_key:
        print("[Telemetry] No Grafana Cloud keys found. Skipping remote export.")
        return

    auth_bytes = f"{user_id}:{api_key}".encode("utf-8")
    auth_header = base64.b64encode(auth_bytes).decode("utf-8")
    headers = {"Authorization": f"Basic {auth_header}"}

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
        metric_exporter, export_interval_millis=15000
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)

    # 3. Logs Configuration (Sends to Grafana Loki)
    logger_provider = LoggerProvider(resource=resource)
    log_exporter = OTLPLogExporter(
        endpoint=f"{endpoint.rstrip('/')}/v1/logs", headers=headers
    )
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
    set_logger_provider(logger_provider)

    # Attach OpenTelemetry Handler to Python's root logger
    handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)

    # 4. Automatic FastAPI Instrumentation
    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)

    # 5. Automatic SQLAlchemy DB Instrumentation
    if db_engine:
        SQLAlchemyInstrumentor().instrument(engine=db_engine)

    logging.info(
        f"[Telemetry] Successfully configured OTLP export (Traces, Metrics,"
        f" Logs) for '{service_name}'."
    )
