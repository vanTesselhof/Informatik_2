################################################################################
# Author 1:      Jakob Marktl
# MatNr 1:       12335939
# Author 2:      Christoph Nagy
# MatNr 2:       12331569
# Author 3:      Maria Mikic
# MatNr 3:       12234490
# File:          classifierMetrics.py
# Description: ... short description of the file ...
# Comments:    ... comments for the tutors ...
#              ... can be multiline ...
################################################################################


from typing import Literal

import numpy as np
from numpy.typing import NDArray
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


class ClassifierMetrics:
    """
    A class containing static methods to compute various classification metrics.
    """

    @staticmethod
    def accuracy(y_true: NDArray[np.int16], y_pred: NDArray[np.int16]) -> float:
        """
        Compute the accuracy score.

        Args:
            y_true (NDArray[np.int16]): True labels.
            y_pred (NDArray[np.int16]): Predicted labels.

        Returns:
            float: Accuracy score.
        """
        return float(np.mean(y_true == y_pred))

    @staticmethod
    def precision(
        y_true: NDArray[np.int16],
        y_pred: NDArray[np.int16],
        average: Literal["micro", "macro", "samples", "weighted"] = "macro",
    ) -> float:
        """
        Compute the precision score.

        Args:
            y_true (NDArray[np.int16]): True labels.
            y_pred (NDArray[np.int16]): Predicted labels.
            average (str): Type of averaging to perform on the data. Default is "macro".

        Returns:
            float: Precision score.
        """
        return float(precision_score(y_true, y_pred, average=average, zero_division=0))

    @staticmethod
    def recall(
        y_true: NDArray[np.int16],
        y_pred: NDArray[np.int16],
        average: Literal["micro", "macro", "samples", "weighted"] = "macro",
    ) -> float:
        """
        Compute the recall score.

        Args:
            y_true (NDArray[np.int16]): True labels.
            y_pred (NDArray[np.int16]): Predicted labels.
            average (str): Type of averaging to perform on the data. Default is "macro".

        Returns:
            float: Recall score.
        """
        return float(recall_score(y_true, y_pred, average=average, zero_division=0))

    @staticmethod
    def f1_score(
        y_true: NDArray[np.int16],
        y_pred: NDArray[np.int16],
        average: Literal["micro", "macro", "samples", "weighted"] = "macro",
    ) -> float:
        """
        Compute the F1 score.

        Args:
            y_true (NDArray[np.int16]): True labels.
            y_pred (NDArray[np.int16]): Predicted labels.
            average (str): Type of averaging to perform on the data. Default is "macro".

        Returns:
            float: F1 score.
        """
        return float(f1_score(y_true, y_pred, average=average, zero_division=0))
