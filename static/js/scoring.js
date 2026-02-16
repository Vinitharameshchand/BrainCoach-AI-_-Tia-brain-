export class ScoringSystem {
    constructor(threshold = 85) {
        this.threshold = threshold;
        this.totalFrames = 0;
        this.matchedFrames = 0;
        this.accuracySum = 0;

        // Dummy target trajectory (normalized center of screen)
        this.targetLandmarks = Array(21).fill(0).map(() => ({ x: 0.5, y: 0.5, z: 0 }));
    }

    calculateAccuracy(landmarks) {
        if (!landmarks) return 0;

        let totalDistance = 0;
        landmarks.forEach((point, index) => {
            const target = this.targetLandmarks[index];
            const dist = Math.sqrt(
                Math.pow(point.x - target.x, 2) +
                Math.pow(point.y - target.y, 2)
            );
            totalDistance += dist;
        });

        // Convert distance to accuracy (inverse relationship)
        let avgDist = totalDistance / 21;
        let accuracy = Math.max(0, 100 * (1 - avgDist * 2));

        this.updateStats(accuracy);
        return accuracy;
    }

    updateStats(accuracy) {
        this.totalFrames++;
        this.accuracySum += accuracy;
        if (accuracy >= this.threshold) {
            this.matchedFrames++;
        }
    }

    getAverageAccuracy() {
        return this.totalFrames > 0 ? this.accuracySum / this.totalFrames : 0;
    }

    getTotalScore() {
        return Math.round(this.getAverageAccuracy() * (this.matchedFrames / (this.totalFrames || 1)));
    }
}
