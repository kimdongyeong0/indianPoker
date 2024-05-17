import numpy as np
import random
import indianPokerUtil as util


class SimpleDNN:
    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.01):
        self.learning_rate = self.learning_rate
        self.weights1 = np.random.randn(input_size, hidden_size) * 0.01
        self.biases1 = np.zeros((1, hidden_size))
        self.weights2 = np.random.randn(hidden_size, output_size) * 0.01
        self.biases2 = np.zeros((1, output_size))

    def relu(self, z):
        return np.maximum(0, z)

    def relu_derivative(self, z):
        return z > 0

    def forward(self, x):
        self.z1 = np.dot(x, self.weights1) + self.biases1
        self.a1 = self.relu(self.z1)
        self.z2 = np.dot(self.a1, self.weights2) + self.biases2
        return self.z2  # Linear output

    def backward(self, x, y, output):
        m = y.shape[0]

        dz2 = output - y
        dw2 = np.dot(self.a1.T, dz2) / m
        db2 = np.sum(dz2, axis=0, keepdims=True) / m

        dz1 = np.dot(dz2, self.weights2.T) * self.relu_derivative(self.z1)
        dw1 = np.dot(x.T, dz1) / m
        db1 = np.sum(dz1, axis=0, keepdims=True) / m

        self.weights2 -= self.learning_rate * dw2
        self.biases2 -= self.learning_rate * db2
        self.weights1 -= self.learning_rate * dw1
        self.biases1 -= self.learning_rate * db1

    def train(self, x, y, epochs):
        for epoch in range(epochs):
            output = self.forward(x)
            self.backward(x, y, output)
            if (epoch + 1) % 100 == 0:
                loss = np.mean(np.square(y - output))
                print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss:.4f}")

    def predict(self, x):
        return self.forward(x)


class Algorithm:
    def __init__(self):
        self.deck = [i for i in range(1, 11)]
        self.deck = 2 * self.deck
        self.point = 100
        self.model = self.train_dnn()

    def train_dnn(self):
        num_samples = 1000
        bets, cards = self.generate_training_data(num_samples)

        bets = bets / np.max(bets)
        cards = cards / 10.0

        input_size = bets.shape[1]
        hidden_size = 10
        output_size = cards.shape[1]

        model = SimpleDNN(input_size, hidden_size, output_size)
        model.train(bets, cards, epochs=1000)
        return model

    def generate_training_data(self, num_samples):
        np.random.seed(42)
        cards = np.random.randint(1, 11, size=(num_samples, 1))
        bets = cards * np.random.randint(1, 10, size=(num_samples, 1))
        return bets, cards

    def pick(self) -> int:
        return self.deck.pop(random.randint(0, len(self.deck) - 1))

    def giveUp(self, currentBet) -> bool:
        predicted_card = self.predict_card(currentBet)
        if predicted_card <= 2:
            return True
        return False

    def raiseBet(self, currentBet) -> int:
        return min(currentBet + 10, self.point)

    def bet(self) -> int:
        return min(10, self.point)

    def predict_card(self, bet):
        normalized_bet = np.array([[bet]]) / 100.0
        predicted_card = self.model.predict(normalized_bet)
        return predicted_card[0][0] * 10


if __name__ == "__main__":
    util.main()
