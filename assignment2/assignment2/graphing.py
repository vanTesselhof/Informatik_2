import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from numpy.typing import NDArray
from sklearn.metrics import confusion_matrix
import pandas as pd

from assignment2.datasetClassifier import DatasetHandler

from typing import cast


class Graphing:
    def __init__(self, dataset_handler: DatasetHandler) -> None:
        self.dataset_handler = dataset_handler

    def print_feature_importances(self, importances: NDArray) -> None:
        feature_names = self.dataset_handler.x_train.columns
        sorted_indices = np.argsort(importances)[::-1]

        print("Feature ranking:")
        for i, index in enumerate(sorted_indices):
            feature = feature_names[index]
            importance = importances[index]
            print(f"{i + 1}. Feature {feature} ({importance:.4f})")

    def plot_feature_importances(self, importances: NDArray) -> None:
        feature_names = self.dataset_handler.x_train.columns
        indices = np.argsort(importances)[::-1]
        sorted_features = feature_names[indices]
        sorted_importances = importances[indices]

        fig = go.Figure(
            go.Bar(
                x=sorted_features,
                y=sorted_importances,
            )
        )
        fig.update_layout(
            title="Feature Importances",
            xaxis_title="Feature",
            yaxis_title="Importance",
        )
        fig.show()

    def plot_feature_correspondence(self, features: list[str]) -> None:
        for feature in features:
            self.visualize_boxplot_with_feature(feature)

    def visualize_boxplot_with_feature(self, feature: str) -> None:
        df = self.dataset_handler.dataset
        fig = px.box(
            df,
            x="G3",
            y=feature,
            points="all",
            title=f'Feature "{feature}" Correspondence to Grades',
            labels={"G3": "Grade", feature: feature},
        )
        fig.show()

    def plot_confusion_matrix(self, y_true: NDArray[np.int16], y_pred: NDArray[np.int16], classifier_name: str) -> None:
        cm = confusion_matrix(y_true, y_pred)
        raw_labels = np.unique(np.concatenate((y_true, y_pred)))
        labels = sorted(cast(list[int], raw_labels.tolist()))
        z_text = [[str(y) for y in x] for x in cm]

        fig = go.Figure(
            data=go.Heatmap(
                z=cm,
                x=labels,
                y=labels,
                text=z_text,
                hoverinfo="text",
                colorscale="Blues",
            )
        )
        fig.update_layout(
            title=f"Confusion Matrix for {classifier_name}",
            xaxis_title="Predicted Label",
            yaxis_title="True Label",
        )
        fig.show()

    def plot_evaluation_metrics(
        self, classifiers: list[str], metrics: dict[str, list[int]], title: str = "Evaluation Metrics by Classifier"
    ) -> None:
        fig = go.Figure()
        for metric_name, values in metrics.items():
            fig.add_trace(
                go.Bar(
                    name=metric_name,
                    x=classifiers,
                    y=values,
                )
            )

        fig.update_layout(
            barmode="group",
            title=title,
            xaxis_title="Classifiers",
            yaxis_title="Score",
        )
        fig.show()
