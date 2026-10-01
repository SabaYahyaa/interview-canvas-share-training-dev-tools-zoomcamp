from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

provider = TracerProvider()
processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("my-app")


def calculate_total(price, quantity):
    with tracer.start_as_current_span("calculate_total") as span:
        span.set_attribute("price", price)
        span.set_attribute("quantity", quantity)
        results = price * quantity
        return results


from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

provider = TracerProvider()

provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

trace.set_tracer_provider(provider)


app = FastAPI()

FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)


@app.get("/hello")
def hello():
    return {"message": "hello"}


if __name__ == "__main__":
    # Example usage
    price = 10.0
    quantity = 5
    total_cost = calculate_total(price, quantity)
    print(f"Total cost for {quantity} items at ${price} each is: ${total_cost}")


# You can store all 3 signals (Metrics, Logs, Traces) directly inside your single PostgreSQL database using isolated schemas (dev_telemetry / prod_telemetry), and visualize them directly in Grafana for zero cost:

# [ FastAPI App ] ──(OTLP)──> [ OpenTelemetry Collector ] ──(SQL)──> [ Postgres DB ] ──> [ Grafana ]
#    (App Code)               (otel-collector)                     (dev/prod_telemetry)     (Dashboards)
# Traces: Stored in structured JSONB tables inside PostgreSQL.

# Metrics: Stored as time-series metrics inside PostgreSQL.

# Logs: Stored as structured log rows (timestamp, severity, body, attributes) inside PostgreSQL.

# Grafana: Connects directly to PostgreSQL using the native PostgreSQL data source plugin—allowing you to build full dashboard panels for traces, error logs, and endpoint latencies without paying a dime or spinning up Tempo/Loki.
