# Advanced Scoring System - Integration Guide

This guide walks you through integrating the advanced scoring system into your existing BrainCoach AI application.

## Step-by-Step Integration

### Step 1: Database Migration

Run the SQL migration to add new tables and fields:

```bash
# If using SQLite directly
sqlite3 instance/braincoach.db < migrations/add_advanced_scoring_fields.sql

# Or using Flask-Migrate (recommended)
flask db upgrade
```

### Step 2: Update Models (models.py)

Add new model classes for advanced features:

```python
# Add to models.py

class PatternDetection(db.Model):
    __tablename__ = 'pattern_detection'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    landmark_index = db.Column(db.Integer)
    error_mean = db.Column(db.Float)
    error_std = db.Column(db.Float)
    anomaly_count = db.Column(db.Integer)
    anomaly_percentage = db.Column(db.Float)
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)

class TrendAnalysis(db.Model):
    __tablename__ = 'trend_analysis'
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), nullable=False)
    analysis_date = db.Column(db.DateTime, default=datetime.utcnow)
    slope = db.Column(db.Float)
    intercept = db.Column(db.Float)
    r_squared = db.Column(db.Float)
    trend_direction = db.Column(db.String(50))
    confidence_score = db.Column(db.Float)
    predicted_next = db.Column(db.Float)
    sessions_analyzed = db.Column(db.Integer)

class SessionComparison(db.Model):
    __tablename__ = 'session_comparison'
    id = db.Column(db.Integer, primary_key=True)
    current_session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    previous_session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    cohens_d = db.Column(db.Float)
    improvement_percentage = db.Column(db.Float)
    effect_interpretation = db.Column(db.String(100))
    comparison_date = db.Column(db.DateTime, default=datetime.utcnow)

class Recommendation(db.Model):
    __tablename__ = 'recommendation'
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    category = db.Column(db.String(50))
    priority = db.Column(db.String(20))
    message = db.Column(db.Text)
    action_suggestion = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    acknowledged = db.Column(db.Boolean, default=False)

# Update existing Session model with new fields
class Session(db.Model):
    # ... existing fields ...

    # Add new fields for advanced scoring
    smoothed_accuracy = db.Column(db.Float)
    consistency_score = db.Column(db.Float)
    improvement_rate = db.Column(db.Float)
    composite_score = db.Column(db.Float)
    performance_grade = db.Column(db.String(2))
    pattern_detected = db.Column(db.Boolean, default=False)

    # Add new relationships
    pattern_detections = db.relationship('PatternDetection', backref='session', lazy=True)
    comparisons_as_current = db.relationship('SessionComparison',
                                            foreign_keys='SessionComparison.current_session_id',
                                            backref='current_session', lazy=True)
    comparisons_as_previous = db.relationship('SessionComparison',
                                             foreign_keys='SessionComparison.previous_session_id',
                                             backref='previous_session', lazy=True)
```

### Step 3: Register Analytics Blueprint (app.py)

```python
# In app.py

from routes.analytics import analytics

# Register blueprint
app.register_blueprint(analytics, url_prefix='/analytics')

print("✓ Analytics blueprint registered")
```

### Step 4: Update Session Completion Route (routes/session.py)

Replace the existing `complete_session` function:

```python
from utils.advanced_scoring import analyze_session_comprehensive
import json

@session.route('/api/session/complete', methods=['POST'])
@login_required
def complete_session():
    data = request.json
    session_id = data.get('session_id')
    avg_accuracy = data.get('avg_accuracy')
    total_score = data.get('total_score')

    sess = Session.query.get_or_404(session_id)

    # Verify session ownership
    if sess.child.parent_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    sess.end_time = datetime.utcnow()
    sess.avg_accuracy = avg_accuracy
    sess.total_score = total_score
    sess.result_status = 'Completed'

    # Perform advanced analysis
    analysis = analyze_session_comprehensive(session_id, db.session)

    if 'error' not in analysis:
        # Store advanced metrics
        sess.smoothed_accuracy = analysis.get('average_accuracy')
        sess.consistency_score = analysis.get('consistency_score')
        composite = analysis.get('composite_score', {})
        sess.composite_score = composite.get('composite_score')
        sess.performance_grade = composite.get('grade')

        # Check for patterns
        patterns = analysis.get('pattern_analysis', {})
        sess.pattern_detected = patterns.get('patterns_detected', False)

        # Store pattern detections
        if patterns.get('patterns_detected'):
            for landmark in patterns.get('problematic_landmarks', []):
                pattern_entry = PatternDetection(
                    session_id=session_id,
                    landmark_index=landmark,
                    anomaly_percentage=patterns.get('outlier_percentage', 0)
                )
                db.session.add(pattern_entry)

        # Store trend analysis
        trend = analysis.get('trend_analysis', {})
        if trend.get('trend_available'):
            trend_entry = TrendAnalysis(
                child_id=sess.child_id,
                slope=trend.get('slope'),
                intercept=trend.get('intercept'),
                r_squared=trend.get('r_squared'),
                trend_direction=trend.get('trend_direction'),
                confidence_score=trend.get('confidence')
            )
            db.session.add(trend_entry)

        # Store recommendations
        for rec in analysis.get('recommendations', []):
            rec_entry = Recommendation(
                child_id=sess.child_id,
                session_id=session_id,
                category=rec.get('category'),
                priority=rec.get('priority'),
                message=rec.get('message'),
                action_suggestion=rec.get('action')
            )
            db.session.add(rec_entry)

    # Add score entry with detailed feedback
    score_entry = Score(
        session_id=session_id,
        accuracy_percentage=avg_accuracy,
        feedback=f"Session completed with {avg_accuracy:.2f}% accuracy.",
        recommendations=json.dumps(analysis.get('recommendations', [])) if 'error' not in analysis else None
    )
    db.session.add(score_entry)
    db.session.commit()

    # Generate PDF
    try:
        pdf_dir = os.path.join('reports', f'child_{sess.child_id}')
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)

        pdf_path = os.path.join(pdf_dir, f'session_{session_id}.pdf')
        generate_session_report(sess, pdf_path)
    except Exception as e:
        print(f"PDF generation failed: {e}")

    return jsonify({
        "status": "success",
        "redirect": url_for('dashboard.index'),
        "analysis": analysis
    })
```

### Step 5: Update Session HTML Template (templates/session.html)

Replace the scoring system initialization:

```html
<!-- At the top of the file, update imports -->
<script type="module">
    import { AdvancedScoringSystem, formatRecommendations } from '/static/js/scoring_advanced.js';

    // Get child age from template
    const childAge = {{ child.age if child.age else 10 }};
    const sessionId = {{ session_id }};

    // Initialize advanced scoring system
    const scorer = new AdvancedScoringSystem(childAge);

    let frameCount = 0;

    // In your hand tracking callback
    function onHandsDetected(results) {
        if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
            const landmarks = results.multiHandLandmarks[0];

            // Calculate accuracy with advanced features
            const accuracyResult = scorer.calculateAccuracy(landmarks);

            // Update display
            document.getElementById('accuracy').textContent =
                accuracyResult.smoothed.toFixed(1) + '%';

            // Update progress bar
            const progressBar = document.getElementById('progressBar');
            progressBar.style.width = accuracyResult.smoothed + '%';
            progressBar.className = accuracyResult.smoothed >= scorer.dynamicThreshold
                ? 'progress-bar bg-success'
                : 'progress-bar bg-warning';

            // Display threshold
            document.getElementById('threshold').textContent =
                scorer.dynamicThreshold.toFixed(1) + '%';

            // Show real-time recommendations every 30 frames
            if (frameCount % 30 === 0) {
                const recommendations = scorer.getRealtimeRecommendations();
                document.getElementById('recommendations').innerHTML =
                    formatRecommendations(recommendations);
            }

            // Save frame data to backend
            frameCount++;
            if (frameCount % 10 === 0) {
                fetch('/api/session/update', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        session_id: sessionId,
                        frame_number: frameCount,
                        accuracy: accuracyResult.smoothed,
                        landmarks: landmarks
                    })
                });
            }
        }
    }

    // On session completion
    function completeSession() {
        const summary = scorer.getSessionSummary();

        // Display summary
        console.log('Session Summary:', summary);

        // Show modal with results
        showResultsModal(summary);

        // Send to backend
        fetch('/api/session/complete', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: sessionId,
                avg_accuracy: summary.averageAccuracy,
                total_score: summary.totalScore
            })
        })
        .then(r => r.json())
        .then(data => {
            if (data.status === 'success') {
                // Display comprehensive analysis
                displayAdvancedAnalysis(data.analysis);

                setTimeout(() => {
                    window.location.href = data.redirect;
                }, 5000);
            }
        });
    }

    function showResultsModal(summary) {
        const modal = document.getElementById('resultsModal');
        document.getElementById('finalScore').textContent = summary.totalScore;
        document.getElementById('finalGrade').textContent = summary.grade;
        document.getElementById('finalAccuracy').textContent = summary.averageAccuracy + '%';
        document.getElementById('consistency').textContent = summary.consistency.score.toFixed(1) + '%';
        document.getElementById('performanceTrend').textContent = summary.performance.trend;

        // Show pattern warnings if detected
        if (summary.patterns.detected) {
            document.getElementById('patternWarning').innerHTML = `
                <div class="alert alert-warning">
                    ⚠️ Detected ${summary.patterns.count} problematic hand positions.
                    Review the recommendations for improvement.
                </div>
            `;
        }

        // Show modal
        modal.style.display = 'block';
    }

    function displayAdvancedAnalysis(analysis) {
        // Display recommendations
        const recContainer = document.getElementById('recommendationsContainer');
        recContainer.innerHTML = '<h5>Personalized Recommendations</h5>';

        analysis.recommendations.forEach(rec => {
            const priority = rec.priority.toLowerCase();
            const alertClass = priority === 'high' ? 'alert-danger' :
                              priority === 'medium' ? 'alert-warning' : 'alert-info';

            recContainer.innerHTML += `
                <div class="alert ${alertClass}">
                    <h6>${rec.category}</h6>
                    <p>${rec.message}</p>
                    <small><strong>Action:</strong> ${rec.action}</small>
                </div>
            `;
        });

        // Display trend analysis
        if (analysis.trend_analysis && analysis.trend_analysis.trend_available) {
            const trend = analysis.trend_analysis;
            document.getElementById('trendInfo').innerHTML = `
                <div class="card">
                    <div class="card-body">
                        <h6>Improvement Trend</h6>
                        <p><strong>Direction:</strong> ${trend.trend_direction}</p>
                        <p><strong>Confidence:</strong> ${(trend.confidence * 100).toFixed(1)}%</p>
                        <p><strong>Predicted Next:</strong> ${trend.predicted_next.toFixed(1)}%</p>
                    </div>
                </div>
            `;
        }
    }
</script>

<!-- Add new HTML elements for display -->
<div class="container mt-4">
    <div class="row">
        <div class="col-md-8">
            <!-- Video feed -->
            <video id="videoElement" autoplay></video>
            <canvas id="canvasElement"></canvas>
        </div>

        <div class="col-md-4">
            <!-- Real-time metrics -->
            <div class="card mb-3">
                <div class="card-body">
                    <h5>Performance Metrics</h5>
                    <p>Accuracy: <span id="accuracy">0</span></p>
                    <p>Threshold: <span id="threshold">85</span></p>

                    <div class="progress mb-3">
                        <div id="progressBar" class="progress-bar" style="width: 0%"></div>
                    </div>

                    <h6>Real-time Feedback</h6>
                    <div id="recommendations"></div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Results Modal -->
<div id="resultsModal" class="modal" style="display: none;">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <h5>Session Complete! 🎉</h5>
            </div>
            <div class="modal-body">
                <div class="row">
                    <div class="col-md-6">
                        <h3>Score: <span id="finalScore">0</span></h3>
                        <h4>Grade: <span id="finalGrade">-</span></h4>
                    </div>
                    <div class="col-md-6">
                        <p>Accuracy: <span id="finalAccuracy">0%</span></p>
                        <p>Consistency: <span id="consistency">0%</span></p>
                        <p>Trend: <span id="performanceTrend">-</span></p>
                    </div>
                </div>

                <div id="patternWarning"></div>

                <hr>

                <div id="recommendationsContainer"></div>
                <div id="trendInfo"></div>
            </div>
        </div>
    </div>
</div>
```

### Step 6: Update Dashboard to Show Advanced Metrics

Add to `templates/dashboard.html`:

```html
<!-- Add analytics card -->
<div class="col-md-12 mb-4">
    <div class="card">
        <div class="card-header">
            <h5>Advanced Analytics</h5>
        </div>
        <div class="card-body">
            {% for child in children %}
            <div class="child-analytics mb-3">
                <h6>{{ child.name }}</h6>
                <button class="btn btn-sm btn-primary"
                        onclick="loadAnalytics({{ child.id }})">
                    View Detailed Analytics
                </button>
            </div>
            {% endfor %}
        </div>
    </div>
</div>

<script>
function loadAnalytics(childId) {
    fetch(`/analytics/api/analytics/child/${childId}/overview`)
        .then(r => r.json())
        .then(data => {
            console.log('Analytics:', data);
            showAnalyticsModal(data);
        });
}

function showAnalyticsModal(data) {
    // Create and display analytics modal
    const modalContent = `
        <div class="modal" id="analyticsModal">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5>${data.child_name}'s Performance Analytics</h5>
                        <button type="button" class="close" onclick="closeModal()">×</button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-md-3">
                                <div class="stat-card">
                                    <h6>Average Accuracy</h6>
                                    <h3>${data.statistics.average_accuracy}%</h3>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="stat-card">
                                    <h6>Consistency</h6>
                                    <h3>${data.statistics.consistency_score}%</h3>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="stat-card">
                                    <h6>Total Sessions</h6>
                                    <h3>${data.total_sessions}</h3>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="stat-card">
                                    <h6>Practice Hours</h6>
                                    <h3>${data.statistics.total_practice_hours}</h3>
                                </div>
                            </div>
                        </div>

                        <div class="row mt-4">
                            <div class="col-md-12">
                                <h6>Performance Trend</h6>
                                <p><strong>Direction:</strong> ${data.trend_analysis.trend_direction}</p>
                                <p><strong>Slope:</strong> ${data.trend_analysis.slope?.toFixed(3)}</p>
                                <p><strong>Confidence:</strong> ${(data.trend_analysis.confidence * 100).toFixed(1)}%</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modalContent);
    document.getElementById('analyticsModal').style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('analyticsModal');
    modal.remove();
}
</script>
```

### Step 7: Test the Integration

```bash
# Start the Flask development server
flask run

# In browser, test:
# 1. Start a training session
# 2. Complete the session
# 3. Check dashboard for new analytics
# 4. Navigate to /analytics/api/analytics/child/1/overview
```

## Verification Checklist

- [ ] Database migration completed successfully
- [ ] New models added to models.py
- [ ] Analytics blueprint registered in app.py
- [ ] Session completion updated with advanced analysis
- [ ] Session template updated with new scoring system
- [ ] Dashboard shows advanced metrics
- [ ] Real-time recommendations display during session
- [ ] Pattern detection working (check console logs)
- [ ] Trend analysis shows on completion
- [ ] Personalized recommendations generate correctly

## Troubleshooting

### Issue: Import Error for `numpy`
**Solution**: Install dependencies
```bash
pip install numpy scipy
```

### Issue: Analytics endpoints return 404
**Solution**: Ensure blueprint is registered
```python
# In app.py
from routes.analytics import analytics
app.register_blueprint(analytics, url_prefix='/analytics')
```

### Issue: Session analysis shows "No frame data"
**Solution**: Ensure frames are being saved with landmark data
```javascript
// Check that landmarks are being sent in correct format
fetch('/api/session/update', {
    body: JSON.stringify({
        landmarks: landmarks,  // Must be array of 21 objects
        // ...
    })
});
```

## Performance Tips

1. **Limit Frame Saves**: Save every 10th frame instead of every frame
2. **Async Analysis**: Perform heavy analysis in background after session
3. **Cache Results**: Store analyzed results to avoid recomputation
4. **Pagination**: Limit history queries to recent sessions (last 10-20)

## Next Steps

1. Create visualization charts for trend analysis
2. Implement email notifications with recommendations
3. Add export functionality for analytics reports
4. Create parent dashboard with multi-child comparison
5. Implement A/B testing for algorithm parameter tuning

---

**Integration Complete!** Your BrainCoach AI now has advanced scoring capabilities with personalized recommendations and comprehensive analytics.
