import tkinter.font as font
from tkinter import messagebox
# This module contains the custom classes for MyLabels, BtnClass and MyEntries
from UI_classes import *
from tkinter import ttk
import sqlite3
from tkinter import filedialog
import csv
from datetime import date

# conn = sqlite3.connect('products.db')
#
# c = conn.cursor()
#
# c.execute("DROP TABLE categories")
# c.execute("DROP TABLE product")
#
#
#
# c.execute("""CREATE TABLE categories (
#            category_name TEXT NOT NULL,
#            category_code INTEGER NOT NULL PRIMARY KEY UNIQUE
#           )""")
#
# c.execute("""CREATE TABLE product (
#            product_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
#            product_name TEXT NOT NULL,
#            category_code INTEGER NOT NULL,
#            manufacturer TEXT,
#            import_date CURRENT_TIMESTAMP,
#            quantity INTEGER,
#            price REAL,
#            weight REAL,
#            image BLOB,
#            description TEXT,
#            FOREIGN KEY (category_code)
#                 REFERENCES categories (category_code)
#                    ON UPDATE CASCADE
#                    ON DELETE RESTRICT
#          )""")
#
#
# conn.commit()
# conn.close()


# This is the Login window class
class LoginWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self["bg"] = '#282828'

        self.title('All About Toys Login')

        # This code sets the window characteristics
        self.width, self.height = 600, 600
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        x_cord = int((self.screen_width / 2) - (self.width / 2))
        y_cord = int((self.screen_height / 2) - (self.height / 2))
        self.geometry("{}x{}+{}+{}".format(self.width, self.height, x_cord, y_cord))
        self.iconphoto(True, tk.PhotoImage(file='aatLogo.png'))

        # Here I am setting a container for the elements of the window
        # I wanted everything centered and using a container worked
        self.container = tk.Frame(self, background='#282828')
        self.container.pack(pady=100)

        # self["bg"] = '#282828'
        # self.pack()

        self.lbl_font = font.Font(family='Verdana', size='12')

        self.btn_font = font.Font(family='Verdana', size='8')

        # Set the title of the frame
        self.lbl_login = MyLabels(self.container, "LOGIN", self.lbl_font, 50, 0, 1)

        # Set the buttons and the entries
        self.login_btn_img = tk.PhotoImage(file="images/login.png")
        self.btn_login = BtnClass(self.container, self.login_btn_img, self.check_user_id, 30, 5, 1)

        # # Button to skip the login
        # self.skip_login_btn_img = tk.PhotoImage(file="images/login.png")
        # self.btn_skip_login = BtnClass(self.container, self.login_btn_img, self.skip_login, 30, 6, 1)

        # This is the entry field and the label for the user ID
        self.lbl_user_id = MyLabels(self.container, "USER ID", self.btn_font, 5, 2, 1)
        self.login_user_id_entry = MyEntries(self.container, 1, 1, 1, 1)

        # This is the entry field and label for the user password
        self.lbl_user_pass = MyLabels(self.container, "PASSWORD", self.btn_font, 5, 4, 1)
        self.login_pass = MyEntries(self.container, 1, 5, 3, 1)

    def skip_login(self):
        LoginWindow.destroy(self)
        self.new_window()

    # This function opens the main window after a successful login
    def new_window(self):
        app = MainWindow()
        app.mainloop()

    def check_user_id(self):
        """This method checks if the user is in the
        database and if the password is the right one"""
        # Here the connection to the database is opened
        self.conn = sqlite3.connect('users.db')

        self.c = self.conn.cursor()

        with self.conn:
            self.c.execute("SELECT * fROM users ")
        self.user_list = self.c.fetchall()
        self.user_data = dict(self.user_list)

        # This is just for developing purpose. Check if the dictionary is created successfully
        print(self.user_data)

        # If the user name and the password are correct the login window is destroyed and the main window opens
        self.user_id = self.login_user_id_entry.get_entr()
        self.user_pass = self.login_pass.get_entr()
        if self.user_id in self.user_data:
            if self.user_data[self.user_id] == self.user_pass:
                messagebox.showinfo('Login', 'Successful login')
                self.login_user_id_entry.clear_entr()
                self.login_pass.clear_entr()
                LoginWindow.destroy(self)
                self.new_window()
            # If the user name does not exists or is wrong
            else:
                messagebox.showerror('Error', 'Wrong password')
                self.login_user_id_entry.clear_entr()
                self.login_pass.clear_entr()
        # If the password is not correct
        else:
            messagebox.showerror('Error', 'Wrong user name')
            self.login_user_id_entry.clear_entr()
            self.login_pass.clear_entr()


'''
This is the main window frame
The building of this class and the idea for the function that changes the frames is partially taken 
from an YouTube tutorial https://www.youtube.com/watch?v=jBUpjijYtCk&t=14s
The difference is that instead of raising tha frame to the top, which didn't work for me,
I hide all the frames and show only the one I need.
'''


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title('All About Toys')

        # Setting the new window
        self.width, self.height = 800, 600
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        x_cord = int((self.screen_width / 2) - (self.width / 2))
        y_cord = int((self.screen_height / 2) - (self.height / 2))
        self.geometry("{}x{}+{}+{}".format(self.width, self.height, x_cord, y_cord))
        self.iconphoto(True, tk.PhotoImage(file='aatLogo.png'))

        # This is the menu bar
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # First drop menu
        self.main_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='Main Menu', command=lambda: self.show_frames(MainMenuFrame))
        # self.main_menu.add_command(label="Main menu", command=lambda: self.show_frames(MainMenuFrame))

        # Categories drop menu
        self.category_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.category_menu.add_command(label='New Category', command=lambda: self.show_frames(NewCategoryFrame))
        self.category_menu.add_command(label='Edit Category', command=lambda: self.show_frames(EditCategoryFrame))
        self.category_menu.add_command(label='Delete Category', command=lambda: self.show_frames(DeleteCategoryFrame))
        self.menu_bar.add_cascade(label='Categories', menu=self.category_menu)

        # Products drop menu
        self.products_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.products_menu.add_command(label='Add product', command=lambda: self.show_frames(NewProductFrame))
        self.products_menu.add_command(label='Edit product', command=lambda: self.show_frames(EditProductFrame))
        self.products_menu.add_command(label='Delete product', command=lambda: self.show_frames(DeleteProductFrame))
        self.menu_bar.add_cascade(label='Products', menu=self.products_menu)

        # Reports drop menu
        # self.reports_menu = tk.Menu(self.menu_bar, tearoff=0)
        # self.reports_menu.add_command(label='Stock reports', command=lambda: self.show_frames(ReportsFrame))
        self.menu_bar.add_cascade(label='Reports', command=lambda: self.show_frames(ReportsFrame))

        self.menu_bar.add_cascade(label='Exit', command=quit)

        # Create the container for all frames
        container = tk.Frame(self)
        container.configure(bg='#282828')
        container.pack(side="top", fill="both", expand=True)

        # configuring the container
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create the frames list that will be used to switch between frames
        self.frames = {}

        for f in (MainMenuFrame, CategoriesFrame, NewCategoryFrame, DeleteCategoryFrame, EditCategoryFrame,
                  ProductsMenuFrame, NewProductFrame, DeleteProductFrame, EditProductFrame, ReportsFrame):
            frame = f(container, self)
            self.frames[f] = frame
            # frame.grid(row=0, column=0, sticky="ns")
            print(self.frames)  # This is for developing purpose
    #
        self.show_frames(MainMenuFrame)

    # This method hides all frames and shows only the one that is needed
    def show_frames(self, count):
        for f in (MainMenuFrame, CategoriesFrame, NewCategoryFrame, DeleteCategoryFrame, EditCategoryFrame,
                  ProductsMenuFrame, NewProductFrame, DeleteProductFrame, EditProductFrame, ReportsFrame):
            frame = self.frames[f]
            print("hide" + str(frame))  # This is for developing purpose
            frame.grid_forget()
        # frame = self.frames[old]
        # print("hide" + str(frame))
        # frame.grid_forget()
        frame = self.frames[count]
        print("show" + str(frame))  # This is for developing purpose
        # frame.tkraise()
        frame.grid(row=0, column=0, sticky="ns")


# This class contains all main buttons that lead to the functions of the program
class MainMenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self["bg"] = '#282828'

        self.lbl_font = font.Font(family='Verdana', size='12')

        self.btn_font = font.Font(family='Verdana', size='8')
        # #
        self.lbl_main_menu = MyLabels(self, "MAIN MENU", self.lbl_font, 50, 0, 0)

        self.products_btn_img = tk.PhotoImage(file='images/products_btn.png')
        self.btn_products = BtnClass(self, self.products_btn_img, lambda: controller.show_frames(ProductsMenuFrame),
                                     20, 1, 0)

        self.categories_btn_img = tk.PhotoImage(file='images/categories_btn.png')
        self.btn_categories = BtnClass(self, self.categories_btn_img, lambda: controller.show_frames(CategoriesFrame),
                                       20, 2, 0)

        self.reports_btn_img = tk.PhotoImage(file='images/reports_btn.png')
        self.btn_reports = BtnClass(self, self.reports_btn_img, lambda: controller.show_frames(ReportsFrame), 20, 3, 0)


# This class contains the buttons that show the option for the categories
class CategoriesFrame(tk.Frame):
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        self["bg"] = '#282828'

        self.lbl_font = font.Font(family='Verdana', size='12')

        self.btn_font = font.Font(family='Verdana', size='8')

        self.lbl_categories_menu = MyLabels(self, "CATEGORIES", self.lbl_font, 50, 0, 0)

        self.add_category_img = tk.PhotoImage(file='images/new_category_btn.png')
        self.edit_category_img = tk.PhotoImage(file='images/edit_category_btn.png')
        self.del_category_img = tk.PhotoImage(file='images/delete_category_btn.png')
        self.go_back_img = tk.PhotoImage(file='images/go_back_btn.png')

        self.btn_add_category = BtnClass(self, self.add_category_img,
                                         lambda: controller.show_frames(NewCategoryFrame), 20, 1, 0)

        self.btn_edit_category = BtnClass(self, self.edit_category_img,
                                          lambda: controller.show_frames(EditCategoryFrame), 20, 2, 0)

        self.btn_del_category = BtnClass(self, self.del_category_img,
                                         lambda: controller.show_frames(DeleteCategoryFrame), 20, 3, 0)

        self.btn_go_back = BtnClass(self, self.go_back_img, lambda: controller.show_frames(MainMenuFrame), 20, 4, 0)


# This class contains the buttons that show the option for the categories
class ProductsMenuFrame(tk.Frame):
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        self["bg"] = '#282828'

        self.lbl_font = font.Font(family='Verdana', size='12')
        self.btn_font = font.Font(family='Verdana', size='8')

        self.lbl_products_menu = MyLabels(self, "PRODUCTS", self.lbl_font, 50, 0, 0)

        self.add_product_img = tk.PhotoImage(file='images/add_product_btn.png')
        self.edit_product_img = tk.PhotoImage(file='images/edit_product_btn.png')
        self.del_product_img = tk.PhotoImage(file='images/delete_product_button.png')
        self.go_back_img = tk.PhotoImage(file='images/go_back_btn.png')

        self.btn_add_product = BtnClass(self, self.add_product_img,
                                        lambda: controller.show_frames(NewProductFrame), 20, 1, 0)

        self.btn_edit_product = BtnClass(self, self.edit_product_img,
                                         lambda: controller.show_frames(EditProductFrame), 20, 2, 0)

        self.btn_del_product = BtnClass(self, self.del_product_img,
                                        lambda: controller.show_frames(DeleteProductFrame), 20, 3, 0)

        self.btn_go_back = BtnClass(self, self.go_back_img, lambda: controller.show_frames(MainMenuFrame), 20, 4, 0)


# This is the class that contains the attributes and methods needed to add a category
class NewCategoryFrame(tk.Frame):
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        self["bg"] = '#282828'

        self.lbl_font = font.Font(family='Verdana', size='12')
        self.btn_font = font.Font(family='Verdana', size='8')

        self.lbl_new_categories_menu = MyLabels(self, "ADD NEW CATEGORY", self.lbl_font, 50, 0, 0)
        self.lbl_new_categories_menu.set_columnspan(2)

        self.lbl_category_name = MyLabels(self, "New category name", self.btn_font, 0, 1, 0)
        self.lbl_category_name.set_alignment('E')

        self.add_category_name_entr = MyEntries(self, 0, 20, 1, 1)
        self.add_category_name_entr.set_size_entr(40)

        self.lbl_category_code = MyLabels(self, "New category code", self.btn_font, 0, 2, 0)
        self.lbl_category_code.set_alignment('E')

        self.add_category_code_entr = MyEntries(self, 0, 10, 2, 1)
        self.add_category_code_entr.set_size_entr(40)

        # This is the save new category btn
        self.save_img = tk.PhotoImage(file='images/save_btn.png')
        self.btn_save_category = BtnClass(self, self.save_img, self.add_new_category, 20, 3, 1)
        self.btn_save_category.set_alignment('E')

        # This is Go back btn in add new category
        self.go_back_img = tk.PhotoImage(file='images/go_back_btn.png')
        self.btn_go_back = BtnClass(self, self.go_back_img, lambda: controller.show_frames(CategoriesFrame), 20, 3, 0)
        self.btn_go_back.set_alignment('W')

        # This is the button to view all categories
        self.view_categories_img = tk.PhotoImage(file='images/view_categories_btn.png')
        self.btn_view_categories_list = BtnClass(self, self.view_categories_img, self.get_categories, 10, 6, 1)
        self.btn_view_categories_list.set_alignment('E')

    def add_new_category(self):
        """This method adds the new category to the database"""

        # connect to database
        self.conn = sqlite3.connect('products.db')

        # create the cursor
        self.c = self.conn.cursor()

        # First I am getting a list with all the existing categories
        # in order to perform checks to avoid duplicating name or a code
        with self.conn:
            self.c.execute("SELECT * FROM categories ORDER BY category_name ASC")
        categories = self.c.fetchall()

        # This code produces two lists with the names and the codes of the categories
        self.list_names = []
        self.list_codes = []
        for item in categories:
            # list += str(item[0]) + '-' + str(item[1]) + '\n'
            self.list_names.append(str(item[0]))
            self.list_codes.append(str(item[1]))
        # print(self.list_names, self.list_codes)

        # Getting the values from entries
        self.name = self.add_category_name_entr.get_entr()
        self.code = self.add_category_code_entr.get_entr()
        if self.name in self.list_names:
            print("Name already in list")
            messagebox.showerror('Error', 'This category already exists')  # Check the name
            self.add_category_name_entr.clear_entr()
            self.add_category_code_entr.clear_entr()
        else:
            if len(self.name) == 0:
                messagebox.showerror('Error', 'The  "Category name" field is empty')   # Check for name input
                self.add_category_name_entr.clear_entr()
                self.add_category_code_entr.clear_entr()
            else:
                if self.code in self.list_codes:
                    print("Code already in the list")
                    messagebox.showerror('Error', 'This code already exists')  # Check the code
                    self.add_category_name_entr.clear_entr()
                    self.add_category_code_entr.clear_entr()
                else:
                    if len(self.code) == 0:
                        messagebox.showerror('Error', 'The "Code" field is empty')  # Check for code input
                        self.add_category_name_entr.clear_entr()
                        self.add_category_code_entr.clear_entr()
                    else:
                        try:
                            # If all checks are passed the category can be added
                            with self.conn:
                                self.c.execute("INSERT INTO categories VALUES(?,?)", (self.name, self.code))
                                messagebox.showinfo('New category', self.name + ' category has been created')
                        except sqlite3.IntegrityError:
                            messagebox.showerror('Error', 'Please use a number for the category code')  # Check for code input

        self.add_category_name_entr.clear_entr()
        self.add_category_code_entr.clear_entr()

    # This method uses an instance of the ListCategories class to show all categories
    # available in the database in a new window
    def get_categories(self):
        # Existing categories
        self.list = ListCategories(self)
        return self.list


# This is the class that shows all available categories in the database in a new window
class ListCategories(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

    # The instance of this class opens in a new window
        self.new_window = tk.Toplevel(root)

        self.new_window.title('Existing categories')
        self.new_window["bg"] = '#282828'
        self.lbl_font = font.Font(family='Verdana', size='12')
        self.btn_font = font.Font(family='Verdana', size='8')
        self.new_window.width, self.new_window.height = 400, 400
        self.new_window.screen_width = self.new_window.winfo_screenwidth()
        self.new_window.screen_height = self.new_window.winfo_screenheight()
        x_cord = int((self.new_window.screen_width / 2) + (self.new_window.width / 2))
        y_cord = int((self.new_window.screen_height / 2) - (self.new_window.height / 2))
        self.new_window.geometry("{}x{}+{}+{}".format(self.new_window.width, self.new_window.height, x_cord, y_cord))

        # Here I need a container so the elements can appear centered
        self.container = tk.Frame(self.new_window)
        self.container.pack(pady=30)
        self.container.configure(bg='#282828')
        # self.container.grid(row=0, column=0, sticky="ew")

        self.lbl_categories_list = MyLabels(self.container, "EXISTING CATEGORIES", self.lbl_font, 10, 8, 0)
        self.lbl_categories_list.set_columnspan(2)

        self.refresh_list()

    # This function is used to refresh the categories view after a change has been made
    def refresh_list(self):
        # connect to database
        self.conn = sqlite3.connect('products.db')

        # create the cursor
        self.c = self.conn.cursor()

        with self.conn:
            self.c.execute("SELECT * FROM categories ORDER BY category_name ASC")
        self.categories = self.c.fetchall()
        self.list = dict(self.categories)
        i = 9
        for key in self.list:
            self.lbl_category_name = MyLabels(self.container, str(key), self.btn_font, 5, i, 0)
            self.lbl_category_name.set_alignment('E')
            self.lbl_category_code = MyLabels(self.container, "Code " + str(self.list[key]), self.btn_font, 5, i, 1)
            i += 1

        print(i)  # This is for developing purposes. Check if the loop does it's job

        # This is the button to view all categories and refresh the list
        self.refresh_btn = tk.PhotoImage(file='images/refresh_btn.png')
        self.btn_refresh = BtnClass(self.container, self.refresh_btn, self.refresh_list, 10, i, 0)
        self.btn_refresh.set_alignment('W')

        # This is the button to close the categories window
        self.close_btn = tk.PhotoImage(file='images/close_btn.png')
        self.btn_close = BtnClass(self.container, self.close_btn, self.new_window.destroy, 10, i, 1)
        self.btn_close.set_alignment('E')


# This is the class that opens the frame with attributes for deleting a category
class DeleteCategoryFrame(tk.Frame):
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        self["bg"] = '#282828'

        self.lbl_font = font.Font(family='Verdana', size='12')
        self.btn_font = font.Font(family='Verdana', size='8')
        # This is the page title
        self.lbl_del_categories_menu = MyLabels(self, "DELETE CATEGORY", self.lbl_font, 50, 0, 0)
        self.lbl_del_categories_menu.set_columnspan(2)

        self.lbl_choose_category_name = MyLabels(self, "Choose category \nto delete", self.btn_font, 0, 1, 0)
        self.lbl_choose_category_name.set_alignment('w')

        # This is the btn to delete a category
        self.delete_img = tk.PhotoImage(file='images/delete_btn.png')
        self.btn_delete_category = BtnClass(self, self.delete_img, self.delete_category_by_name, 20, 3, 1)
        self.btn_delete_category.set_alignment('E')

        # This is Go back btn in add new category
        self.go_back_img = tk.PhotoImage(file='images/go_back_btn.png')
        self.btn_go_back = BtnClass(self, self.go_back_img, lambda: controller.show_frames(CategoriesFrame), 20, 3, 0)
        self.btn_go_back.set_alignment('W')

        # This is an instance of the combo class that adds a drop menu to choose a category
        self.combo = ComboMenus()
        self.combo.add_categories_combo(self, 30, 0, 0, 1, 1, None)
        # self.combo.add_codes_combo(self, 20, 20, 5, 2, 1, 'W')

        # This is the button to view all categories
        self.view_categories_img = tk.PhotoImage(file='images/view_categories_btn.png')
        self.btn_view_categories_list = BtnClass(self, self.view_categories_img, self.get_categories, 10, 6, 1)
        self.btn_view_categories_list.set_alignment('E')

    # This is the method to delete the chosen category if it exists
    def delete_category_by_name(self):
        # connect to database
        self.conn = sqlite3.connect('products.db')

        # create the cursor
        self.c = self.conn.cursor()

        print(self.combo.get_category_name())

        if self.combo.get_category_name():
            # Making sure the user wants to delete the chosen category
            self.answer = messagebox.askokcancel('DELETE', 'Are you sure you want to delete \''
                                                 + self.combo.get_category_name() + '\' category?')
            # This is the delete query
            if self.answer == 1:
                with self.conn:
                    self.c.execute("DELETE FROM categories WHERE category_name=:cat",
                                   {'cat': self.combo.get_category_name()})
            messagebox.showinfo("DELETED", self.combo.get_category_name() + ' category has been deleted.')
        else:
            messagebox.showerror("Error", "Please choose a category")

    # This method uses an instance of the ListCategories class to show all categories
    # available in the database in a new window
    def get_categories(self):
        # Existing categories
        self.list = ListCategories(self)
        return self.list


# This class contains attributes and methods needed in order to edit a category
class EditCategoryFrame(tk.Frame):
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        self["bg"] = '#282828'

        self.lbl_font = font.Font(family='Verdana', size='12')
        self.btn_font = font.Font(family='Verdana', size='8')

        self.lbl_edit_categories_menu = MyLabels(self, "EDIT CATEGORY", self.lbl_font, 30, 0, 0)
        self.lbl_edit_categories_menu.set_columnspan(2)

        # This is the class with combo buttons for the category names
        self.combo = ComboMenus()
        self.combo.add_categories_combo(self, 30, 5, 5, 2, 0, 'W')

        self.lbl_choose_category_name = MyLabels(self, "Choose category to edit", self.btn_font, 0, 1, 0)
        self.lbl_choose_category_name.set_alignment('W')

        self.lbl_enter_category_name = MyLabels(self, "Enter new name", self.btn_font, 0, 1, 1)
        self.lbl_enter_category_name.set_alignment('w')

        self.new_category_name_entr = MyEntries(self, 5, 10, 2, 1)

        # This part is if we want to change a category code
        # self.combo.add_codes_combo(self, 30, 5, 5, 4, 0, 'W')
        # self.lbl_category_name = MyLabels(self, "Choose category code to edit", self.btn_font, 0, 3, 0)
        # self.lbl_category_name.set_alignment('w')
        #
        #
        # self.lbl_category_name = MyLabels(self, "Enter new code", self.btn_font, 0, 3, 1)
        # self.lbl_category_name.set_alignment('w')
        #
        # self.new_category_code_entr = MyEntries(self, 5, 10, 4, 1)

        # This is the edit category name btn
        self.submit_img = tk.PhotoImage(file='images/submit_btn.png')
        self.btn_submit_category = BtnClass(self, self.submit_img, self.edit_category_by_name, 10, 5, 1)
        self.btn_submit_category.set_alignment('E')

        # This is Go back btn in add new category
        self.go_back_img = tk.PhotoImage(file='images/go_back_btn.png')
        self.btn_go_back = BtnClass(self, self.go_back_img, lambda: controller.show_frames(CategoriesFrame), 10, 5, 0)
        self.btn_go_back.set_alignment('W')

        # This is the button to view all categories
        self.view_categories_img = tk.PhotoImage(file='images/view_categories_btn.png')
        self.btn_view_categories_list = BtnClass(self, self.view_categories_img, self.get_categories, 10, 6, 1)
        self.btn_view_categories_list.set_alignment('E')

    def get_categories(self):
        # Existing categories
        self.list = ListCategories(self)
        return self.list

    def edit_category_by_name(self):
        # connect to database
        self.conn = sqlite3.connect('products.db')

        # create the cursor
        self.c = self.conn.cursor()

        print(self.combo.get_category_name())
        with self.conn:
            self.c.execute("SELECT * FROM categories")
        categories = self.c.fetchall()
        list_cat = dict(categories)
        if self.combo.get_category_name():
            if self.new_category_name_entr.get_entr():
                if self.new_category_name_entr.get_entr() in list_cat:
                    messagebox.showerror('Error', 'This name already exists')
                else:
                    self.answer = messagebox.askokcancel('EDIT', 'Are you sure you want to edit \''
                                                         + self.combo.get_category_name() + '\' category')
                    if self.answer == 1:
                        with self.conn:
                            self.c.execute("""UPDATE categories SET category_name=:new_name
                                            WHERE category_name=:old_name
                                            """, {'new_name': self.new_category_name_entr.get_entr(),
                                                  'old_name': self.combo.get_category_name()})
                            messagebox.showinfo("Edit", "The category name changed successfully")
            else:
                messagebox.showerror("Error", "The new name field is empty")
        else:
            messagebox.showerror("Error", "Please choose a category")


# This class contains the combo menus that are used throughout the program
class ComboMenus(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self["bg"] = '#282828'
        self.lbl_font = font.Font(family='Verdana', size='12')
        self.btn_font = font.Font(family='Verdana', size='8')

    # This is the combo with categories names
    def add_categories_combo(self, root, size_cat, pady, padx, row, column, sticky):
        self.get_categories_list()
        self.categories_combo = ttk.Combobox(root, value=self.get_categories_list(), width=size_cat)
        self.categories_combo.current(None)
        self.categories_combo.grid(pady=pady, padx=padx, row=row, column=column, sticky=sticky)

    # This combo contains the category codes
    def add_codes_combo(self, root, size_codes, pady, padx, row, column, sticky):
        self.get_codes_list()
        self.codes_combo = ttk.Combobox(root, value=self.get_codes_list(), width=size_codes)
        self.codes_combo.current(None)
        self.codes_combo.grid(pady=pady, padx=padx, row=row, column=column, sticky=sticky)

    # This method returns the chosen name
    def get_category_name(self):
        name = self.categories_combo.get()
        return name

    # This method returns the chosen code
    def get_category_code(self):
        code = self.codes_combo.get()
        return code

    # Getting all category names in a list
    def get_categories_list(self):
        # connect to database
        self.conn = sqlite3.connect('products.db')

        # create the cursor
        self.c = self.conn.cursor()

        # Getting all category names in a list
        self.list_names = []
        with self.conn:
            self.c.execute("SELECT * FROM categories ORDER BY category_name ASC")
        categories = self.c.fetchall()
        for item in categories:
            self.list_names.append(str(item[0]))

        print(self.list_names)
        return self.list_names

    # Getting all category codes in a list
    def get_codes_list(self):
        # connect to database
        self.conn = sqlite3.connect('products.db')

        # create the cursor
        self.c = self.conn.cursor()

        self.list_codes = []
        with self.conn:
            self.c.execute("SELECT * FROM categories ORDER BY category_name ASC")
        categories = self.c.fetchall()
        for item in categories:
            self.list_codes.append(str(item[1]))

        print(self.list_codes)
        return self.list_codes


# This class contains attributes and methods needed to add a new product or change product details.
class Product(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self["height"] = 600
        self["width"] = 600
        self["bg"] = '#282828'
        self.grid()

        self.lbl_font = font.Font(family='Verdana', size='12')
        self.btn_font = font.Font(family='Verdana', size='8')

        self.lbl_product_name = MyLabels(self, "Product name", self.btn_font, 0, 1, 0)
        self.lbl_product_name.set_alignment('E')

        self.add_product_name_entr = MyEntries(self, 10, 10, 1, 1)
        self.add_product_name_entr.set_size_entr(40)
        self.add_product_name_entr.set_alignment('W')

        self.lbl_category_name = MyLabels(self, "Choose product category", self.btn_font, 0, 2, 0)
        self.lbl_category_name.set_alignment('E')

        # This is the class with combo buttons for the category names
        self.combo = ComboMenus()
        self.combo.add_categories_combo(self, 37, 5, 10, 2, 1, 'W')

        self.lbl_manufacturer = MyLabels(self, "Manufacturer", self.btn_font, 5, 3, 0)
        self.lbl_manufacturer.set_alignment('E')
        self.entr_manufacturer = MyEntries(self, 10, 10, 3, 1)
        self.entr_manufacturer.set_size_entr(40)
        self.entr_manufacturer.set_alignment('W')

        self.lbl_quantity = MyLabels(self, "Quantity", self.btn_font, 5, 5, 0)
        self.lbl_quantity.set_alignment('E')
        self.entr_quantity = MyEntries(self, 10, 10, 5, 1)
        self.entr_quantity.set_size_entr(40)
        self.entr_quantity.set_alignment('W')

        self.lbl_price = MyLabels(self, "Price(£)", self.btn_font, 5, 6, 0)
        self.lbl_price.set_alignment('E')
        self.entr_price = MyEntries(self, 10, 10, 6, 1)
        self.entr_price.set_size_entr(20)
        self.entr_price.set_alignment('W')

        self.lbl_weight = MyLabels(self, "Weight(kg)", self.btn_font, 5, 7, 0)
        self.lbl_weight.set_alignment('E')
        self.entr_weight = MyEntries(self, 10, 10, 7, 1)
        self.entr_weight.set_size_entr(20)
        self.entr_weight.set_alignment('W')

        self.lbl_description = MyLabels(self, "Description", self.btn_font, 5, 8, 0)
        self.lbl_description.set_alignment('NE')
        self.entr_description = tk.Text(self, height=5, width=30)
        self.entr_description.grid(padx=10, pady=10, row=8, column=1, sticky='W')

        # This is the btn to choose image of the product
        self.choose_img = tk.PhotoImage(file='images/choose_image.png')
        self.btn_choose_img = BtnClass(self, self.choose_img, self.choose_image, 5, 9, 0)
        self.btn_choose_img.set_alignment('W')

        self.image = ""

    def choose_image(self):
        """This method is used to choose an image
        from a folder and save it as BLOB in the database"""
        try:
            self.my_filetype = [('image files', '.png')]
            self.answer = filedialog.askopenfilename(parent=self, initialdir="C:\\",
                                                     title="Please choose an image", filetypes=self.my_filetype)
            # print(answer)
            # here we open the as binary and save it in variable
            with open(self.answer, 'rb') as f:
                self.image = f.read()
            self.path = self.answer.split("/")
            self.file_name = self.path[-1]

            # This label shows the name of the chosen file
            self.lbl_chosen_file = MyLabels(self, self.file_name, self.btn_font, 0, 10, 0)
            self.lbl_chosen_file.set_columnspan(2)
            self.lbl_chosen_file.set_alignment('W')
        # Exception is raised when there is no chosen image
        except FileNotFoundError:
            pass

    def save_product_to_db(self):
        """This method saves the new product to the database"""

        # here we get the category code corresponding to the chosen name
        # This is the name of the category from the entry
        self.category_name = self.combo.get_category_name()

        # Here we get the code of the chosen category
        self.conn = sqlite3.connect("products.db")
        self.c = self.conn.cursor()
        # category_name = self.combo.get_category_name()
        self.c.execute("SELECT * FROM categories WHERE category_name=:category_name",
                       {'category_name': self.category_name})
        self.category = self.c.fetchall()
        for item in self.category:
            self.category_code = item[1]

        self.conn.commit()
        self.conn.close()

        # This is the SQL query that adds the new product to the database
        self.conn = sqlite3.connect("products.db")

        self.c = self.conn.cursor()
        try:
            # Check if the required fields are filled
            if self.add_product_name_entr.get_entr() \
                    and self.category_code \
                    and self.entr_manufacturer.get_entr() \
                    and self.entr_quantity.get_entr() \
                    and self.entr_price.get_entr() \
                    and self.entr_weight.get_entr() \
                    and self.entr_description.get(1.0, 1.1):
                # Save the product to database if the check is passed
                self.c.execute("""
                INSERT INTO product (product_name, category_code, manufacturer,
                                    import_date, quantity, price, weight, image, description)
                VALUES (:product_name, :category_code, :manufacturer,
                        datetime('now', 'localtime'), :quantity, :price, :weight, :image, :description)""",
                               {'product_name': self.add_product_name_entr.get_entr(),
                                'category_code': self.category_code,
                                'manufacturer': self.entr_manufacturer.get_entr(),
                                'quantity': int(self.entr_quantity.get_entr()),
                                'price': float(self.entr_price.get_entr()),
                                'weight': float(self.entr_weight.get_entr()),
                                'image': self.image,
                                'description': self.entr_description.get(1.0, tk.END)})
                messagebox.showinfo('New product', 'The product has been added successfully')

                self.add_product_name_entr.clear_entr()
                self.entr_weight.clear_entr()
                self.entr_price.clear_entr()
                self.entr_description.delete(1.0, tk.END)
                self.entr_manufacturer.clear_entr()
                self.entr_quantity.clear_entr()
                try:
                    self.lbl_chosen_file.hide_lbl()
                except AttributeError:
                    pass
            else:
                messagebox.showerror("Empty field",
                                     "Only the Image field can be empty.\nPlease, fill in all the fields.")

        except ValueError:
            messagebox.showerror("Wrong value", "Quantity value needs to be a whole number. \n "
                                                "Input value for price and weight should be in the format 00.00")
        except AttributeError:
            messagebox.showerror("Empty field", "Please choose a category")

        finally:
            self.conn.commit()
            self.conn.close()


# This is the class to add a new product
class NewProductFrame(Product):
    def __init__(self, root, controller):
        Product.__init__(self, root)
        self["height"] = 600
        self["width"] = 600
        self["bg"] = '#282828'

        self.lbl_font = font.Font(family='Verdana', size='12')
        self.btn_font = font.Font(family='Verdana', size='8')

        self.lbl_add_new_product = MyLabels(self, "ADD NEW PRODUCT", self.lbl_font, 40, 0, 0)
        self.lbl_add_new_product.set_columnspan(2)

        # # This is the save new category btn
        self.save_img = tk.PhotoImage(file='images/save_btn.png')
        self.btn_save_product_to_db = BtnClass(self, self.save_img, self.save_product_to_db, 20, 11, 1)
        self.btn_save_product_to_db.set_alignment('E')

        # This is Go back btn in add new product
        self.go_back_img = tk.PhotoImage(file='images/go_back_btn.png')
        self.btn_go_back = BtnClass(self, self.go_back_img,
                                    lambda: controller.show_frames(ProductsMenuFrame), 20, 11, 0)
        self.btn_go_back.set_alignment('W')


# This class contains the methods to view, edit and delete products
class ViewProduct(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self["bg"] = '#282828'

        self.lbl_font = font.Font(family='Verdana', size='12')
        self.btn_font = font.Font(family='Verdana', size='8')

        self.lbl_product_id = MyLabels(self, "Product ID", self.btn_font, 0, 1, 0)
        self.lbl_product_id.set_alignment('E')

        # This is the entry that gets an ID input from the user
        self.add_product_id_entr = MyEntries(self, 0, 10, 1, 1)
        self.add_product_id_entr.set_size_entr(40)

        # With this button we can view the chosen product
        self.view_product_img = tk.PhotoImage(file='images/view_btn.png')
        self.btn_view_product = BtnClass(self, self.view_product_img, self.view_product, 10, 2, 1)
        self.btn_view_product.set_alignment('E')

        self.reset_view()

    def view_product(self):

        self.lbl_del_product_preview.hide_lbl()

        self.product_id = self.add_product_id_entr.get_entr()

        try:
            self.conn = sqlite3.connect('products.db')

            self.c = self.conn.cursor()
            self.c.execute("""SELECT P.product_id, P.product_name, P.manufacturer, P.quantity, 
                                    P.price, P.weight, C.category_name
                            FROM product AS P, categories AS C
                            WHERE product_id=:product_id
                            AND P.category_code=C.category_code""",
                           {'product_id': self.product_id})
            product = self.c.fetchall()
            print(product)

            self.lbl_del_product_preview = MyLabels(self, "Product ID: " + str(product[0][0]) +
                                                    "\n\n Product name: " + str(product[0][1]) +
                                                    "\n\n Product category: " + str(product[0][6]) +
                                                    "\n\n Manufacturer: " + str(product[0][2]) +
                                                    "\n\n Available quantity: " + str(product[0][3]) + " units" +
                                                    "\n\n Price: " + "£" + str(product[0][4]) +
                                                    "\n\n Weight: " + str(product[0][5]) +
                                                    " kg", self.lbl_font, 10, 3, 0)
            self.lbl_del_product_preview.set_columnspan(2)
        #     If the product does not exists in the database it throws an exception
        except IndexError:
            self.reset_view()
            messagebox.showerror('Error', 'No product with this ID')
        finally:
            self.conn.commit()
            self.conn.close()

    # This part clears the view of the product
    def reset_view(self):
        self.lbl_del_product_preview = MyLabels(self, " " +
                                                "\n\n " +
                                                "\n\n " +
                                                "\n\n " +
                                                "\n\n " +
                                                "\n\n " +
                                                "\n\n ", self.lbl_font, 10, 3, 0)
        self.lbl_del_product_preview.set_columnspan(2)

    def edit_product(self):
        """This function opens a new window with fields to enter product details"""
        self.product_id = self.add_product_id_entr.get_entr()
        # First I need to make a manual check if the ID exists in the database.
        self.conn = sqlite3.connect('products.db')
        with self.conn:
            self.c = self.conn.cursor()
            self.c.execute("SELECT product_id FROM product WHERE product_id=:product_id",
                           {'product_id': self.product_id})
            self.list = self.c.fetchall()
        # This checks if there is an ID in the list
        if not self.list:
            messagebox.showerror('Error', 'No product with this ID')
        else:
            self.new_window = tk.Toplevel(self)
            self.new_window.title('Edit product')
            self.new_window["bg"] = '#282828'
            self.lbl_font = font.Font(family='Verdana', size='12')
            self.btn_font = font.Font(family='Verdana', size='8')
            self.new_window.width, self.new_window.height = 600, 600
            self.new_window.screen_width = self.new_window.winfo_screenwidth()
            self.new_window.screen_height = self.new_window.winfo_screenheight()
            x_cord = int((self.new_window.screen_width / 2) + (self.new_window.width / 2))
            y_cord = int((self.new_window.screen_height / 2) - (self.new_window.height / 2))
            self.new_window.geometry(
                "{}x{}+{}+{}".format(self.new_window.width, self.new_window.height, x_cord, y_cord))

            self.container = tk.Frame(self.new_window, bg='#282828')
            self.container.pack()

            self.lbl_edit_product_window = MyLabels(self.container, "PLEASE ENTER NEW DETAILS", self.lbl_font, 40, 0, 0)
            self.lbl_edit_product_window.set_columnspan(2)

            # This is an instance of the Product class which contains all product fields
            self.product_info = Product(self.container)

            # This is the button to close the edit product window
            self.close_btn = tk.PhotoImage(file='images/close_btn.png')
            self.btn_close = BtnClass(self.container, self.close_btn, self.new_window.destroy, 10, 15, 0)
            self.btn_close.set_alignment('W')

            # this button submits changes
            self.submit_img = tk.PhotoImage(file='images/submit_btn.png')
            self.btn_submit_product = BtnClass(self.container, self.submit_img, self.submit_edit, 10, 15, 1)
            self.btn_submit_product.set_alignment('E')

    def submit_edit(self):
        """This function submits the new data to the database"""

        # here we get the category code corresponding to the chosen name
        # This is the name of the category from the entry
        try:
            self.category_name = self.product_info.combo.get_category_name()

            # Here we get the code of the chosen category
            self.conn = sqlite3.connect("products.db")
            self.c = self.conn.cursor()
            # category_name = self.combo.get_category_name()
            self.c.execute("SELECT * FROM categories WHERE category_name=:category_name",
                           {'category_name': self.category_name})
            self.category = self.c.fetchall()
            for item in self.category:
                self.category_code = item[1]
        except AttributeError:
            self.category_code = ""
        finally:
            self.conn.commit()
            self.conn.close()

        # This is the SQL query that adds the new product to the database
        self.conn = sqlite3.connect("products.db")

        # Here is the query for updating the database
        # First I am checking if there is a value in the field
        # and update only the fields that have new values
        self.c = self.conn.cursor()
        if self.product_info.add_product_name_entr.get_entr():
            self.c.execute("""UPDATE product SET product_name=:product_name
                            WHERE product_id=:product_id""",
                           {'product_id': self.add_product_id_entr.get_entr(),
                            'product_name': self.product_info.add_product_name_entr.get_entr()})
        else:
            pass
        # Here I was getting an AttributeError if there is no new category and had to add an exception
        try:
            if self.category_code:
                self.c.execute("""UPDATE product SET category_code=:category_code
                                WHERE product_id=:product_id""",
                               {'product_id': self.add_product_id_entr.get_entr(),
                                'category_code': self.category_code})
            else:
                pass
        except AttributeError:
            pass

        if self.product_info.entr_manufacturer.get_entr():
            self.c.execute("""UPDATE product SET manufacturer=:manufacturer
                            WHERE product_id=:product_id""",
                           {'product_id': self.add_product_id_entr.get_entr(),
                            'manufacturer': self.product_info.entr_manufacturer.get_entr()})
        else:
            pass
        if self.product_info.entr_quantity.get_entr():
            self.c.execute("""UPDATE product SET quantity=:quantity
                               WHERE product_id=:product_id""",
                           {'product_id': self.add_product_id_entr.get_entr(),
                            'quantity': self.product_info.entr_quantity.get_entr()})
        else:
            pass
        if self.product_info.entr_price.get_entr():
            self.c.execute("""UPDATE product SET price=:price
                               WHERE product_id=:product_id""",
                           {'product_id': self.add_product_id_entr.get_entr(),
                            'price': self.product_info.entr_price.get_entr()})
        else:
            pass
        if self.product_info.entr_weight.get_entr():
            self.c.execute("""UPDATE product SET weight=:weight
                               WHERE product_id=:product_id""",
                           {'product_id': self.add_product_id_entr.get_entr(),
                            'weight': self.product_info.entr_weight.get_entr()})
        else:
            pass
        if self.product_info.image:
            self.c.execute("""UPDATE product SET image=:image
                                      WHERE product_id=:product_id""",
                           {'product_id': self.add_product_id_entr.get_entr(),
                            'image': self.product_info.image})
        else:
            pass
        if self.product_info.entr_description.get(1.0, tk.END):
            self.c.execute("""UPDATE product SET description=:description
                                         WHERE product_id=:product_id""",
                           {'product_id': self.add_product_id_entr.get_entr(),
                            'description': self.product_info.entr_description.get(1.0, tk.END)})
        else:
            pass

        self.conn.commit()
        self.conn.close()

        messagebox.showinfo('Edit product', 'The product has been updated successfully')

    def del_product(self):
        """This function deletes the chosen product"""
        self.product_id = self.add_product_id_entr.get_entr()
        # First I need to make a manual check if the ID exists in the database.
        # For some reason the IndexError does not work with DELETE
        self.conn = sqlite3.connect('products.db')
        with self.conn:
            self.c = self.conn.cursor()
            self.c.execute("SELECT product_id FROM product WHERE product_id=:product_id",
                           {'product_id': self.product_id})
            self.list = self.c.fetchall()
        # This checks if there is an ID in the list
        if not self.list:
            messagebox.showerror('Error', 'No product with this ID')
        else:
            self.answer = messagebox.askokcancel('DELETE',
                                                 'Are you sure you want to delete product with ID:' + self.product_id)
            if self.answer == 1:
                try:
                    self.conn = sqlite3.connect('products.db')

                    self.c = self.conn.cursor()
                    self.c.execute("DELETE FROM product WHERE product_id=:product_id",
                                   {'product_id': self.product_id})
                    messagebox.showinfo('Delete product', 'The product has been deleted successfully')
                    self.add_product_id_entr.clear_entr()
                    self.lbl_del_product_preview.hide_lbl()
                    self.reset_view()
                except IndexError:
                    self.reset_view()
                    messagebox.showerror('Error', 'No product with this ID')
                finally:
                    self.conn.commit()
                    self.conn.close()


# This class is to delete a product and inherits from ViewProduct class and consequently from tk.Frame
class DeleteProductFrame(ViewProduct):
    def __init__(self, root, controller):
        ViewProduct.__init__(self, root)
        self["height"] = 600
        self["width"] = 600
        self["bg"] = '#282828'

        self.lbl_font = font.Font(family='Verdana', size='12')
        self.btn_font = font.Font(family='Verdana', size='8')

        self.lbl_del_product = MyLabels(self, "DELETE PRODUCT", self.lbl_font, 40, 0, 0)
        self.lbl_del_product.set_columnspan(2)

        # with this button we delete the chosen product using the delete method from ViewProduct class
        self.delete_img = tk.PhotoImage(file='images/delete_btn.png')
        self.btn_delete_product = BtnClass(self, self.delete_img, self.del_product, 10, 9, 1)
        self.btn_delete_product.set_alignment('E')

        # This is Go back btn in add new category
        self.go_back_img = tk.PhotoImage(file='images/go_back_btn.png')
        self.btn_go_back = BtnClass(self, self.go_back_img, lambda: controller.show_frames(ProductsMenuFrame), 10, 9, 0)
        self.btn_go_back.set_alignment('W')


# This is the class for editing a product and inherits
# from ViewProduct class and consequently from tk.Frame
class EditProductFrame(ViewProduct):
    def __init__(self, root, controller):
        ViewProduct.__init__(self, root)
        self["bg"] = '#282828'

        self.lbl_font = font.Font(family='Verdana', size='12')
        self.btn_font = font.Font(family='Verdana', size='8')

        self.lbl_edit_product = MyLabels(self, "EDIT PRODUCT", self.lbl_font, 40, 0, 0)
        self.lbl_edit_product.set_columnspan(2)

        # This is the btn to confirm the edit of the product using the edit method from Products class
        self.edit_img = tk.PhotoImage(file='images/edit_btn.png')
        self.btn_edit = BtnClass(self, self.edit_img, self.edit_product, 10, 10, 1)
        self.btn_edit.set_alignment('E')

        # This is Go back btn in add new category
        self.go_back_img = tk.PhotoImage(file='images/go_back_btn.png')
        self.btn_go_back = BtnClass(self, self.go_back_img,
                                    lambda: controller.show_frames(ProductsMenuFrame), 20, 10, 0)
        self.btn_go_back.set_alignment('W')


# This class contains all attributes and methods connected to the report generation
class ReportsFrame(tk.Frame):
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        self["bg"] = '#282828'

        self.lbl_font = font.Font(family='Verdana', size='12')
        self.btn_font = font.Font(family='Verdana', size='8')

        self.lbl_reports_menu = MyLabels(self, "STOCK REPORT", self.lbl_font, 40, 0, 0)
        self.lbl_reports_menu.set_columnspan(2)

        self.show_available_stock()

        # This is Go back btn in add new category
        self.go_back_img = tk.PhotoImage(file='images/go_back_btn.png')
        self.btn_go_back = BtnClass(self, self.go_back_img, lambda: controller.show_frames(MainMenuFrame), 20, 11, 0)
        self.btn_go_back.set_alignment('W')

        # This date is used for the saving of the csv files
        self.date = date.today()

    def show_available_stock(self):
        """This function shows all available products in the database """

        # Open the connection to the database
        self.conn = sqlite3.connect("products.db")

        self.c = self.conn.cursor()

        self.c.execute("""SELECT P.product_id, P.product_name, C.category_name, P.manufacturer, P.import_date, 
                                P.quantity, P.price, P.weight
                                FROM product AS P, categories AS C
                                WHERE P.category_code=C.category_code
                                """)
        self.products_list = self.c.fetchall()
        self.conn.close()

        # This is the table that will show all the products in the database after the frame is open
        self.products_table = ttk.Treeview(self, height=18)
        self.products_table['columns'] = ('ID', 'Product', 'Category', 'Manufacturer', 'Import date', 'Quantity',
                                          'Price', 'Weight')
        # These are the columns
        self.products_table.column("#0", width=0, stretch="NO")
        self.products_table.column("ID", anchor="center", width=20, minwidth=20)
        self.products_table.column("Product", anchor="w", width=100, minwidth=20)
        self.products_table.column("Category", anchor="w", width=100, minwidth=20)
        self.products_table.column("Manufacturer", anchor="w", width=100, minwidth=20)
        self.products_table.column("Import date", anchor="w", width=100, minwidth=20)
        self.products_table.column("Quantity", anchor="center", width=70, minwidth=20)
        self.products_table.column("Price", anchor="center", width=50, minwidth=20)
        self.products_table.column("Weight", anchor="center", width=70, minwidth=20)

        self.products_table.heading("ID", anchor="center", text="ID")
        self.products_table.heading("Product", anchor="w", text="Product")
        self.products_table.heading("Category", anchor="w", text="Category")
        self.products_table.heading("Manufacturer", anchor="w", text="Manufacturer")
        self.products_table.heading("Import date", anchor="w", text="Import date")
        self.products_table.heading("Quantity", anchor="center", text="Quantity")
        self.products_table.heading("Price", anchor="center", text="Price")
        self.products_table.heading("Weight", anchor="center", text="Weight")

        # self.low_stock_table.grid_forget()
        self.products_table.grid(row=1, column=0)

        # This loop fills the table with data from the database
        self.count = 0
        for row in self.products_list:
            self.products_table.insert(parent='', index='end', iid=self.count, values=row)
            self.count += 1

        # This is the btn to show the stock availability
        self.show_stock_img = tk.PhotoImage(file='images/show_stock_btn.png')
        self.btn_show_stock = BtnClass(self, self.show_stock_img, self.show_available_stock, 10, 10, 0)
        self.btn_show_stock.set_alignment('E')

        # This is the btn to show the products which are low in stock
        self.show_low_stock_neg_img = tk.PhotoImage(file='images/show_low_stock_neg_btn.png')
        self.btn_show_low_stock_neg = BtnClass(self, self.show_low_stock_neg_img, self.show_low_stock, 10, 10, 0)
        self.btn_show_low_stock_neg.set_alignment('W')

        #  This is the button to save the list of all products to a CSV file
        self.save_csv_img = tk.PhotoImage(file='images/save_as_csv.png')
        self.btn_save_csv = BtnClass(self, self.save_csv_img, self.save_products_to_csv, 20, 11, 0)
        self.btn_save_csv.set_alignment('E')

    def show_low_stock(self):
        """This method shows all products in the data"""
        # Open the connection to the database
        self.conn = sqlite3.connect("products.db")

        self.c = self.conn.cursor()

        self.c.execute("""SELECT P.product_id, P.product_name, C.category_name, P.manufacturer, P.import_date, 
                                P.quantity, P.price, P.weight
                                FROM product AS P, categories AS C
                                WHERE P.category_code=C.category_code
                                AND P.quantity<20""")
        self.low_stock_list = self.c.fetchall()
        self.conn.close()

        # This is the table that will show all the products in the database after the frame is open
        self.low_stock_table = ttk.Treeview(self, height=18)
        self.low_stock_table['columns'] = ('ID', 'Product', 'Category', 'Manufacturer', 'Import date', 'Quantity',
                                           'Price', 'Weight')
        # These are the columns
        self.low_stock_table.column("#0", width=0, stretch="NO")
        self.low_stock_table.column("ID", anchor="center", width=20, minwidth=20)
        self.low_stock_table.column("Product", anchor="w", width=100, minwidth=20)
        self.low_stock_table.column("Category", anchor="w", width=100, minwidth=20)
        self.low_stock_table.column("Manufacturer", anchor="w", width=100, minwidth=20)
        self.low_stock_table.column("Import date", anchor="w", width=100, minwidth=20)
        self.low_stock_table.column("Quantity", anchor="center", width=70, minwidth=20)
        self.low_stock_table.column("Price", anchor="center", width=50, minwidth=20)
        self.low_stock_table.column("Weight", anchor="center", width=70, minwidth=20)

        self.low_stock_table.heading("ID", anchor="center", text="ID")
        self.low_stock_table.heading("Product", anchor="w", text="Product")
        self.low_stock_table.heading("Category", anchor="w", text="Category")
        self.low_stock_table.heading("Manufacturer", anchor="w", text="Manufacturer")
        self.low_stock_table.heading("Import date", anchor="w", text="Import date")
        self.low_stock_table.heading("Quantity", anchor="center", text="Quantity")
        self.low_stock_table.heading("Price", anchor="center", text="Price")
        self.low_stock_table.heading("Weight", anchor="center", text="Weight")

        self.products_table.grid_forget()
        self.low_stock_table.grid(row=1, column=0)

        # This loop fills the table with data from the database
        self.count = 0
        for row in self.low_stock_list:
            self.low_stock_table.insert(parent='', index='end', iid=self.count, values=row)
            self.count += 1

        # This is the btn to show the stock availability
        self.show_stock_neg_img = tk.PhotoImage(file='images/show_stock_neg_btn.png')
        self.btn_show_stock = BtnClass(self, self.show_stock_neg_img, self.show_available_stock, 10, 10, 0)
        self.btn_show_stock.set_alignment('E')

        # This is the btn to show the products which are low in stock
        self.show_low_stock_img = tk.PhotoImage(file='images/show_low_stock_btn.png')
        self.btn_show_low_stock = BtnClass(self, self.show_low_stock_img, self.show_low_stock, 10, 10, 0)
        self.btn_show_low_stock.set_alignment('W')

        #  This is the button to save the list of all products to a CSV file
        self.save_csv_img = tk.PhotoImage(file='images/save_as_csv.png')
        self.btn_save_csv = BtnClass(self, self.save_csv_img, self.save_low_stock_to_csv, 20, 11, 0)
        self.btn_save_csv.set_alignment('E')

    # This is the function to save the all products to a CSV file
    def save_products_to_csv(self):
        """This function saves the list of all products to a CSV file"""
        with open('stock_report_{}.csv'.format(self.date), "w") as f:
            fieldnames = ["Product ID", "Product name", "Category",
                          "Manufacturer", "Date", "Quantity", "Price", "Weight"]
            add_rows = csv.DictWriter(f, fieldnames=fieldnames)
            add_rows.writeheader()
            for i in self.products_list:
                add_rows.writerow({"Product ID": str(i[0]),
                                   "Product name": str(i[1]),
                                   "Category": str(i[2]),
                                   "Manufacturer": str(i[3]),
                                   "Date": str(i[4]),
                                   "Quantity": str(i[5]),
                                   "Price": str(i[6]),
                                   "Weight": str(i[7])})
        messagebox.showinfo('Save to file', 'The report is successfully saved to \n' +
                                            'stock_report_{}.csv'.format(self.date))

    # This is the function to save the low quantity list to a CSV file
    def save_low_stock_to_csv(self):
        """This function saves the list of all products that have quantity under 20 to a CSV file"""
        with open('low_stock_report_{}.csv'.format(self.date), "w") as f:
            fieldnames = ["Product ID", "Product name", "Category",
                          "Manufacturer", "Date", "Quantity", "Price", "Weight"]
            add_rows = csv.DictWriter(f, fieldnames=fieldnames)
            add_rows.writeheader()
            for i in self.low_stock_list:
                add_rows.writerow({"Product ID": str(i[0]),
                                   "Product name": str(i[1]),
                                   "Category": str(i[2]),
                                   "Manufacturer": str(i[3]),
                                   "Date": str(i[4]),
                                   "Quantity": str(i[5]),
                                   "Price": str(i[6]),
                                   "Weight": str(i[7])})

        messagebox.showinfo('Save to file', 'The report is successfully saved to \n' +
                            'low_stock_report_{}.csv'.format(self.date))


# app = tk.Tk()
app = LoginWindow()
app.mainloop()
# app = MainWindow()
# app.mainloop()
