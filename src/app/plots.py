from datetime import datetime as dt, timedelta

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


class Plots:
    def __init__(self):
        # set theme here
        plt.rcParams.update({
            'figure.facecolor': 'none',  # Transparent background
            'axes.facecolor': 'none',  # Transparent background for axes
            'savefig.facecolor': 'none',  # Transparent background for saved figures
            'text.color': 'white',  # White text
            'axes.labelcolor': 'white',  # White axes labels
            'xtick.color': 'white',  # White x-tick labels
            'ytick.color': 'white',  # White y-tick labels
            'axes.edgecolor': 'white',  # White axes edge
            'grid.color': 'white',  # White grid lines
            'lines.color': 'white',  # White lines
            'patch.edgecolor': 'white',  # White edge color for patches
            'patch.facecolor': 'none',  # Transparent patch faces
            'font.family': 'sans-serif',  # Default font family
            'font.sans-serif': ['Calibri'],  # Default font style (change 'Arial' to your preferred font)
        })

    def plot_monthly_expenses_bar_chart(self, df: pd.DataFrame, start_date: dt, end_date: dt):
        daily_sum = pd.DataFrame(index=pd.date_range(start_date, end_date - timedelta(days=1)))
        df = df.set_index('DATE', drop=True)
        sums = df.groupby(df.index.date)['AMOUNT'].sum()
        daily_sum['AMOUNT'] = sums
        daily_sum = daily_sum.fillna(0)

        # Create bar chart
        fig, ax = plt.subplots(figsize=(7, 2))
        ax.bar(daily_sum.index.strftime('%m-%d'), daily_sum['AMOUNT'], color='springgreen', alpha=0.8, edgecolor='black')
        ax.grid(axis='y', alpha=0.2)
        ax.set_xlabel('Date', fontsize=8)
        ax.set_ylabel('Expenses (Php)', fontsize=8)
        ax.set_title(f'Expenses from {start_date.date()} to {end_date.date()}', fontsize=8)
        plt.xticks(rotation=90, fontsize=6)
        plt.yticks(fontsize=6)
        st.pyplot(fig)