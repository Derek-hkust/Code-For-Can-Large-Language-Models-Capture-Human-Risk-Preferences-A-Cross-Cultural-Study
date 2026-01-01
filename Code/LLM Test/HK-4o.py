import pandas as pd
import openai
import time

# 设置 OpenAI API 密钥
openai.api_key = ''  # 请替换为您的实际 API 密钥

# 固定的小问题列表
questions_per_round = [
    "Option 1: you will have 50% chance of winning 50 HKD and the remaining 50% chance of winning 2000 HKD.\nOption 2: you will have 100% chance of winning 800 HKD.",
    "Option 1: you will have 70% chance of winning 50 HKD and the remaining 30% chance of winning 2000 HKD.\nOption 2: you will have 100% chance of winning 100 HKD.",
    "Option 1: you will have 90% chance of winning 50 HKD and the remaining 10% chance of winning 2000 HKD.\nOption 2: you will have 100% chance of winning 400 HKD.",
    "Option 1: you will have 50% chance of winning 50 HKD and the remaining 50% chance of winning 2000 HKD.\nOption 2: you will have 100% chance of winning 600 HKD.",
    "Option 1: you will have 70% chance of winning 50 HKD and the remaining 30% chance of winning 2000 HKD.\nOption 2: you will have 100% chance of winning 200 HKD.",
    "Option 1: you will have 90% chance of winning 50 HKD and the remaining 10% chance of winning 2000 HKD.\nOption 2: you will have 100% chance of winning 200 HKD.",
    "Option 1: you will have 50% chance of winning 50 HKD and the remaining 50% chance of winning 2000 HKD.\nOption 2: you will have 100% chance of winning 400 HKD.",
    "Option 1: you will have 70% chance of winning 50 HKD and the remaining 30% chance of winning 2000 HKD.\nOption 2: you will have 100% chance of winning 500 HKD.",
    "Option 1: you will have 90% chance of winning 50 HKD and the remaining 10% chance of winning 2000 HKD.\nOption 2: you will have 100% chance of winning 100 HKD.",
]

def ask_openai(conversation):
    """调用 OpenAI API 获取响应并维护对话上下文。"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # 使用 GPT-4 模型
            messages=conversation,
            max_tokens=600,
        )
        answer = response['choices'][0]['message']['content']
        tokens_used = response['usage']['total_tokens']
        return answer.strip(), tokens_used
    except Exception as e:
        print(f"发生错误: {e}")
        return "错误", 0  # 返回错误消息并将使用的令牌数设为 0

def save_results(results, run_number):
    """将结果保存到 Excel 文件。"""
    output_filename = f'output_gpt4_hk_2-55.xlsx'
    results.to_excel(output_filename, index=False)
    print(f"所有响应已保存到 '{output_filename}'。")

if __name__ == "__main__":
    delay_between_requests = 1
    responses_df = pd.read_excel('survey_responses-55.xlsx')  # 从 Excel 文件读取

    if 'prompt' not in responses_df.columns:
        raise ValueError("在 Excel 文件中未找到 'prompt' 列。")

    run_number = 1  # 设置运行编号为 1
    start_time = time.time()
    results = responses_df.copy()

    # 初始化答案列
    for i in range(10):
        results[f'a{i + 1}'] = None

    # 遍历每一行的响应
    total_rounds = len(responses_df)

    for round_num in range(total_rounds):
        main_question = responses_df.iloc[round_num]['prompt']
        conversation = [
            {"role": "user", "content": "This survey aims to estimate people's risk attitudes."},
            {"role": "user", "content": main_question}
        ]

        # 按顺序处理每个问题
        for question in questions_per_round:
            conversation.append({
                "role": "user",
                "content": f"Here is your question:\n{question}\n\n"
                           "Please evaluate the expected differences and choose 'Option 1' or 'Option 2'. You do not need to provide your thought process in your answer."
            })

            print(f"开始处理第 {round_num + 1} 轮的问题: {question}")
            answer, tokens_used = ask_openai(conversation)

            # 将响应存储在结果 DataFrame 中
            question_index = questions_per_round.index(question)
            results.at[round_num, f'a{question_index + 1}'] = answer

            print(f"第 {question_index + 1} 问题的响应: {answer} (使用了 {tokens_used} 个令牌)\n")
            time.sleep(delay_between_requests)

    save_results(results, run_number)
    elapsed_time = time.time() - start_time
    print(f"程序运行时间: {elapsed_time:.2f} 秒")