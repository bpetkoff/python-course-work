import tkinter as tk


class BtnClass:
    def __init__(self, main_root, image, command, pady, row, column):
        self.btn = tk.Button(main_root, image=image, command=command, borderwidth=0, bg='#282828',
                             activebackground='#282828')
        self.btn.grid(pady=pady, row=row, column=column)

    def set_grid(self, pady, row, columnspan):
        self.btn.grid(pady=pady, row=row, columnspan=columnspan)

    def set_alignment(self, align):
        self.btn.grid(sticky=align)


class MyLabels:
    def __init__(self, main_root, text, font, pady, row, column):
        self.lbl = tk.Label(main_root, bg='#282828', fg='#b1b1b1', font=font, text=text)
        self.lbl.grid(pady=pady, row=row, column=column)

    def set_columnspan(self, columnspan):
        self.lbl.grid(columnspan=columnspan)

    def set_colour(self, fg):
        self.lbl.configure(fg=fg)

    def set_background(self, bg):
        self.lbl.configure(bg=bg)

    def set_padx(self, padx):
        self.lbl.grid(padx=padx)

    def set_alignment(self, align):
        self.lbl.grid(sticky=align)

    def hide_lbl(self):
        self.lbl.grid_forget()



class MyEntries:
    def __init__(self, main_root, padx, pady, row, column):
        self.entr = tk.Entry(main_root)
        self.entr.grid(padx=padx, pady=pady, row=row, column=column)

    def set_grid(self, pady, row, columnspan):
        self.entr.grid(pady=pady, row=row, columnspan=columnspan)

    def get_entr(self):
        value = self.entr.get()
        return value

    def clear_entr(self):
        self.entr.delete(0, 'end')

    def set_size_entr(self, width):
        self.entr.configure(width=width)

    def set_alignment(self, align):
        self.entr.grid(sticky=align)

