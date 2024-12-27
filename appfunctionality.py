from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from layout import MasterLayout
from imageFilter import Filters
from state_tracker import Tracker
from PIL import Image
import sys
import os
import io


class AppCore(MasterLayout, Filters):
    
    def __init__(self):
        super().__init__()

        self.original_img = None
        self.editable_img = None
        self.preview_img = None
        self.tracker = None

        self.init_menu()
        self.init_features()
    


    # setting action for the menu items
    def init_menu(self):

        """ assining trigger function to the menu bar items """

        for menu in self.menu_item_actions:
            for item in self.menu_item_actions[menu]:
                item.triggered.connect(self.menu_actions)


    # setting triggers
    def menu_actions(self):
        signal = self.sender()
        path = os.path.expanduser("~/Quick access")
        
        if signal.text() == "New Photo":

            file_path,_ = QFileDialog.getOpenFileName(self, "Open Image", path, "Images (*.png *.jpg *.jpeg *.bmp *.gif)")

            if file_path:
                self.original_img = self.get_img(file_path)
                self.editable_img = self.original_img.copy()
                self.preview_img = self.editable_img.copy()
                self.tracker = Tracker()
                self.tracker.append(self.editable_img)
                self.load_img(self.tracker.current.image)
            else:
                self.show_message("Cancelled", "No Image is selected")

        elif signal.text() == "Save":

            if self.editable_img is not None:
                file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", path, "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;All Files (*)")

                if file_path:
                    self.save_img(self.editable_img, file_path)
                    self.show_message(f"Success", "Image saved")
            
        elif signal.text() == "Exit":
            sys.exit(0)

        else:
            self.load_theme(f"assets/themes/{signal.text()}.qss")

    def init_features(self):
        self.side_bar.itemDoubleClicked.connect(self.image_filters)
        self.slider.valueChanged.connect(self.slider_handler)
        self.Apply_changes.clicked.connect(self.apply_changes)
        self.previous_btn.clicked.connect(self.prev_view)
        self.next_btn.clicked.connect(self.next_view)
        self.original.toggled.connect(lambda: self.radio_toggle(self.original))
        self.Edited.toggled.connect(lambda: self.radio_toggle(self.Edited))

    
    def image_filters(self, item):
        if self.editable_img:
            if item.text() in ["Brightness", "Sharpness", "Blur"]:
                self.slider_filter.setText(item.text())
                self.slider.show()
                self.place_holder_value.show()
            else:
                self.preview_img = self.apply_filter(self.preview_img,item.text())
                self.load_img(self.preview_img)
            
            self.tracker.current = self.tracker.tail

    def slider_handler(self, value):
        self.preview_img = self.tracker.tail.image
        self.place_holder_value.setText(f"{value}%")
        self.preview_img = self.apply_filter(self.preview_img,self.slider_filter.text(), value/100)
        self.load_img(self.preview_img)

    def apply_changes(self):
        if self.editable_img is not None:
            if not self.compare_img(self.editable_img, self.preview_img):
                self.editable_img = self.preview_img.copy()
                self.tracker.append(self.editable_img)
                self.load_img(self.tracker.tail.image)

    def prev_view(self):
        if self.editable_img:
            if self.tracker.current.prev is not None:
                self.tracker.current = self.tracker.current.prev
                self.load_img(self.tracker.current.image)

    
    def next_view(self):
        if self.editable_img:
            if self.tracker.current.next is not None:
                self.tracker.current = self.tracker.current.next
                self.load_img(self.tracker.current.image)

    def radio_toggle(self, toggle):
        if toggle.isChecked():
            if self.editable_img:
                if toggle.text() == "Original Image":
                    self.load_img(self.original_img)
                else:
                    self.load_img(self.editable_img)

    def get_img(self, file_path: str)-> Image:
        img = Image.open(file_path)

        return img

    
    def save_img(self, image: Image, file_path: str):
        image.save(file_path)
    

    def load_img(self, image: Image):
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        img = QImage()
        img.loadFromData(buffer.read(), "PNG")
        pixmap_img = QPixmap.fromImage(img)

        self.image_body.setPixmap(pixmap_img.scaled(self.image_body.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


