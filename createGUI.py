from tkinter import *
import tkinter.filedialog as filedialog
import os
import createLogic


class CreateGUI:
    def __init__(self, window):
        self.window = window
        self.logic = createLogic.CreateProject()

        self.create_gui()

    def create_gui(self):
        self.frame = Frame(self.window, width=480, height=520)
        self.frame.grid(row=0, column=1, rowspan=7, columnspan=4)

        self.name = Label(self.frame, text="Name: ", font="Helvetica 14")
        self.name.grid(row=0, column=0, pady=5, sticky=E)
        self.readme = Label(self.frame, text="README: ", height=5, font="Helvetica 14")
        self.readme.grid(row=6, column=0, rowspan=2, sticky=E)
        self.directory = Label(self.frame, text="Directory: ", font="Helvetica 14")
        self.directory.grid(row=1, column=0, pady=(0, 20), sticky=E)
        self.username = Label(self.frame, text="Username: ", font="Helvetica 14")
        self.username.grid(row=3, column=0, sticky=E)
        self.password = Label(self.frame, text="Password: ", font="Helvetica 14")
        self.password.grid(row=4, column=0, sticky=E)
        self.verified_status = Label(
            self.frame, text="Status: Not verified", font="Helvetica 16")
        self.verified_status.grid(row=5, column=1, pady=(3, 3), sticky=N)

        self.name_entry = Entry(self.frame, width=25, font="Helvetica 16")
        self.name_entry.grid(row=0, column=1, columnspan=2, sticky=W)
        self.readme_entry = Text(self.frame, width=40, height=10, font="Helvetica 12")
        self.readme_entry.grid(row=6, column=1, columnspan=2, rowspan=2, sticky=W)
        self.directory_chosen = Entry(
            self.frame, width=32, font="Helvetica 13")
        self.directory_chosen.grid(row=1, column=1, columnspan=2, pady=(0, 15), sticky=W)
        self.username_entry = Entry(self.frame, width=26, font="Helvetica 14")
        self.username_entry.grid(row=3, column=1, columnspan=2, sticky=W)
        self.password_entry = Entry(self.frame, width=26, font="Helvetica 14", show="*")
        self.password_entry.grid(row=4, column=1, columnspan=2, sticky=W)


        self.browse_button = Button(self.frame, text="Browse", command=self.browse_directory,
                               width=6, font="Helvetica 13")
        self.browse_button.grid(row=1, column=2, pady=(0, 18), sticky=E)
        self.upload = IntVar(value=0)
        self.verify_button = Button(
            self.frame, text="Verify", command=self.verify_auth, width=6, font="Helvetica 13")
        self.verify_button.grid(row=3, column=2, padx=(0, 3), rowspan=2, sticky=E)
        self.upload_to_github = Checkbutton(self.frame, text="Upload to Github", variable=self.upload,
                                       command=self.upload_choice, font="Helvetica 16")
        self.upload_to_github.grid(row=2, column=1, pady=(0, 0), sticky=N)
        self.open = IntVar(value=1)
        self.open_project = Checkbutton(self.frame, text="Open Project", variable=self.open,
                                   font="Helvetica 16")
        self.open_project.grid(row=9, column=1, sticky=N)
        self.cancel_button = Button(
            self.frame, text="Cancel", command=self.cancel_creation, width=6, font="Helvetica 16")
        self.cancel_button.grid(row=10, column=0, pady=(0, 5), padx=(5, 0), sticky=W)
        self.create_button = Button(
            self.frame, text="Create", command=self.create_project, width=6, font="Helvetica 16")
        self.create_button.grid(row=10, column=2, pady=(0, 5), sticky=E)

        self.upload_mode = StringVar(value="PUBLIC")
        self.upload_mode_public = Radiobutton(self.frame, text="Public", value="PUBLIC", variable=self.upload_mode,
                                         font="Helvetica 14")
        self.upload_mode_public.grid(row=8, column=1, padx=(0, 100), sticky=S)
        self.upload_mode_private = Radiobutton(self.frame, text="Private", value="PRIVATE", variable=self.upload_mode,
                                          font="Helvetica 14")
        self.upload_mode_private.grid(row=8, column=1, padx=(100, 0), sticky=S)
        self.upload_choice()

    def upload_choice(self):
        if self.upload.get() == 1:
            self.verify_button.config(state=ACTIVE)
            self.username.config(state=NORMAL)
            self.username_entry.config(state=NORMAL)
            self.password.config(state=NORMAL)
            self.password_entry.config(state=NORMAL)
            self.verified_status.config(state=NORMAL)
            self.upload_mode_public.config(state=ACTIVE)
            self.upload_mode_private.config(state=ACTIVE)
            self.readme.config(state=NORMAL)
            self.readme_entry.config(state=NORMAL)
        else:
            self.verify_button.config(state=DISABLED)
            self.username.config(state=DISABLED)
            self.username_entry.config(state=DISABLED)
            self.password.config(state=DISABLED)
            self.password_entry.config(state=DISABLED)
            self.verified_status.config(state=DISABLED)
            self.upload_mode_public.config(state=DISABLED)
            self.upload_mode_private.config(state=DISABLED)
            self.readme.config(state=DISABLED)
            self.readme_entry.config(state=DISABLED)

    def browse_directory(self):
        """
        Opens a folder selection dialog to choose the save location
        """
        choice = filedialog.askdirectory(
            initialdir=os.getcwd(), title="Select the project save location")

        if choice:
            self.directory_chosen.delete(0, END)
            self.directory_chosen.insert(0, choice)

    def verify_auth(self):
        result = self.logic.login_successful(self.username_entry.get(), self.password_entry.get())
        if result:
            self.verified_status.config(text="Status: Verified")
        else:
            self.verified_status.config(text="Status: Invalid Credentials")

    def cancel_creation(self):
        self.window.destroy()

    def create_project(self):
        self.logic.setup_project(
            self.name_entry.get(),
            readme=self.readme_entry.get("1.0", END),
            mode=self.upload_mode.get(),
            upload=True if self.upload.get() == 1 else False,
            directory=self.directory_chosen.get(),
            open_project=True if self.open.get() == 1 else False
            )
        self.window.destroy()



if __name__ == "__main__":
    create = Tk()
    create.title("Project Auto-Creater")
    create.geometry("480x520")
    # create.option_add("*Font", "Helvetica 12")
    create.resizable(FALSE, FALSE)
    gui = CreateGUI(create)
    create.mainloop()
