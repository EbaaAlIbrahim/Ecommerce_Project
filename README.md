## Real-Time E-Commerce Streaming Architecture & Personalization Pipeline
A production-grade, event-driven data ecosystem simulating a hyper-scale live e-commerce platform. Moving away from traditional overnight batch processing, this project implements an always-on, real-time data streaming pipeline. It processes in-flight transactions, executes instant machine learning predictions, and updates active operational business intelligence (BI) dashboards concurrently.
## System Architecture & Data Flow
The infrastructure divides system computing power into five decoupled, asynchronous processes running simultaneously via Inter-Process Communication (IPC):

                       ┌──> [live_ai_engine.py] ──────> Updates Live Recommendations
                       │
[server_simulator.py] ──> [live_stream_buffer.json] ──>
                       │
                       ├──> [streaming_pipeline.py] ──> Commits Clean Data to SQL Warehouse
                       │
                       ├──> [live_dashboard.py] ──────> Outputs Live Text KPIs & Conversions
                       │
                       └──> [live_graphs.py] ─────────> Renders Animating Visual Charts

------------------------------
## Core Infrastructure File Breakdown
##  1. Platform Core & Ingestion Influx: server_simulator.py

* Purpose: Simulates live user traffic by generating unstructured e-commerce payloads at 1-second intervals.
* Payload Components: Collects User IDs, product keys, user actions, timestamps, and geolocation parameters.
* Engineering Challenge: Injects real-world anomalies like malformed string arrays, empty JSON elements, and a 5% transaction duplication rate.

## 2. The Streaming Highway Buffer: live_stream_buffer.json

* Purpose: Acts as an asynchronous messaging queue and data stream broker.
* Architectural Value: Decouples the frontend web application from core database writes to protect systems during high-traffic checkout spikes.
* Stability Factor: Retains sequential records chronologically to prevent data loss and isolate the main platform from system crashes.

## 3. The Data Engineer Pipeline: streaming_pipeline.py

* Purpose: Operates the central infrastructure ingestion loop.
* Memory Management: Uses low-level file pointers to intercept new data lines without loading massive log files into RAM.
* Stream Operations:
* Deduplication: Maintains a high-speed memory cache of recent event IDs to instantly discard duplicate payloads.
   * Stream Cleanse: Uses programmatic string manipulation to strip structural brackets on the fly.
   * Null Resolution: Catches empty geographic values and substitutes them with "Unknown" strings.
   * Continuous Loading: Micro-batches and streams cleaned data directly into relational SQL tables in milliseconds.

## 4. The Data Scientist Engine: live_ai_engine.py

* Purpose: Establishes an Instant Personalization Engine by continuously listening to the data warehouse.
* Predictive Analytics: Intercepts purchase events to query a pre-trained Item-Based Co-occurrence rules matrix.
* User Customization: Extracts complementary product suggestions and writes them directly into live user recommendation tables.

## 5. The Data Analyst Dashboard: live_dashboard.py

* Purpose: Powers an operational Command Line Interface (CLI) business intelligence dashboard updating every 2 seconds.
* Metrics Tracked: Computes running user traffic counts, total orders placed, conversion rates, and gross estimated revenue.

## 6. The Visual BI Dashboard: live_graphs.py

* Purpose: Renders a Graphical User Interface (GUI) dashboard powered by the Matplotlib Animation Engine.
* Visual Components: Generates a live Pie Chart showing click-to-buy ratios and an animating Bar Chart mapping regional activity hubs.

------------------------------
##  Key Technical Competencies

* Advanced Python Systems: Built concurrent, infinite event loop programs using time throttling and object parsing.
* Real-Time Stream ETL: Accomplished rolling RAM data deduplication, telemetry dropout resolution, and data serialization.
* Relational Storage Deployment: Structured continuous micro-batch insert statements into live relational SQL databases.
* Predictive ML Execution: Applied implicit e-commerce transaction feedback models to drive live programmatic user personalization profile stores.
* Live Visual Analytics: Structured self-refreshing algorithmic database aggregation calls to power interactive graphical dashboards.

