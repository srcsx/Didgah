import pandas as pd
import os

class CSVImport:

    def loadCsv(csv_file_path):
        """
        Reads a CSV file and returns the headers and rows.

        Parameters:
            csv_file_path: Path to the CSV file.

        Returns:
            pandas.DataFrame: Processed data.
            None or an empty DataFrame if an error occurs.
        """
        if os.path.exists(csv_file_path):
            try:
                return pd.read_csv(csv_file_path)
            except Exception as e:
                print(f"ERROR: Encoutering problem while reading csv file.\nInnerException: {e}")
        else:
            print(f"ERROR: File path not found.\nGiven Path: {csv_file_path}")


    def saveCsvTotable(csv_file_path, save_method):
        """
        Saves a CSV file content in database.

        Parameters:
            csv_file_path: Path to the CSV file.
            save_method: Model method which gets data and saves it.

        Returns:
            list: The output of this function is a list of the table's column ID or -1,
            where -1 indicates that the operation has encountered an error.
        """
        dataframe = CSVImport.loadCsv(csv_file_path)
        save_result = []

        if dataframe is not None:
            for i in dataframe.values:
                try:
                    result = save_method(i[0])
                    save_result.append(result)
                except Exception as e:
                    print(f"ERROR: There is an exception in the given parameter: save_method.\nInnerException: {e}")
        else:
            print('ERROR: Dataframe is empty.')
            save_result.append(-1)

        return save_result


# # Usage Test
# if __name__ == "__main__":
#     from ..database.query.prof import createProf # A database save method dedicated for Prof model
#     from ..database.query.course import createCourse
#     CSVImport.saveCsvTotable("path", createProf)
#     CSVImport.saveCsvTotable("path", createCourse)