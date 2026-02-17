"""
Advanced Scoring Algorithm for BrainCoach AI
=============================================

This module implements a sophisticated scoring system with:
1. Moving Average Smoothing
2. Dynamic Threshold Based on Age
3. Pattern Recognition for Repeated Mistakes
4. Session Comparison Algorithm
5. Improvement Trend Detection
6. AI-based Personalized Recommendations

Mathematical Formulas Used:
===========================

1. EXPONENTIAL MOVING AVERAGE (EMA):
   EMA_t = α × X_t + (1 - α) × EMA_(t-1)
   where α = 2/(N+1), N = smoothing window

2. DYNAMIC THRESHOLD:
   T_age = T_base × (1 - β × e^(-age/λ))
   where β = age sensitivity, λ = age decay constant

3. PATTERN RECOGNITION (Z-Score):
   Z = (x - μ) / σ
   Pattern detected if |Z| > threshold (typically 2)

4. SESSION COMPARISON (Cohen's d):
   d = (μ₁ - μ₂) / √((σ₁² + σ₂²) / 2)
   Small effect: d < 0.5, Medium: 0.5 ≤ d < 0.8, Large: d ≥ 0.8

5. IMPROVEMENT TREND (Linear Regression):
   y = mx + b
   where m = Σ((x_i - x̄)(y_i - ȳ)) / Σ((x_i - x̄)²)
   Trend strength: R² = 1 - (SS_res / SS_tot)

6. CONFIDENCE SCORE:
   C = (1 - CV) × √(n / (n + k))
   where CV = coefficient of variation, n = sample size, k = constant

7. WEIGHTED PERFORMANCE INDEX:
   WPI = w₁×accuracy + w₂×consistency + w₃×improvement + w₄×pattern_score
   Σw_i = 1
"""

import numpy as np
from collections import deque
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import json
from models import Session, HandTrackingFrame, Score, Child


class AdvancedScoringSystem:
    """
    Advanced scoring system with multiple algorithms for comprehensive assessment.
    """

    def __init__(self, child_age: int = 10):
        """
        Initialize the scoring system.

        Args:
            child_age: Age of the child for dynamic threshold calculation
        """
        self.child_age = child_age
        self.base_threshold = 85.0
        self.dynamic_threshold = self._calculate_dynamic_threshold()

        # Moving average parameters
        self.ema_alpha = 0.3  # Smoothing factor (α)
        self.ema_window = 10  # Window size for EMA
        self.ema_buffer = deque(maxlen=self.ema_window)
        self.current_ema = None

        # Pattern recognition
        self.error_buffer = deque(maxlen=50)
        self.pattern_threshold = 2.0  # Z-score threshold

        # Weights for composite score
        self.weights = {
            'accuracy': 0.35,
            'consistency': 0.25,
            'improvement': 0.25,
            'pattern_score': 0.15
        }

    def _calculate_dynamic_threshold(self) -> float:
        """
        Calculate age-adjusted difficulty threshold.

        Formula: T_age = T_base × (1 - β × e^(-age/λ))

        Younger children get lower thresholds (more lenient)
        Older children get higher thresholds (more challenging)
        """
        beta = 0.4  # Age sensitivity factor
        lambda_decay = 5.0  # Decay constant

        age_factor = 1 - beta * np.exp(-self.child_age / lambda_decay)
        threshold = self.base_threshold * age_factor

        # Clamp between reasonable bounds
        return max(60.0, min(95.0, threshold))

    def calculate_moving_average(self, accuracy: float) -> float:
        """
        Apply exponential moving average smoothing to reduce noise.

        Formula: EMA_t = α × X_t + (1 - α) × EMA_(t-1)

        Args:
            accuracy: Current frame accuracy

        Returns:
            Smoothed accuracy value
        """
        self.ema_buffer.append(accuracy)

        if self.current_ema is None:
            # Initialize with first value
            self.current_ema = accuracy
        else:
            # Apply EMA formula
            self.current_ema = (self.ema_alpha * accuracy +
                               (1 - self.ema_alpha) * self.current_ema)

        return self.current_ema

    def detect_error_patterns(self, landmark_errors: List[float]) -> Dict:
        """
        Detect repeated mistakes using statistical pattern recognition.

        Formula: Z = (x - μ) / σ

        Args:
            landmark_errors: List of error magnitudes per landmark

        Returns:
            Dictionary with pattern detection results
        """
        self.error_buffer.extend(landmark_errors)

        if len(self.error_buffer) < 10:
            return {
                'patterns_detected': False,
                'problematic_landmarks': [],
                'confidence': 0.0
            }

        # Convert to numpy array for analysis
        errors_array = np.array(list(self.error_buffer))

        # Calculate statistics
        mean_error = np.mean(errors_array)
        std_error = np.std(errors_array)

        if std_error == 0:
            return {
                'patterns_detected': False,
                'problematic_landmarks': [],
                'confidence': 0.0
            }

        # Calculate z-scores
        z_scores = (errors_array - mean_error) / std_error

        # Identify outliers (repeated high errors)
        outlier_indices = np.where(np.abs(z_scores) > self.pattern_threshold)[0]

        # Calculate confidence in pattern detection
        confidence = min(1.0, len(outlier_indices) / (0.1 * len(errors_array)))

        return {
            'patterns_detected': len(outlier_indices) > 5,
            'problematic_landmarks': outlier_indices.tolist(),
            'error_mean': float(mean_error),
            'error_std': float(std_error),
            'confidence': float(confidence),
            'outlier_percentage': len(outlier_indices) / len(errors_array)
        }

    def compare_sessions(self, current_session_data: List[float],
                        previous_session_data: List[float]) -> Dict:
        """
        Compare current session performance with previous sessions.

        Uses Cohen's d for effect size:
        Formula: d = (μ₁ - μ₂) / √((σ₁² + σ₂²) / 2)

        Args:
            current_session_data: Current session accuracy values
            previous_session_data: Previous session accuracy values

        Returns:
            Dictionary with comparison metrics
        """
        if not current_session_data or not previous_session_data:
            return {
                'comparison_available': False,
                'effect_size': 0.0,
                'improvement': 0.0,
                'interpretation': 'Insufficient data'
            }

        current = np.array(current_session_data)
        previous = np.array(previous_session_data)

        mean_current = np.mean(current)
        mean_previous = np.mean(previous)
        std_current = np.std(current)
        std_previous = np.std(previous)

        # Calculate pooled standard deviation
        pooled_std = np.sqrt((std_current**2 + std_previous**2) / 2)

        if pooled_std == 0:
            return {
                'comparison_available': True,
                'effect_size': 0.0,
                'improvement': 0.0,
                'interpretation': 'No variance detected'
            }

        # Cohen's d
        cohens_d = (mean_current - mean_previous) / pooled_std

        # Interpret effect size
        if abs(cohens_d) < 0.2:
            interpretation = 'Negligible change'
        elif abs(cohens_d) < 0.5:
            interpretation = 'Small improvement' if cohens_d > 0 else 'Small decline'
        elif abs(cohens_d) < 0.8:
            interpretation = 'Medium improvement' if cohens_d > 0 else 'Medium decline'
        else:
            interpretation = 'Large improvement' if cohens_d > 0 else 'Large decline'

        improvement_percentage = ((mean_current - mean_previous) / mean_previous) * 100

        return {
            'comparison_available': True,
            'effect_size': float(cohens_d),
            'improvement': float(improvement_percentage),
            'mean_current': float(mean_current),
            'mean_previous': float(mean_previous),
            'interpretation': interpretation
        }

    def detect_improvement_trend(self, session_accuracies: List[float]) -> Dict:
        """
        Detect improvement trends using linear regression.

        Formula: y = mx + b
        where m = Σ((x_i - x̄)(y_i - ȳ)) / Σ((x_i - x̄)²)

        R² = 1 - (SS_res / SS_tot)

        Args:
            session_accuracies: List of session average accuracies over time

        Returns:
            Dictionary with trend analysis
        """
        if len(session_accuracies) < 3:
            return {
                'trend_available': False,
                'slope': 0.0,
                'r_squared': 0.0,
                'trend_direction': 'Unknown'
            }

        n = len(session_accuracies)
        x = np.arange(n)
        y = np.array(session_accuracies)

        # Calculate means
        x_mean = np.mean(x)
        y_mean = np.mean(y)

        # Calculate slope (m)
        numerator = np.sum((x - x_mean) * (y - y_mean))
        denominator = np.sum((x - x_mean) ** 2)

        if denominator == 0:
            return {
                'trend_available': True,
                'slope': 0.0,
                'r_squared': 0.0,
                'trend_direction': 'Flat'
            }

        slope = numerator / denominator

        # Calculate intercept (b)
        intercept = y_mean - slope * x_mean

        # Calculate R² (coefficient of determination)
        y_pred = slope * x + intercept
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - y_mean) ** 2)

        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

        # Determine trend direction
        if abs(slope) < 0.5:
            trend = 'Stable'
        elif slope > 0:
            trend = 'Improving' if r_squared > 0.3 else 'Slightly improving'
        else:
            trend = 'Declining' if r_squared > 0.3 else 'Slightly declining'

        # Calculate confidence based on R² and sample size
        confidence = r_squared * np.sqrt(n / (n + 10))

        return {
            'trend_available': True,
            'slope': float(slope),
            'intercept': float(intercept),
            'r_squared': float(r_squared),
            'trend_direction': trend,
            'confidence': float(confidence),
            'predicted_next': float(slope * n + intercept)
        }

    def calculate_consistency_score(self, accuracies: List[float]) -> float:
        """
        Calculate consistency score using coefficient of variation.

        Formula: CV = (σ / μ) × 100
        Consistency Score = 100 × (1 - min(CV/100, 1))

        Args:
            accuracies: List of accuracy values

        Returns:
            Consistency score (0-100)
        """
        if len(accuracies) < 2:
            return 50.0  # Neutral score for insufficient data

        arr = np.array(accuracies)
        mean = np.mean(arr)
        std = np.std(arr)

        if mean == 0:
            return 0.0

        # Coefficient of variation
        cv = (std / mean) * 100

        # Convert to consistency score (lower CV = higher consistency)
        consistency = 100 * (1 - min(cv / 100, 1))

        return float(consistency)

    def generate_personalized_recommendations(self,
                                             analysis_data: Dict) -> List[Dict]:
        """
        Generate AI-based personalized recommendations.

        Args:
            analysis_data: Dictionary containing all analysis results

        Returns:
            List of recommendation dictionaries
        """
        recommendations = []

        # Analyze accuracy
        avg_accuracy = analysis_data.get('average_accuracy', 0)
        if avg_accuracy < self.dynamic_threshold:
            recommendations.append({
                'category': 'Accuracy',
                'priority': 'High',
                'message': f'Current accuracy ({avg_accuracy:.1f}%) is below the recommended '
                          f'threshold ({self.dynamic_threshold:.1f}%). Consider practicing '
                          f'with slower movements and focus on precision.',
                'action': 'Reduce exercise speed by 30%'
            })
        elif avg_accuracy > 90:
            recommendations.append({
                'category': 'Progression',
                'priority': 'Medium',
                'message': f'Excellent accuracy ({avg_accuracy:.1f}%)! Ready to advance to '
                          f'more challenging exercises.',
                'action': 'Try next difficulty level'
            })

        # Analyze patterns
        pattern_data = analysis_data.get('pattern_detection', {})
        if pattern_data.get('patterns_detected', False):
            problematic = pattern_data.get('problematic_landmarks', [])
            if len(problematic) > 0:
                recommendations.append({
                    'category': 'Pattern Recognition',
                    'priority': 'High',
                    'message': f'Detected repeated errors in {len(problematic)} hand landmarks. '
                              f'Focus on specific finger movements and hand positioning.',
                    'action': 'Practice targeted hand exercises'
                })

        # Analyze consistency
        consistency = analysis_data.get('consistency_score', 50)
        if consistency < 60:
            recommendations.append({
                'category': 'Consistency',
                'priority': 'Medium',
                'message': f'Performance consistency ({consistency:.1f}%) can be improved. '
                          f'Try to maintain steady focus throughout the exercise.',
                'action': 'Take short breaks between attempts'
            })

        # Analyze trend
        trend_data = analysis_data.get('trend_analysis', {})
        if trend_data.get('trend_direction') == 'Declining':
            recommendations.append({
                'category': 'Trend',
                'priority': 'High',
                'message': 'Performance trend shows decline. Consider reviewing previous '
                          'exercises or taking a brief rest before continuing.',
                'action': 'Review basics and rest if needed'
            })
        elif trend_data.get('trend_direction') == 'Improving':
            recommendations.append({
                'category': 'Motivation',
                'priority': 'Low',
                'message': f'Great progress! Performance is steadily improving with slope '
                          f'{trend_data.get("slope", 0):.2f}. Keep up the excellent work!',
                'action': 'Continue current practice routine'
            })

        # Analyze session comparison
        comparison = analysis_data.get('session_comparison', {})
        if comparison.get('improvement', 0) < -10:
            recommendations.append({
                'category': 'Performance',
                'priority': 'High',
                'message': f'Performance dropped {abs(comparison.get("improvement", 0)):.1f}% '
                          f'compared to previous session. Ensure adequate rest and focus.',
                'action': 'Check fatigue levels and environment'
            })

        # Age-specific recommendations
        if self.child_age < 6:
            recommendations.append({
                'category': 'Age-Appropriate',
                'priority': 'Low',
                'message': 'For younger children, keep sessions short (5-10 minutes) and '
                          'include frequent breaks with positive reinforcement.',
                'action': 'Limit session duration'
            })
        elif self.child_age > 12:
            recommendations.append({
                'category': 'Age-Appropriate',
                'priority': 'Low',
                'message': 'Consider introducing more complex exercises and longer practice '
                          'sessions to maximize learning potential.',
                'action': 'Explore advanced modules'
            })

        return recommendations

    def calculate_composite_score(self, metrics: Dict) -> Dict:
        """
        Calculate weighted performance index combining all metrics.

        Formula: WPI = w₁×accuracy + w₂×consistency + w₃×improvement + w₄×pattern_score

        Args:
            metrics: Dictionary containing all performance metrics

        Returns:
            Dictionary with composite score and breakdown
        """
        accuracy = metrics.get('average_accuracy', 0)
        consistency = metrics.get('consistency_score', 0)

        # Normalize improvement to 0-100 scale
        improvement = metrics.get('improvement_percentage', 0)
        improvement_normalized = max(0, min(100, 50 + improvement))

        # Pattern score (inverse of error rate)
        pattern_data = metrics.get('pattern_detection', {})
        pattern_score = 100 * (1 - pattern_data.get('outlier_percentage', 0.5))

        # Calculate weighted score
        composite = (
            self.weights['accuracy'] * accuracy +
            self.weights['consistency'] * consistency +
            self.weights['improvement'] * improvement_normalized +
            self.weights['pattern_score'] * pattern_score
        )

        return {
            'composite_score': float(composite),
            'breakdown': {
                'accuracy': float(accuracy),
                'consistency': float(consistency),
                'improvement': float(improvement_normalized),
                'pattern_score': float(pattern_score)
            },
            'weights': self.weights,
            'grade': self._calculate_grade(composite)
        }

    def _calculate_grade(self, score: float) -> str:
        """Calculate letter grade based on score."""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'


def analyze_session_comprehensive(session_id: int, db_session) -> Dict:
    """
    Perform comprehensive analysis of a session.

    Args:
        session_id: ID of the session to analyze
        db_session: Database session object

    Returns:
        Dictionary with complete analysis results
    """
    from models import Session, HandTrackingFrame, Child

    # Get session data
    session = db_session.query(Session).get(session_id)
    if not session:
        return {'error': 'Session not found'}

    # Get child info for age-based adjustment
    child = db_session.query(Child).get(session.child_id)
    child_age = child.age if child and child.age else 10

    # Initialize scoring system
    scorer = AdvancedScoringSystem(child_age=child_age)

    # Get all frames for this session
    frames = db_session.query(HandTrackingFrame).filter_by(
        session_id=session_id
    ).order_by(HandTrackingFrame.frame_number).all()

    if not frames:
        return {'error': 'No frame data available'}

    # Extract accuracies
    accuracies = [f.frame_accuracy for f in frames if f.frame_accuracy is not None]

    if not accuracies:
        return {'error': 'No accuracy data available'}

    # Apply moving average smoothing
    smoothed_accuracies = []
    for acc in accuracies:
        smoothed = scorer.calculate_moving_average(acc)
        smoothed_accuracies.append(smoothed)

    # Extract landmark errors for pattern detection
    landmark_errors = []
    for frame in frames:
        if frame.landmark_data:
            try:
                landmarks = json.loads(frame.landmark_data)
                # Calculate error magnitude per landmark (simplified)
                errors = [abs(lm.get('x', 0.5) - 0.5) + abs(lm.get('y', 0.5) - 0.5)
                         for lm in landmarks]
                landmark_errors.extend(errors)
            except:
                pass

    # Detect patterns
    pattern_analysis = scorer.detect_error_patterns(landmark_errors)

    # Get previous sessions for comparison
    previous_sessions = db_session.query(Session).filter(
        Session.child_id == session.child_id,
        Session.id < session_id,
        Session.avg_accuracy.isnot(None),
        Session.result_status == 'Completed'
    ).order_by(Session.start_time.desc()).limit(5).all()

    # Session comparison
    session_comparison = {}
    if previous_sessions:
        prev_accuracies = [s.avg_accuracy for s in previous_sessions
                          if s.avg_accuracy is not None]
        if prev_accuracies:
            session_comparison = scorer.compare_sessions(
                smoothed_accuracies,
                prev_accuracies
            )

    # Get all historical sessions for trend analysis
    all_sessions = db_session.query(Session).filter(
        Session.child_id == session.child_id,
        Session.avg_accuracy.isnot(None),
        Session.result_status == 'Completed'
    ).order_by(Session.start_time).all()

    historical_accuracies = [s.avg_accuracy for s in all_sessions]
    trend_analysis = scorer.detect_improvement_trend(historical_accuracies)

    # Calculate consistency
    consistency_score = scorer.calculate_consistency_score(smoothed_accuracies)

    # Compile metrics
    avg_accuracy = np.mean(smoothed_accuracies)
    improvement = session_comparison.get('improvement', 0) if session_comparison else 0

    metrics = {
        'average_accuracy': avg_accuracy,
        'consistency_score': consistency_score,
        'improvement_percentage': improvement,
        'pattern_detection': pattern_analysis
    }

    # Calculate composite score
    composite_result = scorer.calculate_composite_score(metrics)

    # Generate recommendations
    analysis_data = {
        'average_accuracy': avg_accuracy,
        'consistency_score': consistency_score,
        'pattern_detection': pattern_analysis,
        'session_comparison': session_comparison,
        'trend_analysis': trend_analysis
    }

    recommendations = scorer.generate_personalized_recommendations(analysis_data)

    return {
        'session_id': session_id,
        'child_age': child_age,
        'dynamic_threshold': scorer.dynamic_threshold,
        'raw_accuracies': accuracies,
        'smoothed_accuracies': smoothed_accuracies,
        'average_accuracy': float(avg_accuracy),
        'consistency_score': float(consistency_score),
        'pattern_analysis': pattern_analysis,
        'session_comparison': session_comparison,
        'trend_analysis': trend_analysis,
        'composite_score': composite_result,
        'recommendations': recommendations,
        'analysis_timestamp': datetime.utcnow().isoformat()
    }
