from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QMenuBar, QMenu, QAction, QListWidget, QLabel, 
QPushButton, QRadioButton, QMessageBox, QSlider)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

class MasterLayout(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photo Editor")
        self.showMaximized()
        self.load_theme("assets/themes/Dark Mode.qss")

        # main Application layout
        self.main_layout = QVBoxLayout()

        # sub-layouts
        self.menu_layout = QHBoxLayout() # layout for the menu bar
        self.body_layout = QHBoxLayout() # layout for the application body
        self.footer_layout = QHBoxLayout() # layout for the tools and imported photos

        self.setup_menu()
        self.setup_body()
        self.setup_footer()

        self.main_layout.addLayout(self.menu_layout)
        self.main_layout.addLayout(self.body_layout)
        self.main_layout.addLayout(self.footer_layout)
        self.main_layout.setContentsMargins(0,0,0,0)

        self.setLayout(self.main_layout)

    

    def setup_menu(self):

        """ setting up menu bar """

        menu_items = {
            "File": ["New Photo", "Save", "Exit"],
            "Themes": ["Dark Mode", "Light Mode", "Dark Contrast", "Light Contrast"]
        }

        self.menu_item_actions = {"File":[], "Themes":[]}

        # main menu bar
        self.menu_bar = QMenuBar(self)

        # menu
        self.file_menu = QMenu("File", self)
        self.preferences_menu = QMenu("Themes", self)

        # setting up file menu item actions
        for item in menu_items["File"]:
            action = QAction(item, self)
            self.file_menu.addAction(action)
            self.menu_item_actions["File"].append(action)

        # setting up preferences menu item actions  
        for item in menu_items["Themes"]:
            action = QAction(item,self)
            self.preferences_menu.addAction(action)
            self.menu_item_actions["Themes"].append(action)
        
        self.menu_bar.addMenu(self.file_menu)
        self.menu_bar.addMenu(self.preferences_menu)

        self.menu_layout.addWidget(self.menu_bar)
    
    def setup_body(self):
        
        """setting up Body layout"""

        self.side_bar = QListWidget() # side bar with application image manipulation functions
        self.image_body = QLabel("image",self)  # image holder

        self.side_bar.addItems(["Brightness", "Sharpness", "Rotate Left", "Rotate Right", "Mirror", "Blur", "B/W", "Remove Background"])
        self.image_body.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.image_body.setPixmap(QPixmap("assets/logos/buttons_logo/place_holder.ico").scaled(self.image_body.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.body_layout.addWidget(self.side_bar, 20) # list Widget with 10% of screen
        self.body_layout.addWidget(self.image_body,80) # image with 90% of screen with in the body Layout
    
    def setup_footer(self):
        self.state_control_layout = QVBoxLayout() # holds the prev,next state button and original,apply changes button
        self.tools_layout = QHBoxLayout() # holds the filter control values

        self.previous_btn = QPushButton("")
        self.next_btn = QPushButton("")
        self.Apply_changes = QPushButton("Apply Changes")

        self.original = QRadioButton("Original Image")
        self.Edited = QRadioButton("Edited")

        self.previous_btn.setIcon(QIcon("assets/logos/buttons_logo/left-arrow.ico"))
        self.next_btn.setIcon(QIcon("assets/logos/buttons_logo/right-arrow.ico"))

        self.previous_btn.setIconSize(self.previous_btn.sizeHint())
        self.next_btn.setIconSize(self.next_btn.sizeHint())
        
        self.Edited.setChecked(True)

        self.state_control_layout.addWidget(self.previous_btn)
        self.state_control_layout.addWidget(self.next_btn)
        self.state_control_layout.addWidget(self.Apply_changes)
        self.state_control_layout.addWidget(self.original)
        self.state_control_layout.addWidget(self.Edited)

        self.slider_filter = QLabel("")
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.place_holder_value = QLabel("100%")
        self.slider.setMinimum(1)
        self.slider.setMaximum(200)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(5)
        self.slider.setValue(100)


        self.tools_layout.addWidget(self.slider_filter)
        self.tools_layout.addWidget(self.slider)
        self.tools_layout.addWidget(self.place_holder_value)

        self.slider.hide()
        self.place_holder_value.hide()
        
        

        self.footer_layout.addLayout(self.state_control_layout, 20)
        self.footer_layout.addLayout(self.tools_layout, 80)



    def load_theme(self, theme_path):
        with open(theme_path, 'r') as styleSheet:
            self.setStyleSheet(styleSheet.read())

    def show_message(self, title: str, message: str):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)

        msg_box.exec_()
    


