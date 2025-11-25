from abc import ABC, abstractmethod
from difflib import SequenceMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class CodeComparator:
    def __init__(self, min_block_size=3):
        self.min_block_size = min_block_size

    def find_matching_blocks(self, seq_a, seq_b):
        matcher = SequenceMatcher(None, seq_a, seq_b, autojunk=False)
        return [
            (a, b, size)
            for a, b, size in matcher.get_matching_blocks()
            if size >= self.min_block_size
        ]

    def compare_sequences(self, code_a, code_b):
        return SequenceMatcher(None, code_a, code_b).ratio()

    def compare_structures(self, code_a, code_b):
        tfidf = TfidfVectorizer().fit_transform([code_a, code_b])
        return cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]


class BaseSimilarityDetector(ABC):
    def __init__(self, min_block_size=3):
        self.comparator = CodeComparator(min_block_size)

    @abstractmethod
    def parse_ast_with_lines(self, code: str):
        """Parse AST and return (sequence, line_numbers)."""
        pass

    def _remove_overlapping_matches(self, matches):
        if not matches:
            return []

        filtered = []
        for match in matches:
            a_start, a_end = match['code_a']
            b_start, b_end = match['code_b']

            if not any(
                    not (a_end < f['code_a'][0] or a_start > f['code_a'][1]) and
                    not (b_end < f['code_b'][0] or b_start > f['code_b'][1])
                    for f in filtered
            ):
                filtered.append(match)

        return sorted(filtered, key=lambda m: m['code_a'][0])

    def compare(self, code_a: str, code_b: str):
        seq_a, lines_a = self.parse_ast_with_lines(code_a)
        seq_b, lines_b = self.parse_ast_with_lines(code_b)

        struct_a = " ".join(seq_a)
        struct_b = " ".join(seq_b)

        seq_score1 = self.comparator.compare_sequences(seq_a, seq_b)
        seq_score2 = self.comparator.compare_sequences(seq_b, seq_a)
        seq_score = (seq_score1 + seq_score2) / 2

        struct_score1 = self.comparator.compare_structures(struct_a, struct_b)
        struct_score2 = self.comparator.compare_structures(struct_b, struct_a)
        struct_score = (struct_score1 + struct_score2) / 2

        avg_score = (seq_score + struct_score) / 2

        ast_matches = self.comparator.find_matching_blocks(seq_a, seq_b)

        line_matches = []
        for a_start, b_start, size in ast_matches:
            a_lines = [lines_a[i] for i in range(a_start, a_start + size) if lines_a[i] > 0]
            b_lines = [lines_b[i] for i in range(b_start, b_start + size) if lines_b[i] > 0]

            if a_lines and b_lines:
                line_matches.append({
                    'code_a': (min(a_lines), max(a_lines)),
                    'code_b': (min(b_lines), max(b_lines)),
                })

        filtered_matches = self._remove_overlapping_matches(line_matches)

        return {
            'seq_score': seq_score,
            'struct_score': struct_score,
            'avg_score': avg_score,
            'line_matches': filtered_matches
        }


class JavaSimilarityDetector(BaseSimilarityDetector):
    def parse_ast_with_lines(self, code: str):
        try:
            import javalang
            parse = javalang.parse.parse(code)
            sequence, line_numbers = [], []

            def walk(node, last_line=1):
                if isinstance(node, javalang.ast.Node):
                    sequence.append(node.__class__.__name__)
                    pos = getattr(node, 'position', None)
                    line = pos.line if pos and getattr(pos, 'line', None) else last_line
                    line_numbers.append(line)
                    for child in node.children:
                        if isinstance(child, list):
                            for c in child:
                                walk(c, line)
                        else:
                            walk(child, line)

            walk(parse)
            return sequence, line_numbers
        except Exception:
            return [], []


class PythonSimilarityDetector(BaseSimilarityDetector):
    def parse_ast_with_lines(self, code: str):
        import ast
        try:
            tree = ast.parse(code)
            sequence, line_numbers = [], []

            for node in ast.walk(tree):
                sequence.append(node.__class__.__name__)
                line_numbers.append(getattr(node, 'lineno', line_numbers[-1] if line_numbers else 1))

            return sequence, line_numbers
        except Exception:
            return [], []


def format_matches(matches):
    for i, m in enumerate(matches, 1):
        print(f"Match {i}: code_a lines {m['code_a'][0]}-{m['code_a'][1]}, "
              f"code_b lines {m['code_b'][0]}-{m['code_b'][1]}")


def main():
    file1 = "C:/Users/gabot/Downloads/text2.java"
    file2 = "C:/Users/gabot/Downloads/text1.java"
    detector = JavaSimilarityDetector()

    try:
        with open(file1, encoding='utf-8') as f1, open(file2, encoding='utf-8') as f2:
            code1, code2 = f1.read(), f2.read()

        results = detector.compare(code1, code2)

        print(f"Sequence Score: {results['seq_score']:.0%}")
        print(f"Structure Score: {results['struct_score']:.0%}")
        print(f"Average Score: {results['avg_score']:.0%}\n")
        format_matches(results['line_matches'])

        return {'scores': results, 'matches': results['line_matches']}

    except FileNotFoundError as e:
        print(f"Error: File not found - {e.filename}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
