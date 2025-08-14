from ..Tools.Tool import Tool
import os
import json
import csv

class FileReaderTool(Tool):

    def __init__(self):
        self.__name__ = "read_file"
        self.__description__ = "Read and Return the Contents of a File."
    
    @property
    def name(self):
        return self.__name__
    
    @property
    def description(self):
        return self.__description__
    
    
    def _run_implementation(self, file_path: str):

        file_path = os.path.abspath(file_path)

        if not os.path.exists(file_path):
            return FileNotFoundError(f"{file_path} doesn't exits")
        
        file_type = os.path.splitext(file_path)[1].lower()
        
        with open(file_path, "r") as f:
            
            if file_type == ".json":
                content = json.dumps(json.loads(f.read()), indent=2)
            
            elif file_type == ".csv":
                content = list(csv.DictReader(f))

            elif file_type == ".txt" or file_type == ".md":
                content = f.read()

            else:
                return Exception(f"Invalid File type. accepts only .json, .csv, .txt and .md extention files, but received {file_type}")
            
        return content