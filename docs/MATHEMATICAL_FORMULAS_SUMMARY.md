# Mathematical Formulas Summary

## Complete Reference of All Formulas Used in Advanced Scoring System

---

## 1. Moving Average Smoothing

### Exponential Moving Average (EMA)

```
EMA_t = α × X_t + (1 - α) × EMA_(t-1)
```

**Parameters:**
- `α` = Smoothing factor = 0.3 (default)
- `X_t` = Current observation at time t
- `EMA_(t-1)` = Previous EMA value

**Alternative form:**
```
α = 2 / (N + 1)
```
where N = window size

---

## 2. Dynamic Threshold Based on Age

### Age-Adjusted Threshold

```
T_age = T_base × (1 - β × e^(-age/λ))
```

**Parameters:**
- `T_base` = Base threshold = 85%
- `β` = Age sensitivity factor = 0.4
- `λ` = Age decay constant = 5.0 years
- `age` = Child's age in years

**Constraints:**
```
T_age ∈ [60, 95]  (clamped to range)
```

---

## 3. Pattern Recognition

### Z-Score (Standardized Score)

```
Z = (x - μ) / σ
```

**Where:**
- `x` = Individual observation
- `μ` = Population mean
- `σ` = Population standard deviation

### Mean Calculation
```
μ = (Σ xᵢ) / n
```

### Standard Deviation
```
σ = √(Σ(xᵢ - μ)² / n)
```

### Variance
```
σ² = Σ(xᵢ - μ)² / n
```

### Pattern Detection Rule
```
Pattern detected if |Z| > threshold

where threshold = 2.0 (default)
```

---

## 4. Session Comparison

### Cohen's d (Effect Size)

```
d = (μ₁ - μ₂) / σ_pooled
```

**Where:**
```
σ_pooled = √((σ₁² + σ₂²) / 2)
```

**Parameters:**
- `μ₁` = Mean of current session
- `μ₂` = Mean of previous session
- `σ₁` = Standard deviation of current session
- `σ₂` = Standard deviation of previous session

### Improvement Percentage
```
Improvement% = ((μ₁ - μ₂) / μ₂) × 100
```

### Effect Size Interpretation

| Cohen's d | Interpretation |
|-----------|----------------|
| \|d\| < 0.2 | Negligible |
| 0.2 ≤ \|d\| < 0.5 | Small |
| 0.5 ≤ \|d\| < 0.8 | Medium |
| \|d\| ≥ 0.8 | Large |

---

## 5. Improvement Trend Detection

### Linear Regression

**Slope:**
```
m = Σ((xᵢ - x̄)(yᵢ - ȳ)) / Σ((xᵢ - x̄)²)
```

**Intercept:**
```
b = ȳ - m × x̄
```

**Prediction:**
```
ŷ = mx + b
```

### Means
```
x̄ = Σxᵢ / n

ȳ = Σyᵢ / n
```

### Coefficient of Determination (R²)

```
R² = 1 - (SS_res / SS_tot)
```

**Where:**
```
SS_res = Σ(yᵢ - ŷᵢ)²   (Residual sum of squares)

SS_tot = Σ(yᵢ - ȳ)²    (Total sum of squares)
```

### R² Interpretation

| R² Value | Strength |
|----------|----------|
| 0.7 - 1.0 | Strong |
| 0.3 - 0.7 | Moderate |
| 0.0 - 0.3 | Weak |

---

## 6. Consistency Score

### Coefficient of Variation

```
CV = (σ / μ) × 100
```

### Consistency Score
```
Consistency = 100 × (1 - min(CV/100, 1))
```

**Range:** [0, 100]

**Interpretation:**

| Score | Interpretation |
|-------|----------------|
| ≥ 80 | Excellent |
| 65-79 | Good |
| 50-64 | Moderate |
| < 50 | Poor |

---

## 7. Composite Score (Weighted Performance Index)

### Weighted Sum

```
WPI = Σ(wᵢ × metricᵢ)
```

**Expanded:**
```
WPI = w₁×accuracy + w₂×consistency + w₃×improvement + w₄×pattern_score
```

**Constraint:**
```
Σwᵢ = 1
```

### Default Weights

| Metric | Weight | Percentage |
|--------|--------|------------|
| Accuracy | 0.35 | 35% |
| Consistency | 0.25 | 25% |
| Improvement | 0.25 | 25% |
| Pattern Score | 0.15 | 15% |

### Pattern Penalty
```
Final Score = WPI × penalty_factor

where penalty_factor = 0.9 if patterns detected, else 1.0
```

### Pattern Score
```
Pattern Score = 100 × (1 - outlier_percentage)
```

### Improvement Normalization
```
improvement_normalized = max(0, min(100, 50 + improvement_percentage))
```

---

## 8. Confidence Score

### Statistical Confidence

```
C = (1 - CV) × √(n / (n + k))
```

**Parameters:**
- `CV` = Coefficient of variation
- `n` = Sample size
- `k` = Constant (typically 10)

**Properties:**
```
lim(n→∞) C = 1 - CV

C ∈ [0, 1]
```

---

## 9. Performance Velocity

### Rate of Change

```
v = Δaccuracy / Δtime
```

**Where:**
```
Δaccuracy = accuracy_final - accuracy_initial

Δtime = time_final - time_initial (in seconds)
```

**Units:** Percentage points per second (%/s)

### Velocity Classification

| Velocity (v) | Trend |
|--------------|-------|
| v > 0.05 | Rapidly improving |
| 0 < v ≤ 0.05 | Gradually improving |
| \|v\| ≤ 0.01 | Stable |
| -0.05 ≤ v < 0 | Slightly declining |
| v < -0.05 | Declining |

---

## 10. Distance Metrics

### Euclidean Distance (2D)

```
d = √((x₁ - x₂)² + (y₁ - y₂)²)
```

### Euclidean Distance (3D with weighting)

```
d = √((x₁ - x₂)² + (y₁ - y₂)² + w×(z₁ - z₂)²)
```

where `w` = depth weight (typically 0.5)

### Total Distance (Multiple Points)

```
D_total = Σ dᵢ
```

### Average Distance

```
D_avg = D_total / n
```

---

## 11. Accuracy Calculation

### Distance-to-Accuracy Conversion

```
Accuracy = max(0, 100 × (1 - D_avg × scale_factor))
```

where `scale_factor` = 2.0 (default)

### Match Rate

```
Match Rate = (frames_above_threshold / total_frames) × 100
```

---

## 12. Grading System

### Letter Grade Assignment

```
Grade(score) = {
    'A'  if score ≥ 90
    'B'  if 80 ≤ score < 90
    'C'  if 70 ≤ score < 80
    'D'  if 60 ≤ score < 70
    'F'  if score < 60
}
```

---

## 13. Rolling Statistics

### Rolling Mean (Window Size n)

```
μ_rolling(t) = (Σ xᵢ) / n    for i ∈ [t-n+1, t]
```

### Rolling Variance

```
σ²_rolling(t) = (Σ(xᵢ - μ_rolling)²) / n
```

### Rolling Standard Deviation

```
σ_rolling(t) = √(σ²_rolling(t))
```

---

## 14. Anomaly Detection

### Anomaly Score

```
A = |x - μ_rolling| / σ_rolling
```

### Anomaly Rate

```
Anomaly Rate = (count(A > threshold) / n) × 100
```

where threshold = 2.0 (default for 95% confidence)

---

## 15. Duration Calculations

### Session Duration (in seconds)

```
Duration = (t_end - t_start)
```

### Practice Hours

```
Hours = Duration / 3600
```

### Duration in Days (for database timestamp)

```
Days = JULIANDAY(t_end) - JULIANDAY(t_start)
```

---

## 16. Normalization

### Min-Max Normalization

```
x_norm = (x - x_min) / (x_max - x_min)
```

**Result range:** [0, 1]

### Z-Score Normalization

```
x_norm = (x - μ) / σ
```

**Result:** Mean = 0, Std Dev = 1

---

## 17. Percentage Calculations

### Percentage Change

```
% Change = ((new_value - old_value) / old_value) × 100
```

### Percentage of Total

```
% of Total = (part / whole) × 100
```

---

## 18. Time Series Analysis

### Moving Average (Simple)

```
MA(t) = (1/n) × Σ xᵢ    for i ∈ [t-n+1, t]
```

### Weighted Moving Average

```
WMA(t) = (Σ(wᵢ × xᵢ)) / (Σ wᵢ)
```

---

## 19. Correlation

### Pearson Correlation Coefficient

```
r = Σ((xᵢ - x̄)(yᵢ - ȳ)) / √(Σ(xᵢ - x̄)² × Σ(yᵢ - ȳ)²)
```

**Range:** [-1, 1]
- r = 1: Perfect positive correlation
- r = 0: No correlation
- r = -1: Perfect negative correlation

---

## 20. Sample Statistics

### Sample Mean

```
x̄ = Σxᵢ / n
```

### Sample Variance (Unbiased)

```
s² = Σ(xᵢ - x̄)² / (n - 1)
```

### Sample Standard Deviation

```
s = √s²
```

### Standard Error

```
SE = s / √n
```

---

## Quick Reference Table

| Formula | Purpose | Key Parameters |
|---------|---------|----------------|
| EMA | Smoothing | α = 0.3 |
| T_age | Age adjustment | β = 0.4, λ = 5.0 |
| Z-Score | Pattern detection | threshold = 2.0 |
| Cohen's d | Effect size | Pooled SD |
| Linear Reg | Trend detection | m (slope), R² |
| CV | Consistency | σ/μ |
| WPI | Composite score | Σwᵢ = 1 |
| Confidence | Reliability | n, k = 10 |
| Velocity | Rate of change | %/second |

---

## Implementation Notes

### Numerical Stability

**Avoid division by zero:**
```python
if denominator == 0:
    return default_value
```

**Check for valid data:**
```python
if len(data) < min_required:
    return {'error': 'Insufficient data'}
```

### Floating Point Precision

**Round for display:**
```python
result = round(value, 2)  # 2 decimal places
```

**Use epsilon for comparisons:**
```python
EPSILON = 1e-10
if abs(x - y) < EPSILON:
    # Consider equal
```

---

## References

1. **Statistical Methods**: Howell, D. C. (2012). Statistical Methods for Psychology
2. **Effect Sizes**: Cohen, J. (1988). Statistical Power Analysis
3. **Time Series**: Box, G. E. P., & Jenkins, G. M. (1976). Time Series Analysis
4. **Signal Processing**: Smith, S. W. (1997). Digital Signal Processing

---

**Document Version:** 1.0
**Last Updated:** 2026-02-17
**Author:** BrainCoach AI Development Team
