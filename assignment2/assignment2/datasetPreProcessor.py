################################################################################
# Author 1:      Jakob Marktl
# MatNr 1:       12335939
# Author 2:      Christoph Nagy
# MatNr 2:       12331569
# Author 3:      Firstname Lastname
# MatNr 3:       01234567
# File:          datasetPreProcessor.py
# Description:  A class to preprocess a zipped dataset containing student performance CSV files.
# Comments:    --
################################################################################


import os
import shutil
import zipfile

import pandas as pd


class DatasetPreprocessor:
    """
    A class to preprocess a zipped dataset containing student performance CSV files.
    """

    def __init__(self, zip_file_path):
        self.zip_file_path = zip_file_path
        self.target_column = "G3"
        self._data = None
        self._extract_and_prepare()

    def _extract_and_prepare(self):
        outer_dir = "temp_outer"
        inner_dir = "temp_inner"

        # Setup directories
        if os.path.exists(outer_dir):
            shutil.rmtree(outer_dir)
        if os.path.exists(inner_dir):
            shutil.rmtree(inner_dir)
        os.makedirs(outer_dir)
        os.makedirs(inner_dir)

        # Extract nested zip
        with zipfile.ZipFile(self.zip_file_path, "r") as outer_zip:
            outer_zip.extract("student.zip", outer_dir)
        with zipfile.ZipFile(os.path.join(outer_dir, "student.zip"), "r") as inner_zip:
            inner_zip.extract("student-mat.csv", inner_dir)
            inner_zip.extract("student-por.csv", inner_dir)

        # Load CSVs
        df1 = pd.read_csv(os.path.join(inner_dir, "student-mat.csv"), sep=";")
        df2 = pd.read_csv(os.path.join(inner_dir, "student-por.csv"), sep=";")
        df = pd.concat([df1, df2], ignore_index=True)

        # Replace known placeholders and empty strings with 0
        df.replace(["?", "NA", "null", ""], 0, inplace=True)

        # Encode categorical and binary fields
        mappings = {
            "school": {"GP": 0, "MS": 1},
            "Pstatus": {"T": 0, "A": 1},
            "sex": {"F": 0, "M": 1},
            "address": {"U": 0, "R": 1},
            "famsize": {"LE3": 0, "GT3": 1},
            "Mjob": {"teacher": 0, "health": 1, "services": 2, "at_home": 3, "other": 4},
            "Fjob": {"teacher": 0, "health": 1, "services": 2, "at_home": 3, "other": 4},
            "reason": {"home": 0, "reputation": 1, "course": 2, "other": 3},
            "guardian": {"mother": 0, "father": 1, "other": 2},
        }
        for col, mapping in mappings.items():
            if col in df.columns:
                df[col] = df[col].replace(mapping)

        # Encode yes/no as binary
        df.replace({"yes": 1, "no": 0}, inplace=True)

        # Fill any remaining NaNs with 0
        df.fillna(0, inplace=True)

        # Transform target variable
        df[self.target_column] = df[self.target_column].apply(self._map_grade)

        # Move target column to the end
        cols = [c for c in df.columns if c != self.target_column] + [self.target_column]
        df = df[cols]

        # Clean up
        shutil.rmtree(outer_dir)
        shutil.rmtree(inner_dir)

        self._data = df

    def _map_grade(self, grade):
        if 18 <= grade <= 20:
            return 1
        elif 16 <= grade <= 17:
            return 2
        elif 14 <= grade <= 15:
            return 3
        elif 10 <= grade <= 13:
            return 4
        else:
            return 5

    def to_csv(self, path):
        if self._data is None:
            raise ValueError("Data has not been prepared.")
        self._data.to_csv(path, index=False)
        print(f"Saved cleaned CSV to {path}")

    @property
    def data(self) -> pd.DataFrame:
        """
        Returns the cleaned and preprocessed dataset.

        Returns
        -------
        pd.DataFrame
            The cleaned dataset
        """
        if self._data is None:
            raise ValueError("Data has not been prepared. Please call _extract_and_prepare() first.")
        return self._data


if __name__ == "__main__":
    processor = DatasetPreprocessor("student+performance.zip")
    processor.to_csv("dataset.csv")
