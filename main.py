from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

def search_files(query, search_path='.'):
    results = []
    for root, dirs, files in os.walk(search_path):
        for file in files:
            if query.lower() in file.lower():
                full_path = os.path.join(root, file)
                try:
                    stat = os.stat(full_path)
                    file_info = {
                        "name": file,
                        "path": full_path,
                        "size": stat.st_size,
                        "created": datetime.fromtimestamp(stat.st_ctime).isoformat()
                    }
                    results.append(file_info)
                except Exception as e:
                    print(f"Ошибка получения информации о файле {full_path}: {e}")
    return results

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "Параметр 'query' обязателен"}), 400
    results = search_files(query)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
