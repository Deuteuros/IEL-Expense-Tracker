import flet as ft
import database
from datetime import datetime

def get_summary_view(page: ft.Page):
    # Responsive helper: base width
    w = page.width or 360
    # 1. Fetch Data
    income, expense, balance = database.get_summary_data(days=30)
    total_balance = database.get_total_balance()
    evolution = database.get_evolution_data(days=30)
    cat_distribution = database.get_category_distribution(days=30)
    
    # --- Helper: Summary Card ---
    def create_card(title, value, color, icon, expand=True):
        return ft.Container(
            content=ft.Column([
                ft.Row([ft.Icon(icon, color=color, size=20), ft.Text(title, size=14, color=ft.Colors.GREY_700)]),
                ft.Text(f"Ar {value:,.0f}", size=16 if w < 380 else 18, weight="bold"),
            ], spacing=5),
            padding=15,
            border_radius=15,
            bgcolor="surfacevariant",
            expand=expand,
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
        left_axis=ft.ChartAxis(labels_size=0),
        bottom_axis=ft.ChartAxis(labels_size=0),
        expand=True,
        min_y=0 if not evolution else min(v for d, v in evolution) * 0.9,
    ) if evolution else ft.Text("Tsy misy angona mbola azo asiana kisary.", color=ft.Colors.GREY_500)

    # --- Component: Pie Chart (Distribution) ---
    total_vol = sum(abs(val) for cat, val in cat_distribution)
    pie_chart = ft.PieChart(
        sections=[
            ft.PieChartSection(
                abs(val),
                title=f"{cat}\n{abs(val)/total_vol*100:.0f}%" if total_vol > 0 else cat,
                color=ft.Colors.GREEN_700 if cat in ['Miditra', 'Vente'] else ft.Colors.RED_700,
                radius=50,
                title_style=ft.TextStyle(size=10, weight="bold", color=ft.Colors.WHITE)
            )
            for cat, val in cat_distribution
        ],
        sections_space=2,
        center_space_radius=40,
    ) if cat_distribution else ft.Text("Tsy misy angona.", color=ft.Colors.GREY_500)

    # --- Final Layout ---
    return ft.Container(
        content=ft.Column([
            # Header
            ft.Container(
                content=ft.Text("Témoin (Dataly)", size=24, weight="bold"),
                padding=ft.Padding.only(left=10, top=10, bottom=5)
            ),
            
            # 1. Total Balance Card (All time)
            ft.Container(
                content=ft.Column([
                    ft.Text("Vola Tavela (Solde Total)", size=14, color=ft.Colors.GREY_700),
                    ft.Text(f"Ar {total_balance:,.0f}", size=22 if w < 380 else 28, weight="bold", 
                           color=ft.Colors.GREEN_800 if total_balance >= 0 else ft.Colors.RED_800),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=15,
                bgcolor=ft.Colors.GREEN_50 if total_balance >= 0 else ft.Colors.RED_50,
                border_radius=20,
                alignment=ft.Alignment(0, 0),
            ),

            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),

            # 2. 30-Day Balance
            ft.Container(
                content=ft.Column([
                    ft.Text("Tao anatin'ny 30 andro", size=14, color=ft.Colors.GREY_700),
                    ft.Text(f"Ar {balance:,.0f}", size=26 if w < 380 else 32, weight="bold", 
                           color=ft.Colors.GREEN_700 if balance >= 0 else ft.Colors.RED_700),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=10,
                alignment=ft.Alignment(0, 0),
            ),
            
            # 3. Line Chart Evolution (30 days)
            ft.Container(
                content=ft.Column([
                    ft.Text("Fivoaran'ny Caisse (30 andro)", size=16, weight="bold"),
                    ft.Container(line_chart, height=180, padding=10),
                ]),
                padding=15,
                bgcolor="surfacevariant",
                border_radius=20,
            ),
            
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            
            # 4. Summary Cards (30 days) — responsive grid
            ft.ResponsiveRow([
                ft.Container(create_card("Miditra", income, ft.Colors.GREEN_700, ft.Icons.TRENDING_UP),
                             col={"xs": 12, "sm": 6}),
                ft.Container(create_card("Fandaniana", expense, ft.Colors.RED_700, ft.Icons.TRENDING_DOWN),
                             col={"xs": 12, "sm": 6}),
            ], spacing=10),
            
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),

            # 5. Pie Chart Distribution
            ft.Container(
                content=ft.Column([
                    ft.Text("Miditra vs Fandaniana (30 andro)", size=16, weight="bold"),
                    ft.Row([pie_chart], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Column([
                        ft.Row([ft.Container(width=10, height=10, bgcolor=ft.Colors.GREEN_700), ft.Text("Miditra / Vente", size=12)]),
                        ft.Row([ft.Container(width=10, height=10, bgcolor=ft.Colors.RED_700), ft.Text("Fandaniana / Achat", size=12)]),
                    ], spacing=5)
                ]),
                padding=15,
                bgcolor="surfacevariant",
                border_radius=20,
            ),

            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

            ft.Container(height=40) # Extra bottom padding
            
        ], scroll=ft.ScrollMode.AUTO, expand=True, spacing=15),
        padding=10,
        expand=True
    )
