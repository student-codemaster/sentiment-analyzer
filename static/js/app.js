class SentimentAnalyzer {
    constructor() {
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        const form = document.getElementById('analysisForm');
        form.addEventListener('submit', (e) => this.handleAnalysis(e));
    }

    async handleAnalysis(e) {
        e.preventDefault();
        
        const textInput = document.getElementById('textInput');
        const text = textInput.value.trim();
        
        if (!text) {
            alert('Please enter some text to analyze.');
            return;
        }

        this.showLoading(true);
        
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });

            const result = await response.json();
            
            if (response.ok) {
                this.displayResults(result);
            } else {
                throw new Error(result.error || 'Analysis failed');
            }
        } catch (error) {
            this.displayError(error.message);
        } finally {
            this.showLoading(false);
        }
    }

    displayResults(result) {
        const resultsContainer = document.getElementById('resultsContainer');
        const sentimentClass = this.getSentimentClass(result.unified_sentiment);
        
        resultsContainer.innerHTML = `
            <div class="col-md-6">
                <div class="card analysis-card">
                    <div class="card-header ${sentimentClass}">
                        <h6><i class="fas fa-chart-pie"></i> Unified Analysis</h6>
                    </div>
                    <div class="card-body">
                        <h4 class="card-title ${sentimentClass}">
                            ${result.unified_sentiment} 
                            <small class="text-muted">(${result.unified_score.toFixed(3)})</small>
                        </h4>
                        <p class="card-text">"${result.text}"</p>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card analysis-card">
                    <div class="card-header">
                        <h6><i class="fas fa-chart-bar"></i> Detailed Breakdown</h6>
                    </div>
                    <div class="card-body">
                        <h6>VADER Analysis:</h6>
                        <div class="progress mb-2">
                            <div class="progress-bar bg-success" style="width: ${result.vader.positive * 100}%">
                                Positive: ${(result.vader.positive * 100).toFixed(1)}%
                            </div>
                        </div>
                        <div class="progress mb-2">
                            <div class="progress-bar bg-danger" style="width: ${result.vader.negative * 100}%">
                                Negative: ${(result.vader.negative * 100).toFixed(1)}%
                            </div>
                        </div>
                        
                        <h6 class="mt-3">TextBlob:</h6>
                        <p>Polarity: ${result.textblob.polarity.toFixed(3)}<br>
                        Subjectivity: ${result.textblob.subjectivity.toFixed(3)}</p>
                        
                        <h6>Transformers:</h6>
                        <p>${result.transformers.label}: ${result.transformers.score.toFixed(3)}</p>
                    </div>
                </div>
            </div>
        `;

        document.getElementById('results').style.display = 'block';
    }

    getSentimentClass(sentiment) {
        switch(sentiment) {
            case 'POSITIVE': return 'sentiment-positive';
            case 'NEGATIVE': return 'sentiment-negative';
            case 'NEUTRAL': return 'sentiment-neutral';
            default: return '';
        }
    }

    displayError(message) {
        const resultsContainer = document.getElementById('resultsContainer');
        resultsContainer.innerHTML = `
            <div class="col-12">
                <div class="alert alert-danger" role="alert">
                    <i class="fas fa-exclamation-triangle"></i> Error: ${message}
                </div>
            </div>
        `;
        document.getElementById('results').style.display = 'block';
    }

    showLoading(show) {
        document.getElementById('loading').style.display = show ? 'block' : 'none';
        document.getElementById('analysisForm').querySelector('button').disabled = show;
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new SentimentAnalyzer();
});