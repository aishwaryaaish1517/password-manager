# FILE: main.py
# PURPOSE: The entire GUI (Graphical User Interface).
#          This file creates the window, all buttons, input
#          boxes, and the password table.
#          Run THIS file to start the program: python main.py

# tkinter is Python's built-in GUI library.
# It comes FREE with every Python installation — no pip needed!
# 'tk' is the main module that gives us the window and widgets.
import tkinter as tk

# 'ttk' = themed tkinter — gives us nicer-looking widgets
# like Treeview (the table), Combobox, and Notebook (tabs).
from tkinter import ttk

# 'messagebox' gives us pop-up dialog boxes:
# - messagebox.showinfo()    → shows an info popup
# - messagebox.showerror()   → shows an error popup
# - messagebox.askyesno()    → shows a yes/no question popup
from tkinter import messagebox

# Import our password management functions from manager.py
from manager import (
    add_password,
    get_all_services,
    delete_password,
    get_all_passwords_data,
    get_password
)


# ============================================================
# THE MAIN APPLICATION CLASS
# ============================================================
# A 'class' is a blueprint that bundles related data and
# functions together. Our entire app lives inside this class.
# WHY use a class? Because the GUI has many parts that need
# to talk to each other (buttons, inputs, table). A class
# keeps everything organized and connected.
# ============================================================

class PasswordManagerApp:
    """
    The main Password Manager GUI application.
    All GUI components and their logic live here.
    """

    def __init__(self, root):
        """
        __init__ is the CONSTRUCTOR — it runs automatically
        when we create the app object (at the bottom of this file).
        
        It sets up the entire window and all its components.

        Args:
            root: The main tkinter window object (Tk())
        """

        # Store the root window so other methods can use it
        self.root = root

        # Set the window title (text in the title bar)
        self.root.title("🔐 Password Manager — Python Internship Project")

        # Get the screen width and height automatically
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")

        self.root.resizable(True, True)
        self.root.state("zoomed")

        # Set the background color of the window
        # "#1a1a2e" is a dark navy blue (hex color code)
        self.root.configure(bg="#1a1a2e")

        # ---- Variables ----
        # tk.StringVar() is a special tkinter string variable.
        # WHY use StringVar instead of a normal string?
        # Because tkinter widgets (Entry boxes) can be LINKED to
        # a StringVar — when the variable changes, the widget
        # updates automatically, and vice versa.

        self.service_var  = tk.StringVar()   # For service name input
        self.username_var = tk.StringVar()   # For username input
        self.password_var = tk.StringVar()   # For password input
        self.search_var   = tk.StringVar()   # For search input
        self.show_pass    = tk.BooleanVar()  # For show/hide password checkbox

        # Track whether password is currently hidden (True = hidden)
        self.password_hidden = True

        # ---- Build the UI ----
        # We split the UI into logical methods to keep code clean.
        # Each method builds one section of the window.
        self.build_header()      # Top banner with title
        self.build_left_panel()  # Left: Add password form
        self.build_right_panel() # Right: Password table + search
        self.build_status_bar()  # Bottom: Status message bar

        # Load and display all saved passwords when app starts
        self.refresh_table()


    # ==========================================================
    # SECTION 1: HEADER
    # ==========================================================

    def build_header(self):
        """
        Builds the dark top banner with the app title and subtitle.
        """

        # tk.Frame() creates a container (box) that holds other widgets.
        # bg = background color
        # pady = padding on top and bottom (in pixels)
        header = tk.Frame(self.root, bg="#0f0f1a", pady=15)

        # pack() places the widget inside its parent.
        # fill=tk.X → stretch horizontally to fill the full width
        # side=tk.TOP → place at the top of the window
        header.pack(fill=tk.X, side=tk.TOP)

        # tk.Label() displays text (or images) on screen.
        # font=("Helvetica", 18, "bold") → font family, size, style
        # fg = foreground (text) color
        tk.Label(
            header,
            text="🔐  Password Manager",
            font=("Helvetica", 18, "bold"),
            bg="#0f0f1a",
            fg="#a29bfe"          # Light purple text
        ).pack()

        tk.Label(
            header,
            text="All passwords encrypted with AES-128 · Built with Python + tkinter",
            font=("Helvetica", 9),
            bg="#0f0f1a",
            fg="#636e72"          # Grey subtitle text
        ).pack()


    # ==========================================================
    # SECTION 2: LEFT PANEL — Add Password Form
    # ==========================================================

    def build_left_panel(self):
        """
        Builds the left side of the window containing:
        - Service name input
        - Username input
        - Password input with show/hide toggle
        - Password strength indicator
        - Save button
        - Clear button
        """

        # Create the left panel frame
        # width=320 → 320 pixels wide
        left = tk.Frame(self.root, bg="#16213e", width=320)

        # padx = horizontal padding from window edges
        # pady = vertical padding from top/bottom
        # fill=tk.Y → stretch vertically to fill window height
        # side=tk.LEFT → attach to the left side
        left.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)

        # Prevent the frame from shrinking to fit its children
        # (keeps it at exactly width=320)
        left.pack_propagate(False)

        # ---- Form Title ----
        tk.Label(
            left,
            text="Add New Password",
            font=("Helvetica", 13, "bold"),
            bg="#16213e",
            fg="#dfe6e9"
        ).pack(pady=(20, 5))

        tk.Label(
            left,
            text="Fill in the details below",
            font=("Helvetica", 9),
            bg="#16213e",
            fg="#636e72"
        ).pack(pady=(0, 15))

        # ---- Divider Line ----
        # tk.Frame with height=1 and a color acts as a horizontal line
        tk.Frame(left, bg="#2d3436", height=1).pack(fill=tk.X, padx=20)

        # ---- Helper: make a labeled input field ----
        # We define this as an inner function to avoid repeating code.
        # It creates a label + entry box as a pair.
        def make_field(parent, label_text, variable, show=""):
            """
            Creates a label + text entry field pair.

            Args:
                parent:     The frame to put it in
                label_text: The label displayed above the box
                variable:   The StringVar linked to this field
                show:       If "•", hides typed text (for passwords)

            Returns:
                tk.Entry: The input box widget (so we can customize it)
            """

            # Label above the input
            tk.Label(
                parent,
                text=label_text,
                font=("Helvetica", 10),
                bg="#16213e",
                fg="#b2bec3",
                anchor="w"          # anchor="w" = left-align text
            ).pack(fill=tk.X, padx=20, pady=(10, 2))

            # tk.Entry() is a single-line text input box.
            # textvariable links it to our StringVar.
            # show="•" makes typed text appear as dots (hidden).
            entry = tk.Entry(
                parent,
                textvariable=variable,
                font=("Helvetica", 11),
                bg="#2d3436",        # Dark grey background
                fg="#dfe6e9",        # Light text
                insertbackground="#dfe6e9",  # Cursor color
                relief="flat",       # No 3D border effect
                bd=5,                # Border width (inner padding)
                show=show            # "" = show text, "•" = hide it
            )
            entry.pack(fill=tk.X, padx=20)
            return entry

        # Create the three input fields
        make_field(left, "🌐  Service Name (e.g. gmail)", self.service_var)
        make_field(left, "👤  Username / Email",           self.username_var)

        # We store the password entry to toggle show/hide later
        self.pass_entry = make_field(
            left, "🔑  Password", self.password_var, show="•"
        )

        # ---- Show/Hide Password Checkbox ----
        # tk.Checkbutton() creates a checkbox.
        # variable=self.show_pass links to our BooleanVar.
        # command=self.toggle_password → calls toggle_password() when clicked.
        tk.Checkbutton(
            left,
            text="Show password",
            variable=self.show_pass,
            command=self.toggle_password,
            bg="#16213e",
            fg="#b2bec3",
            selectcolor="#2d3436",     # Background when checked
            activebackground="#16213e",
            font=("Helvetica", 9),
            cursor="hand2"             # Mouse cursor changes to hand on hover
        ).pack(anchor="w", padx=20, pady=(5, 0))

        # ---- Password Strength Bar ----
        # A visual indicator that changes color based on password length.
        tk.Label(
            left,
            text="Password strength:",
            font=("Helvetica", 9),
            bg="#16213e",
            fg="#636e72"
        ).pack(anchor="w", padx=20, pady=(10, 2))

        # Frame to hold the colored strength bar
        self.strength_frame = tk.Frame(left, bg="#16213e")
        self.strength_frame.pack(fill=tk.X, padx=20)

        # Canvas is like a drawing board where we can draw shapes.
        # We draw the colored rectangle inside it.
        self.strength_canvas = tk.Canvas(
            self.strength_frame,
            height=8,
            bg="#2d3436",
            highlightthickness=0    # Remove canvas border
        )
        self.strength_canvas.pack(fill=tk.X)

        # Label that shows "Weak", "Medium", "Strong"
        self.strength_label = tk.Label(
            left,
            text="",
            font=("Helvetica", 8),
            bg="#16213e",
            fg="#636e72"
        )
        self.strength_label.pack(anchor="w", padx=20)

        # Whenever the password_var changes (user types),
        # call update_strength() to refresh the strength bar.
        # trace_add("write", callback) = "watch this variable for changes"
        self.password_var.trace_add("write", self.update_strength)

        # ---- Buttons ----
        btn_frame = tk.Frame(left, bg="#16213e")
        btn_frame.pack(fill=tk.X, padx=20, pady=20)

        # Save button — calls self.save_password when clicked
        tk.Button(
            btn_frame,
            text="💾  Save Password",
            command=self.save_password,
            font=("Helvetica", 11, "bold"),
            bg="#6c5ce7",           # Purple background
            fg="white",
            activebackground="#a29bfe",
            relief="flat",
            bd=0,
            pady=8,
            cursor="hand2"
        ).pack(fill=tk.X, pady=(0, 8))

        # Clear button — calls self.clear_fields when clicked
        tk.Button(
            btn_frame,
            text="🗑  Clear Fields",
            command=self.clear_fields,
            font=("Helvetica", 10),
            bg="#2d3436",
            fg="#b2bec3",
            activebackground="#3d4446",
            relief="flat",
            bd=0,
            pady=6,
            cursor="hand2"
        ).pack(fill=tk.X)

        # ---- Stats at the bottom of left panel ----
        self.stats_label = tk.Label(
            left,
            text="",
            font=("Helvetica", 9),
            bg="#16213e",
            fg="#636e72"
        )
        self.stats_label.pack(pady=10)


    # ==========================================================
    # SECTION 3: RIGHT PANEL — Password Table
    # ==========================================================

    def build_right_panel(self):
        """
        Builds the right side of the window containing:
        - Search bar
        - Password table (Treeview)
        - Copy and Delete buttons
        """

        # Right panel frame — takes up remaining space
        right = tk.Frame(self.root, bg="#1a1a2e")

        # fill=tk.BOTH → expand in both directions
        # expand=True → take up ALL remaining space
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ---- Search Bar Row ----
        search_row = tk.Frame(right, bg="#1a1a2e")
        search_row.pack(fill=tk.X, pady=(5, 8))

        tk.Label(
            search_row,
            text="🔍 Search:",
            font=("Helvetica", 10),
            bg="#1a1a2e",
            fg="#b2bec3"
        ).pack(side=tk.LEFT)

        # Search input box
        search_entry = tk.Entry(
            search_row,
            textvariable=self.search_var,
            font=("Helvetica", 11),
            bg="#2d3436",
            fg="#dfe6e9",
            insertbackground="#dfe6e9",
            relief="flat",
            bd=5,
            width=30
        )
        search_entry.pack(side=tk.LEFT, padx=(5, 10))

        # Every time the search box changes, call search_passwords()
        self.search_var.trace_add("write", self.search_passwords)

        # ---- Password Table (Treeview) ----
        # ttk.Treeview creates a table with rows and columns.
        # It's the most powerful table widget in tkinter.

        # Style customizes how the table looks
        style = ttk.Style()

        # Configure the style for our table rows
        style.configure(
            "Custom.Treeview",
            background="#16213e",       # Row background color
            foreground="#dfe6e9",       # Row text color
            fieldbackground="#16213e",  # Empty area background
            rowheight=35,               # Height of each row in pixels
            font=("Helvetica", 10)
        )

        # Configure the column header row style
        style.configure(
            "Custom.Treeview.Heading",
            background="#0f0f1a",
            foreground="#a29bfe",
            font=("Helvetica", 10, "bold")
        )

        # Style for alternating row colors (odd/even rows)
        style.map(
            "Custom.Treeview",
            background=[("selected", "#6c5ce7")]  # Selected row = purple
        )

        # Create a frame to hold the table + scrollbar together
        table_frame = tk.Frame(right, bg="#1a1a2e")
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Create the table with these columns:
        # "columns" lists the internal column IDs
        # show="headings" hides the first invisible default column
        self.tree = ttk.Treeview(
            table_frame,
            columns=("no", "service", "username", "password", "strength"),
            show="headings",
            style="Custom.Treeview",
            selectmode="browse"   # Only one row selectable at a time
        )

        # Define each column's header text and width
        # anchor="w" = left-align, "center" = center-align
        self.tree.heading("no",       text="#",         anchor="center")
        self.tree.heading("service",  text="Service",   anchor="w")
        self.tree.heading("username", text="Username",  anchor="w")
        self.tree.heading("password", text="Password",  anchor="w")
        self.tree.heading("strength", text="Strength",  anchor="center")

        # Set column widths (in pixels)
        # minwidth = minimum it can be resized to
        # stretch=False = don't auto-stretch this column
        self.tree.column("no",       width=40,  minwidth=40,  anchor="center", stretch=False)
        self.tree.column("service",  width=140, minwidth=100, anchor="w")
        self.tree.column("username", width=180, minwidth=120, anchor="w")
        self.tree.column("password", width=150, minwidth=100, anchor="w")
        self.tree.column("strength", width=90,  minwidth=80,  anchor="center", stretch=False)

        # Vertical scrollbar for the table
        # yscrollcommand links the scrollbar to the table's Y-scroll
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Place table and scrollbar side by side
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # ---- Action Buttons Row ----
        action_row = tk.Frame(right, bg="#1a1a2e")
        action_row.pack(fill=tk.X, pady=(8, 0))

        # Copy Password button
        tk.Button(
            action_row,
            text="📋  Copy Password",
            command=self.copy_password,
            font=("Helvetica", 10),
            bg="#00b894",           # Green
            fg="white",
            activebackground="#00cec9",
            relief="flat",
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(0, 8))

        # Reveal/Hide Password button (shows plain text in table)
        tk.Button(
            action_row,
            text="👁  Reveal / Hide",
            command=self.toggle_table_password,
            font=("Helvetica", 10),
            bg="#0984e3",           # Blue
            fg="white",
            activebackground="#74b9ff",
            relief="flat",
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(0, 8))

        # Delete button
        tk.Button(
            action_row,
            text="🗑  Delete Selected",
            command=self.delete_selected,
            font=("Helvetica", 10),
            bg="#d63031",           # Red
            fg="white",
            activebackground="#e17055",
            relief="flat",
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2"
        ).pack(side=tk.LEFT)

        # Track whether passwords are currently revealed in table
        # False = hidden (show as ••••••), True = shown (plain text)
        self.passwords_revealed = False


    # ==========================================================
    # SECTION 4: STATUS BAR
    # ==========================================================

    def build_status_bar(self):
        """
        Builds the thin status bar at the very bottom of the window.
        It shows messages like "✅ Password saved!" or "❌ Error!"
        """

        # Status bar frame at the bottom
        status_bar = tk.Frame(self.root, bg="#0f0f1a", height=30)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        status_bar.pack_propagate(False)

        # Label inside the status bar
        self.status_label = tk.Label(
            status_bar,
            text="✅  Ready",
            font=("Helvetica", 9),
            bg="#0f0f1a",
            fg="#00b894",
            anchor="w",
            padx=15
        )
        self.status_label.pack(fill=tk.X, expand=True, pady=6)


    # ==========================================================
    # LOGIC METHODS — These run when buttons are clicked
    # ==========================================================

    def set_status(self, message: str, color: str = "#00b894"):
        """
        Updates the bottom status bar message.

        Args:
            message (str): Text to display
            color   (str): Text color (green by default)
        """
        self.status_label.config(text=message, fg=color)


    def get_strength(self, password: str) -> tuple:
        """
        Analyzes password and returns its strength.

        Rules:
        - Less than 6 chars → Weak
        - 6–9 chars OR only letters/numbers → Medium
        - 10+ chars AND has mixed characters → Strong

        Args:
            password (str): The password to analyze

        Returns:
            tuple: (label, color, width_fraction)
                   e.g. ("Strong", "#00b894", 1.0)
        """

        length = len(password)

        # Check if password contains special characters
        # 'any()' returns True if at least ONE character satisfies the condition
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        has_upper   = any(c.isupper() for c in password)   # Has uppercase?
        has_digit   = any(c.isdigit() for c in password)   # Has number?

        if length == 0:
            return ("", "#636e72", 0)
        elif length < 6:
            return ("⚠ Weak", "#e17055", 0.25)     # Red-orange
        elif length < 10 or not (has_special and has_upper and has_digit):
            return ("▲ Medium", "#fdcb6e", 0.6)    # Yellow
        else:
            return ("✔ Strong", "#00b894", 1.0)    # Green


    def update_strength(self, *args):
        """
        Called automatically every time the user types in the password box.
        Updates the colored strength bar and text label.

        *args: Required by tkinter trace (receives variable name, index, mode)
               We don't use them, so we just accept and ignore with *args.
        """

        password = self.password_var.get()   # Get current typed text
        label, color, fraction = self.get_strength(password)

        # Update the text label
        self.strength_label.config(text=label, fg=color)

        # Redraw the colored bar on the canvas
        # First clear everything on the canvas
        self.strength_canvas.delete("all")

        # Get the current canvas width (in pixels)
        canvas_width = self.strength_canvas.winfo_width()

        # If canvas hasn't rendered yet, default to 200px
        if canvas_width < 2:
            canvas_width = 200

        # Draw a colored rectangle.
        # Coordinates: x0=0, y0=0, x1=width*fraction, y1=8
        # fraction=0.25 → fills 25% of the bar (weak)
        # fraction=1.0  → fills 100% of the bar (strong)
        if fraction > 0:
            self.strength_canvas.create_rectangle(
                0, 0,
                canvas_width * fraction, 8,
                fill=color,
                outline=""   # No border on the rectangle
            )


    def toggle_password(self):
        """
        Toggles the password entry between shown (text) and hidden (dots).
        Called when the "Show password" checkbox is clicked.
        """

        if self.show_pass.get():
            # Checkbox is checked → show the real characters
            self.pass_entry.config(show="")
        else:
            # Checkbox is unchecked → hide with bullet dots
            self.pass_entry.config(show="•")


    def save_password(self):
        """
        Reads the form fields and saves the password.
        Called when the "Save Password" button is clicked.

        Validation:
        - All three fields must be filled
        - If service already exists, ask user to confirm overwrite
        """

        # .get() reads the current value from a StringVar
        # .strip() removes leading/trailing whitespace
        # .lower() converts to lowercase for consistency
        service  = self.service_var.get().strip().lower()
        username = self.username_var.get().strip()
        password = self.password_var.get()

        # --- Validation ---
        # Check that none of the fields are empty
        if not service:
            # messagebox.showerror() shows a red X popup with a message
            messagebox.showerror("Error", "Please enter a service name!")
            return  # Stop the function — don't save anything

        if not username:
            messagebox.showerror("Error", "Please enter a username or email!")
            return

        if not password:
            messagebox.showerror("Error", "Please enter a password!")
            return

        # Check if this service already exists
        existing = get_all_services()
        if service in existing:
            # messagebox.askyesno() shows a Yes/No popup
            # Returns True if user clicks Yes, False if No
            confirm = messagebox.askyesno(
                "Confirm Update",
                f"'{service}' already exists. Do you want to update it?"
            )
            if not confirm:
                return  # User said No — cancel the save

        # --- Save ---
        is_new = add_password(service, username, password)

        # Show success message in status bar
        action = "saved" if is_new else "updated"
        self.set_status(f"✅  Password for '{service}' {action} successfully!")

        # Clear the form fields after saving
        self.clear_fields()

        # Refresh the table to show the new entry
        self.refresh_table()


    def clear_fields(self):
        """
        Clears all three input fields and resets the strength bar.
        Called after saving, or when the Clear button is clicked.
        """

        # .set("") sets the StringVar to empty string
        # This automatically clears the linked Entry widget too
        self.service_var.set("")
        self.username_var.set("")
        self.password_var.set("")

        # Reset strength bar
        self.strength_canvas.delete("all")
        self.strength_label.config(text="")

        # Uncheck the show password checkbox
        self.show_pass.set(False)
        self.pass_entry.config(show="•")


    def refresh_table(self):
        """
        Clears and reloads the password table with all saved data.
        Called after save, delete, or app startup.
        """

        # Delete ALL existing rows from the table
        # self.tree.get_children() returns all row IDs
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Get all saved passwords as a dictionary
        all_data = get_all_passwords_data()

        # Insert each password as a row in the table
        for index, (service, info) in enumerate(all_data.items(), start=1):
            # enumerate gives us: (1, "gmail", {...}), (2, "netflix", {...})...

            username = info["username"]
            password = info["password"]

            # Determine what to show in the Password column
            # If passwords are hidden: show "••••••••"
            # If revealed: show the actual password
            display_pass = password if self.passwords_revealed else "••••••••"

            # Determine strength label for this password
            label, color, _ = self.get_strength(password)

            # tree.insert() adds a row to the table.
            # "" = parent (no parent = top-level row)
            # tk.END = insert at the end
            # values = the data for each column (must match column order)
            self.tree.insert(
                "", tk.END,
                values=(index, service.capitalize(), username, display_pass, label),
                tags=(service,)   # Tag the row with the service name
                                  # so we can find it later
            )

        # Update the stats label in the left panel
        count = len(all_data)
        self.stats_label.config(
            text=f"📦  {count} password{'s' if count != 1 else ''} stored"
        )


    def search_passwords(self, *args):
        """
        Filters the table rows based on the search text.
        Called automatically every time the search box changes.
        Shows only rows where service or username contains the search term.
        """

        # Get search text, lowercased for case-insensitive matching
        query = self.search_var.get().strip().lower()

        # Get all saved data
        all_data = get_all_passwords_data()

        # Clear the table
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Re-insert only matching rows
        index = 1
        for service, info in all_data.items():
            username = info["username"]
            password = info["password"]

            # 'in' checks if query appears inside the string
            # e.g. "gma" in "gmail" → True
            if query in service.lower() or query in username.lower():
                display_pass = password if self.passwords_revealed else "••••••••"
                label, _, _ = self.get_strength(password)

                self.tree.insert(
                    "", tk.END,
                    values=(index, service.capitalize(), username, display_pass, label),
                    tags=(service,)
                )
                index += 1


    def toggle_table_password(self):
        """
        Toggles all password cells in the table between
        hidden (••••••••) and revealed (plain text).
        Called when the "Reveal / Hide" button is clicked.
        """

        # Flip the boolean: True → False, False → True
        self.passwords_revealed = not self.passwords_revealed

        # Refresh the table (which reads self.passwords_revealed
        # to decide whether to show real passwords or dots)
        self.refresh_table()

        # Update status bar
        if self.passwords_revealed:
            self.set_status("👁  Passwords revealed — be careful!", "#fdcb6e")
        else:
            self.set_status("🔒  Passwords hidden", "#00b894")


    def copy_password(self):
        """
        Copies the selected row's REAL password to clipboard.
        Called when the "Copy Password" button is clicked.
        """

        # Get the currently selected row's ID
        selected = self.tree.selection()

        # If nothing is selected, show a warning
        if not selected:
            messagebox.showwarning("No Selection", "Please click on a row first!")
            return

        # Get the values from the selected row
        # tree.item(row_id, "values") returns a tuple of the column values
        values = self.tree.item(selected[0], "values")

        # values[1] is the service name (column index 1)
        # .lower() because we stored all services in lowercase
        service = values[1].lower()

        # Get the REAL password from our data (not the "••••••••" display)
        data = get_password(service)

        if data:
            real_password = data["password"]

            # clipboard_clear() removes anything on the clipboard
            self.root.clipboard_clear()

            # clipboard_append() puts text onto the system clipboard
            # Now the user can paste it anywhere with Ctrl+V
            self.root.clipboard_append(real_password)

            self.set_status(f"📋  Password for '{service}' copied to clipboard!")
        else:
            self.set_status("❌  Could not retrieve password.", "#e17055")


    def delete_selected(self):
        """
        Deletes the currently selected row from the table and from storage.
        Called when the "Delete Selected" button is clicked.
        """

        # Get selected row
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("No Selection", "Please click on a row to select it first!")
            return

        # Get the service name from the selected row
        values = self.tree.item(selected[0], "values")
        service = values[1].lower()

        # Show confirmation dialog before deleting
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete the password for '{service}'?\n\nThis cannot be undone!"
        )

        if confirm:
            success = delete_password(service)

            if success:
                self.set_status(f"🗑  Password for '{service}' deleted.", "#e17055")
                self.refresh_table()   # Refresh to remove the row visually
            else:
                self.set_status("❌  Delete failed.", "#e17055")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================
# This block runs ONLY when you execute: python main.py
# It does NOT run if another file imports main.py
# ============================================================

if __name__ == "__main__":

    # tk.Tk() creates the main application window.
    # Every tkinter app needs exactly ONE Tk() window.
    root = tk.Tk()

    # Create our app object.
    # This calls __init__(root) which builds the entire GUI.
    app = PasswordManagerApp(root)

    # root.mainloop() starts the GUI event loop.
    # WHY? tkinter needs to constantly listen for events:
    # - Did the user click a button?
    # - Did they type something?
    # - Did they close the window?
    # mainloop() handles ALL of this automatically.
    # The program stays open until the window is closed.
    root.mainloop()
