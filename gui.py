import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime
import sys
import calendar
from tkcalendar import DateEntry  # You might need to install this: pip install tkcalendar

# Add the directory containing the event_management_system.py to Python's path
# so we can import the code from it
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the event management system
from main import User, Admin, Organizer, RegularUser, Event, DataStorage, UserManager, EventManager, EventManagementSystem

class LoginFrame(tk.Frame):
    def __init__(self, master, on_login, on_register):
        super().__init__(master)
        self.master = master
        self.on_login = on_login
        self.on_register = on_register
        
        # Configure the frame with gradient-like background
        self.configure(bg="#e6f2ff", padx=550, pady=200)
        
        # Create widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Create a decorative top banner
        banner_frame = tk.Frame(self, bg="#4a86e8", padx=30, pady=20)
        banner_frame.grid(row=0, column=0, sticky="ew", pady=(0, 25))
        
        # Center the title with shadow effect
        title_frame = tk.Frame(banner_frame, bg="#4a86e8")
        title_frame.pack(fill="x")
        
        # Shadow label (slightly offset)
        ttk.Label(title_frame, text="Event Management System", 
                 font=("Arial", 22, "bold"), foreground="#2a5698",
                 background="#4a86e8").pack(anchor="center")
        
        # Main title label
        ttk.Label(title_frame, text="Event Management System", 
                 font=("Arial", 22, "bold"), foreground="white",
                 background="#4a86e8").place(relx=0.5, rely=0.5, anchor="center")
        
        # Create a rounded content frame
        content_frame = tk.Frame(self, bg="white", padx=40, pady=30,
                               highlightbackground="#c9daf8", 
                               highlightthickness=2)
        content_frame.grid(row=1, column=0, pady=10)
        
        # Username with centered elements
        username_frame = tk.Frame(content_frame, bg="white")
        username_frame.pack(fill="x", pady=12)
        ttk.Label(username_frame, text="Username", font=("Arial", 12),
                 background="white").pack(anchor="center")
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(username_frame, textvariable=self.username_var, 
                                  width=36, font=("Arial", 11))
        username_entry.pack(anchor="center", pady=(5, 0))
        username_entry.bind("<Return>", lambda event: self.login())
        
        # Password with centered elements
        password_frame = tk.Frame(content_frame, bg="white")
        password_frame.pack(fill="x", pady=12)
        ttk.Label(password_frame, text="Password", font=("Arial", 12),
                 background="white").pack(anchor="center")
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(password_frame, textvariable=self.password_var, 
                                  show="•", width=36, font=("Arial", 11))
        password_entry.pack(anchor="center", pady=(5, 0))
        password_entry.bind("<Return>", lambda event: self.login())
        
        # Create a stylish button frame
        button_frame = tk.Frame(content_frame, bg="white", pady=15)
        button_frame.pack(fill="x")
        
        # Center the buttons in their container
        btn_container = tk.Frame(button_frame, bg="white")
        btn_container.pack(anchor="center")
        
        # Create custom button styles
        style = ttk.Style()
        style.configure("Login.TButton", font=("Arial", 12, "bold"))
        style.configure("Register.TButton", font=("Arial", 12))
        style.map("Login.TButton",
                 foreground=[('pressed', 'white'), ('active', 'white')],
                 background=[('pressed', '!disabled', '#3a7ca5'), ('active', '#4a86e8')])
        
        # Login Button with improved styling
        login_btn = ttk.Button(btn_container, text="LOGIN", style="Login.TButton", 
                             command=self.login, width=15)
        login_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Register Button with improved styling
        register_btn = ttk.Button(btn_container, text="REGISTER", style="Register.TButton", 
                                command=self.show_register, width=15)
        register_btn.pack(side=tk.LEFT)
        
        # Add a decorative footer
        footer_frame = tk.Frame(self, bg="#e6f2ff", pady=10)
        footer_frame.grid(row=2, column=0, sticky="ew")
        ttk.Label(footer_frame, text="© 2025 Event Management System", 
                 foreground="#555555", background="#e6f2ff",
                 font=("Arial", 9)).pack(anchor="center")
    
    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        self.on_login(username, password)
    
    def show_register(self):
        self.on_register()


class RegisterFrame(tk.Frame):
    def __init__(self, master, on_register, on_back):
        super().__init__(master)
        self.master = master
        self.on_register = on_register
        self.on_back = on_back
        
        # Configure the frame with matching style
        self.configure(bg="#e6f2ff", padx=550, pady=280)
        
        # Create widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Create a decorative top banner
        banner_frame = tk.Frame(self, bg="#4a86e8", padx=30, pady=20)
        banner_frame.grid(row=0, column=0, sticky="ew", pady=(0, 25))
        
        # Center the title with shadow effect
        title_frame = tk.Frame(banner_frame, bg="#4a86e8")
        title_frame.pack(fill="x")
        
        # Shadow label (slightly offset)
        ttk.Label(title_frame, text="Register New User", 
                 font=("Arial", 22, "bold"), foreground="#2a5698",
                 background="#4a86e8").pack(anchor="center")
        
        # Main title label
        ttk.Label(title_frame, text="Register New User", 
                 font=("Arial", 22, "bold"), foreground="white",
                 background="#4a86e8").place(relx=0.5, rely=0.5, anchor="center")
        
        # Create a rounded content frame
        content_frame = tk.Frame(self, bg="white", padx=40, pady=30,
                               highlightbackground="#c9daf8", 
                               highlightthickness=2)
        content_frame.grid(row=1, column=0, pady=10)
        
        # Username with centered elements
        username_frame = tk.Frame(content_frame, bg="white")
        username_frame.pack(fill="x", pady=10)
        ttk.Label(username_frame, text="Username", font=("Arial", 12),
                 background="white").pack(anchor="center")
        self.username_var = tk.StringVar()
        ttk.Entry(username_frame, textvariable=self.username_var, 
                 width=36, font=("Arial", 11)).pack(anchor="center", pady=(5, 0))
        
        # Password with centered elements
        password_frame = tk.Frame(content_frame, bg="white")
        password_frame.pack(fill="x", pady=10)
        ttk.Label(password_frame, text="Password", font=("Arial", 12),
                 background="white").pack(anchor="center")
        self.password_var = tk.StringVar()
        ttk.Entry(password_frame, textvariable=self.password_var, 
                 show="•", width=36, font=("Arial", 11)).pack(anchor="center", pady=(5, 0))
        
        # Email with centered elements
        email_frame = tk.Frame(content_frame, bg="white")
        email_frame.pack(fill="x", pady=10)
        ttk.Label(email_frame, text="Email", font=("Arial", 12),
                 background="white").pack(anchor="center")
        self.email_var = tk.StringVar()
        ttk.Entry(email_frame, textvariable=self.email_var, 
                 width=36, font=("Arial", 11)).pack(anchor="center", pady=(5, 0))
        
        # Role selection with better styling and centered
        role_frame = tk.Frame(content_frame, bg="white")
        role_frame.pack(fill="x", pady=10)
        ttk.Label(role_frame, text="Select Your Role", font=("Arial", 12),
                 background="white").pack(anchor="center", pady=(0, 5))
        
        # Center the radio buttons
        role_options_frame = tk.Frame(role_frame, bg="white")
        role_options_frame.pack(anchor="center")
        
        self.role_var = tk.StringVar(value="user")
        
        # Styled radio buttons
        style = ttk.Style()
        style.configure("TRadiobutton", background="white", font=("Arial", 11))
        
        ttk.Radiobutton(role_options_frame, text="Regular User", variable=self.role_var, 
                      value="user", style="TRadiobutton").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(role_options_frame, text="Event Organizer", variable=self.role_var, 
                      value="organizer", style="TRadiobutton").pack(side=tk.LEFT)
        
        # Button frame
        button_frame = tk.Frame(content_frame, bg="white", pady=15)
        button_frame.pack(fill="x")
        
        # Center the buttons in their container
        btn_container = tk.Frame(button_frame, bg="white")
        btn_container.pack(anchor="center")
        
        # Create custom button styles
        style = ttk.Style()
        style.configure("Register.TButton", font=("Arial", 12, "bold"))
        style.configure("Back.TButton", font=("Arial", 12))
        style.map("Register.TButton",
                 foreground=[('pressed', 'white'), ('active', 'white')],
                 background=[('pressed', '!disabled', '#3a7ca5'), ('active', '#4a86e8')])
        
        # Register Button with improved styling
        register_btn = ttk.Button(btn_container, text="CREATE ACCOUNT", style="Register.TButton",
                                command=self.register, width=18)
        register_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Back Button with improved styling
        back_btn = ttk.Button(btn_container, text="BACK TO LOGIN", style="Back.TButton",
                             command=self.on_back, width=18)
        back_btn.pack(side=tk.LEFT)
        
        # Add a decorative footer
        footer_frame = tk.Frame(self, bg="#e6f2ff", pady=10)
        footer_frame.grid(row=2, column=0, sticky="ew")
        ttk.Label(footer_frame, text="© 2025 Event Management System", 
                 foreground="#555555", background="#e6f2ff",
                 font=("Arial", 9)).pack(anchor="center")
    
    def register(self):
        username = self.username_var.get()
        password = self.password_var.get()
        email = self.email_var.get()
        role = self.role_var.get()
        
        if not username or not password or not email:
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        self.on_register(username, password, email, role)

class UserDashboard(tk.Frame):
    def __init__(self, master, system, user_id, role, on_logout):
        super().__init__(master)
        self.master = master
        self.system = system
        self.user_id = user_id
        self.role = role
        self.on_logout = on_logout
        
        # Configure the frame
        self.configure(padx=10, pady=10)
        
        # Create widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs based on role
        self.create_common_tabs()
        
        if self.role == "admin":
            self.create_admin_tabs()
        elif self.role == "organizer":
            self.create_organizer_tabs()
        elif self.role == "user":
            self.create_user_tabs()
        
        # Logout Button
        ttk.Button(self, text="Logout", command=self.on_logout).pack(pady=10)
    
    def create_common_tabs(self):
        # Available Events Tab
        self.events_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.events_tab, text="Available Events")
        
        # Create a frame for filters
        filter_frame = ttk.Frame(self.events_tab)
        filter_frame.pack(fill='x', pady=5)
        
        # Category filter
        ttk.Label(filter_frame, text="Category:").pack(side=tk.LEFT, padx=5)
        self.category_var = tk.StringVar()
        categories = ["All", "Technology", "Music", "Art", "Sports", "Education", "Other"]
        ttk.Combobox(filter_frame, textvariable=self.category_var, values=categories, state="readonly").pack(side=tk.LEFT, padx=5)
        self.category_var.set("All")
        
        # Date sort checkbox
        self.date_sort_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(filter_frame, text="Sort by date", variable=self.date_sort_var).pack(side=tk.LEFT, padx=5)
        
        # Apply filter button
        ttk.Button(filter_frame, text="Apply Filters", command=self.load_events).pack(side=tk.LEFT, padx=5)
        
        # Create the treeview
        self.events_tree = ttk.Treeview(self.events_tab, columns=("Title", "Date", "Venue", "Category", "Available"))
        self.events_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configure the treeview
        self.events_tree.heading("#0", text="ID")
        self.events_tree.heading("Title", text="Title")
        self.events_tree.heading("Date", text="Date")
        self.events_tree.heading("Venue", text="Venue")
        self.events_tree.heading("Category", text="Category")
        self.events_tree.heading("Available", text="Available Seats")
        
        self.events_tree.column("#0", width=50, stretch=tk.NO)
        self.events_tree.column("Title", width=200, stretch=tk.YES)
        self.events_tree.column("Date", width=150, stretch=tk.NO)
        self.events_tree.column("Venue", width=150, stretch=tk.YES)
        self.events_tree.column("Category", width=100, stretch=tk.NO)
        self.events_tree.column("Available", width=100, stretch=tk.NO)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.events_tab, orient="vertical", command=self.events_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        self.events_tree.configure(yscrollcommand=scrollbar.set)
        
        # Add a button frame
        button_frame = ttk.Frame(self.events_tab)
        button_frame.pack(fill='x', pady=5)
        
        # View details button
        ttk.Button(button_frame, text="View Details", command=self.view_event_details).pack(side=tk.LEFT, padx=5)
        
        # Register/unregister button (only for regular users)
        if self.role == "user":
            ttk.Button(button_frame, text="Register for Event", command=self.register_for_event).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Unregister from Event", command=self.unregister_from_event).pack(side=tk.LEFT, padx=5)
        
        # Load events
        self.load_events()
    
    def create_admin_tabs(self):
    # Apply a theme for better appearance
        style = ttk.Style()
        
        # Configure colors for UI elements
        bg_color = "#f5f7fa"  # Light blue-gray background
        header_bg = "#4a6fa5"  # Darker blue for headers
        header_fg = "#ffffff"  # White text for headers
        btn_color = "#000"  # Blue for buttons
        
        # Configure styles
        style.configure("Treeview", rowheight=25, font=('Helvetica', 10), background=bg_color, fieldbackground=bg_color)
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'), background=header_bg, foreground=header_fg)
        style.map('Treeview', background=[('selected', '#007bff')], foreground=[('selected', 'white')])
        
        # Configure TFrame with background color
        style.configure("MainFrame.TFrame", background=bg_color)
        style.configure("Header.TFrame", background=header_bg)
        style.configure("Header.TLabel", background=header_bg, foreground=header_fg, font=('Helvetica', 12, 'bold'))
        style.configure("TButton", background=btn_color)
        
        # Users Management Tab
        users_tab = ttk.Frame(self.notebook, padding=10, style="MainFrame.TFrame")
        self.notebook.add(users_tab, text="Manage Users")
        
        # Title section with colored background
        header_frame = ttk.Frame(users_tab, style="Header.TFrame")
        header_frame.pack(fill='x', pady=(0, 10))
        ttk.Label(header_frame, text="User Management", style="Header.TLabel", padding=5).pack(anchor='w')
        
        # Create frame for treeview and scrollbar
        tree_frame = ttk.Frame(users_tab, style="MainFrame.TFrame")
        tree_frame.pack(fill='both', expand=True)
        
        # Create the treeview
        self.users_tree = ttk.Treeview(tree_frame, columns=("Username", "Email", "Role", "Status"))
        
        # Configure the treeview
        self.users_tree.heading("#0", text="ID")
        self.users_tree.heading("Username", text="Username")
        self.users_tree.heading("Email", text="Email")
        self.users_tree.heading("Role", text="Role")
        self.users_tree.heading("Status", text="Status")
        
        self.users_tree.column("#0", width=50, stretch=tk.NO)
        self.users_tree.column("Username", width=150, stretch=tk.YES)
        self.users_tree.column("Email", width=200, stretch=tk.YES)
        self.users_tree.column("Role", width=100, stretch=tk.NO)
        self.users_tree.column("Status", width=100, stretch=tk.NO)
        
        # Apply alternating row colors (zebra stripes)
        self.users_tree.tag_configure('odd', background='#e6eef7')
        self.users_tree.tag_configure('even', background='#ffffff')
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.users_tree.yview)
        x_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.users_tree.xview)
        
        # Configure the treeview to use the scrollbars
        self.users_tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Pack the treeview and scrollbars
        y_scrollbar.pack(side=tk.RIGHT, fill='y')
        x_scrollbar.pack(side=tk.BOTTOM, fill='x')
        self.users_tree.pack(side=tk.LEFT, fill='both', expand=True)
        
        # Add a button frame with padding and background
        button_frame = ttk.Frame(users_tab, style="MainFrame.TFrame")
        button_frame.pack(fill='x', pady=10)
        
        # Define button style
        style.configure("Action.TButton", background="black", foreground="white", font=('Helvetica', 10))
        
        # Add buttons with consistent styling
        style.configure("BlackButton.TButton", background="black", foreground="black", font=('Helvetica', 10))
        ttk.Button(button_frame, text="Delete User", command=self.delete_user, width=15, style="BlackButton.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.load_users, width=15, style="BlackButton.TButton").pack(side=tk.LEFT, padx=5)
        # Override load_users to apply row tags
        original_load_users = self.load_users
        def styled_load_users(*args, **kwargs):
            original_load_users(*args, **kwargs)
            # Apply tags to rows
            for i, item in enumerate(self.users_tree.get_children()):
                tag = 'even' if i % 2 == 0 else 'odd'
                self.users_tree.item(item, tags=(tag,))
        
        self.load_users = styled_load_users
        
        # Load users
        self.load_users()
        
        # Event Approval Tab
        approval_tab = ttk.Frame(self.notebook, padding=10, style="MainFrame.TFrame")
        self.notebook.add(approval_tab, text="Event Approvals")
        
        # Title section with colored background
        approval_header_frame = ttk.Frame(approval_tab, style="Header.TFrame")
        approval_header_frame.pack(fill='x', pady=(0, 10))
        ttk.Label(approval_header_frame, text="Event Approval Queue", style="Header.TLabel", padding=5).pack(anchor='w')
        
        # Create frame for approval treeview and scrollbar
        approval_tree_frame = ttk.Frame(approval_tab, style="MainFrame.TFrame")
        approval_tree_frame.pack(fill='both', expand=True)
        
        # Create the treeview
        self.approval_tree = ttk.Treeview(approval_tree_frame, columns=("Title", "Organizer", "Date", "Category"))
        
        # Configure the treeview
        self.approval_tree.heading("#0", text="ID")
        self.approval_tree.heading("Title", text="Title")
        self.approval_tree.heading("Organizer", text="Organizer")
        self.approval_tree.heading("Date", text="Date")
        self.approval_tree.heading("Category", text="Category")
        
        self.approval_tree.column("#0", width=50, stretch=tk.NO)
        self.approval_tree.column("Title", width=200, stretch=tk.YES)
        self.approval_tree.column("Organizer", width=150, stretch=tk.YES)
        self.approval_tree.column("Date", width=150, stretch=tk.NO)
        self.approval_tree.column("Category", width=100, stretch=tk.NO)
        
        # Apply alternating row colors (zebra stripes)
        self.approval_tree.tag_configure('odd', background='#e6eef7')
        self.approval_tree.tag_configure('even', background='#ffffff')
        
        # Add scrollbars
        approval_y_scrollbar = ttk.Scrollbar(approval_tree_frame, orient="vertical", command=self.approval_tree.yview)
        approval_x_scrollbar = ttk.Scrollbar(approval_tree_frame, orient="horizontal", command=self.approval_tree.xview)
        
        # Configure the treeview to use the scrollbars
        self.approval_tree.configure(yscrollcommand=approval_y_scrollbar.set, xscrollcommand=approval_x_scrollbar.set)
        
        # Pack the treeview and scrollbars
        approval_y_scrollbar.pack(side=tk.RIGHT, fill='y')
        approval_x_scrollbar.pack(side=tk.BOTTOM, fill='x')
        self.approval_tree.pack(side=tk.LEFT, fill='both', expand=True)
        
        # Add a button frame with padding and background
        approval_button_frame = ttk.Frame(approval_tab, style="MainFrame.TFrame")
        approval_button_frame.pack(fill='x', pady=10)
        
        # Add buttons with consistent styling
        style.configure("BlackButton.TButton", background="black", foreground="black", font=('Helvetica', 10))
        
        ttk.Button(approval_button_frame, text="Approve Event", command=self.approve_event, width=15, style="BlackButton.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(approval_button_frame, text="View Details", command=self.view_approval_details, width=15, style="BlackButton.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(approval_button_frame, text="Refresh", command=self.load_unapproved_events, width=15, style="BlackButton.TButton").pack(side=tk.LEFT, padx=5)
        
        # Override load_unapproved_events to apply row tags
        original_load_events = self.load_unapproved_events
        def styled_load_events(*args, **kwargs):
            original_load_events(*args, **kwargs)
            # Apply tags to rows
            for i, item in enumerate(self.approval_tree.get_children()):
                tag = 'even' if i % 2 == 0 else 'odd'
                self.approval_tree.item(item, tags=(tag,))
        
        self.load_unapproved_events = styled_load_events
        
        # Load unapproved events
        self.load_unapproved_events()
    
    def create_organizer_tabs(self):
        # My Events Tab
        my_events_tab = ttk.Frame(self.notebook)
        self.notebook.add(my_events_tab, text="My Events")
        
        # Create the treeview
        self.my_events_tree = ttk.Treeview(my_events_tab, columns=("Title", "Date", "Status", "Registered"))
        self.my_events_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configure the treeview
        self.my_events_tree.heading("#0", text="ID")
        self.my_events_tree.heading("Title", text="Title")
        self.my_events_tree.heading("Date", text="Date")
        self.my_events_tree.heading("Status", text="Status")
        self.my_events_tree.heading("Registered", text="Registered Users")
        
        self.my_events_tree.column("#0", width=50, stretch=tk.NO)
        self.my_events_tree.column("Title", width=200, stretch=tk.YES)
        self.my_events_tree.column("Date", width=150, stretch=tk.NO)
        self.my_events_tree.column("Status", width=100, stretch=tk.NO)
        self.my_events_tree.column("Registered", width=120, stretch=tk.NO)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(my_events_tab, orient="vertical", command=self.my_events_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        self.my_events_tree.configure(yscrollcommand=scrollbar.set)
        
        # Add a button frame
        button_frame = ttk.Frame(my_events_tab)
        button_frame.pack(fill='x', pady=5)
        
        # Add buttons
        ttk.Button(button_frame, text="Create New Event", command=self.create_event).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Event", command=self.edit_event).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="View Details", command=self.view_my_event_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="View Registrations", command=self.view_registrations).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.load_my_events).pack(side=tk.LEFT, padx=5)
        
        # Load my events
        self.load_my_events()
    
    def create_user_tabs(self):
        # My Registrations Tab
        registrations_tab = ttk.Frame(self.notebook)
        self.notebook.add(registrations_tab, text="My Registrations")
        
        # Create the treeview
        self.registrations_tree = ttk.Treeview(registrations_tab, columns=("Title", "Date", "Venue", "Category"))
        self.registrations_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configure the treeview
        self.registrations_tree.heading("#0", text="ID")
        self.registrations_tree.heading("Title", text="Title")
        self.registrations_tree.heading("Date", text="Date")
        self.registrations_tree.heading("Venue", text="Venue")
        self.registrations_tree.heading("Category", text="Category")
        
        self.registrations_tree.column("#0", width=50, stretch=tk.NO)
        self.registrations_tree.column("Title", width=200, stretch=tk.YES)
        self.registrations_tree.column("Date", width=150, stretch=tk.NO)
        self.registrations_tree.column("Venue", width=150, stretch=tk.YES)
        self.registrations_tree.column("Category", width=100, stretch=tk.NO)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(registrations_tab, orient="vertical", command=self.registrations_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        self.registrations_tree.configure(yscrollcommand=scrollbar.set)
        
        # Add a button frame
        button_frame = ttk.Frame(registrations_tab)
        button_frame.pack(fill='x', pady=5)
        
        # Add buttons
        ttk.Button(button_frame, text="View Details", command=self.view_registration_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Unregister", command=self.unregister_from_registration).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.load_registrations).pack(side=tk.LEFT, padx=5)
        
        # Load registrations
        self.load_registrations()
    
    def load_events(self):
        # Clear existing items
        self.events_tree.delete(*self.events_tree.get_children())
        
        # Get selected category
        category = self.category_var.get()
        if category == "All":
            category = None
        
        # Get sort preference
        sort_by_date = self.date_sort_var.get()
        
        # Get events from the system
        events = self.system.get_available_events(category=category, sort_by_date=sort_by_date)
        
        # Populate the treeview
        for event_id, event in events.items():
            seats = event.seats_available()
            date_str = event.date.strftime("%Y-%m-%d %H:%M")
            
            self.events_tree.insert("", "end", event_id, text=event_id[:8],
                                   values=(event.title, date_str, event.venue, 
                                           event.category, f"{seats}/{event.capacity}"))
    
    def load_users(self):
        # Clear existing items
        self.users_tree.delete(*self.users_tree.get_children())
        
        # Get users from the system
        users = self.system.user_manager.get_all_users()
        
        # Populate the treeview
        for user_id, user in users.items():
            status = "Active" if user.is_active else "Inactive"
            
            self.users_tree.insert("", "end", user_id, text=user_id[:8],
                                  values=(user.username, user.email, user.get_role(), status))
    
    def load_unapproved_events(self):
        # Clear existing items
        self.approval_tree.delete(*self.approval_tree.get_children())
        
        # Get unapproved events from the system
        events = self.system.event_manager.get_unapproved_events()
        
        # Populate the treeview
        for event_id, event in events.items():
            date_str = event.date.strftime("%Y-%m-%d %H:%M")
            
            # Get organizer info
            organizer = self.system.user_manager.get_user(event.organizer_id)
            organizer_name = organizer.username if organizer else "Unknown"
            
            self.approval_tree.insert("", "end", event_id, text=event_id[:8],
                                     values=(event.title, organizer_name, date_str, event.category))
    
    def load_my_events(self):
        # Clear existing items
        self.my_events_tree.delete(*self.my_events_tree.get_children())
        
        # Get organizer's events from the system
        events = self.system.get_user_events(self.user_id)
        
        # Populate the treeview
        for event_id, event in events.items():
            date_str = event.date.strftime("%Y-%m-%d %H:%M")
            status = "Approved" if event.is_approved else "Pending"
            registered = len(event.registered_users)
            
            self.my_events_tree.insert("", "end", event_id, text=event_id[:8],
                                      values=(event.title, date_str, status, 
                                              f"{registered}/{event.capacity}"))
    
    def load_registrations(self):
        # Clear existing items
        self.registrations_tree.delete(*self.registrations_tree.get_children())
        
        # Get user's registered events
        registration_ids = self.system.get_user_registrations(self.user_id)
        
        # Populate the treeview
        for event_id in registration_ids:
            event = self.system.event_manager.get_event(event_id)
            if event and event.is_approved:
                date_str = event.date.strftime("%Y-%m-%d %H:%M")
                
                self.registrations_tree.insert("", "end", event_id, text=event_id[:8],
                                              values=(event.title, date_str, event.venue, event.category))
    
    def view_event_details(self):
        selected_item = self.events_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select an event to view")
            return
        
        event_id = selected_item[0]
        event = self.system.event_manager.get_event(event_id)
        
        if event:
            details = f"Title: {event.title}\n\n"
            details += f"Description: {event.description}\n\n"
            details += f"Date: {event.date.strftime('%Y-%m-%d %H:%M')}\n\n"
            details += f"Venue: {event.venue}\n\n"
            details += f"Category: {event.category}\n\n"
            details += f"Available Seats: {event.seats_available()}/{event.capacity}"
            
            # Create a details window
            details_window = tk.Toplevel(self.master)
            details_window.title(f"Event Details: {event.title}")
            details_window.geometry("400x400")
            
            # Make the window modal
            details_window.transient(self.master)
            details_window.grab_set()
            
            # Add a text widget to display details
            text_widget = tk.Text(details_window, wrap="word", padx=10, pady=10)
            text_widget.insert("1.0", details)
            text_widget.config(state="disabled")
            text_widget.pack(fill="both", expand=True)
            
            # Add a close button
            ttk.Button(details_window, text="Close", command=details_window.destroy).pack(pady=10)
    
    def register_for_event(self):
        selected_item = self.events_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select an event to register for")
            return
        
        event_id = selected_item[0]
        
        # Check if the user is already registered
        user = self.system.user_manager.get_user(self.user_id)
        if isinstance(user, RegularUser) and event_id in user.registered_events:
            messagebox.showinfo("Info", "You are already registered for this event")
            return
        
        # Register for the event
        success = self.system.register_for_event(event_id, self.user_id)
        
        if success:
            messagebox.showinfo("Success", "Registration successful")
            # Refresh events and registrations
            self.load_events()
            if hasattr(self, 'load_registrations'):
                self.load_registrations()
        else:
            messagebox.showerror("Error", "Registration failed. The event might be full.")
    
    def unregister_from_event(self):
        selected_item = self.events_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select an event to unregister from")
            return
        
        event_id = selected_item[0]
        
        # Check if the user is registered
        user = self.system.user_manager.get_user(self.user_id)
        if not isinstance(user, RegularUser) or event_id not in user.registered_events:
            messagebox.showinfo("Info", "You are not registered for this event")
            return
        
        # Unregister from the event
        success = self.system.unregister_from_event(event_id, self.user_id)
        
        if success:
            messagebox.showinfo("Success", "Unregistration successful")
            # Refresh events and registrations
            self.load_events()
            if hasattr(self, 'load_registrations'):
                self.load_registrations()
        else:
            messagebox.showerror("Error", "Unregistration failed")
    
    def delete_user(self):
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a user to delete")
            return
        
        user_id = selected_item[0]
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this user?")
        
        if confirm:
            success, msg = self.system.delete_user(user_id, self.user_id)
            
            if success:
                messagebox.showinfo("Success", msg)
                # Refresh users list
                self.load_users()
                # Also refresh events as they might have changed
                self.load_events()
                if hasattr(self, 'load_unapproved_events'):
                    self.load_unapproved_events()
            else:
                messagebox.showerror("Error", msg)
    
    def approve_event(self):
        selected_item = self.approval_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select an event to approve")
            return
        
        event_id = selected_item[0]
        
        # Approve the event
        success = self.system.approve_event(event_id, self.user_id)
        
        if success:
            messagebox.showinfo("Success", "Event approved successfully")
            # Refresh unapproved events and available events
            self.load_unapproved_events()
            self.load_events()
        else:
            messagebox.showerror("Error", "Event approval failed")
    
    def view_approval_details(self):
        selected_item = self.approval_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select an event to view")
            return
        
        event_id = selected_item[0]
        event = self.system.event_manager.get_event(event_id)
        
        if event:
            # Get organizer info
            organizer = self.system.user_manager.get_user(event.organizer_id)
            organizer_name = organizer.username if organizer else "Unknown"
            
            details = f"Title: {event.title}\n\n"
            details += f"Description: {event.description}\n\n"
            details += f"Date: {event.date.strftime('%Y-%m-%d %H:%M')}\n\n"
            details += f"Venue: {event.venue}\n\n"
            details += f"Category: {event.category}\n\n"
            details += f"Capacity: {event.capacity}\n\n"
            details += f"Organizer: {organizer_name}"
            
            # Create a details window
            details_window = tk.Toplevel(self.master)
            details_window.title(f"Event Details: {event.title}")
            details_window.geometry("400x400")
            
            # Make the window modal
            details_window.transient(self.master)
            details_window.grab_set()
            
            # Add a text widget to display details
            text_widget = tk.Text(details_window, wrap="word", padx=10, pady=10)
            text_widget.insert("1.0", details)
            text_widget.config(state="disabled")
            text_widget.pack(fill="both", expand=True)
            
            # Add buttons
            button_frame = ttk.Frame(details_window)
            button_frame.pack(fill='x', pady=10)
            
            ttk.Button(button_frame, text="Approve", command=lambda: [self.system.approve_event(event_id, self.user_id), details_window.destroy(), self.load_unapproved_events(), self.load_events()]).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Close", command=details_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def create_event(self):
        # Create a window for creating a new event
        create_window = tk.Toplevel(self.master)
        create_window.title("Create New Event")
        create_window.geometry("500x600")
        
        # Make the window modal
        create_window.transient(self.master)
        create_window.grab_set()
        
        # Create a form
        form_frame = ttk.Frame(create_window, padding=20)
        form_frame.pack(fill='both', expand=True)
        
        # Title
        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, sticky="w", pady=5)
        title_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=title_var, width=40).grid(row=0, column=1, sticky="w", pady=5)
        
        # Description
        ttk.Label(form_frame, text="Description:").grid(row=1, column=0, sticky="nw", pady=5)
        description_text = tk.Text(form_frame, width=40, height=5)
        description_text.grid(row=1, column=1, sticky="w", pady=5)
        
        # Date
        ttk.Label(form_frame, text="Date:").grid(row=2, column=0, sticky="w", pady=5)
        date_frame = ttk.Frame(form_frame)
        date_frame.grid(row=2, column=1, sticky="w", pady=5)
        
        # Use DateEntry for date
        date_picker = DateEntry(date_frame, width=12, background='darkblue',
                                foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        date_picker.pack(side=tk.LEFT)
        
        # Time selection
        ttk.Label(date_frame, text="  Time:").pack(side=tk.LEFT)
        hour_var = tk.StringVar(value="12")
        ttk.Combobox(date_frame, textvariable=hour_var, values=[str(i).zfill(2) for i in range(24)], 
                    width=3, state="readonly").pack(side=tk.LEFT)
        ttk.Label(date_frame, text=":").pack(side=tk.LEFT)
        minute_var = tk.StringVar(value="00")
        ttk.Combobox(date_frame, textvariable=minute_var, values=[str(i).zfill(2) for i in range(0, 60, 5)], 
                    width=3, state="readonly").pack(side=tk.LEFT)
        
        # Venue
        ttk.Label(form_frame, text="Venue:").grid(row=3, column=0, sticky="w", pady=5)
        venue_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=venue_var, width=40).grid(row=3, column=1, sticky="w", pady=5)
        
        # Capacity
        ttk.Label(form_frame, text="Capacity:").grid(row=4, column=0, sticky="w", pady=5)
        capacity_var = tk.IntVar(value=50)
        ttk.Spinbox(form_frame, from_=1, to=1000, textvariable=capacity_var, width=10).grid(row=4, column=1, sticky="w", pady=5)
        
        # Category
        ttk.Label(form_frame, text="Category:").grid(row=5, column=0, sticky="w", pady=5)
        category_var = tk.StringVar(value="Technology")
        categories = ["Technology", "Music", "Art", "Sports", "Education", "Other"]
        ttk.Combobox(form_frame, textvariable=category_var, values=categories, width=20, state="readonly").grid(row=5, column=1, sticky="w", pady=5)
        
        # Create button
        def submit_event():
            title = title_var.get()
            description = description_text.get("1.0", "end-1c")
            date_str = date_picker.get()
            hour = hour_var.get()
            minute = minute_var.get()
            venue = venue_var.get()
            capacity = capacity_var.get()
            category = category_var.get()
            
            if not title or not description or not venue:
                messagebox.showerror("Error", "Please fill all required fields")
                return
            
            # Create a datetime object
            try:
                event_date = datetime.strptime(f"{date_str} {hour}:{minute}", "%Y-%m-%d %H:%M")
                if event_date < datetime.now():
                    messagebox.showerror("Error", "Event date cannot be in the past")
                    return
            except ValueError:
                messagebox.showerror("Error", "Invalid date format")
                return
            
            # Create the event
            event_id, msg = self.system.create_event(title, description, event_date, venue, capacity, category, self.user_id)
            
            if event_id:
                messagebox.showinfo("Success", "Event created successfully")
                create_window.destroy()
                self.load_my_events()
                # If admin, also refresh unapproved events
                if hasattr(self, 'load_unapproved_events'):
                    self.load_unapproved_events()
            else:
                messagebox.showerror("Error", msg)
        
        ttk.Button(form_frame, text="Create Event", command=submit_event).grid(row=6, column=0, columnspan=2, pady=20)
    
    def view_my_event_details(self):
        selected_item = self.my_events_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select an event to view")
            return
        
        event_id = selected_item[0]
        event = self.system.event_manager.get_event(event_id)
        
        if event:
            details = f"Title: {event.title}\n\n"
            details += f"Description: {event.description}\n\n"
            details += f"Date: {event.date.strftime('%Y-%m-%d %H:%M')}\n\n"
            details += f"Venue: {event.venue}\n\n"
            details += f"Category: {event.category}\n\n"
            details += f"Capacity: {event.capacity}\n\n"
            details += f"Status: {'Approved' if event.is_approved else 'Pending Approval'}\n\n"
            details += f"Registered Users: {len(event.registered_users)}/{event.capacity}"
            
            # Create a details window
            details_window = tk.Toplevel(self.master)
            details_window.title(f"Event Details: {event.title}")
            details_window.geometry("400x400")
            
            # Make the window modal
            details_window.transient(self.master)
            details_window.grab_set()
            
            # Add a text widget to display details
            text_widget = tk.Text(details_window, wrap="word", padx=10, pady=10)
            text_widget.insert("1.0", details)
            text_widget.config(state="disabled")
            text_widget.pack(fill="both", expand=True)
            
            # Add a close button
            ttk.Button(details_window, text="Close", command=details_window.destroy).pack(pady=10)
    
    def view_registrations(self):
        selected_item = self.my_events_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select an event to view registrations")
            return
        
        event_id = selected_item[0]
        event = self.system.event_manager.get_event(event_id)
        
        if event:
            # Create a registrations window
            reg_window = tk.Toplevel(self.master)
            reg_window.title(f"Registrations for: {event.title}")
            reg_window.geometry("400x400")
            
            # Make the window modal
            reg_window.transient(self.master)
            reg_window.grab_set()
            
            # Create a treeview for users
            reg_tree = ttk.Treeview(reg_window, columns=("Username", "Email"))
            reg_tree.pack(fill='both', expand=True, padx=10, pady=10)
            
            # Configure the treeview
            reg_tree.heading("#0", text="ID")
            reg_tree.heading("Username", text="Username")
            reg_tree.heading("Email", text="Email")
            
            reg_tree.column("#0", width=50, stretch=tk.NO)
            reg_tree.column("Username", width=150, stretch=tk.YES)
            reg_tree.column("Email", width=200, stretch=tk.YES)
            
            # Add a scrollbar
            scrollbar = ttk.Scrollbar(reg_window, orient="vertical", command=reg_tree.yview)
            scrollbar.pack(side=tk.RIGHT, fill='y')
            reg_tree.configure(yscrollcommand=scrollbar.set)
            
            # Populate the treeview with registered users
            for user_id in event.registered_users:
                user = self.system.user_manager.get_user(user_id)
                if user:
                    reg_tree.insert("", "end", user_id, text=user_id[:8],
                                   values=(user.username, user.email))
            
            # Add a close button
            ttk.Button(reg_window, text="Close", command=reg_window.destroy).pack(pady=10)
    
    def view_registration_details(self):
        selected_item = self.registrations_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a registration to view")
            return
        
        event_id = selected_item[0]
        event = self.system.event_manager.get_event(event_id)
        
        if event:
            details = f"Title: {event.title}\n\n"
            details += f"Description: {event.description}\n\n"
            details += f"Date: {event.date.strftime('%Y-%m-%d %H:%M')}\n\n"
            details += f"Venue: {event.venue}\n\n"
            details += f"Category: {event.category}\n\n"
            details += f"Available Seats: {event.seats_available()}/{event.capacity}"
            
            # Create a details window
            details_window = tk.Toplevel(self.master)
            details_window.title(f"Event Details: {event.title}")
            details_window.geometry("400x400")
            
            # Make the window modal
            details_window.transient(self.master)
            details_window.grab_set()
            
            # Add a text widget to display details
            text_widget = tk.Text(details_window, wrap="word", padx=10, pady=10)
            text_widget.insert("1.0", details)
            text_widget.config(state="disabled")
            text_widget.pack(fill="both", expand=True)
            
            # Add a close button
            ttk.Button(details_window, text="Close", command=details_window.destroy).pack(pady=10)
    
    def unregister_from_registration(self):
        selected_item = self.registrations_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a registration to unregister from")
            return
        
        event_id = selected_item[0]
        
        # Confirm unregistration
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to unregister from this event?")
        
        if confirm:
            # Unregister from the event
            success = self.system.unregister_from_event(event_id, self.user_id)
            
            if success:
                messagebox.showinfo("Success", "Unregistration successful")
                # Refresh registrations and available events
                self.load_registrations()
                self.load_events()
            else:
                messagebox.showerror("Error", "Unregistration failed")
    
    def edit_event(self):
        selected_item = self.my_events_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select an event to edit")
            return
        
        event_id = selected_item[0]
        event = self.system.event_manager.get_event(event_id)
        
        if not event:
            messagebox.showerror("Error", "Event not found")
            return
            
        # Check if user is the organizer of this event
        if event.organizer_id != self.user_id:
            messagebox.showerror("Error", "You can only edit your own events")
            return
        
        # Create a window for editing the event with improved style
        edit_window = tk.Toplevel(self.master)
        edit_window.title(f"Edit Event: {event.title}")
        edit_window.geometry("550x650")
        edit_window.configure(bg="#f5f7fa")  # Light blue-gray background
        
        # Make the window modal
        edit_window.transient(self.master)
        edit_window.grab_set()
        
        # Add a header
        header_frame = tk.Frame(edit_window, bg="#4a6fa5", padx=10, pady=10)
        header_frame.pack(fill='x')
        
        header_label = tk.Label(header_frame, text=f"Edit Event: {event.title}", 
                            bg="#4a6fa5", fg="white", font=("Helvetica", 14, "bold"))
        header_label.pack(anchor="w")
        
        # Create a styled form
        form_frame = tk.Frame(edit_window, bg="#f5f7fa", padx=25, pady=20)
        form_frame.pack(fill='both', expand=True)
        
        # Custom style for labels
        label_style = {"bg": "#f5f7fa", "fg": "#333333", "font": ("Helvetica", 10, "bold")}
        entry_style = {"bg": "white", "relief": "solid", "borderwidth": 1}
        button_style = {"bg": "#5b87c7", "fg": "white", "font": ("Helvetica", 11, "bold"), 
                    "activebackground": "#3a679f", "relief": "raised", "borderwidth": 2, "cursor": "hand2"}
        
        # Title
        tk.Label(form_frame, text="Title:", **label_style).grid(row=0, column=0, sticky="w", pady=10, padx=5)
        title_var = tk.StringVar(value=event.title)
        title_entry = tk.Entry(form_frame, textvariable=title_var, width=40, **entry_style)
        title_entry.grid(row=0, column=1, sticky="w", pady=10, padx=5)
        
        # Description
        tk.Label(form_frame, text="Description:", **label_style).grid(row=1, column=0, sticky="nw", pady=10, padx=5)
        description_frame = tk.Frame(form_frame, bg="#f5f7fa")
        description_frame.grid(row=1, column=1, sticky="w", pady=10, padx=5)
        
        description_text = tk.Text(description_frame, width=40, height=5, **entry_style)
        description_text.pack(side=tk.LEFT, fill="both", expand=True)
        description_scroll = tk.Scrollbar(description_frame, command=description_text.yview)
        description_scroll.pack(side=tk.RIGHT, fill="y")
        description_text.configure(yscrollcommand=description_scroll.set)
        description_text.insert("1.0", event.description)
        
        # Date
        tk.Label(form_frame, text="Date:", **label_style).grid(row=2, column=0, sticky="w", pady=10, padx=5)
        date_frame = tk.Frame(form_frame, bg="#f5f7fa")
        date_frame.grid(row=2, column=1, sticky="w", pady=10, padx=5)
        
        # Use DateEntry for date with the current event date and better styling
        event_date = event.date
        date_picker = DateEntry(date_frame, width=12, background='#5b87c7',
                                foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd',
                                year=event_date.year, month=event_date.month, day=event_date.day)
        date_picker.pack(side=tk.LEFT)
        
        # Time selection with current event time
        tk.Label(date_frame, text="  Time:", bg="#f5f7fa").pack(side=tk.LEFT)
        hour_var = tk.StringVar(value=str(event_date.hour).zfill(2))
        ttk.Combobox(date_frame, textvariable=hour_var, values=[str(i).zfill(2) for i in range(24)], 
                    width=3, state="readonly").pack(side=tk.LEFT)
        tk.Label(date_frame, text=":", bg="#f5f7fa").pack(side=tk.LEFT)
        minute_var = tk.StringVar(value=str(event_date.minute).zfill(2))
        ttk.Combobox(date_frame, textvariable=minute_var, values=[str(i).zfill(2) for i in range(0, 60, 5)], 
                    width=3, state="readonly").pack(side=tk.LEFT)
        
        # Venue
        tk.Label(form_frame, text="Venue:", **label_style).grid(row=3, column=0, sticky="w", pady=10, padx=5)
        venue_var = tk.StringVar(value=event.venue)
        tk.Entry(form_frame, textvariable=venue_var, width=40, **entry_style).grid(row=3, column=1, sticky="w", pady=10, padx=5)
        
        # Capacity
        tk.Label(form_frame, text="Capacity:", **label_style).grid(row=4, column=0, sticky="w", pady=10, padx=5)
        capacity_frame = tk.Frame(form_frame, bg="#f5f7fa")
        capacity_frame.grid(row=4, column=1, sticky="w", pady=10, padx=5)
        
        capacity_var = tk.IntVar(value=event.capacity)
        capacity_spinner = ttk.Spinbox(capacity_frame, from_=1, to=1000, textvariable=capacity_var, width=10)
        capacity_spinner.pack(side=tk.LEFT)
        
        # Disable capacity field if there are registered users
        if len(event.registered_users) > 0:
            capacity_spinner.configure(state="disabled")
            reg_label = tk.Label(capacity_frame, 
                                text=f"({len(event.registered_users)} users registered)", 
                                bg="#f5f7fa", fg="#e74c3c")
            reg_label.pack(side=tk.LEFT, padx=10)
        
        # Category
        tk.Label(form_frame, text="Category:", **label_style).grid(row=5, column=0, sticky="w", pady=10, padx=5)
        category_var = tk.StringVar(value=event.category)
        categories = ["Technology", "Music", "Art", "Sports", "Education", "Other"]
        category_combo = ttk.Combobox(form_frame, textvariable=category_var, values=categories, width=20, state="readonly")
        category_combo.grid(row=5, column=1, sticky="w", pady=10, padx=5)
        category_combo.current(categories.index(event.category) if event.category in categories else 0)
        
        # Separator line
        separator = ttk.Separator(form_frame, orient='horizontal')
        separator.grid(row=6, column=0, columnspan=2, sticky="ew", pady=15)
        
        # Button frame
        button_frame = tk.Frame(form_frame, bg="#f5f7fa")
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)
        
        # Update button
        def update_event():
            title = title_var.get()
            description = description_text.get("1.0", "end-1c")
            date_str = date_picker.get()
            hour = hour_var.get()
            minute = minute_var.get()
            venue = venue_var.get()
            capacity = capacity_var.get()
            category = category_var.get()
            
            if not title or not description or not venue:
                messagebox.showerror("Error", "Please fill all required fields")
                return
            
            # Create a datetime object
            try:
                event_date = datetime.strptime(f"{date_str} {hour}:{minute}", "%Y-%m-%d %H:%M")
                if event_date < datetime.now():
                    messagebox.showerror("Error", "Event date cannot be in the past")
                    return
            except ValueError:
                messagebox.showerror("Error", "Invalid date format")
                return
            
            # Update the event
            success, msg = self.system.update_event(event_id, title, description, event_date, 
                                                venue, capacity, category, self.user_id)
            
            if success:
                messagebox.showinfo("Success", "Event updated successfully")
                edit_window.destroy()
                self.load_my_events()
                # If user is admin, also refresh unapproved events
                if hasattr(self, 'load_unapproved_events'):
                    self.load_unapproved_events()
                # Also refresh available events
                self.load_events()
            else:
                messagebox.showerror("Error", msg)
        
        cancel_button = tk.Button(button_frame, text="Cancel", width=15, command=edit_window.destroy, 
                                **button_style, bg="#6c757d")
        cancel_button.pack(side=tk.LEFT, padx=10)
        
        update_button = tk.Button(button_frame, text="Update Event", width=15, command=update_event, **button_style)
        update_button.pack(side=tk.LEFT, padx=10)
        
        # Add some styling to the window
        edit_window.update_idletasks()
        width = edit_window.winfo_width()
        height = edit_window.winfo_height()
        x = (edit_window.winfo_screenwidth() // 2) - (width // 2)
        y = (edit_window.winfo_screenheight() // 2) - (height // 2)
        edit_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


class EventManagementApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Event Management System")
        self.master.geometry("900x600")
        
        # Create a data storage
        self.storage = DataStorage()
        
        # Create the event management system
        self.system = EventManagementSystem(self.storage)
        
        # Initialize the user state
        self.user_id = None
        self.role = None
        
        # Show the login frame
        self.show_login_frame()
    
    def show_login_frame(self):
        # Clear the window
        for widget in self.master.winfo_children():
            widget.destroy()
        
        # Create and show the login frame
        login_frame = LoginFrame(self.master, self.handle_login, self.show_register_frame)
        login_frame.pack(fill='both', expand=True)
    
    def show_register_frame(self):
        # Clear the window
        for widget in self.master.winfo_children():
            widget.destroy()
        
        # Create and show the register frame
        register_frame = RegisterFrame(self.master, self.handle_register, self.show_login_frame)
        register_frame.pack(fill='both', expand=True)
    
    def show_dashboard(self):
        # Clear the window
        for widget in self.master.winfo_children():
            widget.destroy()
        
        # Create and show the dashboard
        dashboard = UserDashboard(self.master, self.system, self.user_id, self.role, self.handle_logout)
        dashboard.pack(fill='both', expand=True)
    
    def handle_login(self, username, password):
        user_id, role = self.system.login(username, password)
        
        if user_id:
            self.user_id = user_id
            self.role = role
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    
    def handle_register(self, username, password, email, role):
        user_id, msg = self.system.register_user(username, password, email, role)
        
        if user_id:
            messagebox.showinfo("Registration Successful", "You can now login with your credentials")
            self.show_login_frame()
        else:
            messagebox.showerror("Registration Failed", msg)
    
    def handle_logout(self):
        self.user_id = None
        self.role = None
        self.show_login_frame()


def main():
    # Create the main window
    root = tk.Tk()
    
    # Create the application
    app = EventManagementApp(root)
    
    # Start the main loop
    root.mainloop()


if __name__ == "__main__":
    main()
