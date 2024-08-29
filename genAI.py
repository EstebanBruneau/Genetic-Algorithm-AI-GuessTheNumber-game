import numpy as np

class GuessTheNumberAI:
    def __init__(self):
        self.weights = np.random.rand(23) * 2 - 1
        self.fitness = 0
        self.guessArray = []
        
        with open('names.csv', 'r') as f:
            names = f.readlines()
        self.name = names[np.random.randint(0, len(names))].strip()
        
    def reset(self):
        self.guessArray = []
        self.fitness = 0    

    def predict(self, bounds):
        features = self.getFeatures(bounds[0], bounds[1])
        
        # Ensure weights and features do not contain excessively large values
        features = np.clip(features, -1e5, 1e5)
        self.weights = np.clip(self.weights, -1e5, 1e5)
        
        # Check for NaN and infinity in features and weights
        if np.any(np.isnan(features)) or np.any(np.isinf(features)) or np.any(np.isnan(self.weights)) or np.any(np.isinf(self.weights)):
            return self.guessArray[-1][0] if len(self.guessArray) > 0 else 999999
        
        # Perform the dot product
        prediction = np.dot(features, self.weights)
        
        # Clip the prediction to avoid infinity
        prediction = np.clip(prediction, -1e10, 1e10)
        
        # Check for NaN and infinity in the prediction
        if np.isnan(prediction) or np.isinf(prediction):
            return self.guessArray[-1][0] if len(self.guessArray) > 0 else 999999
        
        return int(prediction)
        
    def getFeatures(self, lower_bound, upper_bound):
        guessArray = sorted(self.guessArray, key=lambda x: x[0])

        features = np.zeros(23)  
        
        # Boundaries
        features[0] = lower_bound  # Lower Bound
        features[1] = upper_bound  # Upper Bound
        features[2] = (features[0] + features[1]) / 6  # Midpoint (1/6)
        features[3] = (features[0] + features[1]) / 3  # Midpoint (1/3)
        features[4] = (features[0] + features[1]) / 2  # Midpoint (1/2)
        features[5] = 2 * (features[0] + features[1]) / 3  # Midpoint (2/3)
        features[6] = 5 * (features[0] + features[1]) / 6  # Midpoint (5/6)

        if len(guessArray) == 0:
            return features

        # Guesses based features
        guesses = [guess for guess, feedback in guessArray]

        features[7] = max(guesses)  # Maximum Guess
        features[8] = min(guesses)  # Minimum Guess
        features[9] = np.median(guesses)  # Median Guess
        features[10] = sum(guesses) / len(guessArray)  # Average Guess
        features[11] = np.std(guesses)  # Standard Deviation of Guesses
        features[12] = np.var(guesses)  # Variance of Guesses
        features[13] = max(guesses) - min(guesses)  # Range of Guesses

        positive_feedback_count = sum([1 for guess, feedback in guessArray if feedback == 1])
        negative_feedback_count = sum([1 for guess, feedback in guessArray if feedback == -1])
        features[14] = positive_feedback_count / len(guessArray)  # Positive Feedback Ratio
        features[15] = negative_feedback_count / len(guessArray)  # Negative Feedback Ratio

        features[16] = sum(1 for guess, _ in guessArray if guess > upper_bound)  # Guesses above the upper bound
        features[17] = sum(1 for guess, _ in guessArray if guess < lower_bound)  # Guesses below the lower bound

        positive_guesses = [guess for guess, feedback in guessArray if feedback == 1]
        negative_guesses = [guess for guess, feedback in guessArray if feedback == -1]

        features[18] = sum(positive_guesses) / len(positive_guesses) if positive_guesses else 0  # Average Guess for Positive Feedback
        features[19] = sum(negative_guesses) / len(negative_guesses) if negative_guesses else 0  # Average Guess for Negative Feedback

        features[20] = guessArray[-1][1]  # Last Feedback

        # Consecutive feedback counts
        consecutive_positive_count = 0
        consecutive_negative_count = 0
        for i in range(1, len(guessArray)):
            if guessArray[-i][1] == 1:
                consecutive_positive_count += 1
            else:
                break

        for i in range(1, len(guessArray)):
            if guessArray[-i][1] == -1:
                consecutive_negative_count += 1
            else:
                break

        features[21] = consecutive_positive_count  # Consecutive Positive Feedback Count
        features[22] = consecutive_negative_count  # Consecutive Negative Feedback Count

        return features
        
        # check for NaN or Inf values
        for i in range(18):
            if np.isnan(features[i]) or np.isinf(features[i]):
                features[i] = 0

        return features

    def __str__(self):
        return f"{self.name} ({self.fitness})"