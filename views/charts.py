import flet as ft
import flet_charts as fc
import pandas as pd
import database

def get_charts_view():
    df = database.get_df()
    if df.empty:
        return ft.Center(content=ft.Text("Tsy mbola misy angona."))

    df['date'] = pd.to_datetime(df['date'])
    df['categorie_flux'] = df['categorie_flux'].replace({'Income': 'Miditra', 'Expense': 'Fandaniana'})
    
    daily_df = df.groupby(['date', 'categorie_flux'])['montant_total_mga'].sum().unstack(fill_value=0)
    for col in ['Miditra', 'Fandaniana']:
        if col not in daily_df.columns: daily_df[col] = 0
            
    daily_df = daily_df.sort_index()
    
    income_points = []
    expense_points = []
    balance_points = []
    x_labels = []
    
    cum_income = 0
    cum_expense = 0
    cum_balance = 0
    
    # French months mapping
    months_fr = {
        1: "janv.", 2: "févr.", 3: "mars", 4: "avr.", 
        5: "mai", 6: "juin", 7: "juil.", 8: "août", 
        9: "sept.", 10: "oct.", 11: "nov.", 12: "déc."
    }
    
    for i, (date, row) in enumerate(daily_df.iterrows()):
        cum_income += row['Miditra']
        cum_expense += row['Fandaniana']
        cum_balance = cum_income - cum_expense
        
        x_val = float(i)
        income_points.append(fc.LineChartDataPoint(x_val, cum_income))
        expense_points.append(fc.LineChartDataPoint(x_val, cum_expense))
        balance_points.append(fc.LineChartDataPoint(x_val, cum_balance))
        
        # X-Axis Labels (Dates in French)
        if len(daily_df) <= 10 or i % (max(1, len(daily_df) // 5)) == 0:
            date_str = f"{date.day} {months_fr[date.month]}"
            x_labels.append(
                fc.ChartAxisLabel(
                    value=x_val,
                    label=ft.Text(date_str, size=11, color=ft.Colors.GREY_600)
                )
            )

    # Calculate Y-axis labels based on data range across ALL curves
    all_y = [p.y for p in income_points + expense_points + balance_points]
    y_min = min(all_y) if all_y else 0
    y_max = max(all_y) if all_y else 1000000
    y_range = y_max - y_min
    if y_range == 0: y_range = 1000000
    
    y_labels = []
    step = y_range / 4
    for i in range(5):
        val = y_min + i * step
        abs_val = abs(val)
        if abs_val >= 1000000:
            label_text = f"{val/1000000:.1f} M".replace('.', ',')
        elif abs_val >= 1000:
            label_text = f"{val/1000:.1f} k".replace('.', ',') if abs_val < 10000 else f"{val/1000:.0f} k"
        else:
            label_text = f"{val:.0f}"
            
        y_labels.append(
            fc.ChartAxisLabel(
                value=val,
                label=ft.Text(label_text, size=11, color=ft.Colors.GREY_500)
            )
        )

    chart = fc.LineChart(
        data_series=[
            # Flux Rentrant (Green)
            fc.LineChartData(
                points=income_points,
                stroke_width=2,
                color=ft.Colors.GREEN_400,
                curved=True,
            ),
            # Flux Sortant (Red)
            fc.LineChartData(
                points=expense_points,
                stroke_width=2,
                color=ft.Colors.RED_400,
                curved=True,
            ),
            # Caisse (Teal - Boldest)
            fc.LineChartData(
                points=balance_points,
                stroke_width=5,
                color="#3A8D9D",
                curved=True,
                below_line_bgcolor=ft.Colors.with_opacity(0.1, "#3A8D9D"),
                below_line_gradient=ft.LinearGradient(
                    begin=ft.Alignment(0, -1),
                    end=ft.Alignment(0, 1),
                    colors=[ft.Colors.with_opacity(0.2, "#3A8D9D"), ft.Colors.TRANSPARENT],
                ),
            ),
        ],
        border=ft.Border.all(0, ft.Colors.TRANSPARENT),
        horizontal_grid_lines=fc.ChartGridLines(
            interval=step if step > 0 else 1000, 
            width=1, 
            color=ft.Colors.with_opacity(0.1, ft.Colors.ON_SURFACE),
            dash_pattern=[5, 5]
        ),
        vertical_grid_lines=fc.ChartGridLines(
            interval=1, 
            width=1, 
            color=ft.Colors.with_opacity(0.1, ft.Colors.ON_SURFACE),
            dash_pattern=[5, 5]
        ),
        left_axis=fc.ChartAxis(
            labels=y_labels,
            label_size=60,
            show_labels=True,
        ),
        bottom_axis=fc.ChartAxis(
            labels=x_labels,
            label_size=40,
            show_labels=True,
        ),
        expand=True,
        min_y=y_min - step*0.2,
        max_y=y_max + step*0.2,
    )

    return ft.Column([
        ft.Container(
            content=ft.Row([
                ft.Text("Fivoarana", size=24, weight="bold"),
                ft.Row([
                    ft.Container(bgcolor=ft.Colors.GREEN_400, width=12, height=12, border_radius=6),
                    ft.Text("Miditra", size=12),
                    ft.Container(bgcolor=ft.Colors.RED_400, width=12, height=12, border_radius=6),
                    ft.Text("Fandaniana", size=12),
                    ft.Container(bgcolor="#3A8D9D", width=12, height=12, border_radius=6),
                    ft.Text("Caisse", size=12, weight="bold"),
                ], spacing=10)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.only(left=20, top=20, right=20)
        ),
        ft.Container(
            content=chart, 
            expand=True, 
            padding=20,
            margin=10,
            bgcolor="#F8FBFC", # Light background like image
            border_radius=15,
        )
    ], expand=True)
