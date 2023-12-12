import pandas as pd
df = pd.read_csv('piaozone.csv')
with open('piaozone.faq', 'w', encoding='utf-8') as f:
    for i, row in df.iterrows():
        q = row['Q']
        a = row['A']
        f.write(f'Question: {q}\n\n')
        f.write(f'Answer: {a}\n')
        f.write('\n=====\n')