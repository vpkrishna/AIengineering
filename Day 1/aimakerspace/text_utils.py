import os
from PyPDF2  import PdfReader
from typing import List


class TextFileLoader:
    def __init__(self, path: str, encoding: str = "utf-8"):
        self.documents = []
        self.path = path
        self.encoding = encoding

    def load(self):
        if os.path.isdir(self.path):
            self.load_directory()
        elif os.path.isfile(self.path) and self.path.endswith(".txt"):
            self.load_file()
        else:
            raise ValueError(
                "Provided path is neither a valid directory nor a .txt file."
            )

    def load_file(self):
        with open(self.path, "r", encoding=self.encoding) as f:
            self.documents.append(f.read())

    def load_directory(self):
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith(".txt"):
                    with open(
                        os.path.join(root, file), "r", encoding=self.encoding
                    ) as f:
                        self.documents.append(f.read())

    def load_documents(self):
        self.load()
        return self.documents
    

class TextORPDFFileLoader:
    def __init__(self, path: str,encoding: str = "utf-8"):
        self.documents = []
        self.path = path
        self.encoding = encoding

    def load(self):
        if os.path.isdir(self.path):
            self.load_directory()
        elif os.path.isfile(self.path) and self.path.endswith((".txt", ".pdf")):
            self.load_file()
        else:
            raise ValueError(
                "Provided path is neither a valid directory nor a .txt or .pdf file."
            )

    def load_file(self):
        if self.path.endswith(".txt"):
            with open(self.path, "r") as f:
                self.documents.append(f.read())
        elif self.path.endswith(".pdf"):
            with open(self.path, "rb") as f:
                pdf = PdfReader(f)
                for page in pdf.pages:
                    self.documents.append(page.extract_text())

    def load_directory(self):
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith((".txt", ".pdf")):
                    with open(
                        os.path.join(root, file), "rb" if file.endswith(".pdf") else "r"
                    ) as f:
                        if file.endswith(".txt"):
                            self.documents.append(f.read())
                        elif file.endswith(".pdf"):
                            pdf = PdfReader(f)
                            for page in pdf.pages:
                                self.documents.append(page.extract_text())


    def load_documents(self):
        self.load()
        return self.documents



class CharacterTextSplitter:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        assert (
            chunk_size > chunk_overlap
        ), "Chunk size must be greater than chunk overlap"

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> List[str]:
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunks.append(text[i : i + self.chunk_size])
        return chunks

    def split_texts(self, texts: List[str]) -> List[str]:
        chunks = []
        for text in texts:
            chunks.extend(self.split(text))
        return chunks


if __name__ == "__main__":
    loader = TextFileLoader("data/KingLear.txt")
    loader.load()
    splitter = CharacterTextSplitter()
    chunks = splitter.split_texts(loader.documents)
    print(len(chunks))
    print(chunks[0])
    print("--------")
    print(chunks[1])
    print("--------")
    print(chunks[-2])
    print("--------")
    print(chunks[-1])
