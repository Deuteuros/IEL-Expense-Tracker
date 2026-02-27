import flet as ft
import database
import config
from views.summary import get_summary_view
from views.history import get_history_view
from views.charts import get_charts_view
from components.segmented_control import CustomSegmentedControl, Segment

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
            main_content.content = get_history_view(page)
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
        cat_flux_selector = CustomSegmentedControl(
            segments=[
                Segment(value="Miditra", label="Miditra", icon=ft.Icons.ADD),
                Segment(value="Fandaniana", label="Fandaniana", icon=ft.Icons.REMOVE),
            ],
            selected_index=1, # Default to Fandaniana
        )
        item_field = ft.TextField(label="Item (Zavatra)", autofocus=True)
        qty_field = ft.TextField(label="Quantite", keyboard_type=ft.KeyboardType.NUMBER)
        unit_field = ft.TextField(label="Unite (Ohatra: kg, lany...)")
        price_field = ft.TextField(label="Prix Unitaire (Ar)", keyboard_type=ft.KeyboardType.NUMBER)
        total_field = ft.TextField(label="Montant Total (Ar)", read_only=True, value="0")
        client_field = ft.TextField(label="Fournisseur / Client")

        def update_total(e):
            try:
                qty = float(qty_field.value) if qty_field.value else 0
                price = float(price_field.value) if price_field.value else 0
                total = qty * price
                total_field.value = f"{total:,.0f}"
                page.update()
            except ValueError:
                total_field.value = "Erreur"
                page.update()

        qty_field.on_change = update_total
        price_field.on_change = update_total
        
        def close_dialog(e):
            dialog.open = False
            page.update()

        def save_entry_callback(e):
            if not qty_field.value or not price_field.value or not item_field.value:
                if not qty_field.value: qty_field.error_text = "Ilaina ity"
                if not price_field.value: price_field.error_text = "Ilaina ity"
                if not item_field.value: item_field.error_text = "Ilaina ity"
                page.update()
                return
            
            try:
                q_val = float(qty_field.value)
                p_val = float(price_field.value)
                t_val = q_val * p_val
                
                f_type = cat_flux_selector.segments[cat_flux_selector.selected_index].value
                
                # Save via database module
                database.save_entry(
                    f_type, 
                    item_field.value, 
                    q_val, 
                    unit_field.value, 
                    p_val, 
                    t_val, 
                    client_field.value
                )
                
                # Feedback
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Voatahiry: {item_field.value} (Ar {t_val:,.0f})"),
                    bgcolor=ft.Colors.GREEN_700
                )
                page.snack_bar.open = True
                
                # Reset UI
                item_field.value = ""
                qty_field.value = ""
                unit_field.value = ""
                price_field.value = ""
                total_field.value = "0"
                client_field.value = ""
                
                # Refresh current view
                refresh_view()
                page.update()
            except ValueError:
                page.snack_bar = ft.SnackBar(content=ft.Text("Nisy fahadisoana teo amin'ny isa"), bgcolor=ft.Colors.RED_700)
                page.snack_bar.open = True
                page.update()

        dialog = ft.AlertDialog(
            title=ft.Row([
                ft.Text("Ampidiro fandaniana / miditra"),
                ft.IconButton(ft.Icons.CLOSE, on_click=close_dialog),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            content=ft.Column([
                cat_flux_selector,
                item_field,
                ft.Row([qty_field, unit_field], spacing=10),
                price_field,
                total_field,
                client_field,
            ], tight=True, spacing=10, scroll=ft.ScrollMode.AUTO),
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
            main_content.content = get_history_view(page)
        elif idx == 2:
            main_content.content = get_charts_view()
        page.update()

    # Expose refresh_view to allow views to trigger global refresh
    page.refresh_view = refresh_view

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
    import sys
    if "--web" in sys.argv:
        # Mode web pour contourner l'absence de libmpv si nécessaire
        ft.app(target=main, view=ft.AppView.WEB_BROWSER)
    else:
        # Mode Desktop par défaut
        ft.app(target=main)

