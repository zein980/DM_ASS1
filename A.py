import pandas as pd
from collections import defaultdict
from itertools import combinations
import tkinter as tk
from tkinter import ttk

# Read data from Bakery.csv file
df = pd.read_csv('Bakery.csv')
df = df.drop_duplicates()
transactions = df.groupby('TransactionNo')['Items'].apply(list).tolist()

# Apriori Algorithm
def get_frequency_itemset(transactions, itemset, min_support):
    item_counter = defaultdict(int)
    for transaction in transactions:
        for item in itemset:
            if set(item).issubset(transaction):
                item_counter[item] += 1

    freq_itemset = {item: support for item, support in item_counter.items() if support >= min_support}

    return freq_itemset


def get_candidate_itemset(prev_freq_itemset, length):
    candidates = set()

    for item1 in prev_freq_itemset:
        for item2 in prev_freq_itemset:
            union_item = set(item1).union(set(item2))
            if len(union_item) == length:
                candidates.add(tuple(sorted(union_item)))

    return candidates


def apriori(transactions, min_support):
    itemset = set([item for transaction in transactions for item in transaction])
    itemset = {(item,) for item in itemset}
    frequent_item_sets = {}
    k = 1

    while itemset:
        freq_itemset = get_frequency_itemset(transactions, itemset, min_support)
        frequent_item_sets.update(freq_itemset)

        if not freq_itemset:
            break

        k += 1
        candidates = get_candidate_itemset(freq_itemset, k)
        itemset = candidates

    return frequent_item_sets


def generate_association_rules(frequent_item_sets, min_confidence):
    rules = []
    for item_set in frequent_item_sets:
        if len(item_set) > 1:
            for i in range(1, len(item_set)):
                for subset in combinations(item_set, i):
                    antecedent = set(subset)
                    consequent = set(item_set) - antecedent

                    support_item_set = frequent_item_sets[item_set]
                    if tuple(antecedent) in frequent_item_sets:
                        support_antecedent = frequent_item_sets[tuple(antecedent)]
                        confidence = support_item_set / support_antecedent

                        if confidence >= min_confidence:
                            rules.append((antecedent, consequent, support_item_set, confidence))

    return rules

# GUI for user input
def run_algorithm():
    min_support = float(min_support_entry.get())
    min_confidence_percent = float(min_confidence_entry.get())
    min_confidence = min_confidence_percent / 100
    data_percentage = float(data_percentage_entry.get()) / 100

    num_transactions_to_read = int(len(transactions) * data_percentage)
    transactions_subset = transactions[:num_transactions_to_read]

    # Applying Apriori Algorithm
    frequent_item_sets = apriori(transactions_subset, min_support)

    # Output the Frequent Item Sets
    frequent_item_sets_text.config(state=tk.NORMAL)
    frequent_item_sets_text.delete('1.0', tk.END)
    for item_set, support in frequent_item_sets.items():
        frequent_item_sets_text.insert(tk.END, f"{item_set}: Support={support}\n")
    frequent_item_sets_text.config(state=tk.DISABLED)

    # Generate Association Rules
    association_rules = generate_association_rules(frequent_item_sets, min_confidence)

    # Output the generated association rules
    association_rules_text.config(state=tk.NORMAL)
    association_rules_text.delete('1.0', tk.END)
    for rule in association_rules:
        antecedent, consequent, support, confidence = rule
        association_rules_text.insert(tk.END, f"Rule: {antecedent} -> {consequent}, Support={support}, Confidence={confidence}\n")
    association_rules_text.config(state=tk.DISABLED)

# Create GUI window
root = tk.Tk()
root.title("Association Rules Mining")
root.geometry("800x600")
root.configure(bg='#f0f0f0')

# GUI inputs and styling
style = ttk.Style()
style.configure('My.TButton', foreground='#fff', background='#007bff', font=('Arial', 12, 'bold'))

min_support_label = ttk.Label(root, text="Minimum Support:", font=('Arial', 12))
min_support_label.pack(pady=10)
min_support_entry = tk.Entry(root, font=('Arial', 12))
min_support_entry.pack()

min_confidence_label = ttk.Label(root, text="Minimum Confidence (%):", font=('Arial', 12))
min_confidence_label.pack(pady=10)
min_confidence_entry = tk.Entry(root, font=('Arial', 12))
min_confidence_entry.pack()

data_percentage_label = ttk.Label(root, text="Data Percentage (%):", font=('Arial', 12))
data_percentage_label.pack(pady=10)
data_percentage_entry = tk.Entry(root, font=('Arial', 12))
data_percentage_entry.pack()

run_button = ttk.Button(root, text="Run Algorithm", style='My.TButton', command=run_algorithm)
run_button.pack(pady=20)

# Output boxes
output_frame = ttk.Frame(root, padding=(10, 10, 10, 10), relief='ridge')
output_frame.pack(pady=20, fill='both', expand=True)

frequent_item_sets_label = ttk.Label(output_frame, text="Frequent Item Sets:", font=('Arial', 14, 'bold'))
frequent_item_sets_label.pack()
frequent_item_sets_text = tk.Text(output_frame, height=10, width=70, font=('Arial', 12))
frequent_item_sets_text.pack()
frequent_item_sets_text.insert(tk.END, "Frequent Item Sets:\n")
frequent_item_sets_text.config(state=tk.DISABLED)

association_rules_label = ttk.Label(output_frame, text="Association Rules:", font=('Arial', 14, 'bold'))
association_rules_label.pack()
association_rules_text = tk.Text(output_frame, height=10, width=70, font=('Arial', 12))
association_rules_text.pack()
association_rules_text.insert(tk.END, "Association Rules:\n")
association_rules_text.config(state=tk.DISABLED)

# Start the GUI main loop
root.mainloop()