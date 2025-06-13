import numpy as np  # noqa: N999
from numpy.typing import NDArray


class SimpleBaselineClassifier:
    """
    A simple baseline classifier that makes predictions based on a specified strategy.

    Supported strategies:
    - "most_frequent": Predict the most common label in training data.
    - "uniform": Predict random labels between min and max seen in training.
    - "constant": Always predict a fixed constant value.
    """

    def __init__(self, strategy="most_frequent", random_state=None, constant=None):
        self.strategy = strategy
        self.random_state = random_state
        self.constant = constant
        self._X_train = None
        self._y_train = None

    def __repr__(self):
        return (
            f"SimpleBaselineClassifier("
            f"strategy={self.strategy}, "
            f"random_state={self.random_state}, "
            f"constant={self.constant})"
        )

    @property
    def X_train(self) -> NDArray[np.int16]:
        if self._X_train is None:
            raise ValueError("X_train has not been set. Please call fit() before predict().")
        return self._X_train

    @X_train.setter
    def X_train(self, X_train: NDArray[np.int16]):
        self._X_train = X_train

    @property
    def y_train(self) -> NDArray[np.int16]:
        if self._y_train is None:
            raise ValueError("y_train has not been set. Please call fit() before predict().")
        return self._y_train

    @y_train.setter
    def y_train(self, y_train: NDArray[np.int16]):
        self._y_train = y_train

    def fit(self, X_train: NDArray[np.int16], y_train: NDArray[np.int16]):
        self.X_train = X_train
        self.y_train = y_train

        if self.strategy == "constant":
            if self.constant not in np.unique(y_train):
                raise ValueError(f"Constant value '{self.constant}' is not in the training labels.")

    def predict(self, X_test: NDArray[np.int16]) -> NDArray[np.int16]:
        if self.strategy == "uniform":
            rng = np.random.RandomState(self.random_state)
            return rng.randint(np.min(self.y_train), np.max(self.y_train) + 1, size=len(X_test)).astype(np.int16)

        elif self.strategy == "constant":
            return np.full(len(X_test), self.constant)

        elif self.strategy == "most_frequent":
            values, counts = np.unique(self.y_train, return_counts=True)
            most_frequent = values[np.argmax(counts)]
            return np.full(len(X_test), most_frequent)

        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")
