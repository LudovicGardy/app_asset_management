import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def plot_savings(x, y1, y2, y3, title, labels):
    plt.figure(figsize=(12, 8))
    sns.lineplot(x=x, y=y1, label=labels[0], color='blue', marker="o", linewidth=3, markersize=10)
    sns.lineplot(x=x, y=y2, label=labels[1], color='green', marker="o", dashes=(5, 2))
    sns.lineplot(x=x, y=y3, label=labels[2], color='red', marker="o", dashes=(5, 2))
    plt.title(title)
    plt.xlabel('Années')
    plt.ylabel('Montant (€)')
    plt.legend()
    return plt

def plot_mortgage(years, remaining_balance, interest_paid, principal_paid, annual_total_paid, title):
    plt.figure(figsize=(12, 8))
    sns.lineplot(x=years, y=remaining_balance, label='Solde Restant', color='skyblue', marker="o", linewidth=3, markersize=10)
    sns.lineplot(x=years, y=np.cumsum(annual_total_paid), label='Total Payé', color='blue', marker="o", linewidth=3, markersize=10)
    sns.lineplot(x=years, y=np.cumsum(interest_paid), label='Total Intérêts Payés', color='salmon', marker="o", dashes=(5, 2))
    sns.lineplot(x=years, y=np.cumsum(principal_paid), label='Principal Payé', color='lightgreen', marker="o", dashes=(5, 2))
    plt.title(title)
    plt.xlabel('Années')
    plt.ylabel('Montant (€)')
    plt.legend()
    return plt