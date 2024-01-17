import textstat

def evaluate_text(text):
    flesch_reading_ease = textstat.flesch_reading_ease(text)
    flesch_kincaid_grade = textstat.flesch_kincaid_grade(text)

    print(f"Flesch Reading Ease: {flesch_reading_ease}")
    print(f"Flesch-Kincaid Grade Level: {flesch_kincaid_grade}")

def main():
    text = input("Enter a sentence to evaluate: ")
    evaluate_text(text)

if __name__ == "__main__":
    main()
