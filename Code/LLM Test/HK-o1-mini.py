import pandas as pd
import openai
import time
import os

# Set OpenAI API key
openai.api_key = ''  # Replace with your actual API key

# Fixed list of small questions in Chinese
questions_per_round = [
    "选项1：你有50%的机会赢得50港币，以及50%的机会赢得2000港币。\n选项2：你有100%的机会赢得800港币。",
    "选项1：你有70%的机会赢得50港币，以及30%的机会赢得2000港币。\n选项2：你有100%的机会赢得100港币。",
    "选项1：你有90%的机会赢得50港币，以及10%的机会赢得2000港币。\n选项2：你有100%的机会赢得400港币。",
    "选项1：你有50%的机会赢得50港币，以及50%的机会赢得2000港币。\n选项2：你有100%的机会赢得600港币。",
    "选项1：你有70%的机会赢得50港币，以及30%的机会赢得2000港币。\n选项2：你有100%的机会赢得200港币。",
    "选项1：你有90%的机会赢得50港币，以及10%的机会赢得2000港币。\n选项2：你有100%的机会赢得200港币。",
    "选项1：你有50%的机会赢得50港币，以及50%的机会赢得2000港币。\n选项2：你有100%的机会赢得400港币。",
    "选项1：你有70%的机会赢得50港币，以及30%的机会赢得2000港币。\n选项2：你有100%的机会赢得500港币。",
    "选项1：你有90%的机会赢得50港币，以及10%的机会赢得2000港币。\n选项2：你有100%的机会赢得100港币。",
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
        print(f"发生错误: {e}")
        return "错误", 0  # Return error message and tokens used as 0

def save_results(results):
    """Save results to an Excel file."""
    output_filename = 'output_o1-mini-HK-CHN-3.xlsx'
    results.to_excel(output_filename, index=False)
    print(f"所有响应已保存到 '{output_filename}'。")

if __name__ == "__main__":
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define input and output file paths
    input_filename = os.path.join(script_dir, 'survey_responses-chn.xlsx')  # Input file path
    output_filename = os.path.join(script_dir, 'output_o1-mini-HK-CHN-1.xlsx')  # Output file path

    delay_between_requests = 1
    responses_df = pd.read_excel(input_filename)  # Read from Excel file

    if 'prompt' not in responses_df.columns:
        raise ValueError("未找到 'prompt' 列在Excel文件中。")

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
                "content": f"这是你的问题:\n{question}\n\n"
                           "请评估预期差异并选择 '选项1' 或 '选项2'。你只需要提供这个答案，并不需要告诉我你思考的过程。"
            })

            print(f"开始第 {round_num + 1} 轮的问题: {question}")
            answer, tokens_used = ask_openai(conversation)

            # Store the response in the results DataFrame
            question_index = questions_per_round.index(question)
            results.at[round_num, f'a{question_index + 1}'] = answer

            print(f"第 {question_index + 1} 个问题的响应: {answer} (使用了 {tokens_used} 个token)\n")
            time.sleep(delay_between_requests)  # Delay between requests

    save_results(results)  # Save results after processing all rounds