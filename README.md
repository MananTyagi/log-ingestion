# Log Management System

## Table of Contents

* Introduction
* Features
* System Design
* Getting Started
* Usage
* Known issues

## Introduction

The Log Management System is a web-based application built to ingest, store, and query logs efficiently. It provides a user-friendly interface for searching logs based on various parameters.

## Features

* Log ingestion over HTTP on port 3000
* Full-text search across logs
* Filters based on log attributes (level, message, resourceId, timestamp, traceId, spanId, commit)
* Additional Advanced Features (Bonus):
  * Search within specific date ranges
  * Allow combining multiple filters
  * Real-time log ingestion and searching capabilities

## System Design

The system is designed with a Flask web server for log ingestion and querying, and Elasticsearch for efficient log storage and retrieval. WebSocket is employed for real-time updates.

**Components:**

* Flask Web Server (Log Ingestor and Query Interface)
* Elasticsearch Database for fast and efficient text based query
* WebSocket for Real-Time Updates
* Celery for Asynchronous Log Ingestion for high scalablity
* RabbitMQ as the Message Queue

## Getting Started

Follow these steps to set up and run the Log Management System:

1. **Clone the Repository:**
   git clone "repo url"
2. **Install Dependencies:**
   pip install -r requirements.txt
3. **Configure Elasticsearch:**
   * Install and run Elasticsearch on the default port.
4. **Run the Flask Application:**
   py app.py
5. Run celery worker and start Rabbitmq and Elasticsearch services in your OS
6. **Access the Web Interface:**
   Open your web browser and navigate to `http://localhost:3000` to interact with the Log Management System.

## Usage

* Log Ingestor is available at http://127.0.0.1:3000/ingest. you can send post request in any volume.
* Query Interface is accessible at `http://localhost:3000`.

## Known Issues

* Role based accessing (RBAC) is under development and will be available from next version

Feel free to contribute by opening issues or submitting pull requests.

**Happy Logging!**
