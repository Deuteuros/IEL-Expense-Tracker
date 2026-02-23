import flet as ft
import database

def get_history_view():
    df = database.get_df()
    items = []
    for _, row in df.iloc[::-1].iterrows():
        is_income = row['Type'] in ["Income", "Miditra"]
        items.append(
            ft.ListTile(
                leading=ft.CircleAvatar(
                    content=ft.Icon(ft.Icons.MONEY, color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.GREEN if is_income else ft.Colors.RED,
                ),
                title=ft.Text(row['Category'], weight="bold"),
                subtitle=ft.Text(row['Date']),
                trailing=ft.Text(
                    f"{' + ' if is_income else ' - '} Ar {row['Amount']:,.0f}",
                    color=ft.Colors.GREEN if is_income else ft.Colors.RED,
                    weight="bold"
                ),
            )
        )
    return ft.Column([
        ft.Container(
            content=ft.Text("Tantara", size=24, weight="bold"),
            padding=20
        ),
        ft.Column(items, scroll=ft.ScrollMode.AUTO, expand=True)
    ], expand=True)
