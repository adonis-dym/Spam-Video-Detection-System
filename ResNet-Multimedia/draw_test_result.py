import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('test_result.txt')
label = ['Test Accuracy', 'Test Precision', 'Test Recall', 'F1_score']

F_score = []
for elem in zip(list(df['precision']), list(df['recall'])):
    F_score.append(2 * elem[0] * elem[1] / (elem[0] + elem[1]))

plt.plot(df['steps'], df['accuracy'])
plt.plot(df['steps'], df['precision'])
plt.plot(df['steps'], df['recall'])
plt.plot(df['steps'], F_score)
plt.xlabel('Number of steps')
plt.ylabel('Evaluation index')
plt.legend(label, fontsize=11)
plt.show()
