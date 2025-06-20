################################################################################
# Author 1:      Jakob Marktl
# MatNr 1:       12335939
# Author 2:      Christoph Nagy
# MatNr 2:       12331569
# Author 3:      Firstname Lastname
# MatNr 3:       01234567
# File:          datasetClassifier.py
# Description: ... short description of the file ...
# Comments:    ... comments for the tutors ...
#              ... can be multiline ...
################################################################################


from typing import Literal

import numpy as np
import pandas as pd
from numpy.typing import NDArray

from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from assignment2.classifierMetrics import ClassifierMetrics
from assignment2.simpleBaselineClassifier import SimpleBaselineClassifier


class DatasetHandler:
    """
    A class to handle dataset loading and preprocessing for bike sharing data.

    Attributes:
        dataset (pd.DataFrame): The loaded dataset.
        X (pd.DataFrame): Features from the dataset.
        y (pd.Series): Labels from the dataset.
        x_train (pd.DataFrame): Training features after the train-test split.
        x_test (pd.DataFrame): Testing features after the train-test split.
        y_train (pd.Series): Training labels after the train-test split.
        y_test (pd.Series): Testing labels after the train-test split.
    """

    def __init__(self, dataset_path: str) -> None:
        """
        Initialize the DatasetHandler with the path to the dataset.

        Args:
            dataset_path (str): Path to the CSV file containing the dataset.
        """
        self.dataset = pd.read_csv(dataset_path, sep=",")
        self.X = self.dataset.iloc[:, :-1]
        self.y = self.dataset.iloc[:, -1]

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=0
        )


class ClassifierBase:
    """
    A base class for classifiers.

    Attributes:
        y_pred (NDArray[np.int16]): Predictions made by the classifier.
        name (str): Name of the classifier.
    """

    def __init__(self) -> None:
        """
        Initialize the ClassifierBase.
        """
        self.y_pred = None
        self.name = "ClassifierBase"

    def predict(self, x_test: NDArray[np.int16]) -> NDArray[np.int16]:
        """
        Make predictions using the classifier.

        Args:
            x_test (NDArray[np.int16]): Testing features.

        Returns:
            NDArray[np.int16]: Predicted labels.
        """
        raise NotImplementedError("Subclasses should implement this method")

    def fit(self, x_train: NDArray[np.int16], y_train: NDArray[np.int16]) -> None:
        """
        Fit the classifier to the training data.

        Args:
            x_train (NDArray[np.int16]): Training features.
            y_train (NDArray[np.int16]): Training labels.
        """
        self.x_train = x_train
        self.y_train = y_train

    def metrics(self, y_test: NDArray[np.int16], y_pred: NDArray[np.int16]) -> str:
        """
        Calculate and return performance metrics for the classifier.

        Args:
            y_test (NDArray[np.int16]): True labels.
            y_pred (NDArray[np.int16]): Predicted labels.

        Returns:
            str: A string summarizing accuracy, precision, recall, and F1 score.
        """
        return (
            f"Classifier: {self.__class__.__name__}\n"
            f"Accuracy: {ClassifierMetrics.accuracy(y_test, y_pred):.4f}\n"
            f"Precision: {ClassifierMetrics.precision(y_test, y_pred):.4f}\n"
            f"Recall: {ClassifierMetrics.recall(y_test, y_pred):.4f}\n"
            f"F1 Score: {ClassifierMetrics.f1_score(y_test, y_pred):.4f}"
        )


class GaussianNBClassifier(ClassifierBase):
    """
    A Gaussian Naive Bayes classifier.
    """

    def __init__(self) -> None:
        """
        Initialize the GaussianNBClassifier.
        """
        super().__init__()
        self.name = "GaussianNB"

    def predict(self, x_test: NDArray[np.int16]) -> NDArray[np.int16]:
        """
        Make predictions using the Gaussian Naive Bayes classifier.

        Args:
            x_test (NDArray[np.int16]): Testing features.

        Returns:
            NDArray[np.int16]: Predicted labels.
        """
        gnb = GaussianNB()
        gnb.fit(self.x_train, self.y_train)
        return gnb.predict(x_test)


class DecisionTreeClassifier(ClassifierBase):
    """
    A Decision Tree classifier.
    """

    def __init__(self) -> None:
        """
        Initialize the DecisionTreeClassifier.
        """
        super().__init__()
        self.name = "DecisionTree"

    def predict(self, x_test: NDArray[np.int16]) -> NDArray[np.int16]:
        """
        Make predictions using the Decision Tree classifier.

        Args:
            x_test (NDArray[np.int16]): Testing features.

        Returns:
            NDArray[np.int16]: Predicted labels.
        """
        clf = tree.DecisionTreeClassifier(random_state=0)
        clf.fit(self.x_train, self.y_train)
        return clf.predict(x_test).astype(np.int16)


class KNNClassifier(ClassifierBase):
    """
    A k-Nearest Neighbors classifier.

    Attributes:
        k (int): The number of neighbors to use.
    """

    def __init__(self, k: int = 5) -> None:
        """
        Initialize the KNNClassifier.

        Args:
            k (int): The number of neighbors to use (default is 5).
        """
        super().__init__()
        self.k = k
        self.name = "KNN"

    def predict(self, x_test: NDArray[np.int16]) -> NDArray[np.int16]:
        """
        Make predictions using the k-Nearest Neighbors classifier.

        Args:
            x_test (NDArray[np.int16]): Testing features.

        Returns:
            NDArray[np.int16]: Predicted labels.
        """
        knn = KNeighborsClassifier(n_neighbors=self.k)
        knn.fit(self.x_train, self.y_train)
        return knn.predict(x_test).astype(np.int16)


class RandomForestClassifierModel(ClassifierBase):
    """
    A Random Forest classifier.

    Attributes:
        n_estimators (int): The number of trees in the forest.
        random_state (int): The random seed.
        feature_importances (NDArray[np.float64]): The feature importances after fitting.
    """

    def __init__(self, n_estimators: int = 100, random_state: int = 0) -> None:
        """
        Initialize the RandomForestClassifierModel.

        Args:
            n_estimators (int): The number of trees in the forest (default is 100).
            random_state (int): The random seed (default is 0).
        """
        super().__init__()
        self.name = "RandomForest"
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.feature_importances = None

    def predict(self, x_test: NDArray[np.int16]) -> NDArray[np.int16]:
        """
        Make predictions using the Random Forest classifier.

        Args:
            x_test (NDArray[np.int16]): Testing features.

        Returns:
            NDArray[np.int16]: Predicted labels.
        """
        rf = RandomForestClassifier(n_estimators=self.n_estimators, random_state=self.random_state)
        rf.fit(self.x_train, self.y_train)
        self.feature_importances = rf.feature_importances_
        return rf.predict(x_test).astype(np.int16)


class SVMClassifier(ClassifierBase):
    """
    A Support Vector Machine classifier.

    Attributes:
        kernel (str): The kernel type to be used in the algorithm.
        C (float): Regularization parameter.
    """

    def __init__(self, kernel: Literal["linear", "rbf", "poly", "sigmoid"] = "linear", c: float = 1.0) -> None:
        """
        Initialize the SVMClassifier.

        Args:
            kernel (str): The kernel type to be used in the algorithm (default is 'linear').
            c (float): Regularization parameter (default is 1.0).
        """
        super().__init__()
        self.kernel: Literal["linear"] | Literal["rbf"] | Literal["poly"] | Literal["sigmoid"] = kernel
        self.c = c
        self.name = "SVM"

    def predict(self, x_test: NDArray[np.int16]) -> NDArray[np.int16]:
        """
        Make predictions using the Support Vector Machine classifier.

        Args:
            x_test (NDArray[np.int16]): Testing features.

        Returns:
            NDArray[np.int16]: Predicted labels.
        """
        svm = SVC(kernel=self.kernel, C=self.c)
        svm.fit(self.x_train, self.y_train)
        return svm.predict(x_test).astype(np.int16)


class LogisticRegressionClassifier(ClassifierBase):
    """
    A Logistic Regression classifier.

    Attributes:
        max_iter (int): Maximum number of iterations for solver to converge.
        random_state (int): The random seed.
    """

    def __init__(self, max_iter: int = 1000, random_state: int = 0) -> None:
        """
        Initialize the LogisticRegressionClassifier.

        Args:
            max_iter (int): Maximum number of iterations (default is 1000).
            random_state (int): The random seed (default is 0).
        """
        super().__init__()
        self.max_iter = max_iter
        self.random_state = random_state
        self.name = "LogisticRegression"

    def predict(self, x_test: NDArray[np.int16]) -> NDArray[np.int16]:
        """
        Make predictions using the Logistic Regression classifier.

        Args:
            x_test (NDArray[np.int16]): Testing features.

        Returns:
            NDArray[np.int16]: Predicted labels.
        """
        lr = LogisticRegression(max_iter=self.max_iter, random_state=self.random_state)
        lr.fit(self.x_train, self.y_train)
        return lr.predict(x_test).astype(np.int16)


class StudentPerformanceExperiment:
    """
    A class to run machine learning experiments on the bike sharing dataset.
    """

    def __init__(self, dataset_path: str) -> None:
        """
        Initialize the experiment with the dataset path.

        Args:
            dataset_path (str): Path to the dataset file (CSV or ZIP).
        """
        self.dataset_handler = DatasetHandler(dataset_path)
        self.classifiers = []
        self.results = {}
        self._initialize_classifiers()

    def _initialize_classifiers(self) -> None:
        """
        Initialize all classifiers for the experiment.
        """
        self.classifiers = [
            SimpleBaselineClassifier(strategy="most_frequent", random_state=0),
            SimpleBaselineClassifier(strategy="uniform", random_state=0),
            GaussianNBClassifier(),
            DecisionTreeClassifier(),
            KNNClassifier(k=5),
            RandomForestClassifierModel(n_estimators=100, random_state=0),
            SVMClassifier(kernel="rbf", c=1.0),
            LogisticRegressionClassifier(max_iter=1000, random_state=0),
        ]
