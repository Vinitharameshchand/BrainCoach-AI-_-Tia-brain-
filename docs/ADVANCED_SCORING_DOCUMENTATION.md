# Advanced Scoring Algorithm Documentation

## Overview

This document describes the upgraded scoring system for BrainCoach AI, which implements sophisticated algorithms for comprehensive performance assessment and personalized learning recommendations.

---

## Mathematical Formulas

### 1. Moving Average Smoothing

**Purpose**: Reduce noise in frame-by-frame measurements and provide stable performance metrics.

**Formula: Exponential Moving Average (EMA)**

```
EMA_t = α × X_t + (1 - α) × EMA_(t-1)
```

Where:
- `EMA_t` = Exponential moving average at time t
- `X_t` = Current measurement at time t
- `α` = Smoothing factor = 2/(N+1), typically 0.3 for responsive smoothing
- `N` = Window size (typically 10 frames)

**Properties**:
- Recent data has more weight than older data
- Responds quickly to real changes while filtering noise
- Computationally efficient (O(1) per update)

**Implementation**:
```javascript
// JavaScript
currentEMA = alpha * newValue + (1 - alpha) * previousEMA;
```

```python
# Python
self.current_ema = (self.ema_alpha * accuracy +
                   (1 - self.ema_alpha) * self.current_ema)
```

---

### 2. Dynamic Threshold Based on Age

**Purpose**: Adjust difficulty expectations based on child's developmental stage.

**Formula**:
```
T_age = T_base × (1 - β × e^(-age/λ))
```

Where:
- `T_age` = Age-adjusted threshold
- `T_base` = Base threshold (default 85%)
- `β` = Age sensitivity factor (0.4)
- `λ` = Age decay constant (5.0 years)
- `age` = Child's age in years

**Behavior**:
- Younger children (3-6 years): 60-70% threshold
- School-age children (7-12 years): 70-85% threshold
- Teenagers (13+ years): 85-95% threshold

**Example Calculations**:
```
Age 5:  85 × (1 - 0.4 × e^(-5/5))  ≈ 72.5%
Age 10: 85 × (1 - 0.4 × e^(-10/5)) ≈ 80.4%
Age 15: 85 × (1 - 0.4 × e^(-15/5)) ≈ 83.1%
```

---

### 3. Pattern Recognition for Repeated Mistakes

**Purpose**: Identify systematic errors and problematic movement patterns.

**Formula: Z-Score (Standard Score)**
```
Z = (x - μ) / σ
```

Where:
- `Z` = Standardized score
- `x` = Individual observation (landmark error)
- `μ` = Mean error across observations
- `σ` = Standard deviation of errors

**Detection Rule**:
- Pattern detected if `|Z| > threshold` (typically 2.0)
- Indicates observation is 2+ standard deviations from mean
- Multiple outliers suggest systematic issue

**Statistical Foundation**:
- Normal distribution: 95% of data within ±2σ
- Values beyond 2σ are statistically significant
- Repeated outliers indicate non-random pattern

**Implementation**:
```python
mean_error = np.mean(errors)
std_error = np.std(errors)
z_scores = (errors - mean_error) / std_error
outliers = np.where(np.abs(z_scores) > 2.0)[0]

if len(outliers) > threshold_count:
    pattern_detected = True
```

---

### 4. Session Comparison Algorithm

**Purpose**: Quantify improvement or decline between practice sessions.

**Formula: Cohen's d (Effect Size)**
```
d = (μ₁ - μ₂) / √((σ₁² + σ₂²) / 2)
```

Where:
- `d` = Cohen's d (effect size)
- `μ₁` = Mean of current session
- `μ₂` = Mean of previous session
- `σ₁²` = Variance of current session
- `σ₂²` = Variance of previous session

**Interpretation**:
- `|d| < 0.2`: Negligible change
- `0.2 ≤ |d| < 0.5`: Small effect
- `0.5 ≤ |d| < 0.8`: Medium effect
- `|d| ≥ 0.8`: Large effect

**Percentage Improvement**:
```
Improvement% = ((μ₁ - μ₂) / μ₂) × 100
```

**Example**:
```
Session 1: μ₁ = 85%, σ₁ = 8
Session 2: μ₂ = 75%, σ₂ = 10

Pooled SD = √((64 + 100) / 2) = 9.06
Cohen's d = (85 - 75) / 9.06 = 1.10 (Large improvement)
Improvement% = (85 - 75) / 75 × 100 = 13.3%
```

---

### 5. Improvement Trend Detection

**Purpose**: Identify long-term learning patterns and predict future performance.

**Formula: Linear Regression**

Slope:
```
m = Σ((xᵢ - x̄)(yᵢ - ȳ)) / Σ((xᵢ - x̄)²)
```

Intercept:
```
b = ȳ - m × x̄
```

Prediction:
```
y = mx + b
```

Where:
- `m` = Slope (rate of improvement)
- `b` = Y-intercept
- `xᵢ` = Session number
- `yᵢ` = Session accuracy
- `x̄`, `ȳ` = Means

**R² (Coefficient of Determination)**:
```
R² = 1 - (SS_res / SS_tot)

SS_res = Σ(yᵢ - ŷᵢ)²  (Residual sum of squares)
SS_tot = Σ(yᵢ - ȳ)²   (Total sum of squares)
```

**Interpretation**:
- `R² = 1.0`: Perfect linear fit
- `R² = 0.7-1.0`: Strong trend
- `R² = 0.3-0.7`: Moderate trend
- `R² < 0.3`: Weak/no trend

**Trend Classification**:
```
if |m| < 0.5:
    trend = "Stable"
elif m > 2.0 and R² > 0.5:
    trend = "Rapidly improving"
elif m > 0:
    trend = "Gradually improving"
elif m < -2.0 and R² > 0.5:
    trend = "Declining"
else:
    trend = "Slightly declining"
```

---

### 6. Consistency Score

**Purpose**: Measure performance stability across frames/sessions.

**Formula: Coefficient of Variation (CV)**
```
CV = (σ / μ) × 100

Consistency Score = 100 × (1 - min(CV/100, 1))
```

Where:
- `σ` = Standard deviation of accuracies
- `μ` = Mean accuracy
- `CV` = Coefficient of variation (%)

**Interpretation**:
- `Consistency ≥ 80%`: Excellent (very stable)
- `65% ≤ Consistency < 80%`: Good
- `50% ≤ Consistency < 65%`: Moderate
- `Consistency < 50%`: Poor (high variability)

**Example**:
```
Accuracies: [85, 87, 83, 86, 84, 88, 85]
Mean (μ) = 85.43
Std Dev (σ) = 1.72
CV = (1.72 / 85.43) × 100 = 2.01%
Consistency = 100 × (1 - 0.0201) = 97.99% (Excellent)
```

---

### 7. Weighted Performance Index (Composite Score)

**Purpose**: Combine multiple metrics into single comprehensive score.

**Formula**:
```
WPI = w₁×accuracy + w₂×consistency + w₃×improvement + w₄×pattern_score
```

Where: `Σwᵢ = 1` (weights sum to 1)

**Default Weights**:
- `w₁` (Accuracy): 0.35 (35%)
- `w₂` (Consistency): 0.25 (25%)
- `w₃` (Improvement): 0.25 (25%)
- `w₄` (Pattern Score): 0.15 (15%)

**Pattern Score Calculation**:
```
Pattern Score = 100 × (1 - outlier_percentage)

If patterns_detected:
    apply penalty = 0.9 (10% reduction)
```

**Example Calculation**:
```
Accuracy: 85%
Consistency: 75%
Improvement: +10% → normalized to 60/100
Pattern Score: 90% (10% outliers)

WPI = 0.35×85 + 0.25×75 + 0.25×60 + 0.15×90
    = 29.75 + 18.75 + 15.00 + 13.50
    = 77.0

Final Score = 77.0 × 1.0 (no pattern penalty) = 77
Grade: C
```

---

### 8. Confidence Score

**Purpose**: Indicate reliability of statistical measurements.

**Formula**:
```
C = (1 - CV) × √(n / (n + k))
```

Where:
- `C` = Confidence score (0-1)
- `CV` = Coefficient of variation
- `n` = Sample size (number of observations)
- `k` = Constant (typically 10)

**Properties**:
- Increases with sample size
- Decreases with high variability (CV)
- Asymptotically approaches (1 - CV) as n → ∞

**Example**:
```
n = 30 frames, CV = 0.15

C = (1 - 0.15) × √(30 / (30 + 10))
  = 0.85 × √(0.75)
  = 0.85 × 0.866
  = 0.736 (73.6% confidence)
```

---

### 9. Performance Velocity

**Purpose**: Measure rate of improvement during a session.

**Formula**:
```
v = Δaccuracy / Δtime
```

Where:
- `v` = Velocity (percentage points per second)
- `Δaccuracy` = Change in accuracy
- `Δtime` = Time elapsed (seconds)

**Classification**:
- `v > 0.05`: Rapidly improving
- `0 < v ≤ 0.05`: Gradually improving
- `|v| ≤ 0.01`: Stable
- `-0.05 ≤ v < 0`: Slightly declining
- `v < -0.05`: Declining

**Example**:
```
Initial accuracy: 70% at t=0
Final accuracy: 85% at t=300s

v = (85 - 70) / 300 = 0.05 %/sec
Trend: "Rapidly improving"
```

---

## Implementation Guide

### Backend Integration

1. **Install Dependencies**:
```bash
pip install numpy scipy
```

2. **Register Analytics Blueprint** in `app.py`:
```python
from routes.analytics import analytics

app.register_blueprint(analytics, url_prefix='/analytics')
```

3. **Update Session Completion** in `routes/session.py`:
```python
from utils.advanced_scoring import analyze_session_comprehensive

@session.route('/api/session/complete', methods=['POST'])
@login_required
def complete_session():
    # ... existing code ...

    # Perform advanced analysis
    analysis = analyze_session_comprehensive(session_id, db.session)

    # Store additional metrics
    score_entry = Score(
        session_id=session_id,
        accuracy_percentage=avg_accuracy,
        feedback=json.dumps(analysis.get('recommendations', []))
    )
    db.session.add(score_entry)
    db.session.commit()

    return jsonify({
        "status": "success",
        "analysis": analysis
    })
```

### Frontend Integration

1. **Import Advanced Scoring** in session template:
```html
<script type="module">
    import { AdvancedScoringSystem } from '/static/js/scoring_advanced.js';

    const scorer = new AdvancedScoringSystem(childAge);

    // Use in hand tracking loop
    function onHandsDetected(landmarks) {
        const accuracy = scorer.calculateAccuracy(landmarks);

        // Get real-time recommendations
        const recommendations = scorer.getRealtimeRecommendations();
        displayRecommendations(recommendations);

        // Update UI
        updateProgressDisplay(scorer.getSessionSummary());
    }
</script>
```

2. **Display Analytics Dashboard**:
```html
<!-- Session Summary -->
<div id="session-summary"></div>

<script>
    fetch(`/analytics/api/analytics/session/${sessionId}`)
        .then(r => r.json())
        .then(data => {
            document.getElementById('session-summary').innerHTML = `
                <div class="card">
                    <h5>Performance Analysis</h5>
                    <p>Composite Score: ${data.composite_score.composite_score}/100</p>
                    <p>Grade: ${data.composite_score.grade}</p>
                    <p>Consistency: ${data.consistency_score}%</p>
                    <p>Trend: ${data.trend_analysis.trend_direction}</p>
                </div>
            `;

            // Display recommendations
            displayRecommendations(data.recommendations);
        });
</script>
```

---

## API Endpoints

### 1. Session Analytics
```
GET /analytics/api/analytics/session/<session_id>
```
Returns comprehensive analysis for a session.

### 2. Child Overview
```
GET /analytics/api/analytics/child/<child_id>/overview?limit=10
```
Returns overall performance metrics and trends.

### 3. Personalized Recommendations
```
GET /analytics/api/analytics/child/<child_id>/recommendations
```
Returns AI-generated recommendations.

### 4. Progress Chart Data
```
GET /analytics/api/analytics/child/<child_id>/progress-chart?days=30&metric=accuracy
```
Returns data for visualization.

### 5. Compare Children
```
POST /analytics/api/analytics/compare-children
Body: { "child_ids": [1, 2], "metric": "accuracy" }
```
Compares performance across multiple children.

### 6. Export Analytics
```
GET /analytics/api/analytics/export/<child_id>
```
Exports complete analytics in JSON format.

---

## Example Usage

### Real-Time Scoring During Exercise

```javascript
import { AdvancedScoringSystem, formatRecommendations } from '/static/js/scoring_advanced.js';

// Initialize
const scorer = new AdvancedScoringSystem(childAge=8);

// In hand tracking callback
function processFrame(landmarks) {
    // Calculate accuracy with pattern detection
    const result = scorer.calculateAccuracy(landmarks);

    // Display smoothed accuracy
    document.getElementById('accuracy').textContent =
        result.smoothed.toFixed(1) + '%';

    // Get and display recommendations
    const recs = scorer.getRealtimeRecommendations();
    document.getElementById('recommendations').innerHTML =
        formatRecommendations(recs);

    // Check for patterns
    const patterns = scorer.detectErrorPatterns();
    if (patterns.detected) {
        console.log('Problematic landmarks:', patterns.problematicLandmarks);
    }
}

// On session end
function endSession() {
    const summary = scorer.getSessionSummary();

    console.log('Final Score:', summary.totalScore);
    console.log('Grade:', summary.grade);
    console.log('Consistency:', summary.consistency.score);
    console.log('Performance Trend:', summary.performance.trend);

    // Send to backend
    fetch('/api/session/complete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            session_id: sessionId,
            avg_accuracy: summary.averageAccuracy,
            total_score: summary.totalScore
        })
    });
}
```

### Backend Analysis After Session

```python
from utils.advanced_scoring import analyze_session_comprehensive

# Analyze completed session
analysis = analyze_session_comprehensive(session_id=123, db_session=db.session)

print(f"Composite Score: {analysis['composite_score']['composite_score']:.1f}")
print(f"Grade: {analysis['composite_score']['grade']}")
print(f"Dynamic Threshold: {analysis['dynamic_threshold']:.1f}%")
print(f"Consistency: {analysis['consistency_score']:.1f}%")

# Check for patterns
if analysis['pattern_analysis']['patterns_detected']:
    print("Detected issues with landmarks:",
          analysis['pattern_analysis']['problematic_landmarks'])

# Review recommendations
for rec in analysis['recommendations']:
    print(f"[{rec['priority']}] {rec['category']}: {rec['message']}")
    print(f"   Action: {rec['action']}")

# Trend analysis
trend = analysis['trend_analysis']
if trend['trend_available']:
    print(f"Trend: {trend['trend_direction']}")
    print(f"Slope: {trend['slope']:.3f}")
    print(f"R²: {trend['r_squared']:.3f}")
    print(f"Predicted next: {trend['predicted_next']:.1f}%")
```

---

## Performance Considerations

### Computational Complexity

- **EMA Calculation**: O(1) per frame
- **Pattern Detection**: O(n) for n frames
- **Linear Regression**: O(n) for n sessions
- **Session Comparison**: O(n) for n frames per session

### Memory Usage

- **Buffer Sizes**: 50-1000 frames (configurable)
- **Error Maps**: 21 landmarks × 50 errors = ~8KB
- **Session History**: Minimal (aggregate stats only)

### Optimization Tips

1. Use EMA instead of full moving average (saves memory)
2. Limit buffer sizes to recent data (50-100 frames)
3. Compute trends only on session completion (not real-time)
4. Cache analyzed sessions to avoid recomputation

---

## Validation and Testing

### Unit Tests

```python
import numpy as np
from utils.advanced_scoring import AdvancedScoringSystem

def test_dynamic_threshold():
    scorer_young = AdvancedScoringSystem(child_age=5)
    scorer_old = AdvancedScoringSystem(child_age=15)

    assert scorer_young.dynamic_threshold < scorer_old.dynamic_threshold
    assert 60 <= scorer_young.dynamic_threshold <= 75
    assert 80 <= scorer_old.dynamic_threshold <= 90

def test_ema_smoothing():
    scorer = AdvancedScoringSystem()

    # Test with noisy data
    values = [80, 90, 75, 85, 82]
    ema_values = [scorer.calculate_moving_average(v) for v in values]

    # EMA should be smoother than raw
    raw_variance = np.var(values)
    ema_variance = np.var(ema_values)
    assert ema_variance < raw_variance

def test_pattern_detection():
    scorer = AdvancedScoringSystem()

    # Create data with outliers
    normal_errors = [0.1] * 40
    abnormal_errors = [0.8] * 10
    all_errors = normal_errors + abnormal_errors

    result = scorer.detect_error_patterns(all_errors)
    assert result['patterns_detected'] == True
```

---

## Troubleshooting

### Common Issues

**Issue**: Trend analysis shows "Insufficient data"
- **Solution**: Ensure at least 3 completed sessions exist

**Issue**: Pattern detection always returns False
- **Solution**: Check that landmark_data is being properly stored as JSON

**Issue**: Recommendations are repetitive
- **Solution**: Implement recommendation history and diversification logic

**Issue**: Composite score is always low
- **Solution**: Verify weight distribution and normalize improvement metric correctly

---

## Future Enhancements

1. **Machine Learning Integration**:
   - Train predictive models for personalized difficulty adjustment
   - Use neural networks for advanced pattern recognition
   - Implement reinforcement learning for optimal exercise sequencing

2. **Multi-Modal Analysis**:
   - Incorporate gaze tracking data
   - Add audio feedback analysis
   - Include facial expression recognition

3. **Social Features**:
   - Peer comparison (anonymized)
   - Group challenges
   - Leaderboards with privacy controls

4. **Adaptive Algorithms**:
   - Real-time difficulty adjustment
   - Personalized weight optimization
   - Context-aware recommendations

---

## References

### Statistical Methods
1. Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences (2nd ed.)
2. Box, G. E. P., & Jenkins, G. M. (1976). Time Series Analysis: Forecasting and Control

### Signal Processing
3. Smith, S. W. (1997). The Scientist and Engineer's Guide to Digital Signal Processing

### Educational Psychology
4. Bloom, B. S. (1984). The 2 Sigma Problem: The Search for Methods of Group Instruction

---

## License

Copyright © 2026 BrainCoach AI. All rights reserved.
