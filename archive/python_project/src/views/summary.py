import flet as ft
import flet_charts as fc
import database
import datetime as dt


def fmt(val):
    return f"{val:,.0f}".replace(",", " ")


def make_line_chart(evolution):
    if not evolution:
        return fc.LineChart(expand=True)

    dates = [d for d, v in evolution]
    values = [v for d, v in evolution]

    min_val = min(values)
    max_val = max(values)
    range_span = max_val - min_val
    padding = range_span * 0.1 if range_span > 0 else 1000
    min_y = min(min_val * 0.9, 0) - padding
    max_y = max(max_val * 1.1, 0) + padding

    balance_final = values[-1]
    line_color = ft.Colors.RED_700 if balance_final < 0 else ft.Colors.GREEN_700

    first_date = dt.datetime.fromisoformat(dates[0]).strftime("%d %b")
    last_date = dt.datetime.fromisoformat(dates[-1]).strftime("%d %b")

    return fc.LineChart(
        data_series=[
            fc.LineChartData(
                points=[
                    fc.LineChartDataPoint(
                        x=i,
                        y=val,
                        tooltip=f"{dates[i]}: Ar {fmt(val)}",
                    )
                    for i, (date, val) in enumerate(evolution)
                ],
                stroke_width=3,
                color=line_color,
                curved=True,
                rounded_stroke_cap=True,
                below_line_bgcolor=ft.Colors.with_opacity(0.1, line_color),
                below_line_gradient=ft.LinearGradient(
                    begin=ft.Alignment.TOP_CENTER,
                    end=ft.Alignment.BOTTOM_CENTER,
                    colors=[
                        ft.Colors.with_opacity(0.3, line_color),
                        ft.Colors.with_opacity(0, line_color),
                    ],
                ),
            )
        ],
        interactive=True,
        tooltip=fc.LineChartTooltip(
            max_width=200,
            padding=10,
        ),
        left_axis=fc.ChartAxis(
            labels=[
                fc.ChartAxisLabel(
                    value=0,
                    label=ft.Container(
                        content=ft.Text(
                            "0 Ar",
                            size=11,
                            color=ft.Colors.OUTLINE_VARIANT,
                        ),
                        padding=ft.Padding(0, 0, 0, 0),
                    ),
                )
            ],
            show_labels=True,
            label_size=40,
        ),
        horizontal_grid_lines=fc.ChartGridLines(
            interval=abs(min_y - max_y) / 10,
            color=ft.Colors.with_opacity(0.1, ft.Colors.OUTLINE_VARIANT),
        ),
        bottom_axis=fc.ChartAxis(
            labels=[
                fc.ChartAxisLabel(
                    value=0,
                    label=ft.Container(
                        content=ft.Text(
                            first_date,
                            size=11,
                            color=ft.Colors.OUTLINE_VARIANT,
                        ),
                        padding=ft.Padding(8, 0, 0, 0),
                    ),
                ),
                fc.ChartAxisLabel(
                    value=len(evolution) - 1,
                    label=ft.Container(
                        content=ft.Text(
                            last_date,
                            size=11,
                            color=ft.Colors.OUTLINE_VARIANT,
                        ),
                        padding=ft.Padding(8, 0, 0, 0),
                    ),
                ),
            ],
            show_labels=True,
            label_size=40,
        ),
        expand=True,
        min_y=min_y,
        max_y=max_y,
    )

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
                ft.Text(f"Ar {fmt(value)}", size=16 if w < 380 else 18, weight="bold"),
            ], spacing=5),
            padding=15,
            border_radius=15,
            bgcolor="surfacevariant",
            expand=expand,
        )

    # --- Component: Line Chart (Evolution) ---
    line_chart = make_line_chart(evolution)

    # --- Component: Pie Chart (Distribution) ---
    total_vol = sum(abs(val) for cat, val in cat_distribution)
    pie_chart = fc.PieChart(
        sections=[
            fc.PieChartSection(
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
                    ft.Text(f"Ar {fmt(total_balance)}", size=22 if w < 380 else 28, weight="bold", 
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
                    ft.Text(f"Ar {fmt(balance)}", size=26 if w < 380 else 32, weight="bold", 
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
