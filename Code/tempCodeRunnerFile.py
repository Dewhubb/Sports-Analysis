import pandas as pd
import matplotlib.pyplot as plt

# Sample data
data = {
    'batting': [0.25, 0.3, 0.2, 0.28, 0.27, 0.32, 0.22, 0.18, 0.3, 0.26],
    'weather': ['晴れ', '晴れ', '曇り', '曇り', '雨', '雨', '晴れ', '曇り', '雨', '晴れ']
}

df = pd.DataFrame(data)

# Group batting averages by weather
grouped = df.groupby('weather')['batting'].apply(list)

# Optional: define order for x-axis
order = ['晴れ', '曇り', '雨']

# Prepare data for boxplot
box_data = [grouped[w] for w in order]

# Create boxplot
plt.figure(figsize=(8, 6))
plt.boxplot(box_data, labels=order)
plt.ylabel("打率")
plt.xlabel("天気")
plt.title("打率と天気の関係（サンプル）")
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.show()
