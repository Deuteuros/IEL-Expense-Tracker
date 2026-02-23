import flet as ft
import pandas as pd
import plotly.graph_objects as go
from flet_charts import PlotlyChart
from datetime import datetime
import os

DATA_FILE = "expenses.csv"

def main(page: ft.Page):
    page.title = "Mpanara-maso ny fandaniana"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=['Date', 'Type', 'Category', 'Amount'])
        df.to_csv(DATA_FILE, index=False)

    # --- UI Containers ---
    summary_container = ft.Container() 
    history_column = ft.Column()
    chart_container = ft.Container(height=350, padding=10)

    # --- UI Inputs ---
    amt_input = ft.TextField(label="Vola (Ar)", keyboard_type=ft.KeyboardType.NUMBER)
    cat_input = ft.TextField(label="Sokajy")
    type_dropdown = ft.Dropdown(
        label="Karazany",
        value="Fandaniana",
        options=[ft.dropdown.Option("Miditra"), ft.dropdown.Option("Fandaniana")]
    )

    def get_summary_row():
        """Kajy ny fitambarany ary mamerina andalana karatra."""
        df = pd.read_csv(DATA_FILE)
        # Handle English values if they exist in the CSV from previous runs
        income = df[df['Type'].isin(['Income', 'Miditra'])]['Amount'].sum()
        expense = df[df['Type'].isin(['Expense', 'Fandaniana'])]['Amount'].sum()
        balance = income - expense

        def create_stat_card(label, value, color):
            return ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(label, size=12, weight="bold", color=ft.Colors.GREY_700),
                        ft.Text(f"{value:,.0f}", size=16, weight="bold", color=color),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=10,
                    expand=True,
                ),
                expand=True,
            )

        return ft.Row(
            [
                create_stat_card("Miditra", income, ft.Colors.GREEN),
                create_stat_card("Fandaniana", expense, ft.Colors.RED),
                create_stat_card("Sodiny", balance, ft.Colors.BLUE if balance >= 0 else ft.Colors.RED_ACCENT),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def get_trend_chart():
        df = pd.read_csv(DATA_FILE)
        if df.empty:
            return ft.Text("Tsy mbola misy angona.")

        df['Date'] = pd.to_datetime(df['Date'])
        # Grouping with both English and Malagasy labels for compatibility
        df['Type'] = df['Type'].replace({'Income': 'Miditra', 'Expense': 'Fandaniana'})
        daily_df = df.groupby(['Date', 'Type'])['Amount'].sum().unstack(fill_value=0)
        
        for col in ['Miditra', 'Fandaniana']:
            if col not in daily_df.columns: daily_df[col] = 0
                
        daily_df['Cumulative Income'] = daily_df['Miditra'].cumsum()
        daily_df['Cumulative Expenses'] = daily_df['Fandaniana'].cumsum()
        daily_df['Balance'] = daily_df['Cumulative Income'] - daily_df['Cumulative Expenses']

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=daily_df.index, y=daily_df['Cumulative Income'], name='Miditra', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=daily_df.index, y=daily_df['Cumulative Expenses'], name='Fandaniana', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=daily_df.index, y=daily_df['Balance'], name='Sodiny', line=dict(color='blue', width=3)))
        
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h", y=-0.2))
        return PlotlyChart(figure=fig, expand=True)

    def update_dashboard(e=None):
        df = pd.read_csv(DATA_FILE)
        
        # 1. Update Summary Cards
        summary_container.content = get_summary_row()

        # 2. Update History (last 5 items)
        history_column.controls.clear()
        for _, row in df.tail(5).iterrows():
            is_income = row['Type'] in ["Income", "Miditra"]
            icon = ft.Icons.ARROW_UPWARD if is_income else ft.Icons.ARROW_DOWNWARD
            color = ft.Colors.GREEN if is_income else ft.Colors.RED
            history_column.controls.append(
                ft.ListTile(
                    leading=ft.Icon(icon, color=color),
                    title=ft.Text(f"{row['Category']}"),
                    trailing=ft.Text(f"Ar {row['Amount']:,.0f}")
                )
            )
        
        # 3. Update Chart
        chart_container.content = get_trend_chart()
        
        page.update()

    def add_entry(e):
        try:
            if not amt_input.value or not cat_input.value: return
            val = float(amt_input.value)
            new_data = [[datetime.now().strftime("%Y-%m-%d"), type_dropdown.value, cat_input.value, val]]
            new_df = pd.DataFrame(new_data, columns=['Date', 'Type', 'Category', 'Amount'])
            new_df.to_csv(DATA_FILE, mode='a', header=False, index=False)
            
            amt_input.value = ""
            cat_input.value = ""
            update_dashboard()
        except ValueError:
            pass

    # --- PAGE LAYOUT ---
    page.add(
        ft.Text("💰 Mpanara-maso fandaniana", size=25, weight="bold"),
        summary_container, 
        ft.Divider(),
        type_dropdown, 
        cat_input, 
        amt_input,
        ft.ElevatedButton("Ampidiro", icon=ft.Icons.ADD, on_click=add_entry),
        ft.Divider(),
        ft.Text("Tantara vao haingana", size=18, weight="bold"),
        history_column,
        ft.Divider(),
        ft.Text("Fivoaran'ny fandaniana", size=18, weight="bold"),
        chart_container 
    )
    
    update_dashboard()

ft.app(target=main)