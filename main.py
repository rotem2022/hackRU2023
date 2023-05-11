# This is a sample Python script.
import openai

openai.api_key = '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'


def askGPT(text, conv):
    message = text
    if len(conv) != 1:
        message = f"Conversation history:{' '.join(conv)}\nQuestion: {text}\nAnswer:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message,
        temperature=0.6,
        max_tokens=10,
    )
    conv.append(response.choices[0].text)
    return response.choices[0].text


if __name__ == '__main__':
    conversation_history = []  # Initialize conversation history as empty list
    while True:
        question = input("What is your question? ")
        conversation_history.append(question)
        answer = askGPT(question, conversation_history)
        print(answer)
