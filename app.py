from flask import Flask, request, render_template 
from elasticsearch import Elasticsearch
app = Flask(__name__)
es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/search', methods=['GET', 'POST'])
def search():
    search_term = request.form["search_query"]
    res = es.search(
        index="flickrphotos", 
        size=30, 
        body={
            
            "query": {
                "multi_match" : {
                    "query": search_term, 
                    "fields": [
                        "url", 
                        "title", 
                        "tags"
                    ],
                    "fuzziness" : "AUTO",
                    "prefix_length" : 1
                    
                }
            }
        }
    )
    return render_template('results.html', res=res )

    
if __name__ == '__main__':
    app.run(debug=True)