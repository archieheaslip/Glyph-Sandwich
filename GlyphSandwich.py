# MenuTitle: Glyph Sandwich
# -*- coding: utf-8 -*-
__doc__="""
Places a chosen glyph on either side of all selected glyphs.
"""

from vanilla import FloatingWindow, TextBox, EditText, Button
from GlyphsApp import Glyphs, Message

class CustomGlyphWindow:
    def __init__(self):
        self.w = FloatingWindow((300, 100), "Glyph Sandwich")
        self.w.input_glyph = EditText((10, 10, -10, 22), placeholder="Enter Glyph", callback=self.validate_glyph)
        self.w.submit_button = Button((10, 40, -10, 22), "Make Sandwich", callback=self.submit_glyph)
        
        self.custom_glyph = None
        self.w.open()

    def validate_glyph(self, sender):
        entered_glyph = sender.get()
        font = Glyphs.font
        if font:
            if font.glyphs[entered_glyph]:
                self.custom_glyph = entered_glyph
            else:
                self.custom_glyph = None

    def submit_glyph(self, sender):
        if self.custom_glyph:
            self.w.close()
            self.add_custom_glyph(self.custom_glyph)
        else:
            Message("Glyph not found in the font.", "Glyph Missing")

    def add_custom_glyph(self, glyph_name):
        font = Glyphs.font
        current_tab = font.currentTab
        if current_tab:
            selected_glyphs = current_tab.layers
            custom_glyph = font.glyphs[glyph_name]
            
            new_layers = []
            if selected_glyphs:
                custom_layer = custom_glyph.layers[current_tab.masterIndex]
                new_layers.append(custom_layer)  # Add the custom glyph at the beginning
            
            for layer in selected_glyphs:
                new_layers.append(layer)
                new_layers.append(custom_layer)
            
            if selected_glyphs:
                new_layers.pop()  # Remove the extra custom glyph at the end
            
            new_layers.append(custom_layer)  # Add the custom glyph at the end
            
            current_tab.layers = new_layers
        else:
            # Handle glyph overview case
            selected_glyphs = font.selectedLayers
            if selected_glyphs:
                custom_glyph = font.glyphs[glyph_name]
                
                new_layers = []
                # Get the index of the master from the font's masters list
                current_master_index = font.selectedFontMaster.id
                custom_layer = custom_glyph.layers[current_master_index]
                
                new_layers.append(custom_layer)  # Add the custom glyph at the beginning
                for index, glyph_layer in enumerate(selected_glyphs):
                    new_layers.append(glyph_layer)
                    new_layers.append(custom_layer)
                new_layers.pop()  # Remove the extra custom glyph at the end
                new_layers.append(custom_layer)  # Add the custom glyph at the end
                
                font.newTab().layers = new_layers

if __name__ == "__main__":
    CustomGlyphWindow()

