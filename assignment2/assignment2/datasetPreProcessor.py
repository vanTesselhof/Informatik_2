import os
import shutil
import zipfile
import numpy as np
import pandas as pd


class DatasetPreprocessor:
    """
    A class to preprocess a zipped dataset containing student performance CSV files.

    This class handles:
    - Extracting nested zip files
    - Loading and cleaning data from CSV files
    - Encoding categorical and binary variables
    - Binning the target variable into performance categories
    - Saving the cleaned dataset to CSV

    Attributes:
    -----------
    zip_file_path : str
        Path to the main zip file
    target_column : str
        Name of the target column (default: "G3")
    _data : pd.DataFrame
        Cleaned and preprocessed data
    """

    def __init__(self, zip_file_path):
        """
        Initializes the DatasetPreprocessor with a given zip file path and starts preprocessing.

        Parameters
        ----------
        zip_file_path : str
            Path to the zip file containing the dataset
        """
        self.zip_file_path = zip_file_path
        self.target_column = "G3"
        self._data = None
        self._extract_and_prepare()

    def _extract_and_prepare(self):
        """
        Extracts the nested zip files, reads the CSV files, cleans the data,
        encodes categorical values, transforms the target variable, and stores the result internally.
        """
        outer_dir = "temp_outer"
        inner_dir = "temp_inner"

        # Cleanup and setup temporary directories
        if os.path.exists(outer_dir):
            shutil.rmtree(outer_dir)
        if os.path.exists(inner_dir):
            shutil.rmtree(inner_dir)
        os.makedirs(outer_dir)
        os.makedirs(inner_dir)

        # Extract nested zip files
        with zipfile.ZipFile(self.zip_file_path, "r") as outer_zip:
            outer_zip.extract("student.zip", outer_dir)
        with zipfile.ZipFile(os.path.join(outer_dir, "student.zip"), "r") as inner_zip:
            inner_zip.extract("student-mat.csv", inner_dir)
            inner_zip.extract("student-por.csv", inner_dir)

        # Load CSV files
        df1 = pd.read_csv(os.path.join(inner_dir, "student-mat.csv"), sep=";")
        df2 = pd.read_csv(os.path.join(inner_dir, "student-por.csv"), sep=";")
        df = pd.concat([df1, df2], ignore_index=True)

        # Replace and fill missing values
        df.replace(["?", "NA", "null", ""], np.nan, inplace=True)
        df.fillna(df.median(numeric_only=True), inplace=True)

        # Convert to numeric where possible
        for col in df.columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                df[col] = pd.to_numeric(df[col], errors="coerce")

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
                df[col].replace(mapping, inplace=True)

        df.replace({"yes": 1, "no": 0}, inplace=True)

        # Transform target column
        df[self.target_column] = df[self.target_column].apply(self._map_grade)

        # Move target column to the end
        columns = [col for col in df.columns if col != self.target_column] + [self.target_column]
        df = df[columns]

        # Clean up temporary directories
        shutil.rmtree(outer_dir)
        shutil.rmtree(inner_dir)

        self._data = df

    def _map_grade(self, grade):
        """
        Maps a numerical grade (G3) into categorical performance levels from 1 (best) to 5 (worst).

        Parameters
        ----------
        grade : int or float
            Original grade value

        Returns
        -------
        int
            Binned performance category
        """
        if 18 <= grade <= 20:
            return 1
        if 16 <= grade <= 17:
            return 2
        if 14 <= grade <= 15:
            return 3
        if 10 <= grade <= 13:
            return 4
        return 5

    def to_csv(self, path):
        """
        Exports the cleaned and transformed dataset to a CSV file.

        Parameters
        ----------
        path : str
            File path to save the CSV
        """
        if self._data is None:
            raise ValueError("Data has not been prepared. Please call _extract_and_prepare() first.")
        self._data.to_csv(path, index=False)
        print(f"Saved cleaned CSV to {path}")


if __name__ == "__main__":
    processor = DatasetPreprocessor("student+performance.zip")
    processor.to_csv("cleaned_student_dataset.csv")
