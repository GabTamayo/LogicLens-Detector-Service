from abc import ABC, abstractmethod

class CodeComparator:
    def __init__(self, diff_weight=0.4, cosine_weight=0.6):
        self.diff_weight = diff_weight
        self.cosine_weight = cosine_weight

    def compare_sequences(self, code_a, code_b):
        import difflib
        return difflib.SequenceMatcher(None, code_a, code_b, False).ratio()

    def compare_structures(self, code_a, code_b):
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        tfidf = TfidfVectorizer().fit_transform([code_a, code_b])
        return cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

    def compare(self, code_a_seq, code_b_seq, code_a_struct, code_b_struct):
        diff_score = self.compare_sequences(code_a_seq, code_b_seq)
        cos_score = self.compare_structures(code_a_struct, code_b_struct)
        return (self.diff_weight * diff_score) + (self.cosine_weight * cos_score)

class BaseSimilarityDetector(ABC):
    def __init__(self):
        self.comparator = CodeComparator()

    @abstractmethod
    def parse_ast(self, code: str):
        pass

    def compare(self, code_a: str, code_b: str) -> float:
        ast_seq_a = self.parse_ast(code_a)
        ast_seq_b = self.parse_ast(code_b)

        ast_struct_a = " ".join(ast_seq_a)
        ast_struct_b = " ".join(ast_seq_b)

        return self.comparator.compare(ast_seq_a, ast_seq_b, ast_struct_a, ast_struct_b)

class JavaSimilarityDetector(BaseSimilarityDetector):
    def parse_ast(self, code: str):
        try:
            import javalang
            parse = javalang.parse.parse(code)
            sequence = []

            def walk(node):
                if isinstance(node, javalang.ast.Node):
                    sequence.append(node.__class__.__name__)
                    for child in node.children:
                        if isinstance(child, list):
                            for item in child:
                                walk(item)
                        else:
                            walk(child)

            walk(parse)
            return sequence
        except Exception:
            return []

class PythonSimilarityDetector(BaseSimilarityDetector):
    def parse_ast(self, code: str):
        import ast
        try:
            tree = ast.parse(code)
            sequence = [node.__class__.__name__ for node in ast.walk(tree)]
            return sequence
        except Exception:
            return []

def main():

    file_path1 = "D:/Submission Testing/rot13_1.java"
    file_path2 = "D:/Submission Testing/rot13_1.java"

    detector = JavaSimilarityDetector()

    try:
        with open(file_path1, 'r', encoding='utf-8') as f1, open(file_path2, 'r', encoding='utf-8') as f2:
            code1 = f1.read()
            code2 = f2.read()

        score = detector.compare(code1, code2)
        print(f"Similarity Score: {score:.0%}")
        return score

    except FileNotFoundError as e:
        print(f"Error: File not found - {e.filename}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    main()