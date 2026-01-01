import pandas as pd
import openai
import time

# Set OpenAI API key
openai.api_key = ''  # Replace with your actual API key

# Fixed list of small questions
questions_per_round = [
    "Option 1: you will have 50% chance of winning 0.5 AUD and the remaining 50% chance of winning 20 AUD.\nOption 2: you will win 8 AUD for sure.",
    "Option 1: you will have 70% chance of winning 0.5 AUD and the remaining 30% chance of winning 20 AUD.\nOption 2: you will win 1 AUD for sure.",
    "Option 1: you will have 90% chance of winning 0.5 AUD and the remaining 10% chance of winning 20 AUD.\nOption 2: you will win 4 AUD for sure.",
    "Option 1: you will have 50% chance of winning 0.5 AUD and the remaining 50% chance of winning 20 AUD.\nOption 2: you will win 6 AUD for sure.",
    "Option 1: you will have 70% chance of winning 0.5 AUD and the remaining 30% chance of winning 20 AUD.\nOption 2: you will win 2 AUD for sure.",
    "Option 1: you will have 90% chance of winning 0.5 AUD and the remaining 10% chance of winning 20 AUD.\nOption 2: you will win 2 AUD for sure.",
    "Option 1: you will have 50% chance of winning 0.5 AUD and the remaining 50% chance of winning 20 AUD.\nOption 2: you will win 4 AUD for sure.",
    "Option 1: you will have 70% chance of winning 0.5 AUD and the remaining 30% chance of winning 20 AUD.\nOption 2: you will win 5 AUD for sure.",
    "Option 1: you will have 90% chance of winning 0.5 AUD and the remaining 10% chance of winning 20 AUD.\nOption 2: you will win 1 AUD for sure."
]

def ask_openai(conversation):
    """Call OpenAI API to get a response and maintain conversation context."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Use GPT-4 model
            messages=conversation,
        )
        answer = response['choices'][0]['message']['content']
        tokens_used = response['usage']['total_tokens']
        return answer.strip(), tokens_used
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Error", 0  # Return error message and tokens used as 0

def save_results(results, run_number):
    """Save results to an Excel file."""
    output_filename = f'output_gpt4_aus_{run_number}.xlsx'
    results.to_excel(output_filename, index=False)
    print(f"All responses have been saved to '{output_filename}'.")

if __name__ == "__main__":
    delay_between_requests = 1
    responses_df = pd.read_excel('output_survey_responses_no_income.xlsx')  # Read from Excel file

    if 'prompt' not in responses_df.columns:
        raise ValueError("The 'prompt' column is not found in the Excel file.")

    for run_number in range(1, 4):
        start_time = time.time()
        results = responses_df.copy()

        # Initialize columns for answers
        for i in range(9):
            results[f'a{i + 1}'] = None

        total_rounds = len(responses_df)

        for round_num in range(total_rounds):
            main_question = responses_df.iloc[round_num]['prompt']
            conversation = [
                {"role": "user", "content": "This survey aims to estimate people's risk attitudes."},
                {"role": "user", "content": main_question}
            ]

            # Step through each question one at a time
            for question in questions_per_round:
                conversation.append({
                    "role": "user",
                    "content": f"Here is your question:\n{question}\n\n"
                               "Please evaluate the expected differences and choose 'Option 1' or 'Option 2'."
                })

                print(f"Starting question for round {round_num + 1}: {question}")
                answer, tokens_used = ask_openai(conversation)

                # Store the response in the results DataFrame
                question_index = questions_per_round.index(question)
                results.at[round_num, f'a{question_index + 1}'] = answer

                print(f"Response for question {question_index + 1}: {answer} (used {tokens_used} tokens)\n")
                time.sleep(delay_between_requests)

        save_results(results, run_number)
        elapsed_time = time.time() - start_time
        print(f"Program run time: {elapsed_time:.2f} seconds")