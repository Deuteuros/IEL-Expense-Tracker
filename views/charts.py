import flet as ft
import flet_charts as fc
import pandas as pd
import database

def get_charts_view():
    df = database.get_df()
    if df.empty:
        return ft.Center(content=ft.Text("Tsy mbola misy angona."))

    df['Date'] = pd.to_datetime(df['Date'])
    df['Type'] = df['Type'].replace({'Income': 'Miditra', 'Expense': 'Fandaniana'})
    
    daily_df = df.groupby(['Date', 'Type'])['Amount'].sum().unstack(fill_value=0)
    for col in ['Miditra', 'Fandaniana']:
        if col not in daily_df.columns: daily_df[col] = 0
            
    daily_df = daily_df.sort_index()
    
    income_points = []
    expense_points = []
    balance_points = []
    
    cum_income = 0
    cum_expense = 0
    
    for i, (date, row) in enumerate(daily_df.iterrows()):
        cum_income += row['Miditra']
        cum_expense += row['Fandaniana']
        income_points.append(fc.LineChartDataPoint(i, cum_income))
        expense_points.append(fc.LineChartDataPoint(i, cum_expense))
        balance_points.append(fc.LineChartDataPoint(i, cum_income - cum_expense))

    chart = fc.LineChart(
        data_series=[
            fc.LineChartData(
                points=income_points,
                stroke_width=4,
                color=ft.Colors.GREEN,
                curved=True,
                below_line_bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN),
                below_line_gradient=ft.LinearGradient(
                    begin=ft.Alignment(0, -1),
                    end=ft.Alignment(0, 1),
                    colors=[ft.Colors.with_opacity(0.2, ft.Colors.GREEN), ft.Colors.TRANSPARENT],
                ),
            ),
            fc.LineChartData(
                points=expense_points,
                stroke_width=4,
                color=ft.Colors.RED,
                curved=True,
                below_line_bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.RED),
            ),
            fc.LineChartData(
                points=balance_points,
                stroke_width=6,
                color=ft.Colors.BLUE,
                curved=True,
            ),
        ],
        border=ft.Border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE)),
        horizontal_grid_lines=fc.ChartGridLines(interval=10000, width=1, color=ft.Colors.with_opacity(0.1, ft.Colors.ON_SURFACE)),
        vertical_grid_lines=fc.ChartGridLines(interval=1, width=1, color=ft.Colors.with_opacity(0.1, ft.Colors.ON_SURFACE)),
        left_axis=fc.ChartAxis(label_size=40),
        bottom_axis=fc.ChartAxis(label_size=32),
        expand=True,
    )

    return ft.Column([
        ft.Container(content=ft.Text("Fivoarana", size=24, weight="bold"), padding=20),
        ft.Container(content=chart, expand=True, padding=20)
    ], expand=True)
