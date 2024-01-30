import kivy
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from Database import Database

from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.tab import MDTabsBase

from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp

kivy.require('2.3.0')


class FloatView(MDFloatLayout):
    pass


# Available MySql DBs for given user
class Tab(MDFloatLayout, MDTabsBase):
    pass


class OperationsContent(MDBoxLayout):
    pass


class Divider(MDBoxLayout):
    pass


class Spacer(MDBoxLayout):
    pass


class KivySqlApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = None
        self.menu_list = []
        self.table_widget = None
        self.db = Database()
        self.curr_db = self.db.curr_db
        self.curr_op = 'Create'

    def build(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.accent_palette = 'LightBlue'

    def on_start(self):
        self.generate_tabs()

    def dropdown(self):
        """ generate dropdown if there isn't, otherwise open existing dropdown
             used by MDTextField with id of table_field """
        if len(self.menu_list) == 0:
            # populate dropdown items with column names from current db
            for table_name in self.db.get_all_tables():
                self.menu_list.append(
                    {
                        'viewclass': 'OneLineListItem',
                        'text': table_name,
                        'on_release': lambda t=table_name: self.select_table(t)
                    }
                )
            # instantiate menu
            self.menu = MDDropdownMenu(
                caller=self.root.ids.table_field,
                items=self.menu_list,
                position='bottom',
                width_mult=4
            )
        self.menu.open()

    def select_table(self, table):
        """ select table target from dropdown """
        self.db.curr_table = table
        self.root.ids.table_field.text = self.db.curr_table
        self.generate_table()
        self.menu.dismiss()

    def generate_table(self):
        """ used in kv file - on_release for get_table button """
        if self.table_widget:
            self.root.remove_widget(self.table_widget)

        rows_data = [tuple(str(value) for value in row) for row in self.db.get_all_cols()]
        cols_data = [(x, dp(40)) for x in self.db.get_table_cols_list()]

        table = MDDataTable(pos_hint={'center_x': .5, 'top': .70},
                            size_hint=(.8, .625),
                            column_data=cols_data,
                            row_data=rows_data,
                            use_pagination=True)
        self.root.add_widget(table)
        self.table_widget = table

    def operations_dialog(self):
        dialog = MDDialog(
            type='custom',
            content_cls=OperationsContent(),
            buttons=[
                MDFlatButton(
                    text="Add",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                ),
                MDFlatButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.error_color,
                    on_release=lambda *args: self.dismiss_dialog(dialog)
                ),

            ])
        dialog.open()

    def dismiss_dialog(self, dialog):
        dialog.dismiss()

    def handle_segment_selection(self, *args):
        segment_text = args[1].text
        self.curr_op = segment_text

    def generate_tabs(self):
        """ add tabs to MDTabs with id tab_container """
        for i in self.db.get_all_dbs():
            tab = Tab(title=i)
            self.root.ids.tab_container.add_widget(tab)

    def on_tab_switch(self, *args):
        """ set db to current selected and clear menu_list """
        tab_text = args[3]
        self.db.set_db(tab_text)
        self.menu_list.clear()


if __name__ == '__main__':
    Window.maximize()  # set to full screen
    KivySqlApp().run()
