# Advanced Scoring System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    BrainCoach AI Platform                        │
│                 Advanced Scoring & Analytics                     │
└─────────────────────────────────────────────────────────────────┘

                              ┌─────────┐
                              │  User   │
                              │ (Child) │
                              └────┬────┘
                                   │
                    ┌──────────────┴──────────────┐
                    ↓                             ↓
            ┌───────────────┐           ┌────────────────┐
            │  Web Browser  │           │  Hand Tracking │
            │   Interface   │←─────────→│   (MediaPipe)  │
            └───────┬───────┘           └────────┬───────┘
                    │                            │
                    │    Real-time Frames        │
                    │    + Landmarks Data        │
                    │                            │
                    ↓                            ↓
            ┌──────────────────────────────────────────┐
            │     Advanced Scoring System (JS)         │
            │  • EMA Smoothing                         │
            │  • Real-time Pattern Detection           │
            │  • Performance Velocity                  │
            │  • Live Recommendations                  │
            └──────────────┬───────────────────────────┘
                          │
                          │ Frame Data (every 10 frames)
                          ↓
            ┌──────────────────────────────────┐
            │      Flask Backend (Python)       │
            │  routes/session.py               │
            │  • Session Management            │
            │  • Frame Storage                 │
            │  • Completion Triggers           │
            └──────────────┬───────────────────┘
                          │
                          │ Session Complete
                          ↓
            ┌──────────────────────────────────┐
            │  Advanced Scoring Engine (Python) │
            │  utils/advanced_scoring.py       │
            │  • Comprehensive Analysis        │
            │  • Multi-algorithm Processing    │
            │  • Recommendation Generation     │
            └──────────────┬───────────────────┘
                          │
                ┌─────────┴─────────┐
                ↓                   ↓
    ┌────────────────────┐  ┌──────────────────┐
    │   Database         │  │   Analytics API   │
    │   (SQLite)         │  │  routes/analytics │
    │  • Sessions        │  │  • Overview       │
    │  • Frames          │  │  • Trends         │
    │  • Patterns        │  │  • Comparisons    │
    │  • Trends          │  │  • Export         │
    │  • Recommendations │  └──────────┬────────┘
    └────────────────────┘            │
                                      │
                          ┌───────────┴──────────┐
                          ↓                      ↓
                  ┌───────────────┐      ┌──────────────┐
                  │   Dashboard   │      │  PDF Reports │
                  │   Visualizations│     │  Generation  │
                  └───────────────┘      └──────────────┘
```

---

## Data Flow Diagram

### Phase 1: Real-time Session Processing

```
Frame N → Landmark Detection → Advanced Scoring JS
                                        ↓
                        ┌───────────────┴────────────────┐
                        │                                │
                        ↓                                ↓
            Calculate Accuracy              Detect Patterns
            (with smoothing)                (Z-Score Analysis)
                        │                                │
                        └───────────────┬────────────────┘
                                       ↓
                        Update UI with Real-time Feedback
                                       ↓
                        Every 10th frame → Send to Backend
```

### Phase 2: Session Completion Analysis

```
Session Complete Event
        ↓
Retrieve All Frames (N frames)
        ↓
┌───────────────────────────────────────────────┐
│      Advanced Scoring Engine                  │
│                                               │
│  1. Moving Average Smoothing                  │
│     Input: Raw accuracies [N values]          │
│     Output: Smoothed accuracies [N values]    │
│     Formula: EMA_t = α×X_t + (1-α)×EMA_(t-1) │
│                                               │
│  2. Dynamic Threshold Calculation             │
│     Input: Child age                          │
│     Output: Age-adjusted threshold            │
│     Formula: T = T_base × (1 - β×e^(-age/λ))  │
│                                               │
│  3. Pattern Recognition                       │
│     Input: Landmark errors                    │
│     Output: Problematic landmarks + confidence│
│     Formula: Z = (x - μ) / σ                  │
│                                               │
│  4. Session Comparison                        │
│     Input: Current + Previous sessions        │
│     Output: Effect size + improvement %       │
│     Formula: d = (μ₁-μ₂) / σ_pooled          │
│                                               │
│  5. Trend Detection                           │
│     Input: Historical session accuracies      │
│     Output: Slope, R², trend direction        │
│     Formula: m = Σ((x-x̄)(y-ȳ))/Σ((x-x̄)²)    │
│                                               │
│  6. Consistency Score                         │
│     Input: Accuracy values                    │
│     Output: Consistency percentage            │
│     Formula: 100×(1 - σ/μ)                    │
│                                               │
│  7. Composite Score                           │
│     Input: All metrics                        │
│     Output: Weighted score + grade            │
│     Formula: Σ(wᵢ × metricᵢ)                  │
│                                               │
│  8. Recommendation Generation                 │
│     Input: Complete analysis                  │
│     Output: Personalized recommendations      │
│     Logic: Rule-based + heuristic             │
└───────────────────────────────────────────────┘
        ↓
Store Results in Database
        ↓
Return Analysis to Frontend
        ↓
Display Summary + Recommendations
```

---

## Component Interaction Matrix

| Component | Inputs | Outputs | Dependencies |
|-----------|--------|---------|--------------|
| **Hand Tracking** | Video frames | 21 landmarks (x,y,z) | MediaPipe |
| **JS Scoring** | Landmarks | Accuracy, patterns | None |
| **Backend Session** | Frame data | Session ID | Flask, SQLAlchemy |
| **Advanced Engine** | Session ID | Complete analysis | NumPy |
| **Analytics API** | Child/Session ID | Formatted metrics | Advanced Engine |
| **Database** | Analysis results | Stored data | SQLite |
| **Dashboard** | User ID | Visualizations | Analytics API |

---

## Algorithm Processing Pipeline

```
                    ┌──────────────┐
                    │  Raw Data    │
                    │  Collection  │
                    └──────┬───────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────┐
│                 PRE-PROCESSING                      │
│  • Remove null values                               │
│  • Validate data ranges                             │
│  • Convert formats                                  │
└─────────────────────┬───────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          ↓                       ↓
┌──────────────────┐    ┌──────────────────┐
│  REAL-TIME       │    │  BATCH           │
│  PROCESSING      │    │  PROCESSING      │
│                  │    │                  │
│  • EMA           │    │  • Pattern Rec   │
│  • Velocity      │    │  • Trend         │
│  • Live Recs     │    │  • Comparison    │
└────────┬─────────┘    └────────┬─────────┘
         │                       │
         └───────────┬───────────┘
                     ↓
         ┌─────────────────────┐
         │   AGGREGATION       │
         │  • Consistency      │
         │  • Composite Score  │
         │  • Final Grade      │
         └──────────┬──────────┘
                    │
                    ↓
         ┌─────────────────────┐
         │  POST-PROCESSING    │
         │  • Recommendations  │
         │  • Visualization    │
         │  • Report Gen       │
         └─────────────────────┘
```

---

## Database Schema

```
┌─────────────────────────────────────────────────────┐
│                    parent                            │
│  id, name, email, password_hash, phone, created_at  │
└─────────────────┬───────────────────────────────────┘
                  │ 1:N
                  ↓
┌─────────────────────────────────────────────────────┐
│                    child                             │
│  id, parent_id, name, age, grade, enrolled_date     │
└─────────────────┬───────────────────────────────────┘
                  │ 1:N
         ┌────────┴────────┐
         ↓                 ↓
┌─────────────────┐   ┌────────────────────┐
│    session      │   │  trend_analysis    │
│  • Basic info   │   │  • slope           │
│  • Scores       │   │  • r_squared       │
│  • Advanced ──┐ │   │  • trend_direction │
│    metrics    │ │   └────────────────────┘
└───────┬───────┘ │
        │ 1:N     │
        ↓         │
┌──────────────┐  │
│   frame      │  │
│  • number    │  │
│  • landmarks │  │
│  • accuracy  │  │
└──────────────┘  │
        │         │
        │ 1:N     │
        ↓         │
┌──────────────────┐
│  pattern_detect  │
│  • landmark_idx  │◄──┘
│  • error_stats   │
│  • anomalies     │
└──────────────────┘
        │
        │ 1:N
        ↓
┌────────────────────┐
│  recommendation    │
│  • category        │
│  • priority        │
│  • message         │
│  • action          │
└────────────────────┘
```

---

## API Endpoint Architecture

```
                    ┌──────────────┐
                    │    Client    │
                    │  (Browser)   │
                    └──────┬───────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ↓                  ↓                  ↓
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Session    │   │  Analytics   │   │  Dashboard   │
│   Endpoints  │   │  Endpoints   │   │  Endpoints   │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                  │
       │                  │                  │
       ↓                  ↓                  ↓

/api/session/          /analytics/api/       /dashboard/
  ├─ update              ├─ session/:id       ├─ index
  └─ complete            ├─ child/:id/        └─ child/:id
                         │  ├─ overview
                         │  ├─ recommendations
                         │  ├─ progress-chart
                         │  └─ export
                         └─ compare-children
```

### Endpoint Details

**Session Management**
```
POST /api/session/update
  Input: { session_id, frame_number, accuracy, landmarks }
  Output: { status: "success" }
  Purpose: Save frame data during session

POST /api/session/complete
  Input: { session_id, avg_accuracy, total_score }
  Output: { status, analysis, redirect }
  Purpose: Finalize session + run analysis
```

**Analytics**
```
GET /analytics/api/analytics/session/:session_id
  Output: Complete analysis with all metrics
  Purpose: Detailed session breakdown

GET /analytics/api/analytics/child/:child_id/overview?limit=10
  Output: Historical performance summary
  Purpose: Long-term progress tracking

GET /analytics/api/analytics/child/:child_id/recommendations
  Output: Personalized recommendations
  Purpose: AI-generated guidance

GET /analytics/api/analytics/child/:child_id/progress-chart
  Output: Chart data (labels, values, trend)
  Purpose: Visualization support

POST /analytics/api/analytics/compare-children
  Input: { child_ids: [1,2], metric: "accuracy" }
  Output: Comparison data
  Purpose: Multi-child analysis

GET /analytics/api/analytics/export/:child_id
  Output: Complete data export (JSON)
  Purpose: Backup/external analysis
```

---

## Mathematical Formula Flow

### Session Scoring Flow

```
                    Raw Landmarks
                          ↓
                    Distance Calc
                d = √((x₁-x₂)² + (y₁-y₂)²)
                          ↓
                    Accuracy Calc
                A = 100×(1 - D_avg×2)
                          ↓
                    EMA Smoothing
            EMA = α×A + (1-α)×EMA_prev
                          ↓
                    Store Frame
                          ↓
              ╔═══════════════════════╗
              ║   Session Complete    ║
              ╚═══════════════════════╝
                          ↓
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                 ↓
  Consistency       Pattern Detect      Trend
  CV = σ/μ          Z = (x-μ)/σ        m = slope
        │                 │                 │
        └─────────────────┴─────────────────┘
                          ↓
                  Composite Score
        WPI = Σ(wᵢ × metricᵢ)
                          ↓
                    Grade + Recs
```

---

## Performance Optimization Strategy

### 1. Real-time Processing
```
Frame Rate: 30 FPS
  ↓
Process every frame: Accuracy calculation (< 1ms)
  ↓
Store every 10th frame: Database write (< 5ms)
  ↓
Pattern check every 30 frames: Statistics (< 10ms)
  ↓
Total overhead: < 2% of frame time
```

### 2. Batch Analysis
```
Session End Trigger
  ↓
Fetch all frames (single query) - 50-500ms
  ↓
NumPy vectorized operations - 10-50ms per algorithm
  ↓
Total analysis time: < 1 second for 1000 frames
```

### 3. Caching Strategy
```
┌─────────────────────────────────────┐
│  Cache Layer (Redis/Memory)         │
│  • Child analytics (TTL: 5 min)     │
│  • Trend analysis (TTL: 1 hour)     │
│  • Recommendations (TTL: 1 day)     │
└─────────────────────────────────────┘
         ↓ (on cache miss)
┌─────────────────────────────────────┐
│  Database Query + Computation       │
└─────────────────────────────────────┘
```

---

## Error Handling & Validation

```
User Input
    ↓
┌─────────────────┐
│  Validation     │
│  • Type check   │
│  • Range check  │
│  • Auth check   │
└────┬────────────┘
     │
     ├─ Valid → Process
     │
     └─ Invalid → Return error (400/403)
         ↓
    Process Data
         ↓
    ┌───────────────┐
    │  Try/Catch    │
    │  • Database   │
    │  • Math ops   │
    │  • File I/O   │
    └───┬───────────┘
        │
        ├─ Success → Return result (200)
        │
        └─ Error → Log + Return error (500)
                    ↓
            Rollback transaction
```

---

## Deployment Architecture

### Development
```
┌──────────────────┐
│  Local Machine   │
│  • Flask dev     │
│  • SQLite        │
│  • Port 5000     │
└──────────────────┘
```

### Production
```
┌─────────────────────────────────────────┐
│           Load Balancer                 │
└───────────────┬─────────────────────────┘
                │
    ┌───────────┴──────────┐
    ↓                      ↓
┌─────────┐          ┌─────────┐
│ Web 1   │          │ Web 2   │
│ Gunicorn│          │ Gunicorn│
│ Flask   │          │ Flask   │
└────┬────┘          └────┬────┘
     │                    │
     └──────────┬─────────┘
                ↓
        ┌───────────────┐
        │  PostgreSQL   │
        │  or MySQL     │
        └───────────────┘
                │
                ↓
        ┌───────────────┐
        │   S3/Storage  │
        │  PDF Reports  │
        └───────────────┘
```

---

## Security Considerations

```
┌─────────────────────────────────────────┐
│         Security Layers                 │
├─────────────────────────────────────────┤
│ 1. Authentication (Flask-Login)         │
│    • Session management                 │
│    • Password hashing                   │
├─────────────────────────────────────────┤
│ 2. Authorization                        │
│    • Parent-child relationship check    │
│    • Session ownership verification     │
├─────────────────────────────────────────┤
│ 3. Input Validation                     │
│    • Type checking                      │
│    • Range validation                   │
│    • SQL injection prevention           │
├─────────────────────────────────────────┤
│ 4. Data Privacy                         │
│    • No PII in URLs                     │
│    • Encrypted sensitive data           │
│    • GDPR compliance                    │
├─────────────────────────────────────────┤
│ 5. Rate Limiting                        │
│    • API request throttling             │
│    • Prevent abuse                      │
└─────────────────────────────────────────┘
```

---

## Testing Strategy

```
┌──────────────────────────────────────┐
│         Unit Tests                   │
│  • Individual formulas               │
│  • Edge cases                        │
│  • Input validation                  │
└────────────────┬─────────────────────┘
                 ↓
┌──────────────────────────────────────┐
│      Integration Tests               │
│  • API endpoints                     │
│  • Database operations               │
│  • End-to-end flows                  │
└────────────────┬─────────────────────┘
                 ↓
┌──────────────────────────────────────┐
│      Performance Tests               │
│  • Load testing                      │
│  • Stress testing                    │
│  • Bottleneck identification         │
└────────────────┬─────────────────────┘
                 ↓
┌──────────────────────────────────────┐
│         User Testing                 │
│  • Usability testing                 │
│  • A/B testing                       │
│  • Feedback collection               │
└──────────────────────────────────────┘
```

---

## Future Enhancements Roadmap

```
Phase 1: Current (MVP)
  ✓ Basic scoring
  ✓ Advanced algorithms
  ✓ Real-time feedback
  ✓ Analytics API

Phase 2: ML Integration
  • Train predictive models
  • Personalized difficulty
  • Smart recommendations
  • Anomaly detection ML

Phase 3: Multi-modal
  • Gaze tracking
  • Facial expressions
  • Voice feedback
  • Combined analysis

Phase 4: Social Features
  • Peer comparison
  • Challenges/goals
  • Gamification
  • Parent community

Phase 5: AI Assistant
  • Natural language feedback
  • Conversational interface
  • Adaptive coaching
  • Progress narratives
```

---

**Document Version:** 1.0
**Last Updated:** 2026-02-17
**Maintained By:** BrainCoach AI Development Team
