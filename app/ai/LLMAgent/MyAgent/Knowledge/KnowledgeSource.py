import json
import os
from ..Knowledge.Knowledge import Knowledge

class FileKnowledge(Knowledge):

    def __init__(self, file_paths:list[str]):
        self.__name__ = "File Knowledge Extractor"
        self.__description__ = "Extracts knowledge (content) from given file paths"
        self.file_paths = file_paths

    @property
    def name(self):
        return self.__name__
    
    @property 
    def description(self):
        return self.__description__
    

    def get_content(self):

        for file_path in self.file_paths:

            file_type = os.path.splitext(file_path)[1].lower()
            # if len(file_path.split("/")) == 1:
            #     file_path = f"./source/{file_path}"
            # print(file_path)

            with open(file_path, "r") as f:

                if file_type == "json":
                    content = json.dumps(json.loads(f), indent=2)
                else:
                    content = f.read()
            
            yield content