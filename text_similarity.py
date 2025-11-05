import os
import difflib

def text_similarity(file_a, file_b):
    with open(file_a, "r") as file_a, open(file_b, "r") as file_b:
        content_a = file_a.read()
        content_b = file_b.read()

        result = difflib.SequenceMatcher(None,content_a,content_b,False).ratio()

        print(f"The similarity result is: {result:.2f}")

def main():
    file_path1 = "D:/PythonCourse/file_handling/file_detection/folder/text.txt"
    file_path2 = "D:/PythonCourse/file_handling/file_detection/folder/text1.txt"

    if os.path.exists(file_path1) and os.path.exists(file_path2):
        text_similarity(file_path1, file_path2)
    else:
        print("Something went wrong!")

if __name__ == "__main__":
    main()