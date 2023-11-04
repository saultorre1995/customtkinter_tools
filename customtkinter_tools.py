#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 18:38:38 2023
@author: Saul Gonzalez Resines
Package containing standard classes for the development of UI, 
based on customtkinter classes
"""

import os
import json
import sys
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.font as font
from tkinter import filedialog
import customtkinter


# Default Fonts that are defined
FONT       = ('Nimbus Sans', 20)
FONT1      = ('Nimbus Sans',25,"bold")
TITLE_FONT = ('Nimbus Sans',50,"bold")


# Needed functions to interpret classes from strings
def class_from_string(class_str):
    '''Get the class by name'''
    return getattr(sys.modules[__name__], class_str)


def divide_arguments(dic_elements):
    class_type = class_from_string(dic_elements["object_type"])
    if "kids_objects" not in list( dic_elements.keys()):
        class_kids=[]
    else:
        class_kids = dic_elements["kids_objects"]
    # Remove both object_type and kids_objects and only 
    dic_kwargs = {}
    for key in dic_elements.keys():
        if key not in ["object_type","kids_objects"]:
            dic_kwargs[key] = dic_elements[key]
    # return divided
    return class_type,class_kids,dic_kwargs

class ContainerFrame(customtkinter.CTkFrame):
    '''Baseframe containing information in the Inner Frame'''
    def __init__(self,root,key,*args,**kwargs):
        super().__init__(root,*args,**kwargs)
        # containing all the objects
        self._key  = key
        self.inner = self
    
    def get_value(self):
        '''Get values from the ContainerFrame childs'''
        _value = {}
        # Get value recursively of other containe frames
        for kid in self.inner.winfo_children():
            if issubclass(type(kid),ContainerFrame):
                _value[kid._key]      = kid.get_value()
        return _value
            

    @classmethod
    def initialize(cls,root,dic_elements):
        '''Initilizes and packs simply the elements of the '''
        # Recursively iterate
        class_type ,class_kids,dic_kwargs = divide_arguments(dic_elements)
        # execute this class
        this_class = class_type(root,**dic_kwargs)
        # Initialize the kids if available
        for kid in class_kids:
            class_kid ,_,_     = divide_arguments(kid)
            this_kid_class     = class_kid.initialize(this_class.inner,kid)
            # Easy Pack in a list
            this_kid_class.pack(fill=BOTH,pady=10)
        return this_class
    
    
    def add_items(self,list_childs):
        '''Add items from a list of dictionaries similar way to initiliaze function'''
        for kid in list_childs:
            class_kid ,_,_     = divide_arguments(kid)
            this_kid_class     = class_kid.initialize(self.inner,kid)
            this_kid_class.pack(fill=BOTH,pady=10)
            
            
    def remove_items(self):
        '''Removes the childs of this frame'''
        for kid in self.inner.winfo_children():
            # Forget the mapping
            if kid.winfo_ismapped():
                kid.pack_forget()
            # destroy
            kid.destroy()
    
    
    def hide_container(self,key):
        '''Hide an specific kid from the container'''
        for kid in self.inner.winfo_children():
            if issubclass(type(kid),ContainerFrame):
                if  kid._key == key:
                    if kid.winfo_ismapped():
                        kid.pack_forget()
                        break
                    else:
                        kid.hide(key)
    
    def unhide_container(self,key):
        '''Unhide an specific kid from the container''' 
        for kid in self.inner.winfo_children():
            if issubclass(type(kid),ContainerFrame):
                if  kid._key == key:
                    if kid.winfo_ismapped():
                        kid.pack_forget()
                        break
                    else:
                        kid.hide(key)
                        
class VerticalFrame(ContainerFrame):
    def __init__(self,root,*args,**kwargs):
        '''Normal frame with a Vertical scrollable frame'''
        super().__init__(root,*args,**kwargs)
        self.inner =  customtkinter.CTkScrollableFrame(self)
        self.inner.pack(fill=BOTH,padx=20,expand=TRUE)



class MainFrame(ContainerFrame):
    def __init__(self,root,title,info_text,button_text="Execute Workflow",font_label=('Courier', 20),font_button=('Courier', 20,'bold'),wraplength=1000,*args,**kwargs):
        super().__init__(root,*args,**kwargs)
        self.label    = customtkinter.CTkLabel(self, text=title, font = TITLE_FONT)
        self.text     = customtkinter.CTkLabel(self,text=info_text,wraplength = wraplength,font=font_label)
        self.button   = customtkinter.CTkButton(self,text= button_text,font=font_button,command=self.execute)
        # Inner frame is an scrollable frame
        self.inner     = customtkinter.CTkScrollableFrame(self)
        # Pack the rest of options 
        self.label.pack(fill=X,expand=TRUE,padx=5, pady=5)
        self.text.pack(fill=X,expand=TRUE,padx=5, pady =5)
        self.inner.pack(fill=BOTH,expand=TRUE,padx=20,pady=5)
        self.button.pack(fill=X,expand=TRUE,padx=50,pady = 5)
            
    
    def execute(self):
        '''Do nothing'''
        pass
    
            

class AppearingFrame(ContainerFrame):
    '''AppearingFrame: It hides the inner content while pressing the button'''
    def __init__(self,root,is_packed,info_text,font_button=('Courier', 20,'bold'),image=None,*args,**kwargs):
        super().__init__(root,*args,**kwargs)
        self.unpack_button=customtkinter.CTkButton(self,text = info_text,
                                                   command = self.do_packing,
                                                   font=font_button,anchor="w",image=image)
        
        self.inner        = ContainerFrame(self,key="inner")
        self.unpack_button.pack(fill=X,expand=TRUE,pady=5,padx=5)
        # Start with packed or unpacked
        if is_packed:
            self.inner.pack(expand=TRUE,fill=BOTH,pady=5,padx=5)
        
        
    def do_packing(self):
        '''Pack or unpack the subframe'''
        if self.inner.winfo_ismapped():
            self.inner.pack_forget()
        else:
            #print(self.winfo_width())
            self.inner.pack(expand=TRUE,fill=BOTH)
    



class GeneralFrame(ContainerFrame):
    def __init__ (self,root,title,info_text,font_label=('Courier', 20,'bold'),font_info=('Courier', 20),wraplength=600,*args,**kwargs):
        super().__init__(root,*args,**kwargs)
        # Descriptor label and the
        self.info_inner = customtkinter.CTkFrame(self,fg_color=self.cget("fg_color"))
        self.label     = customtkinter.CTkLabel(self.info_inner, text=title, font = font_label)
        self.text      = customtkinter.CTkLabel(self.info_inner,text=info_text,wraplength = wraplength,font=font_info)
        # Modifiable
        self.embedded = customtkinter.CTkFrame(self,fg_color=self.cget("fg_color"))
        self.info_inner.pack(side=LEFT,expand=TRUE,fill=BOTH,anchor=W,padx=5,pady=5)
        self.embedded.pack(side=RIGHT,expand=TRUE,fill=BOTH,anchor=W,padx=5,pady=5)
        self.label.pack(side=TOP,expand=TRUE,fill=BOTH,padx=5,pady=5)
        self.text.pack(side=BOTTOM,expand=TRUE,fill=BOTH,padx=5,pady=5)



class GeneralEntry(GeneralFrame):
    def __init__(self,root,default="",font_entry=('Courier', 20),*args,**kwargs):
        '''Frame containing a tkinter Label plus an Entry'''
        # Do the label entry 
        super().__init__(root,*args,**kwargs)
        self.tk_entry = customtkinter.CTkEntry(self.embedded,font=font_entry)
        self.tk_entry.insert(0, default)
        self._value    = default
        # Pack into a toolchain
        self.tk_entry.pack(expand=TRUE,fill=BOTH)
        
    def get_value(self):
        '''Get the internal value of the tk_entry'''
        # reset 
        self.set_value()
        # return the valeu
        return self._value
    
    def set_value(self):
        '''Set the internal value with the info_text'''
        self._value = self.tk_entry.get().strip()


class GeneralCheckButton(GeneralFrame):
    def __init__(self,root,default=True,*args,**kwargs):
        super().__init__(root,*args,**kwargs)
        self._value   =  IntVar(self.embedded)
        self._value.set(int(default))
        self.tk_checkbutton =  customtkinter.CTkCheckBox(self.embedded, text="",variable=self._value, onvalue=1, offvalue=0)
        # Pack into a toolchain
        self.tk_checkbutton.pack(expand=TRUE,fill=BOTH)
    
    def get_value(self):
        '''Gets the value of the StringVar'''
        return bool(int(self._value.get()))
    
    
class GeneralLabelMenu(GeneralFrame):
    '''Label Menu'''
    def __init__(self,root,options,*args,**kwargs):
        super().__init__(root,*args,**kwargs)
        self._value =  StringVar(self.embedded)
        self._value.set(options[0])
        self.tk_menu  =  OptionMenu(self.embedded, self._value, *options)
        self.tk_menu.config(font=FONT1)
        # Pack into a toolchain
        self.tk_menu.pack()
    

    def get_value(self):
        '''Gets the value of the StringVar'''
        return self._value.get().strip()


class GeneralFileExplorer(GeneralFrame):
    '''File explorer'''
    def __init__(self,root,filetypes=(('All files','*.*'),('text files', '*.txt')),*args,**kwargs):
        super().__init__(root,*args,**kwargs)
        self.tk_label          = customtkinter.CTkLabel(self.embedded,text ="Select File",font=FONT)
        self.tk_button         = customtkinter.CTkButton(self.embedded,text = "Browse Files",
                                                         command = self.browseFiles,font=FONT)
        self.filetypes         = filetypes
        # Pack
        self.tk_label.pack(side=TOP)
        self.tk_button.pack(side= BOTTOM)
    
    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir = "/",
                                              title = "Select a File",
                                              filetypes = self.filetypes)
        # Change label contents
        if type(filename)==tuple:
            filename=""
        self.tk_label.configure(text=""+filename)
    
    def get_value(self):
        '''Gets the value of the label'''
        self._value=self.tk_label.cget("text").strip()
        return self._value 


class GeneralDirectoryExplorer(GeneralFrame):
    '''Directory Browser'''
    def __init__(self,root,*args,**kwargs):
        super().__init__(root,*args,**kwargs)
        self.tk_label          = customtkinter.CTkLabel(self.embedded,text ="Select Directory",font=FONT)
        self.tk_button         = customtkinter.CTkButton(self.embedded,text = "Browse Directories",command = self.browseDirectory,font=FONT)
        # Pack
        self.tk_label.pack(side=TOP)
        self.tk_button.pack(side= BOTTOM)
        
    def browseDirectory(self):
        filedir = filedialog.askdirectory(initialdir = "/",
                                               title = "Select a Directory")
        # Change label contents
        if type(filedir)==tuple:
            filedir=""
        self.tk_label.configure(text=filedir)
     
    def get_value(self):
        '''Gets the value of the label'''
        self._value=self.tk_label.cget("text").strip()
        return self._value


class GeneralTextBox(GeneralFrame):
    '''Text Box'''
    def __init__(self,root,default="",is_disabled=False,*args,**kwargs):
        super().__init__(root,*args,**kwargs)
        self.tk_textbox =  customtkinter.CTkTextbox(self.embedded)
        self.tk_textbox.insert("0.0",default)
        # enable or disable the textbox
        if is_disabled:
            self.tk_textbox.configure(state="disabled")
        self.tk_textbox.pack()

    
    def get_value(self):
        '''Get the value of the textbox'''
        return self.tk_textbox.get("0.0", "end")

    def update(self,text):
        '''Update text box'''
        self.tk_textbox.delete("0.0", "end")
        self.tk_textbox.insert("0.0", text)