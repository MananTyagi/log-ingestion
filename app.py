from flask import Flask, request, render_template, jsonify
from elasticsearch import Elasticsearch
from tasks import ingest_log
from flask_socketio import SocketIO




app = Flask(__name__)
es = Elasticsearch("http://localhost:9200")
socketio = SocketIO(app)

# Log Ingestor
@app.route('/ingest', methods=['POST'])
def ingest():
    log_data = request.get_json()
    ingest_log.delay(log_data)
    socketio.emit('log_ingested', {'log_data': log_data}, namespace='/logs')
    return f'Task sent for asynchronous ingestion!', 200


def get_logs():
    # Customize the Elasticsearch query based on your log index and requirements
    query = {
        "query": {
            "match_all": {}
        }
    }
    query['size'] = 100
    # Make a search request to Elasticsearch
    result = es.search(index='logs', body=query)

    # Extract and return logs from the search result
    logs = [hit['_source'] for hit in result['hits']['hits']]
    return logs



@app.route('/')
def index():
    logs = get_logs()
    return render_template('index.html', logs=logs)



@app.route('/search', methods=['POST'])
def search_logs():
    json_data = request.get_json()
    
    level_filter = json_data.get('level', '')
    message_filter = json_data.get('message','')
    start_date = json_data.get('start_date', '')
    end_date = json_data.get('end_date', '')
    resourceId_filter = json_data.get('resource_id','')
    traceId_filter = json_data.get('trace_id','')
    spanId_filter = json_data.get('span_id','')
    commit_filter = json_data.get('commit','')


    
    # Add other filters...

    query_body = {
        "query": {
            "bool": {
                "must": []
            }
        }
    }

    # Add other filter conditions...
    if level_filter:
        query_body['query']['bool']['must'].append({"term": {"level": level_filter}})
    if message_filter:
        query_body['query']['bool']['must'].append({"term": {"message.keyword": message_filter}})
    if resourceId_filter:
        query_body['query']['bool']['must'].append({"term": {"resourceId.keyword": resourceId_filter}})
        
    if traceId_filter:
        query_body['query']['bool']['must'].append({"term": {"traceId.keyword": traceId_filter}})
        
    if spanId_filter:
        query_body['query']['bool']['must'].append({"term": {"spanId.keyword": spanId_filter}})
        
    if  commit_filter:
        query_body['query']['bool']['must'].append({"term": {"commit": commit_filter}})

        
    if start_date and end_date:
            query_body['query']['bool']['must'].append({
                "range": {
                    "timestamp": {
                        "gte": start_date,
                        "lte": end_date
                    }
                }
            })

        
    results = es.search(index='logs', body=query_body)

    # Extract relevant information from the results
    formatted_results = [{"_source": hit["_source"]} for hit in results['hits']['hits']]

    return jsonify(formatted_results)


@socketio.on('connect', namespace='/logs')
def handle_connect():
    print('Client connected')


if __name__ == '__main__':
    socketio.run(app,port=3000, debug=True)
