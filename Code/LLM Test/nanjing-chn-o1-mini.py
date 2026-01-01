import pandas as pd
import openai
import time

# Set OpenAI API key
openai.api_key = ''  # Replace with your actual API key

# Fixed list of small questions (translated into Chinese)
questions_per_round = [
    "选项 1：您有 10% 的机会赢得 2 元，剩下 90% 的机会赢得 1.6 元。\n选项 2：您有 10% 的机会赢得 3.85 元，剩下 90% 的机会赢得 0.1 元。",
    "选项 1：您有 20% 的机会赢得 2 元，剩下 80% 的机会赢得 1.6 元。\n选项 2：您有 20% 的机会赢得 3.85 元，剩下 80% 的机会赢得 0.1 元。",
    "选项 1：您有 30% 的机会赢得 2 元，剩下 70% 的机会赢得 1.6 元。\n选项 2：您有 30% 的机会赢得 3.85 元，剩下 70% 的机会赢得 0.1 元。",
    "选项 1：您有 40% 的机会赢得 2 元，剩下 60% 的机会赢得 1.6 元。\n选项 2：您有 40% 的机会赢得 3.85 元，剩下 60% 的机会赢得 0.1 元。",
    "选项 1：您有 50% 的机会赢得 2 元，剩下 50% 的机会赢得 1.6 元。\n选项 2：您有 50% 的机会赢得 3.85 元，剩下 50% 的机会赢得 0.1 元。",
    "选项 1：您有 60% 的机会赢得 2 元，剩下 40% 的机会赢得 1.6 元。\n选项 2：您有 60% 的机会赢得 3.85 元，剩下 40% 的机会赢得 0.1 元。",
    "选项 1：您有 70% 的机会赢得 2 元，剩下 30% 的机会赢得 1.6 元。\n选项 2：您有 70% 的机会赢得 3.85 元，剩下 30% 的机会赢得 0.1 元。",
    "选项 1：您有 80% 的机会赢得 2 元，剩下 20% 的机会赢得 1.6 元。\n选项 2：您有 80% 的机会赢得 3.85 元，剩下 20% 的机会赢得 0.1 元。",
    "选项 1：您有 90% 的机会赢得 2 元，剩下 10% 的机会赢得 1.6 元。\n选项 2：您有 90% 的机会赢得 3.85 元，剩下 10% 的机会赢得 0.1 元。",
    "选项 1：您有 100% 的机会赢得 2 元，没有机会赢得 1.6 元。\n选项 2：您有 100% 的机会赢得 3.85 元，没有机会赢得 0.1 元。",
]

def ask_openai(conversation):
    """Call OpenAI API to get a response and maintain conversation context."""
    try:
        response = openai.ChatCompletion.create(
            model="o1-mini",  # Use the o1-mini model
            messages=conversation,
        )
        answer = response['choices'][0]['message']['content']
        tokens_used = response['usage']['total_tokens']
        return answer.strip(), tokens_used
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Error", 0  # Return error message and tokens used as 0

def save_results(results):
    """Save results to an Excel file."""
    output_filename = 'output_o1-mini-nanjing-CHN-3-124.xlsx'
    results.to_excel(output_filename, index=False)
    print(f"All responses have been saved to '{output_filename}'.")

if __name__ == "__main__":
    delay_between_requests = 0.8
    responses_df = pd.read_excel('survey_responses-CHN-3-124.xlsx')  # Read from Excel file

    if 'prompt' not in responses_df.columns:
        raise ValueError("The 'prompt' column is not found in the Excel file.")

    # Prepare results DataFrame
    results = responses_df.copy()

    # Initialize columns for answers
    for i in range(10):
        results[f'a{i + 1}'] = None

    total_rounds = len(responses_df)

    for round_num in range(total_rounds):
        main_question = responses_df.iloc[round_num]['prompt']
        conversation = [
            {"role": "user", "content": "本调查旨在评估人们的风险态度。"},
            {"role": "user", "content": main_question}
        ]

        # Step through each question one at a time
        for question in questions_per_round:
            conversation.append({
                "role": "user",
                "content": f"这是您的问题：\n{question}\n\n"
                           "请评估预期的差异并选择 '选项 1' 或 '选项 2'。"
            })

            print(f"Starting question for round {round_num + 1}: {question}")
            answer, tokens_used = ask_openai(conversation)

            # Store the response in the results DataFrame
            question_index = questions_per_round.index(question)
            results.at[round_num, f'a{question_index + 1}'] = answer

            print(f"Response for question {question_index + 1}: {answer} (used {tokens_used} tokens)\n")
            time.sleep(delay_between_requests)  # Delay between requests

    save_results(results)  # Save results after processing all rounds