import flet as ft
import database
import config
from views.summary import get_summary_view
from views.history import get_history_view
from views.charts import get_charts_view

def main(page: ft.Page):
    page.title = "Cashew Expense Tracker"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed="green", use_material3=True)
    page.padding = 0

    database.init_db()

    # --- Consent Check ---
    def show_consent_dialog():
        def on_consent_change(e):
            btn_continue.disabled = not e.control.value
            page.update()

        def on_continue(e):
            config.update_config("consent_accepted", True)
            consent_dialog.open = False
            page.update()

        btn_continue = ft.FilledButton("Manohy", disabled=True, on_click=on_continue)
        
        consent_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Fepetra fampiasana", weight=ft.FontWeight.BOLD),
            content=ft.Column([
                ft.Text("Vakio ny fepetra fampiasana ary mariho ny boaty raha manaiky ianao."),
                ft.Row([
                    ft.Text("Jereo ny "),
                    ft.TextButton("Conditions d'utilisation", url="https://example.com/terms"),
                ], spacing=0, wrap=True),
                ft.Checkbox(
                    label="Avy namako aho dia ekeko ny fepetra fampiasana",
                    on_change=on_consent_change
                ),
            ], tight=True, spacing=10),
            actions=[btn_continue],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.overlay.append(consent_dialog)
        consent_dialog.open = True
        page.update()

    if not config.is_consent_given():
        show_consent_dialog()

    # --- Main Navigation Logic ---
    main_content = ft.Container(expand=True)

    def navigate(e):
        index = e.control.selected_index
        if index == 0:
            main_content.content = get_summary_view()
        elif index == 1:
            main_content.content = get_history_view()
        elif index == 2:
            main_content.content = get_charts_view()
        page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Temoin"),
            ft.NavigationBarDestination(icon=ft.Icons.HISTORY, label="Tantara"),
            ft.NavigationBarDestination(icon=ft.Icons.BAR_CHART, label="Kisary"),
        ],
        on_change=navigate,
        selected_index=0,
    )

    # --- Add Entry Logic ---
    def open_add_dialog(e):
        cat_field = ft.TextField(label="Sokajy", autofocus=True)
        amt_field = ft.TextField(label="Vola (Ar)", keyboard_type=ft.KeyboardType.NUMBER)
        
        type_field = ft.SegmentedButton(
            segments=[
                ft.Segment(value="Miditra", label=ft.Text("Miditra"), icon=ft.Icon(ft.Icons.ADD)),
                ft.Segment(value="Fandaniana", label=ft.Text("Fandaniana"), icon=ft.Icon(ft.Icons.REMOVE)),
            ],
            selected=["Fandaniana"],
            allow_multiple_selection=False,
        )

        def close_dialog(e):
            dialog.open = False
            page.update()

        def save_entry_callback(e):
            if not amt_field.value or not cat_field.value:
                if not amt_field.value: amt_field.error_text = "Ilaina ity"
                if not cat_field.value: cat_field.error_text = "Ilaina ity"
                page.update()
                return
            
            try:
                val = float(amt_field.value)
                selected = type_field.selected
                t_val = list(selected)[0] if selected else "Fandaniana"
                
                # Save via database module
                database.save_entry(t_val, cat_field.value, val)
                
                # Feedback
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Voatahiry: {cat_field.value} (Ar {val:,.0f})"),
                    bgcolor=ft.Colors.GREEN_700
                )
                page.snack_bar.open = True
                
                # Reset UI
                cat_field.value = ""
                amt_field.value = ""
                cat_field.error_text = None
                amt_field.error_text = None
                cat_field.focus()
                
                # Refresh current view
                refresh_view()
                page.update()
            except ValueError:
                amt_field.error_text = "Tsy maintsy isa (ohatra: 500)"
                page.update()

        dialog = ft.AlertDialog(
            title=ft.Row([
                ft.Text("Ampidiro fandaniana"),
                ft.IconButton(ft.Icons.CLOSE, on_click=close_dialog),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            content=ft.Column([
                type_field,
                cat_field,
                amt_field,
            ], tight=True, spacing=20),
            actions=[
                ft.FilledButton("Ampidiro", on_click=save_entry_callback),
            ],
        )
        
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def refresh_view():
        idx = page.navigation_bar.selected_index
        if idx == 0:
            main_content.content = get_summary_view()
        elif idx == 1:
            main_content.content = get_history_view()
        elif idx == 2:
            main_content.content = get_charts_view()

    # --- Initial View ---
    main_content.content = get_summary_view()
    page.add(main_content)

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        bgcolor=ft.Colors.GREEN_700,
        on_click=open_add_dialog,
    )
    page.update()

# Pour éviter le Warning, on utilise le nouveau standard si disponible, 
# mais ft.app(target=main) reste correct pour la version 0.80.2.
# On peut spécifier le mode d'affichage ici.
if __name__ == "__main__":
    # On force le mode web pour contourner l'absence de libmpv sur le système
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
