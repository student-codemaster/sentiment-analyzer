from flask import Flask, render_template, request, jsonify
from models.sentiment_analyzer import UnifiedSentimentAnalyzer
import json
from datetime import datetime

app = Flask(__name__)
analyzer = UnifiedSentimentAnalyzer()

# Store analysis history (in production, use a database)
analysis_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Analyze sentiment
        result = analyzer.analyze_text(text)
        
        # Add timestamp and store in history
        result['timestamp'] = datetime.now().isoformat()
        result['id'] = len(analysis_history) + 1
        analysis_history.append(result)
        
        # Keep only last 50 analyses
        if len(analysis_history) > 50:
            analysis_history.pop(0)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/batch-analyze', methods=['POST'])
def batch_analyze():
    try:
        data = request.get_json()
        texts = data.get('texts', [])
        
        if not texts:
            return jsonify({'error': 'No texts provided'}), 400
        
        results = analyzer.analyze_batch(texts)
        return jsonify({'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', history=analysis_history)

@app.route('/api/history')
def get_history():
    return jsonify(analysis_history)

if __name__ == '__main__':
    app.run(debug=True)