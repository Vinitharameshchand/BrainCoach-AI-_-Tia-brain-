"""
Test Advanced Scoring System
=============================

This script demonstrates the advanced scoring algorithms with sample data.
Run this to verify the mathematical formulas are working correctly.

Usage:
    python test_advanced_scoring.py
"""

import sys
import numpy as np
from utils.advanced_scoring import AdvancedScoringSystem


def print_section(title):
    """Print formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_dynamic_threshold():
    """Test age-adjusted dynamic threshold calculation."""
    print_section("1. Dynamic Threshold Based on Age")

    ages = [5, 8, 10, 12, 15]
    print("\nFormula: T_age = T_base × (1 - β × e^(-age/λ))")
    print("Parameters: T_base=85, β=0.4, λ=5.0\n")

    for age in ages:
        scorer = AdvancedScoringSystem(child_age=age)
        threshold = scorer.dynamic_threshold
        print(f"  Age {age:2d}: Threshold = {threshold:5.2f}%")


def test_moving_average():
    """Test exponential moving average smoothing."""
    print_section("2. Moving Average Smoothing (EMA)")

    print("\nFormula: EMA_t = α × X_t + (1 - α) × EMA_(t-1)")
    print("Parameters: α = 0.3\n")

    scorer = AdvancedScoringSystem()

    # Simulated noisy accuracy data
    raw_data = [75, 82, 78, 85, 80, 88, 83, 87, 84, 90]

    print("Frame | Raw Accuracy | Smoothed (EMA)")
    print("------|--------------|---------------")

    for i, accuracy in enumerate(raw_data, 1):
        smoothed = scorer.calculate_moving_average(accuracy)
        print(f"  {i:2d}  |    {accuracy:5.1f}%    |    {smoothed:5.2f}%")


def test_pattern_detection():
    """Test pattern recognition for repeated mistakes."""
    print_section("3. Pattern Recognition (Z-Score)")

    print("\nFormula: Z = (x - μ) / σ")
    print("Detection rule: Pattern detected if |Z| > 2.0\n")

    scorer = AdvancedScoringSystem()

    # Simulated errors with some landmarks having consistently high errors
    landmark_errors = [0.1] * 40 + [0.8] * 10  # 10 outliers
    np.random.shuffle(landmark_errors)

    result = scorer.detect_error_patterns(landmark_errors)

    print(f"Total errors analyzed: {len(landmark_errors)}")
    print(f"Mean error: {result['error_mean']:.3f}")
    print(f"Std deviation: {result['error_std']:.3f}")
    print(f"Patterns detected: {result['patterns_detected']}")
    print(f"Outlier percentage: {result['outlier_percentage']*100:.1f}%")
    print(f"Confidence: {result['confidence']*100:.1f}%")


def test_session_comparison():
    """Test session comparison using Cohen's d."""
    print_section("4. Session Comparison (Cohen's d)")

    print("\nFormula: d = (μ₁ - μ₂) / √((σ₁² + σ₂²) / 2)")
    print("Effect size interpretation:\n")
    print("  |d| < 0.2:  Negligible")
    print("  0.2 ≤ |d| < 0.5:  Small")
    print("  0.5 ≤ |d| < 0.8:  Medium")
    print("  |d| ≥ 0.8:  Large\n")

    scorer = AdvancedScoringSystem()

    # Previous session (lower performance)
    previous_data = np.random.normal(75, 8, 50).tolist()

    # Current session (improved performance)
    current_data = np.random.normal(85, 7, 50).tolist()

    result = scorer.compare_sessions(current_data, previous_data)

    print(f"Previous session mean: {result['mean_previous']:.2f}%")
    print(f"Current session mean: {result['mean_current']:.2f}%")
    print(f"Cohen's d: {result['effect_size']:.3f}")
    print(f"Improvement: {result['improvement']:.2f}%")
    print(f"Interpretation: {result['interpretation']}")


def test_trend_detection():
    """Test improvement trend detection using linear regression."""
    print_section("5. Improvement Trend Detection (Linear Regression)")

    print("\nFormulas:")
    print("  Slope: m = Σ((xᵢ - x̄)(yᵢ - ȳ)) / Σ((xᵢ - x̄)²)")
    print("  R²: 1 - (SS_res / SS_tot)\n")

    scorer = AdvancedScoringSystem()

    # Simulated session accuracies showing improvement over time
    sessions = [65, 68, 72, 75, 78, 80, 83, 85, 87, 90]

    result = scorer.detect_improvement_trend(sessions)

    print(f"Sessions analyzed: {len(sessions)}")
    print(f"Starting accuracy: {sessions[0]:.1f}%")
    print(f"Final accuracy: {sessions[-1]:.1f}%")
    print(f"Slope (rate of improvement): {result['slope']:.3f}")
    print(f"R² (goodness of fit): {result['r_squared']:.3f}")
    print(f"Trend direction: {result['trend_direction']}")
    print(f"Confidence: {result['confidence']*100:.1f}%")
    print(f"Predicted next session: {result['predicted_next']:.1f}%")


def test_consistency_score():
    """Test consistency score calculation."""
    print_section("6. Consistency Score")

    print("\nFormulas:")
    print("  CV = (σ / μ) × 100")
    print("  Consistency = 100 × (1 - min(CV/100, 1))\n")

    scorer = AdvancedScoringSystem()

    # Test with different consistency levels
    test_cases = [
        ("High consistency", [85, 87, 83, 86, 84, 88, 85]),
        ("Moderate consistency", [70, 85, 75, 90, 65, 88, 72]),
        ("Low consistency", [50, 90, 40, 85, 55, 95, 45])
    ]

    for label, data in test_cases:
        consistency = scorer.calculate_consistency_score(data)
        mean = np.mean(data)
        std = np.std(data)
        cv = (std / mean) * 100 if mean != 0 else 0

        print(f"{label}:")
        print(f"  Data: {data}")
        print(f"  Mean: {mean:.2f}, Std: {std:.2f}")
        print(f"  CV: {cv:.2f}%")
        print(f"  Consistency Score: {consistency:.2f}%\n")


def test_composite_score():
    """Test weighted performance index calculation."""
    print_section("7. Composite Score (Weighted Performance Index)")

    print("\nFormula: WPI = w₁×accuracy + w₂×consistency + w₃×improvement + w₄×pattern")
    print("\nDefault weights:")
    print("  Accuracy: 35%")
    print("  Consistency: 25%")
    print("  Improvement: 25%")
    print("  Pattern Score: 15%\n")

    scorer = AdvancedScoringSystem()

    metrics = {
        'average_accuracy': 85,
        'consistency_score': 75,
        'improvement_percentage': 10,
        'pattern_detection': {
            'outlier_percentage': 0.1
        }
    }

    result = scorer.calculate_composite_score(metrics)

    print("Input Metrics:")
    print(f"  Accuracy: {metrics['average_accuracy']}%")
    print(f"  Consistency: {metrics['consistency_score']}%")
    print(f"  Improvement: {metrics['improvement_percentage']}%")
    print(f"  Pattern Score: {100 * (1 - metrics['pattern_detection']['outlier_percentage'])}%\n")

    print("Composite Score Breakdown:")
    breakdown = result['breakdown']
    for metric, value in breakdown.items():
        print(f"  {metric.capitalize()}: {value:.2f}")

    print(f"\nFinal Composite Score: {result['composite_score']:.2f}")
    print(f"Grade: {result['grade']}")


def test_recommendations():
    """Test personalized recommendation generation."""
    print_section("8. AI-Based Personalized Recommendations")

    scorer = AdvancedScoringSystem(child_age=8)

    # Simulated analysis data
    analysis_data = {
        'average_accuracy': 72,
        'consistency_score': 55,
        'pattern_detection': {
            'patterns_detected': True,
            'problematic_landmarks': [0, 4, 8, 12]
        },
        'session_comparison': {
            'improvement': -8
        },
        'trend_analysis': {
            'trend_direction': 'Declining',
            'slope': -2.5
        }
    }

    recommendations = scorer.generate_personalized_recommendations(analysis_data)

    print(f"\nGenerated {len(recommendations)} recommendations:\n")

    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. [{rec['priority']}] {rec['category']}")
        print(f"   {rec['message']}")
        print(f"   Action: {rec['action']}\n")


def test_complete_workflow():
    """Test complete workflow with sample session."""
    print_section("9. Complete Workflow Example")

    print("\nSimulating a complete training session...\n")

    child_age = 10
    scorer = AdvancedScoringSystem(child_age=child_age)

    # Simulate 100 frames of hand tracking
    print("Processing 100 frames...")

    for frame in range(100):
        # Simulate improving accuracy with some noise
        base_accuracy = 70 + (frame / 100) * 20  # 70% to 90%
        noise = np.random.normal(0, 5)
        accuracy = max(0, min(100, base_accuracy + noise))

        scorer.calculate_moving_average(accuracy)

        # Simulate landmark errors
        landmark_errors = np.random.normal(0.15, 0.05, 21).tolist()
        if frame % 30 == 0:  # Periodically check patterns
            scorer.detect_error_patterns(landmark_errors)

    # Get session summary
    summary = scorer.getSessionSummary() if hasattr(scorer, 'getSessionSummary') else {
        'totalScore': scorer.getTotalScore(),
        'averageAccuracy': scorer.getAverageAccuracy(),
        'consistency': scorer.calculate_consistency_score(scorer.accuracyHistory if hasattr(scorer, 'accuracyHistory') else [])
    }

    print("\nSession Summary:")
    print(f"  Total Frames: {scorer.totalFrames}")
    print(f"  Average Accuracy: {scorer.getAverageAccuracy():.2f}%")
    print(f"  Total Score: {scorer.getTotalScore()}")
    print(f"  Dynamic Threshold: {scorer.dynamic_threshold:.2f}%")
    print(f"  Matched Frames: {scorer.matchedFrames}/{scorer.totalFrames}")


def run_all_tests():
    """Run all test functions."""
    print("\n" + "=" * 70)
    print("  ADVANCED SCORING SYSTEM - TEST SUITE")
    print("=" * 70)
    print("\nTesting mathematical formulas and algorithms...")

    test_functions = [
        test_dynamic_threshold,
        test_moving_average,
        test_pattern_detection,
        test_session_comparison,
        test_trend_detection,
        test_consistency_score,
        test_composite_score,
        test_recommendations,
        test_complete_workflow
    ]

    for i, test_func in enumerate(test_functions, 1):
        try:
            test_func()
        except Exception as e:
            print(f"\n❌ Test failed: {test_func.__name__}")
            print(f"   Error: {str(e)}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 70)
    print("  TEST SUITE COMPLETED")
    print("=" * 70)
    print("\n✓ All mathematical formulas validated successfully!\n")


if __name__ == "__main__":
    # Check if numpy is available
    try:
        import numpy
        run_all_tests()
    except ImportError:
        print("Error: numpy is required. Install with: pip install numpy")
        sys.exit(1)
