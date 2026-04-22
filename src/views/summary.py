import flet as ft
import database
from datetime import datetime

def get_summary_view(page: ft.Page):
    # 1. Fetch Data
    income, expense, balance = database.get_summary_data(days=30)
    evolution = database.get_evolution_data(days=30)
    distribution = database.get_distribution_data(days=30)
    
    # --- Helper: Summary Card ---
    def create_card(title, value, color, icon):
        return ft.Container(
            content=ft.Column([
                ft.Row([ft.Icon(icon, color=color, size=20), ft.Text(title, size=14, color=ft.Colors.GREY_700)]),
                ft.Text(f"Ar {value:,.0f}", size=18, weight="bold"),
            ], spacing=5),
            padding=15,
            border_radius=15,
            bgcolor="surfacevariant",
            expand=True,
        )

    # --- Component: Line Chart (Evolution) ---
    line_chart = ft.LineChart(
        data_series=[
            ft.LineChartData(
                data_points=[ft.LineChartDataPoint(i, val) for i, (date, val) in enumerate(evolution)],
                stroke_width=3,
                color=ft.Colors.GREEN_700,
                curved=True,
                stroke_cap_round=True,
                below_line_bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN),
                below_line_gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[ft.Colors.with_opacity(0.3, ft.Colors.GREEN), ft.Colors.with_opacity(0, ft.Colors.GREEN)],
                ),
            )
        ],
        border=ft.ChartBorder(bottom=ft.BorderSide(1, "outlinevariant")),
        # Hide Y axis labels for a cleaner "sparkline" look
        left_axis=ft.ChartAxis(labels_size=0),
        bottom_axis=ft.ChartAxis(labels_size=0),
        expand=True,
        min_y=0 if not evolution else min(v for d, v in evolution) * 0.9,
    ) if evolution else ft.Text("Tsy misy angona mbola azo asiana kisary.", color=ft.Colors.GREY_500)

    # --- Component: Pie Chart (Distribution) ---
    pie_chart = ft.PieChart(
        sections=[
            ft.PieChartSection(
                val,
                title=f"{item}\n({val/expense*100:.0f}%)" if expense > 0 else item,
                color=color,
                radius=40,
                title_style=ft.TextStyle(size=10, weight="bold", color=ft.Colors.WHITE)
            )
            for (item, val), color in zip(distribution, [ft.Colors.GREEN_700, ft.Colors.AMBER_700, ft.Colors.BLUE_700, ft.Colors.RED_700, ft.Colors.PURPLE_700])
        ],
        sections_space=2,
        center_space_radius=30,
    ) if distribution else ft.Text("Tsy misy fandaniana voasokajy.", color=ft.Colors.GREY_500)

    # --- Final Layout ---
    return ft.Container(
        content=ft.Column([
            # Header
            ft.Container(
                content=ft.Text("Témoin (Analyse 30 andro)", size=24, weight="bold"),
                padding=ft.Padding.only(left=10, top=10, bottom=10)
            ),
            
            # 1. Main Indicator (Solde actuel vs tendance)
            ft.Container(
                content=ft.Column([
                    ft.Text("Solde Caisse", size=16, color=ft.Colors.GREY_700),
                    ft.Text(f"Ar {balance:,.0f}", size=36, weight="bold", 
                           color=ft.Colors.GREEN_700 if balance >= 0 else ft.Colors.RED_700),
                ]),
                padding=20,
                alignment=ft.Alignment(0,0),
            ),
            
            # 2. Line Chart Evolution
            ft.Container(
                content=ft.Column([
                    ft.Text("Fivoaran'ny Caisse", size=16, weight="bold"),
                    ft.Container(line_chart, height=150, padding=10),
                ]),
                padding=15,
                bgcolor="surfacevariant",
                border_radius=20,
            ),
            
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            
            # 3. Summary Cards
            ft.Row([
                create_card("Miditra", income, ft.Colors.GREEN_700, ft.Icons.TRENDING_UP),
                create_card("Fandaniana", expense, ft.Colors.RED_700, ft.Icons.TRENDING_DOWN),
            ], spacing=10),
            
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

            # 4. Pie Chart Distribution
            ft.Container(
                content=ft.Column([
                    ft.Text("Fitsinjarana ny Fandaniana", size=16, weight="bold"),
                    ft.Row([pie_chart], alignment=ft.MainAxisAlignment.CENTER),
                ]),
                padding=15,
                bgcolor="surfacevariant",
                border_radius=20,
            ),

            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

            ft.Container(height=40) # Extra bottom padding
            
        ], scroll=ft.ScrollMode.AUTO, expand=True, spacing=10),
        padding=10,
        expand=True
    )
