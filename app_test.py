from qa import QASystem

qa = QASystem()

while True:
    question = input("\nAsk a question (or type exit): ")
    if question.lower() == "exit":
        break

    answer = qa.answer(question)
    print("\n--- ANSWER ---")
    print(answer)
