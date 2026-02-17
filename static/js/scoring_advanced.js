/**
 * Advanced Scoring System - Client Side
 * =====================================
 *
 * Real-time implementation of advanced scoring algorithms for immediate feedback.
 *
 * Mathematical Formulas Used:
 * ===========================
 *
 * 1. EXPONENTIAL MOVING AVERAGE (EMA):
 *    EMA_t = α × X_t + (1 - α) × EMA_(t-1)
 *    where α = smoothing factor (0.3 for responsive smoothing)
 *
 * 2. REAL-TIME PATTERN DETECTION:
 *    Rolling variance: Var = E[X²] - (E[X])²
 *    Anomaly score: A = |X - μ_rolling| / σ_rolling
 *
 * 3. CONSISTENCY METRIC:
 *    Consistency = 100 × (1 - CV)
 *    where CV = σ / μ (coefficient of variation)
 *
 * 4. ADAPTIVE THRESHOLD:
 *    T = T_base × (1 - β × e^(-age/λ))
 *    Dynamically adjusted based on child's age
 *
 * 5. PERFORMANCE VELOCITY:
 *    v = Δaccuracy / Δtime
 *    Measures rate of improvement during session
 */

export class AdvancedScoringSystem {
    constructor(childAge = 10, baseThreshold = 85) {
        // Age-based configuration
        this.childAge = childAge;
        this.baseThreshold = baseThreshold;
        this.dynamicThreshold = this.calculateDynamicThreshold();

        // EMA parameters
        this.emaAlpha = 0.3;  // Smoothing factor
        this.currentEMA = null;
        this.emaHistory = [];

        // Statistics tracking
        this.totalFrames = 0;
        this.matchedFrames = 0;
        this.accuracySum = 0;
        this.accuracyHistory = [];
        this.errorBuffer = [];
        this.maxBufferSize = 50;

        // Pattern detection
        this.landmarkErrorMap = new Map(); // Track errors per landmark
        this.patternThreshold = 2.0; // Z-score threshold

        // Performance tracking
        this.sessionStartTime = Date.now();
        this.performanceSnapshots = [];

        // Target landmarks (can be customized per exercise)
        this.targetLandmarks = Array(21).fill(0).map(() => ({
            x: 0.5,
            y: 0.5,
            z: 0
        }));
    }

    /**
     * Calculate age-adjusted difficulty threshold
     * Formula: T_age = T_base × (1 - β × e^(-age/λ))
     */
    calculateDynamicThreshold() {
        const beta = 0.4;  // Age sensitivity
        const lambda = 5.0;  // Decay constant

        const ageFactor = 1 - beta * Math.exp(-this.childAge / lambda);
        const threshold = this.baseThreshold * ageFactor;

        // Clamp between 60 and 95
        return Math.max(60, Math.min(95, threshold));
    }

    /**
     * Calculate accuracy with landmark-specific error tracking
     * Enhanced version of basic distance calculation
     */
    calculateAccuracy(landmarks) {
        if (!landmarks || landmarks.length !== 21) return 0;

        let totalDistance = 0;
        const landmarkErrors = [];

        landmarks.forEach((point, index) => {
            const target = this.targetLandmarks[index];
            const dist = Math.sqrt(
                Math.pow(point.x - target.x, 2) +
                Math.pow(point.y - target.y, 2) +
                Math.pow(point.z - target.z, 2) * 0.5  // Z has less weight
            );

            totalDistance += dist;
            landmarkErrors.push({ index, error: dist });

            // Track errors per landmark for pattern detection
            if (!this.landmarkErrorMap.has(index)) {
                this.landmarkErrorMap.set(index, []);
            }
            this.landmarkErrorMap.get(index).push(dist);

            // Keep buffer size manageable
            const errors = this.landmarkErrorMap.get(index);
            if (errors.length > this.maxBufferSize) {
                errors.shift();
            }
        });

        // Convert distance to accuracy (inverse relationship)
        const avgDist = totalDistance / 21;
        const rawAccuracy = Math.max(0, 100 * (1 - avgDist * 2));

        // Apply EMA smoothing
        const smoothedAccuracy = this.applyEMA(rawAccuracy);

        // Update statistics
        this.updateStats(smoothedAccuracy, rawAccuracy, landmarkErrors);

        return {
            raw: rawAccuracy,
            smoothed: smoothedAccuracy,
            landmarkErrors: landmarkErrors
        };
    }

    /**
     * Apply Exponential Moving Average for smoothing
     * Formula: EMA_t = α × X_t + (1 - α) × EMA_(t-1)
     */
    applyEMA(newValue) {
        if (this.currentEMA === null) {
            this.currentEMA = newValue;
        } else {
            this.currentEMA = this.emaAlpha * newValue +
                             (1 - this.emaAlpha) * this.currentEMA;
        }

        this.emaHistory.push(this.currentEMA);
        return this.currentEMA;
    }

    /**
     * Update statistics with new frame data
     */
    updateStats(smoothedAccuracy, rawAccuracy, landmarkErrors) {
        this.totalFrames++;
        this.accuracySum += smoothedAccuracy;
        this.accuracyHistory.push(smoothedAccuracy);

        // Limit history size
        if (this.accuracyHistory.length > 1000) {
            this.accuracyHistory.shift();
        }

        if (smoothedAccuracy >= this.dynamicThreshold) {
            this.matchedFrames++;
        }

        // Store performance snapshot every 30 frames
        if (this.totalFrames % 30 === 0) {
            this.performanceSnapshots.push({
                timestamp: Date.now(),
                accuracy: smoothedAccuracy,
                frameNumber: this.totalFrames
            });
        }
    }

    /**
     * Detect patterns in landmark errors using rolling statistics
     * Formula: Z = (x - μ) / σ
     */
    detectErrorPatterns() {
        const problematicLandmarks = [];

        this.landmarkErrorMap.forEach((errors, landmarkIndex) => {
            if (errors.length < 10) return;

            // Calculate mean and std
            const mean = errors.reduce((a, b) => a + b, 0) / errors.length;
            const variance = errors.reduce((sum, val) =>
                sum + Math.pow(val - mean, 2), 0) / errors.length;
            const std = Math.sqrt(variance);

            if (std === 0) return;

            // Count anomalies (z-score > threshold)
            let anomalyCount = 0;
            errors.forEach(error => {
                const zScore = Math.abs((error - mean) / std);
                if (zScore > this.patternThreshold) {
                    anomalyCount++;
                }
            });

            // If more than 30% are anomalies, mark as problematic
            const anomalyRate = anomalyCount / errors.length;
            if (anomalyRate > 0.3) {
                problematicLandmarks.push({
                    landmarkIndex,
                    anomalyRate,
                    meanError: mean,
                    stdError: std
                });
            }
        });

        return {
            detected: problematicLandmarks.length > 0,
            problematicLandmarks,
            totalLandmarksAnalyzed: this.landmarkErrorMap.size
        };
    }

    /**
     * Calculate consistency score
     * Formula: Consistency = 100 × (1 - CV)
     * where CV = σ / μ (coefficient of variation)
     */
    calculateConsistencyScore() {
        if (this.accuracyHistory.length < 10) {
            return { score: 50, interpretation: 'Insufficient data' };
        }

        const mean = this.accuracyHistory.reduce((a, b) => a + b, 0) /
                    this.accuracyHistory.length;

        const variance = this.accuracyHistory.reduce((sum, val) =>
            sum + Math.pow(val - mean, 2), 0) / this.accuracyHistory.length;

        const std = Math.sqrt(variance);

        if (mean === 0) {
            return { score: 0, interpretation: 'No valid data' };
        }

        // Coefficient of variation
        const cv = std / mean;

        // Consistency score (lower CV = higher consistency)
        const consistencyScore = 100 * (1 - Math.min(cv, 1));

        let interpretation;
        if (consistencyScore >= 80) {
            interpretation = 'Excellent consistency';
        } else if (consistencyScore >= 65) {
            interpretation = 'Good consistency';
        } else if (consistencyScore >= 50) {
            interpretation = 'Moderate consistency';
        } else {
            interpretation = 'Inconsistent performance';
        }

        return {
            score: consistencyScore,
            interpretation,
            coefficientOfVariation: cv,
            mean,
            std
        };
    }

    /**
     * Calculate performance velocity (rate of improvement)
     * Formula: v = Δaccuracy / Δtime
     */
    calculatePerformanceVelocity() {
        if (this.performanceSnapshots.length < 2) {
            return { velocity: 0, trend: 'Insufficient data' };
        }

        const snapshots = this.performanceSnapshots;
        const first = snapshots[0];
        const last = snapshots[snapshots.length - 1];

        const accuracyDelta = last.accuracy - first.accuracy;
        const timeDelta = (last.timestamp - first.timestamp) / 1000; // seconds

        const velocity = accuracyDelta / timeDelta;

        let trend;
        if (Math.abs(velocity) < 0.01) {
            trend = 'Stable';
        } else if (velocity > 0.05) {
            trend = 'Rapidly improving';
        } else if (velocity > 0) {
            trend = 'Gradually improving';
        } else if (velocity < -0.05) {
            trend = 'Declining';
        } else {
            trend = 'Slightly declining';
        }

        return {
            velocity,
            trend,
            accuracyChange: accuracyDelta,
            timeElapsed: timeDelta
        };
    }

    /**
     * Get average accuracy (smoothed)
     */
    getAverageAccuracy() {
        return this.totalFrames > 0 ? this.accuracySum / this.totalFrames : 0;
    }

    /**
     * Calculate total score with enhanced weighting
     * Incorporates consistency and pattern recognition
     */
    getTotalScore() {
        const avgAccuracy = this.getAverageAccuracy();
        const matchRate = this.matchedFrames / (this.totalFrames || 1);
        const consistency = this.calculateConsistencyScore();
        const patterns = this.detectErrorPatterns();

        // Weighted scoring
        const weights = {
            accuracy: 0.40,
            matchRate: 0.30,
            consistency: 0.20,
            patterns: 0.10
        };

        // Pattern penalty (reduce score if problems detected)
        const patternPenalty = patterns.detected ?
            0.9 : 1.0; // 10% penalty for detected patterns

        const totalScore = (
            weights.accuracy * avgAccuracy +
            weights.matchRate * matchRate * 100 +
            weights.consistency * consistency.score +
            weights.patterns * (patterns.detected ? 50 : 100)
        ) * patternPenalty;

        return Math.round(totalScore);
    }

    /**
     * Get comprehensive session summary
     */
    getSessionSummary() {
        const avgAccuracy = this.getAverageAccuracy();
        const consistency = this.calculateConsistencyScore();
        const patterns = this.detectErrorPatterns();
        const velocity = this.calculatePerformanceVelocity();
        const totalScore = this.getTotalScore();

        // Calculate grade
        let grade;
        if (totalScore >= 90) grade = 'A';
        else if (totalScore >= 80) grade = 'B';
        else if (totalScore >= 70) grade = 'C';
        else if (totalScore >= 60) grade = 'D';
        else grade = 'F';

        return {
            totalScore,
            grade,
            averageAccuracy: Math.round(avgAccuracy * 10) / 10,
            totalFrames: this.totalFrames,
            matchedFrames: this.matchedFrames,
            matchRate: Math.round((this.matchedFrames / (this.totalFrames || 1)) * 1000) / 10,
            dynamicThreshold: Math.round(this.dynamicThreshold * 10) / 10,
            consistency: {
                score: Math.round(consistency.score * 10) / 10,
                interpretation: consistency.interpretation
            },
            patterns: {
                detected: patterns.detected,
                count: patterns.problematicLandmarks.length,
                details: patterns.problematicLandmarks
            },
            performance: {
                velocity: Math.round(velocity.velocity * 1000) / 1000,
                trend: velocity.trend
            },
            sessionDuration: Math.round((Date.now() - this.sessionStartTime) / 1000),
            childAge: this.childAge
        };
    }

    /**
     * Generate real-time recommendations
     */
    getRealtimeRecommendations() {
        const recommendations = [];
        const avgAccuracy = this.getAverageAccuracy();
        const consistency = this.calculateConsistencyScore();
        const patterns = this.detectErrorPatterns();

        // Accuracy recommendations
        if (avgAccuracy < this.dynamicThreshold && this.totalFrames > 30) {
            recommendations.push({
                type: 'warning',
                category: 'Accuracy',
                message: 'Try slowing down and focusing on precision',
                icon: '🎯'
            });
        } else if (avgAccuracy > 90 && this.totalFrames > 50) {
            recommendations.push({
                type: 'success',
                category: 'Performance',
                message: 'Excellent work! Keep it up!',
                icon: '⭐'
            });
        }

        // Consistency recommendations
        if (consistency.score < 60 && this.totalFrames > 50) {
            recommendations.push({
                type: 'info',
                category: 'Consistency',
                message: 'Try to maintain steady movements',
                icon: '📊'
            });
        }

        // Pattern recommendations
        if (patterns.detected && patterns.problematicLandmarks.length > 0) {
            const landmarks = patterns.problematicLandmarks
                .map(p => p.landmarkIndex)
                .slice(0, 3)
                .join(', ');

            recommendations.push({
                type: 'warning',
                category: 'Technique',
                message: `Pay attention to hand position (landmarks: ${landmarks})`,
                icon: '✋'
            });
        }

        // Time-based recommendations
        const sessionDuration = (Date.now() - this.sessionStartTime) / 1000;
        if (sessionDuration > 300 && this.childAge < 8) { // 5 minutes
            recommendations.push({
                type: 'info',
                category: 'Break Time',
                message: 'Consider taking a short break',
                icon: '⏸️'
            });
        }

        return recommendations;
    }

    /**
     * Reset the scoring system for a new session
     */
    reset() {
        this.totalFrames = 0;
        this.matchedFrames = 0;
        this.accuracySum = 0;
        this.currentEMA = null;
        this.accuracyHistory = [];
        this.emaHistory = [];
        this.landmarkErrorMap.clear();
        this.performanceSnapshots = [];
        this.sessionStartTime = Date.now();
    }
}

/**
 * Utility function to format recommendations as HTML
 */
export function formatRecommendations(recommendations) {
    if (!recommendations || recommendations.length === 0) {
        return '<p class="text-muted">Keep up the great work!</p>';
    }

    let html = '<div class="recommendations-list">';
    recommendations.forEach(rec => {
        const alertClass = rec.type === 'warning' ? 'alert-warning' :
                          rec.type === 'success' ? 'alert-success' : 'alert-info';

        html += `
            <div class="alert ${alertClass} d-flex align-items-center mb-2" role="alert">
                <span class="me-2" style="font-size: 1.5em;">${rec.icon}</span>
                <div>
                    <strong>${rec.category}:</strong> ${rec.message}
                </div>
            </div>
        `;
    });
    html += '</div>';

    return html;
}

/**
 * Utility function to create a progress visualization
 */
export function createProgressChart(accuracyHistory, canvasId) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    // Clear canvas
    ctx.clearRect(0, 0, width, height);

    if (accuracyHistory.length < 2) return;

    // Draw grid
    ctx.strokeStyle = '#e0e0e0';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
        const y = (height / 4) * i;
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
    }

    // Draw accuracy line
    ctx.strokeStyle = '#4CAF50';
    ctx.lineWidth = 2;
    ctx.beginPath();

    const step = width / (accuracyHistory.length - 1);
    accuracyHistory.forEach((accuracy, index) => {
        const x = index * step;
        const y = height - (accuracy / 100) * height;

        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });

    ctx.stroke();

    // Draw points
    ctx.fillStyle = '#4CAF50';
    accuracyHistory.forEach((accuracy, index) => {
        const x = index * step;
        const y = height - (accuracy / 100) * height;

        ctx.beginPath();
        ctx.arc(x, y, 3, 0, 2 * Math.PI);
        ctx.fill();
    });
}
