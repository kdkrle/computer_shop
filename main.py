from shop_db import *
from data import *
from tkinter import *
import customtkinter as ctk
import CTkMessagebox as cmb
from tkinter import ttk
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import random
from PIL import Image
from datetime import date
import numpy as np

root = ctk.CTk()
root.title("Abstract - Computer Shop")
root.geometry("1200x900")
root.resizable(False, False)
root.iconbitmap("pics/abstract.ico")

# Appearance set to 'dark'
ctk.set_appearance_mode("dark")

# Status of main frame (what it shows)
main_frame_status = ctk.StringVar()

# Combobox style
root.option_add("*TCombobox*Listbox*Background", "#1a1110")
root.option_add("*TCombobox*Listbox*Foreground", "#eee8aa")
root.option_add("*TCombobox*Listbox*Font", "Calibri")

# Treeview style
tv_style = ttk.Style()
tv_style.configure("tv_style.Treeview", rowheight=23, font=("Calibri", 12))
tv_style.configure("tv_style.Treeview.Heading", foreground="#7a0003",
                   font=("Calibri", 12))


def exit_application():
    """Closing the application."""
    
    msg = cmb.CTkMessagebox(
        title="Closing the application",
        message="Do you want to exit the application?",
        icon="warning",
        option_1="No",
        option_2="Yes",
        button_width=100,
        button_color="#1a1110",
        button_hover_color="#4e1609",
        text_color="#eee8aa",
        title_color="#eee8aa",
        button_text_color="#eee8aa",
        font=("Calibri", 16),
        fg_color="#1a1110",
        bg_color="#100c08",
        corner_radius=10
    )
    
    answer = msg.get()
    
    if answer == "Yes":
        root.destroy()


def image_resize(path, width, height):
    """Resizing an image to the desired size."""
    
    img = Image.open(path)
    resize_image = ctk.CTkImage(img, size=(width, height))
    
    return resize_image


def unique_code_generating(old_list, code_length):
    """Generating of unique code with a specified length."""
    
    unique = ""
    for _ in range(code_length):
        unique += str(random.randint(0, 9))
    
    if unique in old_list:
        unique_code_generating(old_list, code_length)
    else:
        return unique


def len_digit_limit(inp, length):
    """Enter only a certain number of digits."""
    
    if inp.isdigit() and len(inp) <= length:
        return True
    elif inp == "":
        return True
    else:
        return False


def disable_scroll(event):
    return "break"


def add_value_label(x_list, y_list, color, h_position):
    for i in range(1, len(x_list) + 1):
        plt.text(i - 1, y_list[i - 1] / 2, y_list[i - 1], color=color,
                 ha=h_position)


def discount_price_calculating(regular_price, discount):
    discount_price = float(round((1 - discount/100) * regular_price))
    
    return discount_price


def discount_update():
    """Discount update in new window."""
    
    # New Toplevel
    discount_update_tl = ctk.CTkToplevel(root, fg_color="#100c08")
    discount_update_tl.title("Discount Update")
    discount_update_tl.attributes("-topmost", "true")
    discount_update_tl.resizable(False, False)
    discount_update_tl.grab_set()
    discount_update_tl.after(200, lambda: discount_update_tl.iconbitmap(
        "pics/abstract.ico"))
    
    def selection_list():
        """Creating a product selection list."""
        
        code_list = products.products_df.product_code.to_list()
        name_list = products.products_df.name.to_list()
        manufacturer_list = products.products_df.manufacturer.to_list()
        type_list = products.products_df.type.to_list()
        
        if sort_var.get() == "1":
            pair_lists = []
            for i in range(len(name_list)):
                code_name_pair = [code_list[i], name_list[i]]
                pair_lists.append(code_name_pair)
            pair_lists.sort()
        
        elif sort_var.get() == "2":
            pair_lists = []
            for i in range(len(name_list)):
                code_name_pair = [code_list[i], name_list[i]]
                pair_lists.append(code_name_pair)
            pair_lists.sort(key=lambda x: x[1].casefold())
        
        elif sort_var.get() == "3":
            pair_lists = []
            for i in range(len(name_list)):
                manufacturer_name_pair = [manufacturer_list[i], name_list[i]]
                pair_lists.append(manufacturer_name_pair)
            pair_lists.sort(key=lambda x: x[0].casefold())
        
        elif sort_var.get() == "4":
            pair_lists = []
            for i in range(len(name_list)):
                type_name_pair = [type_list[i], name_list[i]]
                pair_lists.append(type_name_pair)
            pair_lists.sort(key=lambda x: x[0].casefold())
        
        else:
            discount_code_list = products.products_df.product_code[
                products.products_df.discount > 0].to_list()
            discount_name_list = products.products_df.name[
                products.products_df.discount > 0].to_list()
            
            pair_lists = []
            for i in range(len(discount_name_list)):
                code_name_pair = [discount_code_list[i], discount_name_list[i]]
                pair_lists.append(code_name_pair)
            pair_lists.sort()
        
        product_selection = []
        for pair in pair_lists:
            merged_values = f"{pair[0]} - {pair[1]}"
            product_selection.append(merged_values)
        
        product_select_cb.set("")
        product_select_cb.configure(values=product_selection)
        set_discount_sb.set("")
        set_discount_sb.configure(state="disabled")
        selected_product_lbl.configure(text="No selected product",
                                       text_color="#1a1110")
        selected_code_val.configure(text="-")
        selected_manufacturer_val.configure(text="-")
        selected_type_val.configure(text="-")
        selected_current_discount_val.configure(text="-")
        selected_regular_price_val.configure(text="-")
        selected_discount_price_val.configure(text="-")
    
    def selected_product_data(event):
        """Displaying data of the selected product."""
        
        set_discount_sb.configure(state="readonly")
        
        # Get selected product data
        selected_product_name = combo_value_var.get().split(" - ", 1)[1]
        product_data = products.products_df[
            products.products_df.name == selected_product_name
        ].values.flatten().tolist()
        
        discount_price = discount_price_calculating(product_data[5],
                                                    product_data[6])
        
        # Display data values
        selected_product_lbl.configure(text=selected_product_name,
                                       text_color="white")
        selected_code_val.configure(text=product_data[0])
        selected_manufacturer_val.configure(text=product_data[2])
        selected_type_val.configure(text=product_data[3])
        selected_current_discount_val.configure(text=f"{product_data[6]}%")
        set_discount_sb.set(product_data[6])
        selected_regular_price_val.configure(text=f"{product_data[5]:.2f}")
        selected_discount_price_val.configure(text=f"{discount_price:.2f}")
    
    def new_discount():
        """Set a new discount for the product."""
        
        if product_select_cb.get():
            product_name = product_select_cb.get().split(" - ", 1)[1]
            current_discount = int(products.products_df.discount[
                                       products.products_df.name == product_name].to_string(
                index=False))
            
            if current_discount == int(set_discount_sb.get()):
                cmb.CTkMessagebox(
                    title="No change",
                    message="The discount remained the same.",
                    icon="info",
                    button_width=100,
                    button_color="#1a1110",
                    button_hover_color="#4e1609",
                    text_color="#eee8aa",
                    title_color="#eee8aa",
                    button_text_color="#eee8aa",
                    font=("Calibri", 16),
                    fg_color="#1a1110",
                    bg_color="#100c08",
                    corner_radius=10
                )
            else:
                discount_sql = f"""
                UPDATE products
                SET discount = '{int(set_discount_sb.get())}'
                WHERE name = '{product_name}';
                """
                
                products.products_entry_data(discount_sql)
                products.products_loading()
                
                product_select_cb.set("")
                set_discount_sb.set("")
                set_discount_sb.configure(state="disabled")
                selected_product_lbl.configure(text="No selected product",
                                               text_color="#1a1110")
                selected_code_val.configure(text="-")
                selected_manufacturer_val.configure(text="-")
                selected_type_val.configure(text="-")
                selected_current_discount_val.configure(text="-")
                selected_regular_price_val.configure(text="-")
                selected_discount_price_val.configure(text="-")
                
                sort_var.set("1")
                product_select_cb.configure(values=value_list)
                main_frame_status.set("")
                discounts_pressed()
                
                cmb.CTkMessagebox(
                    title="Update successful",
                    message="The update was completed successfully.",
                    icon="info",
                    button_width=100,
                    button_color="#1a1110",
                    button_hover_color="#4e1609",
                    text_color="#eee8aa",
                    title_color="#eee8aa",
                    button_text_color="#eee8aa",
                    font=("Calibri", 16),
                    fg_color="#1a1110",
                    bg_color="#100c08",
                    corner_radius=10
                )
        
        else:
            cmb.CTkMessagebox(
                title="No selected product",
                message="No product have been selected.",
                icon="info",
                button_width=100, button_color="#1a1110",
                button_hover_color="#4e1609",
                text_color="#eee8aa",
                title_color="#eee8aa",
                button_text_color="#eee8aa",
                font=("Calibri", 16),
                fg_color="#1a1110",
                bg_color="#100c08",
                corner_radius=10
            )
    
    # Set title label
    discount_title_lbl = ctk.CTkLabel(
        discount_update_tl,
        width=800,
        text="DISCOUNT UPDATE",
        text_color="#7a0003",
        font=("Calibri", 48, "bold")
    )
    discount_title_lbl.pack(ipady=40)
    
    # Info label
    update_info_lbl = ctk.CTkLabel(
        discount_update_tl,
        text="Sort products by their code, name, manufacturer, "
             "type or\nshorten the list to only those that are already on "
             "discount.",
        text_color="#eee8aa",
        justify="left",
        font=("Calibri", 16)
    )
    update_info_lbl.pack(pady=(0, 20))
    
    # Radiobutton frame
    sorting_frm = ctk.CTkFrame(
        discount_update_tl,
        border_width=1,
        border_color="#eee8aa"
    )
    sorting_frm.pack(expand=True, fill="x", pady=10, padx=50)
    
    # Frame title
    sorting_frame_title = ctk.CTkLabel(
        sorting_frm,
        fg_color="black",
        text="Sort method",
        font=("Calibri", 16),
        anchor="center"
    )
    sorting_frame_title.pack(fill="x", padx=2, pady=2)
    
    # Variable and values
    sort_var = ctk.StringVar(sorting_frm, "1")
    sort_values = {"Product Code": "1", "Product Name": "2",
                   "Manufacturer": "3", "Product Type": "4",
                   "On Discount": "5"}
    
    for key, value in sort_values.items():
        if value == "5":
            y_pad = (5, 15)
        else:
            y_pad = 5
        
        ctk.CTkRadioButton(
            sorting_frm,
            text=key,
            value=value,
            variable=sort_var,
            text_color="#eee8aa",
            border_color="#eee8aa",
            fg_color="#7a0003",
            hover_color="#7a0003",
            border_width_checked=4,
            border_width_unchecked=2,
            radiobutton_width=15,
            radiobutton_height=15,
            font=("Calibri", 16),
            command=selection_list
        ).pack(fill="x", padx=40, pady=y_pad)
    
    # Product selection frame
    product_selection_frm = ctk.CTkFrame(discount_update_tl, border_width=1,
        border_color="#eee8aa")
    product_selection_frm.pack(expand=True, fill="x", padx=50, pady=10)
    
    product_selection_frm.grid_columnconfigure(0, weight=1)
    product_selection_frame_title = ctk.CTkLabel(
        product_selection_frm,
        fg_color="black",
        text="Product selection",
        font=("Calibri", 16),
        anchor="center"
    )
    product_selection_frame_title.grid(column=0, row=0, padx=2, pady=2,
                                       sticky="we")
    
    select_values_frm = ctk.CTkFrame(product_selection_frm,
        fg_color="transparent")
    select_values_frm.grid(column=0, row=1, padx=20, sticky="we")
    
    select_values_frm.grid_columnconfigure((0, 1), weight=1)
    product_select_lbl = ctk.CTkLabel(
        select_values_frm,
        text="Select product:",
        text_color="#eee8aa",
        font=("Calibri", 16)
    )
    product_select_lbl.grid(column=0, row=0, padx=20, pady=(20, 0), sticky="w")
    
    # Initial list of values for the Combobox
    codes = products.products_df.product_code.to_list()
    names = products.products_df.name.to_list()
    
    value_list = []
    for i in range(len(names)):
        value_list.append(f"{codes[i]} - {names[i]}")
    value_list.sort()
    
    combo_value_var = StringVar()
    product_select_cb = ttk.Combobox(
        select_values_frm,
        width=70,
        state="readonly",
        values=value_list,
        textvariable=combo_value_var
    )
    product_select_cb.grid(column=0, row=1, padx=20, pady=(0, 20), sticky="w")
    product_select_cb.bind("<<ComboboxSelected>>", selected_product_data)
    
    set_discount_lbl = ctk.CTkLabel(
        select_values_frm,
        text="Set discount:",
        text_color="#eee8aa",
        font=("Calibri", 16)
    )
    set_discount_lbl.grid(column=1, row=0, padx=20, pady=(20, 0), sticky="w")
    
    set_discount_sb = ttk.Spinbox(
        select_values_frm,
        width=8,
        from_=0,
        to=90,
        font="Calibri",
        state="disabled"
    )
    set_discount_sb.grid(column=1, row=1, padx=20, pady=(0, 20), sticky="w")
    
    selected_product_lbl = ctk.CTkLabel(
        product_selection_frm,
        text="No selected product",
        text_color="#1a1110",
        font=("Calibri", 24)
    )
    selected_product_lbl.grid(column=0, row=2, padx=40, pady=10, sticky="w")
    
    product_data_frm = ctk.CTkFrame(product_selection_frm,
                                    fg_color="transparent")
    product_data_frm.grid(column=0, row=3, padx=20, pady=(0, 20), sticky="we")
    
    product_data_frm.grid_columnconfigure((0, 1, 2), weight=1)
    selected_code_lbl = ctk.CTkLabel(
        product_data_frm,
        text="Product code:",
        text_color="#eee8aa",
        font=("Calibri", 16)
    )
    selected_code_lbl.grid(column=0, row=0, padx=(20, 0), pady=(10, 0),
                           sticky="w")
    
    selected_manufacturer_lbl = ctk.CTkLabel(
        product_data_frm,
        text="Manufacturer:",
        text_color="#eee8aa",
        font=("Calibri", 16)
    )
    selected_manufacturer_lbl.grid(column=1, row=0, pady=(10, 0), sticky="w")
    
    selected_type_lbl = ctk.CTkLabel(
        product_data_frm,
        text="Product type:",
        text_color="#eee8aa",
        font=("Calibri", 16)
    )
    selected_type_lbl.grid(column=2, row=0, pady=(10, 0), sticky="w")
    
    selected_code_val = ctk.CTkLabel(
        product_data_frm,
        text="-",
        text_color="white",
        font=("Calibri", 16)
    )
    selected_code_val.grid(column=0, row=1, padx=(20, 0), pady=(0, 10),
                           sticky="w")
    
    selected_manufacturer_val = ctk.CTkLabel(
        product_data_frm,
        text="-",
        text_color="white",
        font=("Calibri", 16)
    )
    selected_manufacturer_val.grid(column=1, row=1, pady=(0, 10), sticky="w")
    
    selected_type_val = ctk.CTkLabel(
        product_data_frm,
        text="-",
        text_color="white",
        font=("Calibri", 16)
    )
    selected_type_val.grid(column=2, row=1, pady=(0, 10), sticky="w")
    
    selected_current_discount_lbl = ctk.CTkLabel(
        product_data_frm,
        text="Current discount:",
        text_color="#eee8aa",
        font=("Calibri", 16)
    )
    selected_current_discount_lbl.grid(column=0, row=2, padx=(20, 0),
                                       sticky="w")
    
    selected_regular_price_lbl = ctk.CTkLabel(
        product_data_frm,
        text="Regular price:",
        text_color="#eee8aa",
        font=("Calibri", 16)
    )
    selected_regular_price_lbl.grid(column=1, row=2, sticky="w")
    
    selected_discount_price_lbl = ctk.CTkLabel(
        product_data_frm,
        text="Discount price:",
        text_color="#eee8aa",
        font=("Calibri", 16)
    )
    selected_discount_price_lbl.grid(column=2, row=2, sticky="w")
    
    selected_current_discount_val = ctk.CTkLabel(
        product_data_frm,
        text="-",
        text_color="white",
        font=("Calibri", 16)
    )
    selected_current_discount_val.grid(column=0, row=3, padx=(20, 0),
                                       pady=(0, 10), sticky="w")
    
    selected_regular_price_val = ctk.CTkLabel(
        product_data_frm,
        text="-",
        text_color="white",
        font=("Calibri", 16)
    )
    selected_regular_price_val.grid(column=1, row=3, pady=(0, 10), sticky="w")
    
    selected_discount_price_val = ctk.CTkLabel(
        product_data_frm,
        text="-",
        text_color="white",
        font=("Calibri", 16)
    )
    selected_discount_price_val.grid(column=2, row=3, pady=(0, 10), sticky="w")
    
    discount_buttons_frm = ctk.CTkFrame(discount_update_tl, fg_color="#100c08",
        corner_radius=0)
    discount_buttons_frm.pack(expand=True, fill="x")
    
    discount_quit_btn = ctk.CTkButton(
        discount_buttons_frm,
        width=120,
        fg_color="#1a1110",
        text_color="#eee8aa",
        hover_color="#4e1609",
        text="Quit",
        border_width=1,
        border_color="#eee8aa",
        font=("Calibri", 24, "bold"),
        corner_radius=10,
        command=discount_update_tl.destroy
    )
    discount_quit_btn.pack(padx=40, pady=40, ipady=3, side="right")
    
    new_discount_btn = ctk.CTkButton(
        discount_buttons_frm,
        width=120,
        fg_color="#1a1110",
        text_color="#eee8aa",
        hover_color="#4e1609",
        text="Update",
        border_width=1,
        border_color="#eee8aa",
        font=("Calibri", 24, "bold"),
        corner_radius=10,
        command=new_discount
    )
    new_discount_btn.pack(pady=40, ipady=3, side="right")


def inserting_data_into_treeview(treeview, combobox, spinbox, sum_label):
    """Adding a product and its amount to Treeview."""

    if not combobox.get():
        cmb.CTkMessagebox(
            title="No selected product",
            message="No product have been selected.",
            icon="info",
            button_width=100,
            button_color="#1a1110",
            button_hover_color="#4e1609",
            text_color="#eee8aa",
            title_color="#eee8aa",
            button_text_color="#eee8aa",
            font=("Calibri", 16),
            fg_color="#1a1110",
            bg_color="#100c08",
            corner_radius=10
        )
    else:
        # Previously added data
        previous_data = treeview.get_children()
    
        previous_lists = []
        for row in previous_data:
            row_values = treeview.item(row)["values"]
            previous_lists.append(row_values)
    
        # The previously requested quantity of the selected item
        previous_amount = 0
        for lst in previous_lists:
            if combobox.get() == lst[0]:
                previous_amount += lst[2]
    
        # The quantity of the item we are adding
        adding_amount = int(spinbox.get())
    
        # Required amount
        required_amount = previous_amount + adding_amount
    
        # Quantity of the selected item in stock
        stock_amount = int(products.products_df.quantity[
            products.products_df.name == combobox.get()
        ].to_string(index=False))
    
        if required_amount - stock_amount > 0:
            cmb.CTkMessagebox(
                title="Insufficient supplies",
                message="There is not enough of the selected item in stock.",
                icon="info",
                button_width=100,
                button_color="#1a1110",
                button_hover_color="#4e1609",
                text_color="#eee8aa",
                title_color="#eee8aa",
                button_text_color="#eee8aa",
                font=("Calibri", 16),
                fg_color="#1a1110",
                bg_color="#100c08",
                corner_radius=10
            )
        else:
            # Data to insert into Treeview
            product_to_add = combobox.get()
            amount_to_add = int(spinbox.get())
        
            price_and_discount = products.products_df[
                ["price", "discount"]][
                products.products_df.name == product_to_add
            ].values.flatten().tolist()
        
            price_to_add = discount_price_calculating(price_and_discount[0],
                price_and_discount[1])
            total_to_add = price_to_add * amount_to_add
        
            values_to_add = [product_to_add, price_to_add, amount_to_add,
                             total_to_add]
        
            # Inserting data
            treeview.insert("", index=END, values=values_to_add)
        
            # Update sum
            new_sum = update_sum(treeview)
            sum_label.configure(text=f"{new_sum:.2f} DIN")
        
            # Reset Combobox and Spinbox
            combobox.set("")
            spinbox.set("1")


def delete_treeview_row(treeview, sum_label):
    """Delete selected Treeview row."""

    tv_children = treeview.get_children()
    selected_item = treeview.selection()

    if len(tv_children) == 0:
        cmb.CTkMessagebox(
            title="No item",
            message="There are no items.",
            icon="info",
            button_width=100,
            button_color="#1a1110",
            button_hover_color="#4e1609",
            text_color="#eee8aa",
            title_color="#eee8aa",
            button_text_color="#eee8aa",
            font=("Calibri", 16),
            fg_color="#1a1110",
            bg_color="#100c08",
            corner_radius=10
        )
    elif not selected_item:
        cmb.CTkMessagebox(
            title="No selected row",
            message="No row in the Treeview are selected.",
            icon="info",
            button_width=100,
            button_color="#1a1110",
            button_hover_color="#4e1609",
            text_color="#eee8aa",
            title_color="#eee8aa",
            button_text_color="#eee8aa",
            font=("Calibri", 16),
            fg_color="#1a1110",
            bg_color="#100c08",
            corner_radius=10
        )
    else:
        treeview.delete(selected_item)
    
        # Update sum
        new_sum = update_sum(treeview)
        sum_label.configure(text=f"{new_sum:.2f} DIN")


def clear_all_items(treeview, sum_label):
    """Delete all items from the Treeview."""

    tv_children = treeview.get_children()

    if len(tv_children) == 0:
        cmb.CTkMessagebox(
            title="No item",
            message="There are no items.",
            icon="info",
            button_width=100,
            button_color="#1a1110",
            button_hover_color="#4e1609",
            text_color="#eee8aa",
            title_color="#eee8aa",
            button_text_color="#eee8aa",
            font=("Calibri", 16),
            fg_color="#1a1110",
            bg_color="#100c08",
            corner_radius=10
        )
    else:
        for item in treeview.get_children():
            treeview.delete(item)
    
        # Update sum
        new_sum = update_sum(treeview)
        sum_label.configure(text=f"{new_sum:.2f} DIN")


def discounts_pressed():
    """What happens when the 'Discount' button is pressed."""
    
    # Changes only occur if the main_frame_status variable is not 'Discount'
    if main_frame_status.get() != "Discounts":
        for widget in main_frm.winfo_children():
            widget.destroy()

        # Frame for title, discounts and their values
        discount_frm = ctk.CTkFrame(main_frm, fg_color="#100c08",
                                    corner_radius=0)
        discount_frm.pack(expand=True, fill="both")
        
        # Frame for the 'Setting' button
        update_button_frm = ctk.CTkFrame(main_frm, fg_color="#100c08",
                                         corner_radius=0)
        update_button_frm.pack(fill="x", side="right")
        
        # Title
        discounts_title_lbl = ctk.CTkLabel(
            discount_frm,
            text="DISCOUNTS",
            text_color="#eee8aa",
            font=("Calibri", 48, "bold"),
            anchor="center",
            justify="center"
        )
        discounts_title_lbl.grid(column=0, row=0, padx=40, pady=40, 
                                 columnspan=6, sticky="we")

        # Discount item codes
        codes = products.products_df.product_code[
            products.products_df.discount > 0].to_list()

        if codes:
            for i in range(len(codes)):
                name_type_price_discount_list = products.products_df[[
                    "name", "type", "price", "discount"]][
                    products.products_df.product_code == codes[i]
                ].values.flatten().tolist()
                
                # Find a group of item's type
                for key, value in ITEMS.items():
                    if name_type_price_discount_list[1] in value:
                        item_group = key
                    
                item_group_image = image_resize(
                    path=f"pics/{item_group.lower()}.png",
                    width=75,
                    height=75
                )
                    
                # Create a discount widgets
                discount_item_lbl = ctk.CTkLabel(
                    discount_frm,
                    text=name_type_price_discount_list[0],
                    text_color="white",
                    font=("Calibri", 24),
                    image=item_group_image,
                    compound="left"
                )
                discount_item_lbl.grid(column=0, row=2*i+1, columnspan=6,
                                       padx=(40, 0), pady=(20, 0), sticky="w")
                
                discount_type_lbl = ctk.CTkLabel(
                    discount_frm,
                    text="Type:",
                    text_color="#eee8aa",
                    font=("Calibri", 16)
                )
                discount_type_lbl.grid(column=0, row=2*(i+1), padx=(60, 0),
                                       pady=10, sticky="w")
                
                discount_type_val = ctk.CTkLabel(
                    discount_frm,
                    text=name_type_price_discount_list[1],
                    text_color="white",
                    font=("Calibri", 16)
                )
                discount_type_val.grid(column=1, row=2*(i+1), padx=(10, 20),
                                       pady=10, sticky="w")
                
                regular_price_lbl = ctk.CTkLabel(
                    discount_frm,
                    text="Regular Price:",
                    text_color="#eee8aa",
                    font=("Calibri", 16)
                )
                regular_price_lbl.grid(column=2, row=2*(i+1), padx=(20, 0),
                                       pady=10, sticky="w")
                
                strikeout_font = ctk.CTkFont(family="Calibri", size=16,
                                             overstrike=True)
                regular_price_val = ctk.CTkLabel(
                    discount_frm,
                    text=f"{name_type_price_discount_list[2]:.2f} DIN",
                    text_color="white",
                    font=strikeout_font
                )
                regular_price_val.grid(column=3, row=2*(i+1), padx=(10, 20),
                                       pady=10, sticky="w")
                
                real_price = name_type_price_discount_list[2]
                discount_price_value = discount_price_calculating(
                    real_price, name_type_price_discount_list[3])
                
                discount_price_lbl = ctk.CTkLabel(
                    discount_frm,
                    text="Discount Price:",
                    text_color="#eee8aa",
                    font=("Calibri", 16)
                )
                discount_price_lbl.grid(column=4, row=2*(i+1), padx=(20, 0),
                                        pady=10, sticky="w")
                
                discount_price_val = ctk.CTkLabel(
                    discount_frm,
                    text=f"{discount_price_value:.2f} DIN",
                    text_color="white",
                    font=("Calibri", 16, "bold"),
                    fg_color="darkred",
                    corner_radius=50
                )
                discount_price_val.grid(column=5, row=2 * (i + 1), ipadx=5,
                                        ipady=10, padx=(10, 0), pady=10,
                                        sticky="w")
        else:
            discount_frm.rowconfigure(1, weight=1)
            discount_frm.columnconfigure((0, 1), weight=1)
            ctk.CTkLabel(
                discount_frm,
                text="There are currently no discounts.",
                font=("Calibri", 40, "bold"),
                text_color="#7a0003",
                anchor="center",
                justify="center"
            ).grid(column=0, row=1, columnspan=6, padx=40, pady=(100, 200),
                   sticky="we")

        discount_update_btn = ctk.CTkButton(
            update_button_frm,
            width=120,
            fg_color="#1a1110",
            text_color="#eee8aa",
            hover_color="#4e1609",
            text="Update",
            border_width=1,
            border_color="#eee8aa",
            font=("Calibri", 24, "bold"),
            corner_radius=10,
            command=discount_update
        )
        discount_update_btn.pack(padx=40, pady=40, ipady=3, side="right")

        main_frame_status.set("Discounts")


def update_sum(treeview):
    """Updating the total price of items in the Treeview."""

    treeview_children = treeview.get_children()
    treeview_sum = 0
    for child in treeview_children:
        treeview_sum += float(treeview.item(child)["values"][3])
    
    return treeview_sum


def sale_pressed():
    """What happens when the 'Sale' button is pressed."""
    
    def bill_realization():
        """Bill realization of the items on the list."""

        tv_children = bill_table.get_children()
        
        if len(tv_children) == 0:
            cmb.CTkMessagebox(
                title="No item",
                message="There are no items.",
                icon="info",
                button_width=100,
                button_color="#1a1110",
                button_hover_color="#4e1609",
                text_color="#eee8aa",
                title_color="#eee8aa",
                button_text_color="#eee8aa",
                font=("Calibri", 16),
                fg_color="#1a1110",
                bg_color="#100c08",
                corner_radius=10
            )
        else:
            treeview_rows = bill_table.get_children()

            # Generate new bill number
            bill_numbers_list = sale.sale_df.bill_number.to_list()
            new_bill_number = unique_code_generating(bill_numbers_list, 10)

            for row in treeview_rows:
                row_values = bill_table.item(row)["values"]

                # Item code
                item_code = products.products_df.product_code[
                    products.products_df.name == row_values[0]
                ].to_string(index=False)
                
                # Item amount and price
                item_amount = row_values[2]
                item_price = float(row_values[3])
                
                # Current date
                current_date = date.today()
                
                sale_sql = f"""
                INSERT INTO sale (bill_number, product_code, amount, price,
                sale_date)
                VALUES ('{new_bill_number}', '{item_code}', {item_amount},
                {item_price}, '{current_date}');
                """
                sale.sale_entry_data(sale_sql)
                
                # Update new quantity of the product in stock
                old_quantity = int(products.products_df.quantity[
                    products.products_df.product_code == item_code
                ].to_string(index=False))
                new_quantity = old_quantity - item_amount
                
                quantity_sql = f"""
                UPDATE products
                SET quantity = '{new_quantity}'
                WHERE product_code = '{item_code}';
                """

                products.products_entry_data(quantity_sql)
                products.products_loading()
                
            clear_all_items(bill_table, sale_sum_val)
            sale.sale_loading()

    # Changes only occur if the main_frame_status variable is not 'Sale'
    if main_frame_status.get() != "Sale":
        for widget in main_frm.winfo_children():
            widget.destroy()
        
        # Frames inside main_frm
        sale_frm = ctk.CTkFrame(main_frm, fg_color="#100c08", corner_radius=0)
        sale_frm.pack(expand=True, fill="both")
        sale_frm.grid_columnconfigure(0, weight=1)
        
        sale_buttons_frm = ctk.CTkFrame(main_frm, fg_color="#100c08",
                                        corner_radius=0)
        sale_buttons_frm.pack(fill="x", side="right")

        # Title
        sale_title_lbl = ctk.CTkLabel(
            sale_frm,
            text="SALE",
            text_color="#eee8aa",
            font=("Calibri", 48, "bold")
        )
        sale_title_lbl.grid(column=0, row=0, padx=40, pady=40, sticky="we")
        
        # Product selection frame
        product_selection_frm = ctk.CTkFrame(sale_frm, fg_color="#100c08",
                                             corner_radius=0)
        product_selection_frm.grid(column=0, row=1, sticky="we")
        
        product_selection_frm.grid_columnconfigure((0, 1), weight=1)
        sale_product_select_lbl = ctk.CTkLabel(
            product_selection_frm,
            text="Product:",
            text_color="#eee8aa",
            font=("Calibri", 16)
        )
        sale_product_select_lbl.grid(column=0, row=0, padx=(40, 0), sticky="w")
        
        sale_amount_select_lbl = ctk.CTkLabel(
            product_selection_frm,
            text="Amount:",
            text_color="#eee8aa",
            font=("Calibri", 16)
        )
        sale_amount_select_lbl.grid(column=1, row=0, padx=(0, 40), sticky="w")

        # List of values
        product_names = products.products_df.name.to_list()
        product_names.sort(key=lambda x: x.casefold())
        
        sale_product_select_cb = ttk.Combobox(
            product_selection_frm,
            width=70,
            state="readonly",
            values=product_names
        )
        sale_product_select_cb.grid(column=0, row=1, padx=(40, 0),
                                    pady=(0, 20), sticky="w")

        sale_amount_select_sb = ttk.Spinbox(
            product_selection_frm,
            width=8,
            from_=1,
            to=20,
            font="Calibri",
            state="readonly"
        )
        sale_amount_select_sb.grid(column=1, row=1, padx=(0, 40), pady=(0, 20),
                                   sticky="w")
        sale_amount_select_sb.set(1)
        
        # Treeview frame
        tv_frm = ctk.CTkFrame(sale_frm, corner_radius=0,
                              fg_color="transparent")
        tv_frm.grid(column=0, row=2, padx=40, pady=(20, 10), sticky="w")
        
        # Column names for Treeview
        treeview_columns = ["product", "price", "amount", "total"]
        
        bill_table = ttk.Treeview(
            tv_frm,
            columns=treeview_columns,
            show="headings",
            height=8,
            selectmode="browse",
            style="tv_style.Treeview"
        )
        
        # Heading names
        bill_table.heading("product", text="Product")
        bill_table.heading("price", text="Price")
        bill_table.heading("amount", text="Amount")
        bill_table.heading("total", text="Total")
        
        # The width of the columns and the position of the text in them
        bill_table.column("product", width=450, anchor="w")
        bill_table.column("price", width=120, anchor="e")
        bill_table.column("amount", width=70, anchor="e")
        bill_table.column("total", width=120, anchor="e")
        
        bill_table.pack(side="left")
        
        # Scrollbar for Treeview
        treeview_scroll = ttk.Scrollbar(
            tv_frm,
            orient="vertical",
            command=bill_table.yview
        )
        
        treeview_scroll.bind(
            "<MouseWheel>",
            lambda event: bill_table.yview_scroll(-int(event.delta / 60),
                                                  "units")
        )
        
        treeview_scroll.pack(fill="y", side="right")
        
        bill_table.configure(yscrollcommand=treeview_scroll.set)
        
        # Sum frame
        sum_frm = ctk.CTkFrame(sale_frm, fg_color="#100c08", corner_radius=0)
        sum_frm.grid(column=0, row=3, sticky="we")
        
        sale_sum_val = ctk.CTkLabel(
            sum_frm,
            text="0.00 DIN",
            text_color="white",
            width=150,
            font=("Calibri", 22, "bold"),
            anchor="e"
        )
        sale_sum_val.pack(padx=(0, 80), pady=(10, 0), side="right")
        
        sale_sum_lbl = ctk.CTkLabel(
            sum_frm,
            text="SUM:",
            text_color="#eee8aa",
            font=("Calibri", 22, "bold")
        )
        sale_sum_lbl.pack(padx=10, pady=(10, 0), side="right")
        
        # Buttons
        sale_realize_btn = ctk.CTkButton(
            sale_buttons_frm,
            width=120,
            fg_color="#1a1110",
            text_color="#eee8aa",
            hover_color="#4e1609",
            text="Realize",
            border_width=1,
            border_color="#eee8aa",
            font=("Calibri", 24, "bold"),
            corner_radius=10,
            command=bill_realization
        )
        sale_realize_btn.pack(padx=40, pady=40, ipady=3, side="right")
    
        sale_clear_all_btn = ctk.CTkButton(
            sale_buttons_frm,
            width=120,
            fg_color="#1a1110",
            text_color="#eee8aa",
            hover_color="#4e1609",
            text="Clear All",
            border_width=1,
            border_color="#eee8aa",
            font=("Calibri", 24, "bold"),
            corner_radius=10,
            command=lambda: clear_all_items(bill_table, sale_sum_val)
        )
        sale_clear_all_btn.pack(pady=40, ipady=3, side="right")
    
        sale_delete_btn = ctk.CTkButton(
            sale_buttons_frm,
            width=120,
            fg_color="#1a1110",
            text_color="#eee8aa",
            hover_color="#4e1609",
            text="Delete",
            border_width=1,
            border_color="#eee8aa",
            font=("Calibri", 24, "bold"),
            corner_radius=10,
            command=lambda: delete_treeview_row(bill_table, sale_sum_val)
        )
        sale_delete_btn.pack(padx=40, pady=40, ipady=3, side="right")
    
        sale_add_btn = ctk.CTkButton(
            sale_buttons_frm,
            width=120,
            fg_color="#1a1110",
            text_color="#eee8aa",
            hover_color="#4e1609",
            text="Add",
            border_width=1,
            border_color="#eee8aa",
            font=("Calibri", 24, "bold"),
            corner_radius=10,
            command=lambda: inserting_data_into_treeview(
                bill_table, sale_product_select_cb, sale_amount_select_sb,
                sale_sum_val)
        )
        sale_add_btn.pack(pady=40, ipady=3, side="right")
    
        main_frame_status.set("Sale")


def items_pressed():
    """What happens when the 'Items' button is pressed."""
    
    def display_items(dataframe):
        """Display of data depending on the selected criteria."""

        # Header labels
        ctk.CTkLabel(
            data_frm,
            text="Product Name",
            text_color="#7a0003",
            font=("Calibri", 20, "bold")
        ).grid(column=0, row=0, pady=(0, 10))

        ctk.CTkLabel(
            data_frm,
            text="Manufacturer",
            text_color="#7a0003",
            font=("Calibri", 20, "bold")
        ).grid(column=1, row=0, pady=(0, 10))

        ctk.CTkLabel(
            data_frm,
            text="Type",
            text_color="#7a0003",
            font=("Calibri", 20, "bold")
        ).grid(column=2, row=0, pady=(0, 10))

        ctk.CTkLabel(
            data_frm,
            text="Amount",
            text_color="#7a0003",
            font=("Calibri", 16, "bold")
        ).grid(column=3, row=0, pady=(0, 10))

        ctk.CTkLabel(
            data_frm,
            text="Price",
            text_color="#7a0003",
            font=("Calibri", 20, "bold")
        ).grid(column=4, row=0, pady=(0, 10))

        for i in range(len(dataframe)):
            # Initial data
            row_data = dataframe.iloc[i].values.flatten().tolist()
    
            data_frm.columnconfigure((0, 1, 2, 3, 4), weight=1)
    
            # Data display
            ctk.CTkLabel(
                data_frm,
                text=row_data[1],
                text_color="#eee8aa",
                font=("Calibri", 16)
            ).grid(column=0, row=i + 1, padx=(0, 5), sticky="w")
    
            ctk.CTkLabel(
                data_frm,
                text=row_data[2],
                text_color="#eee8aa",
                font=("Calibri", 16)
            ).grid(column=1, row=i + 1, padx=5, sticky="w")
    
            ctk.CTkLabel(
                data_frm,
                text=row_data[3],
                text_color="#eee8aa",
                font=("Calibri", 16)
            ).grid(column=2, row=i + 1, padx=5, sticky="w")
    
            ctk.CTkLabel(
                data_frm,
                text=row_data[4],
                text_color="#eee8aa",
                font=("Calibri", 16)
            ).grid(column=3, row=i + 1, padx=5)
            
            ctk.CTkLabel(
                data_frm,
                text=f"{row_data[5]:.2f}",
                text_color="#eee8aa",
                font=("Calibri", 16)
            ).grid(column=4, row=i + 1, padx=(5, 0), sticky="e")
    
    def manufacturer_filter_selected(event):
        """Reset the other two filters."""
        
        type_filter_cb.set("")
        group_filter_cb.set("")

    def type_filter_selected(event):
        """Reset the other two filters."""
        
        manufacturer_filter_cb.set("")
        group_filter_cb.set("")

    def group_filter_selected(event):
        """Reset the other two filters."""
        
        manufacturer_filter_cb.set("")
        type_filter_cb.set("")
    
    def reset_choices():
        """Reset Radiobutton and all Comboboxes."""
        sort_data_var.set("1")
        manufacturer_filter_cb.set("")
        type_filter_cb.set("")
        group_filter_cb.set("")

    def apply_choices():
        """Applying of sorting options and selected data."""
        
        # Deleting previous data
        for element in data_frm.winfo_children():
            element.destroy()
        
        if manufacturer_filter_cb.get():
            dataframe = products.products_df[
                products.products_df.manufacturer ==
                manufacturer_filter_cb.get()]
        elif type_filter_cb.get():
            dataframe = products.products_df[
                products.products_df.type == type_filter_cb.get()]
        elif group_filter_cb.get():
            for key, value in ITEMS.items():
                if key == group_filter_cb.get():
                    group_values = value
            dataframe = products.products_df[
                products.products_df.type.isin(group_values)]
        else:
            dataframe = products.products_df
        
        if sort_data_var.get() == "1":
            sorted_df = dataframe.sort_values(by="name", key=lambda col:
            col.str.casefold())
        elif sort_data_var.get() == "2":
            sorted_df = dataframe.sort_values(
                by=["manufacturer", "name"], key=lambda col:
                col.str.casefold())
        elif sort_data_var.get() == "3":
            sorted_df = dataframe.sort_values(
                by=["type", "name"], key=lambda col: col.str.casefold())
        elif sort_data_var.get() == "4":
            sorted_df = dataframe.sort_values(by="quantity")
        elif sort_data_var.get() == "5":
            sorted_df = dataframe.sort_values(by="price")
        elif sort_data_var.get() == "6":
            sorted_df = dataframe.sort_values(by="price", ascending=False)
            
        display_items(sorted_df)

    # Changes only occur if the main_frame_status variable is not 'Items'
    if main_frame_status.get() != "Products":
        for widget in main_frm.winfo_children():
            widget.destroy()

        # Title
        items_title_lbl = ctk.CTkLabel(
            main_frm,
            text="PRODUCT REVIEW",
            text_color="#eee8aa",
            font=("Calibri", 48, "bold")
        )
        items_title_lbl.pack(expand=True, fill="x", padx=40, pady=40)
        
        # A frame for the other two frames and 'Reset' button
        criteria_frm = ctk.CTkFrame(main_frm, corner_radius=0,
                                    fg_color="transparent")
        criteria_frm.pack(expand=True, fill="x")
        
        # Sorting frame
        sorting_data_frm = ctk.CTkFrame(
            criteria_frm,
            border_width=1,
            border_color="#eee8aa"
        )
        sorting_data_frm.pack(expand=True, fill="both", pady=10, padx=20,
                              side="left")

        # Sorting frame title
        sorting_frm_title = ctk.CTkLabel(
            sorting_data_frm,
            fg_color="black",
            text="Sort Data",
            font=("Calibri", 16),
            anchor="center"
        )
        sorting_frm_title.pack(fill="x", padx=2, pady=2)
        
        # Radiobuttons
        sort_data_var = ctk.StringVar(sorting_data_frm, "1")
        sort_data_values = {
            "Product Name": "1",
            "Manufacturer": "2",
            "Product Type": "3",
            "Product Amount": "4",
            "Price - ascending": "5",
            "Price - descending": "6"
        }

        for key, value in sort_data_values.items():
            if value == "1":
                y_pad = (10, 5)
            elif value == "6":
                y_pad = (5, 15)
            else:
                y_pad = 5
    
            ctk.CTkRadioButton(
                sorting_data_frm,
                text=key,
                value=value,
                variable=sort_data_var,
                text_color="#eee8aa",
                border_color="#eee8aa",
                fg_color="#7a0003",
                hover_color="#7a0003",
                border_width_checked=4,
                border_width_unchecked=2,
                radiobutton_width=15,
                radiobutton_height=15,
                font=("Calibri", 16)
            ).pack(fill="x", padx=40, pady=y_pad)
        
        # Filters frame
        filters_frm = ctk.CTkFrame(
            criteria_frm,
            border_width=1,
            border_color="#eee8aa"
        )
        filters_frm.pack(expand=True, fill="both", pady=10, padx=20,
                         side="left")
        
        # Filters frame title
        filters_frm_title = ctk.CTkLabel(
            filters_frm,
            fg_color="black",
            text="Filter Data",
            font=("Calibri", 16),
            anchor="center"
        )
        filters_frm_title.pack(fill="x", padx=2, pady=2)
        
        # Other widgets
        manufacturer_filter_lbl = ctk.CTkLabel(
            filters_frm,
            text="Manufacturer:",
            text_color="#eee8aa",
            font=("Calibri", 16)
        )
        manufacturer_filter_lbl.pack(padx=40, pady=(10, 0), anchor="w")

        manufacturer_list = list(
            set(products.products_df.manufacturer.to_list()))
        manufacturer_list.sort(key=lambda x: x.casefold())
        
        manufacturer_filter_cb = ttk.Combobox(
            filters_frm,
            width=40,
            state="readonly",
            values=manufacturer_list
        )
        manufacturer_filter_cb.pack(padx=40, pady=(0, 10), anchor="w")
        manufacturer_filter_cb.bind("<MouseWheel>", disable_scroll)
        manufacturer_filter_cb.bind("<<ComboboxSelected>>",
                                    manufacturer_filter_selected)

        type_filter_lbl = ctk.CTkLabel(
            filters_frm,
            text="Type:",
            text_color="#eee8aa",
            font=("Calibri", 16),
            anchor="w"
        )
        type_filter_lbl.pack(padx=40, pady=(10, 0), anchor="w")

        type_list = list(set(products.products_df.type.to_list()))
        type_list.sort(key=lambda x: x.casefold())

        type_filter_cb = ttk.Combobox(
            filters_frm,
            width=40,
            state="readonly",
            values=type_list
        )
        type_filter_cb.pack(padx=40, pady=(0, 10), anchor="w")
        type_filter_cb.bind("<MouseWheel>", disable_scroll)
        type_filter_cb.bind("<<ComboboxSelected>>", type_filter_selected)

        group_filter_lbl = ctk.CTkLabel(
            filters_frm,
            text="Group:",
            text_color="#eee8aa",
            font=("Calibri", 16),
            anchor="w"
        )
        group_filter_lbl.pack(padx=40, pady=(10, 0), anchor="w")

        group_list = list(ITEMS.keys())
        group_list.sort()

        group_filter_cb = ttk.Combobox(
            filters_frm,
            width=40,
            state="readonly",
            values=group_list
        )
        group_filter_cb.pack(padx=40, pady=(0, 20), anchor="w")
        group_filter_cb.bind("<MouseWheel>", disable_scroll)
        group_filter_cb.bind("<<ComboboxSelected>>", group_filter_selected)

        # Reset choices button
        reset_choices_btn = ctk.CTkButton(
            criteria_frm,
            width=120,
            fg_color="#1a1110",
            text_color="#eee8aa",
            hover_color="#4e1609",
            text="Reset",
            border_width=1,
            border_color="#eee8aa",
            font=("Calibri", 24, "bold"),
            corner_radius=10,
            command=reset_choices
        )
        reset_choices_btn.pack(padx=(20, 40), pady=10, ipady=3,
                               side="bottom", anchor="e")
        
        # Apply choices button
        apply_choices_btn = ctk.CTkButton(
            criteria_frm,
            width=120,
            fg_color="#1a1110",
            text_color="#eee8aa",
            hover_color="#4e1609",
            text="Apply",
            border_width=1,
            border_color="#eee8aa",
            font=("Calibri", 24, "bold"),
            corner_radius=10,
            command=apply_choices
        )
        apply_choices_btn.pack(padx=(20, 40), pady=10, ipady=3,
                               side="bottom", anchor="e")
        
        # Data frame
        data_frm = ctk.CTkFrame(main_frm, corner_radius=0,
                                fg_color="transparent")
        data_frm.pack(expand=True, fill="both", pady=15, padx=20)
        
        # Required data and their display
        all_data = products.products_df.sort_values(by="name", key=lambda col:
        col.str.casefold())
        
        display_items(all_data)
        
    main_frame_status.set("Products")


def order_pressed():
    """What happens when the 'Order' button is pressed."""
    
    def display_order_values(event):
        """Value display for the selected order."""
        
        for widget in order_details_frm.winfo_children():
            widget.destroy()
        
        # Data needed
        selected_order_values = orders.orders_df[
            orders.orders_df.order_code == order_select_cb.get()
        ].values.flatten().tolist()
        
        order_code_df = order_items.order_items_df[
            order_items.order_items_df.order_code == order_select_cb.get()]
        
        order_item_list = []
        for index, rows in order_code_df.iterrows():
            row_list = [rows.product_code, rows.price, rows.amount]
            order_item_list.append(row_list)
        
        # Value display
        customer_name_val.configure(text=selected_order_values[1])
        order_status_cb.configure(state="readonly")
        order_status_cb.set(selected_order_values[5])
        customer_address_val.configure(text=selected_order_values[2])
        customer_phone_val.configure(text=selected_order_values[3])
        
        order_details_frm.grid_columnconfigure((0, 1, 2), weight=1)
        
        total_price = 0
        counter = 0
        for i in range(len(order_item_list)):
            item_name = products.products_df.name[
                products.products_df.product_code == order_item_list[i][0]
            ].to_string(index=False)
            
            ctk.CTkLabel(
                order_details_frm,
                text=order_item_list[i][2],
                text_color="white",
                font=("Calibri", 20)
            ).grid(column=0, row=i, pady=10, sticky="e")
            
            ctk.CTkLabel(
                order_details_frm,
                text=item_name,
                text_color="white",
                font=("Calibri", 20)
            ).grid(column=1, row=i, padx=40, pady=10, sticky="w")
            
            ctk.CTkLabel(
                order_details_frm,
                text=f"{order_item_list[i][1]:.2f} DIN",
                text_color="white",
                font=("Calibri", 20)
            ).grid(column=2, row=i, pady=10, sticky="e")
            
            total_price += order_item_list[i][1]
            counter += 1
        
        ctk.CTkLabel(
            order_details_frm,
            text=f"TOTAL: {total_price:.2f} DIN",
            text_color="#eee8aa",
            font=("Calibri", 20)
        ).grid(column=2, row=counter, pady=5, sticky="e")

    def status_change():
        """Change of shipment status."""
        
        if not order_select_cb.get():
            cmb.CTkMessagebox(
                title="No selected order",
                message="No order have been selected.",
                icon="info",
                button_width=100,
                button_color="#1a1110",
                button_hover_color="#4e1609",
                text_color="#eee8aa",
                title_color="#eee8aa",
                button_text_color="#eee8aa",
                font=("Calibri", 16),
                fg_color="#1a1110",
                bg_color="#100c08",
                corner_radius=10
            )
        else:
            selected_order_code = order_select_cb.get()
            selected_order_status = orders.orders_df.status[
                orders.orders_df.order_code == selected_order_code
            ].to_string(index=False)
            
            if selected_order_status == order_status_cb.get():
                cmb.CTkMessagebox(
                    title="No change",
                    message="The status remained the same.",
                    icon="info",
                    button_width=100,
                    button_color="#1a1110",
                    button_hover_color="#4e1609",
                    text_color="#eee8aa",
                    title_color="#eee8aa",
                    button_text_color="#eee8aa",
                    font=("Calibri", 16),
                    fg_color="#1a1110",
                    bg_color="#100c08",
                    corner_radius=10
                )
            else:
                status_sql = f"""
                UPDATE orders
                SET status = '{order_status_cb.get()}'
                WHERE order_code = '{selected_order_code}';
                """
                
                orders.orders_entry_data(status_sql)
                orders.orders_loading()

                cmb.CTkMessagebox(
                    title="Change successful",
                    message="Status change completed successfully.",
                    icon="info",
                    button_width=100,
                    button_color="#1a1110",
                    button_hover_color="#4e1609",
                    text_color="#eee8aa",
                    title_color="#eee8aa",
                    button_text_color="#eee8aa",
                    font=("Calibri", 16),
                    fg_color="#1a1110",
                    bg_color="#100c08",
                    corner_radius=10
                )
    
    def create_new_order():
        """Creating new order."""

        # Toplevel
        new_order_tl = ctk.CTkToplevel(root, fg_color="#100c08")
        new_order_tl.title("New Order")
        new_order_tl.attributes("-topmost", "true")
        new_order_tl.resizable(False, False)
        new_order_tl.grab_set()
        new_order_tl.after(200, lambda: new_order_tl.iconbitmap(
            "pics/abstract.ico"))

        def new_order_realization():
            """Creating an order and inserting data into the 'orders' table."""
            
            # Treeview items
            treeview_children = cart_treeview.get_children()

            # Order code list and a new code
            order_code_list = existing_code_list
            new_code = new_order_code
            
            # Customer data and date
            new_name = new_order_customer_val.get()
            new_address = new_order_address_val.get()
            new_phone = new_order_phone_val.get()
            date_today = date.today()
            
            if not new_name:
                cmb.CTkMessagebox(
                    title="Missing name",
                    message="You have not entered the orderer's name.",
                    icon="info",
                    button_width=100,
                    button_color="#1a1110",
                    button_hover_color="#4e1609",
                    text_color="#eee8aa",
                    title_color="#eee8aa",
                    button_text_color="#eee8aa",
                    font=("Calibri", 16),
                    fg_color="#1a1110",
                    bg_color="#100c08",
                    corner_radius=10
                )
            elif not new_address:
                cmb.CTkMessagebox(
                    title="Missing address",
                    message="You have not entered the orderer's address.",
                    icon="info",
                    button_width=100,
                    button_color="#1a1110",
                    button_hover_color="#4e1609",
                    text_color="#eee8aa",
                    title_color="#eee8aa",
                    button_text_color="#eee8aa",
                    font=("Calibri", 16),
                    fg_color="#1a1110",
                    bg_color="#100c08",
                    corner_radius=10
                )
            elif not new_phone:
                cmb.CTkMessagebox(
                    title="Missing phone",
                    message="You have not entered the orderer's phone.",
                    icon="info",
                    button_width=100,
                    button_color="#1a1110",
                    button_hover_color="#4e1609",
                    text_color="#eee8aa",
                    title_color="#eee8aa",
                    button_text_color="#eee8aa",
                    font=("Calibri", 16),
                    fg_color="#1a1110",
                    bg_color="#100c08",
                    corner_radius=10
                )
            elif len(treeview_children) == 0:
                cmb.CTkMessagebox(
                    title="No item",
                    message="There are no items.",
                    icon="info",
                    button_width=100,
                    button_color="#1a1110",
                    button_hover_color="#4e1609",
                    text_color="#eee8aa",
                    title_color="#eee8aa",
                    button_text_color="#eee8aa",
                    font=("Calibri", 16),
                    fg_color="#1a1110",
                    bg_color="#100c08",
                    corner_radius=10
                )
            else:
                new_order_sql = f"""
                INSERT INTO orders (order_code, customer_name,
                customer_address, customer_phone, order_date, status)
                VALUES ('{new_code}', '{new_name}', '{new_address}',
                '{new_phone}', '{date_today}', 'Received');
                """
                orders.orders_entry_data(new_order_sql)
                
                treeview_rows = cart_treeview.get_children()
                for row in treeview_rows:
                    row_values = cart_treeview.item(row)["values"]
                    
                    item_code = products.products_df.product_code[
                        products.products_df.name == row_values[0]
                    ].to_string(index=False)
                    item_price = float(row_values[3])
                    item_amount = row_values[2]
                    
                    new_order_items_sql = f"""
                    INSERT INTO order_items (order_code, product_code,
                    price, amount)
                    VALUES ('{new_code}', '{item_code}',
                    {item_price}, {item_amount});
                    """
                    order_items.order_items_entry_data(new_order_items_sql)

                    # Update new quantity of the product in stock
                    old_amount = int(products.products_df.quantity[
                        products.products_df.product_code == item_code
                    ].to_string(index=False))
                    new_amount = old_amount - item_amount
                    
                    new_amount_sql = f"""
                    UPDATE products
                    SET quantity = '{new_amount}'
                    WHERE product_code = '{item_code}';
                    """
                    
                    products.products_entry_data(new_amount_sql)
                    products.products_loading()

                # Clear entry widgets
                new_order_customer_val.delete(0, END)
                new_order_address_val.delete(0, END)
                new_order_phone_val.delete(0, END)
            
                # Generating and setting a code for a new order
                order_code_list.append(new_code)
                new_code = unique_code_generating(order_code_list, 10)
                new_order_code_val.configure(text=new_code)
            
                # Clear all treeview items
                clear_all_items(cart_treeview, order_sum_val)
                
                # Refresh 'orders' and 'order_items' tables
                orders.orders_loading()
                order_items.order_items_loading()
                
                # Update Combobox values
                code_values = orders.orders_df.order_code.to_list()
                code_values.sort()
                order_select_cb.configure(values=code_values)

        # Title label
        new_order_title_lbl = ctk.CTkLabel(
            new_order_tl,
            text="NEW ORDER",
            text_color="#7a0003",
            font=("Calibri", 48, "bold")
        )
        new_order_title_lbl.pack(ipady=40)
        
        # Frames and their titles
        customer_data_frm = ctk.CTkFrame(
            new_order_tl,
            border_width=1,
            border_color="#eee8aa"
        )
        customer_data_frm.pack(expand=True, fill="x", pady=10, padx=50)
        
        customer_data_frm_title = ctk.CTkLabel(
            customer_data_frm,
            fg_color="black",
            text="Customer Data",
            font=("Calibri", 16),
            anchor="center"
        )
        customer_data_frm_title.grid(column=0, row=0, columnspan=2, padx=2,
                                     pady=2, sticky="we")
        
        cart_frm = ctk.CTkFrame(
            new_order_tl,
            border_width=1,
            border_color="#eee8aa"
        )
        cart_frm.pack(expand=True, fill="x", pady=10, padx=50)

        cart_frm_title = ctk.CTkLabel(
            cart_frm,
            fg_color="black",
            text="Cart",
            font=("Calibri", 16),
            anchor="center"
        )
        cart_frm_title.grid(column=0, row=0, columnspan=2, padx=2, pady=2,
                            sticky="we")

        new_order_button_frm = ctk.CTkFrame(new_order_tl, corner_radius=0,
                                            fg_color="transparent")
        new_order_button_frm.pack(fill="x", pady=10, padx=50)
        
        # Customer data frame
        customer_data_frm.grid_columnconfigure((0, 1), weight=1)
        
        new_order_customer_lbl = ctk.CTkLabel(
            customer_data_frm,
            text="Customer Name:",
            text_color="#eee8aa",
            font=("Calibri", 16)
        )
        new_order_customer_lbl.grid(column=0, row=1, padx=20, pady=(10, 0),
                                    sticky="w")
        
        new_order_customer_val = ctk.CTkEntry(
            customer_data_frm,
            width=250,
            font=("Calibri", 18),
            placeholder_text="Enter name..."
        )
        new_order_customer_val.grid(column=0, row=2, padx=20, pady=(0, 5),
                                    sticky="w")
        
        new_order_code_lbl = ctk.CTkLabel(
            customer_data_frm,
            text="Order Code:",
            text_color="#eee8aa",
            font=("Calibri", 16)
        )
        new_order_code_lbl.grid(column=1, row=1, padx=20, pady=(10, 0),
                                sticky="w")

        # Generating a code for a new order
        existing_code_list = orders.orders_df.order_code.to_list()
        new_order_code = unique_code_generating(existing_code_list, 10)

        new_order_code_val = ctk.CTkLabel(
            customer_data_frm,
            text=new_order_code,
            text_color="white",
            font=("Calibri", 18)
        )
        new_order_code_val.grid(column=1, row=2, padx=20, pady=(0, 5),
                                    sticky="w")
        
        new_order_address_lbl = ctk.CTkLabel(
            customer_data_frm,
            text="Customer Address:",
            text_color="#eee8aa",
            font=("Calibri", 16)
        )
        new_order_address_lbl.grid(column=0, row=3, padx=20, pady=(5, 0),
                                   sticky="w")
        
        new_order_address_val = ctk.CTkEntry(
            customer_data_frm,
            width=250,
            font=("Calibri", 18),
            placeholder_text="Enter address..."
        )
        new_order_address_val.grid(column=0, row=4, padx=20, pady=(0, 20),
                                   sticky="w")
        
        new_order_phone_lbl = ctk.CTkLabel(
            customer_data_frm,
            text="Customer Phone:",
            text_color="#eee8aa",
            font=("Calibri", 16)
        )
        new_order_phone_lbl.grid(column=1, row=3, padx=20, pady=(5, 0),
                                 sticky="w")
        
        new_phone_reg = customer_data_frm.register(
            lambda inp: len_digit_limit(inp, length=10))
        new_order_phone_val = ctk.CTkEntry(
            customer_data_frm,
            width=250,
            font=("Calibri", 18),
            validate="key",
            validatecommand=(new_phone_reg, "%P")
        )
        new_order_phone_val.grid(column=1, row=4, padx=20, pady=(0, 20),
                                 sticky="w")

        # Cart data frame
        cart_frm.grid_columnconfigure((0, 1), weight=1)
        
        new_order_products_lbl= ctk.CTkLabel(
            cart_frm,
            text="Product:",
            text_color="#eee8aa",
            font=("Calibri", 16)
        )
        new_order_products_lbl.grid(column=0, row=1, padx=20, pady=(10, 0),
                                    sticky="w")

        new_order_amount_lbl = ctk.CTkLabel(
            cart_frm,
            text="Amount:",
            text_color="#eee8aa",
            font=("Calibri", 16)
        )
        new_order_amount_lbl.grid(column=1, row=1, padx=20, pady=(10, 0),
                                  sticky="w")
        
        # Value list
        product_list = products.products_df.name.to_list()
        product_list.sort(key=lambda x: x.casefold())

        new_order_products_cb = ttk.Combobox(
            cart_frm,
            width=70,
            state="readonly",
            values=product_list
        )
        new_order_products_cb.grid(column=0, row=2, padx=20, pady=(0, 10),
                                   sticky="w")

        new_order_amount_sb = ttk.Spinbox(
            cart_frm,
            width=8,
            from_=1,
            to=30,
            font="Calibri",
            state="readonly"
        )
        new_order_amount_sb.grid(column=1, row=2, padx=20, pady=(0, 10),
                                 sticky="w")
        new_order_amount_sb.set(1)
        
        # Frame for Treeview
        cart_tv_frm = ctk.CTkFrame(cart_frm, corner_radius=0,
                                   fg_color="transparent")
        cart_tv_frm.grid(column=0, row=3, columnspan=2, padx=20, pady=20)
        
        # Cart Treeview
        cart_tv_columns = ["product", "price", "amount", "total"]
        
        cart_treeview = ttk.Treeview(
            cart_tv_frm,
            columns=cart_tv_columns,
            show="headings",
            height=12,
            selectmode="browse",
            style="tv_style.Treeview"
        )

        # Heading names
        cart_treeview.heading("product", text="Product")
        cart_treeview.heading("price", text="Price")
        cart_treeview.heading("amount", text="Amount")
        cart_treeview.heading("total", text="Total")

        # The width of the columns and the position of the text in them
        cart_treeview.column("product", width=450, anchor="w")
        cart_treeview.column("price", width=120, anchor="e")
        cart_treeview.column("amount", width=70, anchor="e")
        cart_treeview.column("total", width=120, anchor="e")
        
        cart_treeview.pack(side="left")

        # Scrollbar for Treeview
        cart_tv_scroll = ttk.Scrollbar(cart_tv_frm, orient="vertical",
                                       command=cart_treeview.yview)

        cart_tv_scroll.bind(
            "<MouseWheel>",
            lambda event: cart_treeview.yview_scroll(-int(event.delta / 60),
                                                     "units"))

        cart_tv_scroll.pack(fill="y", side="right")

        cart_treeview.configure(yscrollcommand=cart_tv_scroll.set)

        # Sum frame
        cart_sum_frm = ctk.CTkFrame(cart_frm, corner_radius=0,
                                    fg_color="transparent")
        cart_sum_frm.grid(column=0, row=4, columnspan=2, padx=20, pady=(0, 20),
                          sticky="we")

        order_sum_val = ctk.CTkLabel(
            cart_sum_frm,
            text="0.00 DIN",
            text_color="white",
            width=150,
            font=("Calibri", 22, "bold"),
            anchor="e"
        )
        order_sum_val.pack(side="right")

        order_sum_lbl = ctk.CTkLabel(
            cart_sum_frm,
            text="SUM:",
            text_color="#eee8aa",
            font=("Calibri", 22, "bold")
        )
        order_sum_lbl.pack(padx=10, side="right")
        
        # Buttons
        new_order_exit_btn = ctk.CTkButton(
            new_order_button_frm,
            width=120,
            fg_color="#1a1110",
            text_color="#eee8aa",
            hover_color="#4e1609",
            text="Exit",
            border_width=1,
            border_color="#eee8aa",
            font=("Calibri", 24, "bold"),
            corner_radius=10,
            command=new_order_tl.destroy
        )
        new_order_exit_btn.pack(padx=(20, 0), pady=20, ipady=3, side="right")
        
        new_order_create_btn = ctk.CTkButton(
            new_order_button_frm,
            width=120,
            fg_color="#1a1110",
            text_color="#eee8aa",
            hover_color="#4e1609",
            text="Create",
            border_width=1,
            border_color="#eee8aa",
            font=("Calibri", 24, "bold"),
            corner_radius=10,
            command=new_order_realization
        )
        new_order_create_btn.pack(padx=20, pady=20, ipady=3, side="right")
        
        new_order_clear_all_btn = ctk.CTkButton(
            new_order_button_frm,
            width=120,
            fg_color="#1a1110",
            text_color="#eee8aa",
            hover_color="#4e1609",
            text="Clear All",
            border_width=1,
            border_color="#eee8aa",
            font=("Calibri", 24, "bold"),
            corner_radius=10,
            command=lambda: clear_all_items(cart_treeview, order_sum_val)
        )
        new_order_clear_all_btn.pack(padx=20, pady=20, ipady=3, side="right")
        
        new_order_delete_btn = ctk.CTkButton(
            new_order_button_frm,
            width=120,
            fg_color="#1a1110",
            text_color="#eee8aa",
            hover_color="#4e1609",
            text="Delete",
            border_width=1,
            border_color="#eee8aa",
            font=("Calibri", 24, "bold"),
            corner_radius=10,
            command=lambda: delete_treeview_row(cart_treeview, order_sum_val)
        )
        new_order_delete_btn.pack(padx=20, pady=20, ipady=3, side="right")
        
        new_order_add_btn = ctk.CTkButton(
            new_order_button_frm,
            width=120,
            fg_color="#1a1110",
            text_color="#eee8aa",
            hover_color="#4e1609",
            text="Add",
            border_width=1,
            border_color="#eee8aa",
            font=("Calibri", 24, "bold"),
            corner_radius=10,
            command=lambda: inserting_data_into_treeview(
                cart_treeview, new_order_products_cb, new_order_amount_sb,
                order_sum_val)
        )
        new_order_add_btn.pack(padx=20, pady=20, ipady=3, side="right")
    
    # Changes only occur if the main_frame_status variable is not 'Sale'
    if main_frame_status.get() != "Orders":
        for widget in main_frm.winfo_children():
            widget.destroy()
    
        # Frames
        order_frm = ctk.CTkFrame(main_frm, corner_radius=0,
                                 fg_color="transparent")
        order_frm.pack(expand=True, fill="both")
        order_frm.grid_columnconfigure((0, 1), weight=1)
        
        order_buttons_frm = ctk.CTkFrame(main_frm, corner_radius=0,
                                         fg_color="transparent")
        order_buttons_frm.pack(fill="x", side="right")
        
        # Title
        order_title_lbl = ctk.CTkLabel(
            order_frm,
            text="ORDERS",
            text_color="#eee8aa",
            font=("Calibri", 48, "bold")
        )
        order_title_lbl.grid(column=0, row=0, columnspan=2, padx=40, pady=40)
        
        # Order frame
        order_select_lbl = ctk.CTkLabel(
            order_frm,
            text="Select Order:",
            text_color="#eee8aa",
            font=("Calibri", 16)
        )
        order_select_lbl.grid(column=0, row=1, padx=40, sticky="w")
        
        order_code_values = orders.orders_df.order_code.to_list()
        order_code_values.sort()
        order_select_cb = ttk.Combobox(
            order_frm,
            width=30,
            state="readonly",
            values=order_code_values
        )
        order_select_cb.grid(column=0, row=2, padx=40, sticky="w")
        order_select_cb.bind("<MouseWheel>", disable_scroll)
        order_select_cb.bind("<<ComboboxSelected>>", display_order_values)
        
        customer_name_lbl = ctk.CTkLabel(
            order_frm,
            text="Customer Name:",
            text_color="#eee8aa",
            font=("Calibri", 16)
        )
        customer_name_lbl.grid(column=0, row=3, padx=(40, 20),
                               pady=(20, 0), sticky="w")
        
        customer_name_val = ctk.CTkLabel(
            order_frm,
            text="-",
            text_color="white",
            font=("Calibri", 20)
        )
        customer_name_val.grid(column=0, row=4, padx=(40, 20), pady=(0, 20),
                               sticky="w")
    
        order_status_lbl = ctk.CTkLabel(
            order_frm,
            text="Order Status:",
            text_color="#eee8aa",
            font=("Calibri", 16)
        )
        order_status_lbl.grid(column=1, row=3, padx=(20, 40), pady=(20, 0),
                              sticky="w")
        
        order_status_cb = ttk.Combobox(
            order_frm,
            width=30,
            state="disable",
            values=STATUS
        )
        order_status_cb.grid(column=1, row=4, padx=(20, 40), pady=(0, 20),
                             sticky="w")
        order_status_cb.bind("<MouseWheel>", disable_scroll)
    
        customer_address_lbl = ctk.CTkLabel(
            order_frm,
            text="Customer Address:",
            text_color="#eee8aa",
            font=("Calibri", 16)
        )
        customer_address_lbl.grid(column=0, row=5, padx=(40, 20), sticky="w")
        
        customer_address_val = ctk.CTkLabel(
            order_frm,
            text="-",
            text_color="white",
            font=("Calibri", 20)
        )
        customer_address_val.grid(column=0, row=6, padx=(40, 20), sticky="w")
    
        customer_phone_lbl = ctk.CTkLabel(
            order_frm,
            text="Customer Phone:",
            text_color="#eee8aa",
            font=("Calibri", 16)
        )
        customer_phone_lbl.grid(column=1, row=5, padx=(20, 40), sticky="w")
        
        customer_phone_val = ctk.CTkLabel(
            order_frm,
            text="-",
            text_color="white",
            font=("Calibri", 20)
        )
        customer_phone_val.grid(column=1, row=6, padx=(20, 40), sticky="w")

        order_details_lbl = ctk.CTkLabel(
            order_frm,
            text="Order Details:",
            text_color="#eee8aa",
            font=("Calibri", 16)
        )
        order_details_lbl.grid(column=0, row=7, padx=(40, 20), pady=(20, 0),
                               sticky="w")
        
        order_details_frm = ctk.CTkFrame(order_frm, corner_radius=0,
                                         fg_color="transparent")
        order_details_frm.grid(column=0, row=8, columnspan=2,
                               padx=40, sticky="ew")
        
        details_initial_val = ctk.CTkLabel(
            order_details_frm,
            text="-",
            text_color="white",
            font=("Calibri", 20)
        )
        details_initial_val.grid(column=0, row=0, sticky="w")
    
        # Button frame
        order_new_btn = ctk.CTkButton(
            order_buttons_frm,
            width=180,
            fg_color="#1a1110",
            text_color="#eee8aa",
            hover_color="#4e1609",
            text="Create New",
            border_width=1,
            border_color="#eee8aa",
            font=("Calibri", 24, "bold"),
            corner_radius=10,
            command=create_new_order
        )
        order_new_btn.pack(padx=40, pady=40, ipady=3, side="right")
    
        order_status_btn = ctk.CTkButton(
            order_buttons_frm,
            width=180,
            fg_color="#1a1110",
            text_color="#eee8aa",
            hover_color="#4e1609",
            text="Change Status",
            border_width=1,
            border_color="#eee8aa",
            font=("Calibri", 24, "bold"),
            corner_radius=10,
            command=status_change
        )
        order_status_btn.pack(pady=40, ipady=3, side="right")

    main_frame_status.set("Orders")


def stock_pressed():
    """What happens when the 'Stock' button is pressed."""
    
    def stock_selection_list():
        """Creating a product selection list."""
        
        code_list = products.products_df.product_code.to_list()
        name_list = products.products_df.name.to_list()
        type_list = products.products_df.type.to_list()
        amount_list = products.products_df.quantity.to_list()
        
        if stock_sort_var.get() == "1":
            pair_lists = []
            for i in range(len(name_list)):
                code_name_pair = [code_list[i], name_list[i]]
                pair_lists.append(code_name_pair)
            pair_lists.sort()
            
        elif stock_sort_var.get() == "2":
            pair_lists = []
            for i in range(len(name_list)):
                code_name_pair = [code_list[i], name_list[i]]
                pair_lists.append(code_name_pair)
            pair_lists.sort(key=lambda x: x[1].casefold())
            
        elif stock_sort_var.get() == "3":
            pair_lists = []
            for i in range(len(name_list)):
                type_name_pair = [type_list[i], name_list[i]]
                pair_lists.append(type_name_pair)
            pair_lists.sort(key=lambda x: x[0].casefold())
            
        elif stock_sort_var.get() == "4":
            pair_lists = []
            for i in range(len(name_list)):
                amount_name_pair = [amount_list[i], name_list[i]]
                pair_lists.append(amount_name_pair)
            pair_lists.sort()
        
        stock_list = []
        for pair in pair_lists:
            merged_values = f"{pair[0]} - {pair[1]}"
            stock_list.append(merged_values)
        
        stock_product_cb.set("")
        stock_product_cb.configure(values=stock_list)
        stock_selected_name_lbl.configure(text=" No selected product",
                                          image=no_selection_img)
        stock_selected_type_val.configure(text="-")
        stock_selected_price_val.configure(text="-")
        stock_selected_amount_val.configure(text="-")
        update_stock_sb.set(1)
    
    def stock_product_selection(event):
        """Changes that occur when a product is selected."""
        
        # Getting the product name
        selected_name = stock_product_cb.get().split(" - ", 1)[1]
        
        # Getting other data for the selected product
        selected_product_data = products.products_df[
            products.products_df.name == selected_name
        ].values.flatten().tolist()
        
        # Getting the product group and image
        selected_product_group = ""
        for key, value in ITEMS.items():
            if selected_product_data[3] in value:
                selected_product_group = key
        
        group_image = image_resize(
            f"pics/{selected_product_group.lower()}.png", width=75, height=75)
        
        # Display data values
        stock_selected_name_lbl.configure(text=selected_name,
                                          image=group_image)
        stock_selected_type_val.configure(text=selected_product_data[3])
        stock_selected_price_val.configure(text=selected_product_data[5])
        stock_selected_amount_val.configure(text=selected_product_data[4])

    def switch_change():
        """Changes that occur when the switch button is pressed."""
        
        if operation_var.get() == "on":
            operation_switch.configure(text="Adding")
            operation_btn.configure(text="Add")
        else:
            operation_switch.configure(text="Subtracting")
            operation_btn.configure(text="Subtract")
    
    def stock_update():
        """Updating the selected product."""
        
        if not stock_product_cb.get():
            cmb.CTkMessagebox(
                title="No selected product",
                message="No product have been selected.",
                icon="info",
                button_width=100,
                button_color="#1a1110",
                button_hover_color="#4e1609",
                text_color="#eee8aa",
                title_color="#eee8aa",
                button_text_color="#eee8aa",
                font=("Calibri", 16),
                fg_color="#1a1110",
                bg_color="#100c08",
                corner_radius=10
            )
        else:
            product_name = stock_product_cb.get().split(" - ", 1)[1]
            selected_data = products.products_df[
                products.products_df.name == product_name
            ].values.flatten().tolist()
            
            if operation_var.get() == "off":
                if int(update_stock_sb.get()) > selected_data[4]:
                    cmb.CTkMessagebox(
                        title="Insufficient supplies",
                        message="There is not enough of the selected item in stock.",
                        icon="info",
                        button_width=100,
                        button_color="#1a1110",
                        button_hover_color="#4e1609",
                        text_color="#eee8aa",
                        title_color="#eee8aa",
                        button_text_color="#eee8aa",
                        font=("Calibri", 16),
                        fg_color="#1a1110",
                        bg_color="#100c08",
                        corner_radius=10
                    )
                else:
                    new_amount_value = selected_data[4] - int(
                        update_stock_sb.get())
                    
                    subtract_sql = f"""
                    UPDATE products
                    SET quantity = '{new_amount_value}'
                    WHERE name = '{product_name}';
                    """
                    products.products_entry_data(subtract_sql)

                    products.products_loading()
                    stock_selection_list()
            else:
                new_amount_value = selected_data[4] + int(
                    update_stock_sb.get())
    
                add_sql = f"""
                UPDATE products
                SET quantity = '{new_amount_value}'
                WHERE name = '{product_name}';
                """
                products.products_entry_data(add_sql)
            
                products.products_loading()
                stock_selection_list()

    # Changes only occur if the main_frame_status variable is not 'Stock'
    if main_frame_status.get() != "Stock":
        for widget in main_frm.winfo_children():
            widget.destroy()
        
        main_frm.grid_rowconfigure(2, weight=1)
        main_frm.grid_columnconfigure((0, 1), weight=1)
        
        # Title
        stock_title_lbl = ctk.CTkLabel(
            main_frm,
            text="STOCK UPDATE",
            text_color="#eee8aa",
            font=("Calibri", 48, "bold")
        )
        stock_title_lbl.grid(column=0, row=0, columnspan=2, padx=40, pady=40)
        
        # Sort and select row
        sorting_frm = ctk.CTkFrame(
            main_frm,
            border_width=1,
            border_color="#eee8aa"
        )
        sorting_frm.grid(column=0, row=1, padx=(40, 20), pady=10)
        
        sorting_title = ctk.CTkLabel(
            sorting_frm,
            fg_color="black",
            text="Sort Data",
            font=("Calibri", 16),
            anchor="center"
        )
        sorting_title.pack(fill="x", padx=2, pady=2)
        
        # Radiobuttons
        stock_sort_var = ctk.StringVar(sorting_frm, "1")
        stock_sort_values = {"Product Code": "1", "Product Name": "2",
                             "Product Type": "3", "Product Amount": "4"}
        
        for key, value in stock_sort_values.items():
            if value == "1":
                y_pad = (10, 5)
            elif value == "4":
                y_pad = (5, 15)
            else:
                y_pad = 5

            ctk.CTkRadioButton(
                sorting_frm,
                text=key,
                value=value,
                variable=stock_sort_var,
                text_color="#eee8aa",
                border_color="#eee8aa",
                fg_color="#7a0003",
                hover_color="#7a0003",
                border_width_checked=4,
                border_width_unchecked=2,
                radiobutton_width=15,
                radiobutton_height=15,
                font=("Calibri", 16),
                command=stock_selection_list
            ).pack(fill="x", padx=40, pady=y_pad)
        
        # Select and Operation frame
        select_operation_frm = ctk.CTkFrame(
            main_frm,
            border_width=1,
            border_color="#eee8aa"
        )
        select_operation_frm.grid(column=1, row=1, padx=(20, 40), pady=10)
        select_operation_frm.grid_columnconfigure(0, weight=1)
        
        select_operation_title = ctk.CTkLabel(
            select_operation_frm,
            fg_color="black",
            text="Operation and Product Select",
            font=("Calibri", 16),
            anchor="center"
        )
        select_operation_title.grid(column=0, row=0, padx=2, pady=2,
                                    sticky="we")
        
        operation_lbl = ctk.CTkLabel(
            select_operation_frm,
            text="Select Operation:",
            text_color="#eee8aa",
            font=("Calibri", 16)
        )
        operation_lbl.grid(column=0, row=1, padx=40, pady=(5, 0), sticky="w")
        
        # Operation switch
        operation_var = ctk.StringVar(value="on")
        operation_switch = ctk.CTkSwitch(
            select_operation_frm,
            text=" Adding",
            text_color="white",
            font=("Calibri", 16),
            variable=operation_var,
            onvalue="on",
            offvalue="off",
            progress_color="#7a0003",
            button_color="#eee8aa",
            command=switch_change
        )
        operation_switch.grid(column=0, row=2, padx=40, pady=(0, 10),
                              sticky="w")
        
        # Product select
        stock_product_lbl = ctk.CTkLabel(
            select_operation_frm,
            text="Select Product:",
            text_color="#eee8aa",
            font=("Calibri", 16))
        stock_product_lbl.grid(column=0, row=3, padx=40, pady=(10, 0),
                               sticky="w")

        # Initial list of values for the Combobox
        codes = products.products_df.product_code.to_list()
        names = products.products_df.name.to_list()

        value_list = []
        for i in range(len(names)):
            value_list.append(f"{codes[i]} - {names[i]}")
        value_list.sort()
        
        stock_product_cb = ttk.Combobox(
            select_operation_frm,
            width=70,
            state="readonly",
            values=value_list
        )
        stock_product_cb.grid(column=0, row=4, padx=40, pady=(0, 15),
                              sticky="w")
        stock_product_cb.bind("<MouseWheel>", disable_scroll)
        stock_product_cb.bind("<<ComboboxSelected>>", stock_product_selection)
        
        # Product frame
        product_details_frm = ctk.CTkFrame(main_frm, corner_radius=0,
                                           fg_color="transparent")
        product_details_frm.grid(column=0, row=2, columnspan=2, padx=40,
                                 sticky="news")
        
        # Image label
        no_selection_img = image_resize("pics/nothing.png", width=75,
                                        height=75)
        
        stock_selected_name_lbl = ctk.CTkLabel(
            product_details_frm,
            text=" No selected product",
            text_color="white",
            font=("Calibri", 24),
            image=no_selection_img,
            compound="left"
        )
        stock_selected_name_lbl.grid(column=0, row=0, columnspan=6,
                                     padx=(40, 0), pady=(40, 0), sticky="w")
        
        stock_selected_type_lbl = ctk.CTkLabel(
            product_details_frm,
            text="Type:",
            text_color="#eee8aa",
            font=("Calibri", 16)
        )
        stock_selected_type_lbl.grid(column=0, row=1, padx=(60, 0), pady=10,
                                     sticky="w")
        
        stock_selected_type_val = ctk.CTkLabel(
            product_details_frm,
            text="-",
            text_color="white",
            width=150,
            font=("Calibri", 16),
            anchor="w"
        )
        stock_selected_type_val.grid(column=1, row=1, padx=(10, 20),
                                     pady=10, sticky="w")
        
        stock_selected_price_lbl = ctk.CTkLabel(
            product_details_frm,
            text="Price:",
            text_color="#eee8aa",
            font=("Calibri", 16)
        )
        stock_selected_price_lbl.grid(column=2, row=1, padx=(20, 0),
                                      pady=10, sticky="w")
        
        stock_selected_price_val = ctk.CTkLabel(
            product_details_frm,
            text="-",
            text_color="white",
            width=150,
            font=("Calibri", 16),
            anchor="w"
        )
        stock_selected_price_val.grid(column=3, row=1, padx=(10, 20),
                                      pady=10, sticky="w")
        
        stock_selected_amount_lbl = ctk.CTkLabel(
            product_details_frm,
            text="Amount:",
            text_color="#eee8aa",
            font=("Calibri", 16)
        )
        stock_selected_amount_lbl.grid(column=4, row=1, padx=(20, 0),
                                       pady=10, sticky="w")
        
        stock_selected_amount_val = ctk.CTkLabel(
            product_details_frm,
            text="-",
            text_color="white",
            width=150,
            font=("Calibri", 16),
            anchor="w"
        )
        stock_selected_amount_val.grid(column=5, row=1, padx=(10, 20),
                                       pady=10, sticky="w")
        
        # Spinbox
        update_stock_sb = ttk.Spinbox(
            main_frm,
            width=8,
            from_=1,
            to=50,
            font="Calibri",
            state="readonly")
        update_stock_sb.grid(column=1, row=3, padx=60, pady=(20, 0),
                             sticky="e")
        update_stock_sb.set(1)
        
        # Button
        operation_btn = ctk.CTkButton(
            main_frm,
            width=120,
            fg_color="#1a1110",
            text_color="#eee8aa",
            hover_color="#4e1609",
            text="Add",
            border_width=1,
            border_color="#eee8aa",
            font=("Calibri", 24, "bold"),
            corner_radius=10,
            command=stock_update
        )
        operation_btn.grid(column=1, row=4, padx=40, pady=(20, 0), ipady=3,
                           sticky="e")
    
    main_frame_status.set("Stock")


def reports_pressed():
    """What happens when the 'Reports' button is pressed."""

    # New Toplevel
    reports_tl = ctk.CTkToplevel(root, fg_color="#100c08")
    reports_tl.title("Reports")
    reports_tl.resizable(False, False)
    reports_tl.grab_set()
    reports_tl.after(200, lambda: reports_tl.iconbitmap(
        "pics/abstract.ico"))
    
    def best_selling():
        """Chart of the ten best-selling products."""
        
        product_code_list = products.products_df.product_code.to_list()
        
        code_amount_list = []
        for code in product_code_list:
            # Number of products sold in the store
            shop_df = sale.sale_df.amount[sale.sale_df.product_code == code]
            shop_sum = shop_df.sum()
            
            # Number of products sold through orders
            orders_df = order_items.order_items_df.amount[
                order_items.order_items_df.product_code == code]
            orders_sum = orders_df.sum()
            
            total_sold = shop_sum + orders_sum
            
            code_amount_list.append([code, total_sold, shop_sum, orders_sum])
        code_amount_list.sort(key=lambda x: x[1], reverse=True)
        
        # Axes values (for the first 15 members)
        code_values = []
        sold_values = []
        shop_values = []
        orders_values = []
        for lst in code_amount_list[:15]:
            code_values.append(lst[0])
            sold_values.append(lst[1])
            shop_values.append(lst[2])
            orders_values.append(lst[3])
        
        # Bar chart
        legend_list = ["Shop", "Orders"]
        fig, ax = plt.subplots(figsize=(16, 8), facecolor="khaki")
        
        ax.set_facecolor("#f5f5dc")
        ax.spines["bottom"].set_color("purple")
        ax.spines["top"].set_color("purple")
        ax.spines["left"].set_color("purple")
        ax.spines["right"].set_color("purple")

        plt.xticks(color="purple")
        plt.yticks(color="purple")
        ax.tick_params(axis="x", colors="purple")
        ax.tick_params(axis="y", colors="purple")
        
        ax.bar(code_values, shop_values, 0.5, color="purple")
        ax.bar(code_values, orders_values, 0.5, color="#9370db",
               bottom=shop_values)
        plt.title(
            "BEST SELLING PRODUCTS",
            fontdict={"family": "Calibri", "color": "purple", "size": 22,
                      "weight": "bold"},
            pad=30
        )
        plt.xlabel(
            "Product codes",
            fontdict={"family": "Calibri", "color": "purple", "size": 16,
                      "weight": "bold"},
            labelpad=20
        )
        plt.ylabel(
            "Quantity sold",
            fontdict={"family": "Calibri", "color": "purple", "size": 16,
                      "weight": "bold"},
            labelpad=20
        )
        add_value_label(code_values, sold_values, "khaki", "center")
        plt.legend(legend_list)
        plt.subplots_adjust(left=0.08, right=0.95, top=0.85, bottom=0.13)

        plt.show()
    
    def highest_price():
        """Chart of the products with the highest price."""
        
        product_code_list = products.products_df.product_code.to_list()
        product_price_list = products.products_df.price.to_list()
        
        code_price_list = []
        for i in range(len(product_code_list)):
            code_price_list.append([product_code_list[i],
                                    product_price_list[i]])
        
        code_price_list.sort(key=lambda x: x[1], reverse=True)

        # Axes values (for the first 15 members)
        code_values = []
        price_values = []
        for lst in code_price_list[:10]:
            code_values.append(lst[0])
            price_values.append(lst[1])
        
        # Bar chart
        fig, ax = plt.subplots(figsize=(16, 8), facecolor="#87ceeb")

        ax.set_facecolor("#bcd4e6")
        ax.spines["bottom"].set_color("#654321")
        ax.spines["top"].set_color("#654321")
        ax.spines["left"].set_color("#654321")
        ax.spines["right"].set_color("#654321")

        plt.xticks(color="#654321")
        plt.yticks(color="#654321")
        ax.tick_params(axis="x", colors="#654321")
        ax.tick_params(axis="y", colors="#654321")

        ax.bar(code_values, price_values, 0.65, color="orange")
        plt.title("Products with the highest prices".upper(),
            fontdict={"family": "Calibri", "color": "#654321", "size": 22,
                      "weight": "bold"}, pad=30)
        plt.xlabel("Product codes",
            fontdict={"family": "Calibri", "color": "#654321", "size": 16,
                      "weight": "bold"}, labelpad=20)
        plt.ylabel("Product price",
            fontdict={"family": "Calibri", "color": "#654321", "size": 16,
                      "weight": "bold"}, labelpad=20)
        add_value_label(code_values, price_values, "#654321", "center")
        plt.grid()
        plt.subplots_adjust(left=0.1, right=0.95, top=0.85, bottom=0.15)

        plt.show()
    
    def lowest_price():
        """Chart of the products with the lowest price."""

        product_code_list = products.products_df.product_code.to_list()
        product_price_list = products.products_df.price.to_list()

        code_price_list = []
        for i in range(len(product_code_list)):
            code_price_list.append(
                [product_code_list[i], product_price_list[i]])

        code_price_list.sort(key=lambda x: x[1])

        # Axes values (for the first 15 members)
        code_values = []
        price_values = []
        for lst in code_price_list[:10]:
            code_values.append(lst[0])
            price_values.append(lst[1])

        # Bar chart
        fig, ax = plt.subplots(figsize=(16, 8), facecolor="#ace1af")

        ax.set_facecolor("#d0f0c0")
        ax.spines["bottom"].set_color("darkred")
        ax.spines["top"].set_color("darkred")
        ax.spines["left"].set_color("darkred")
        ax.spines["right"].set_color("darkred")

        plt.xticks(color="darkred")
        plt.yticks(color="darkred")
        ax.tick_params(axis="x", colors="darkred")
        ax.tick_params(axis="y", colors="darkred")

        ax.bar(code_values, price_values, 0.5, color="#d40000")
        plt.title("Products with the lowest prices".upper(),
                  fontdict={"family": "Calibri", "color": "darkred",
                            "size": 22, "weight": "bold"}, pad=30)
        plt.xlabel("Product codes",
                   fontdict={"family": "Calibri", "color": "darkred",
                             "size": 16, "weight": "bold"}, labelpad=20)
        plt.ylabel("Product price",
                   fontdict={"family": "Calibri", "color": "darkred",
                             "size": 16, "weight": "bold"}, labelpad=20)
        add_value_label(code_values, price_values, "black", "center")
        plt.grid()
        plt.subplots_adjust(left=0.1, right=0.95, top=0.85, bottom=0.15)

        plt.show()
    
    def highest_income():
        """Chart of the products with the highest income."""
        
        product_code_list = products.products_df.product_code.to_list()
        
        code_price_list = []
        for code in product_code_list:
            # Income of products sold in the store
            shop_income = sale.sale_df.price[sale.sale_df.product_code ==
                                                code]
            shop_income_sum = shop_income.sum()
            
            # Income of products sold through orders
            orders_income = order_items.order_items_df.price[
                order_items.order_items_df.product_code == code]
            orders_income_sum = orders_income.sum()
            
            total_income = shop_income_sum + orders_income_sum
            
            code_price_list.append([code, total_income, shop_income_sum,
                                    orders_income_sum])
        code_price_list.sort(key=lambda x: x[1], reverse=True)

        # Axes values (for the first 15 members)
        code_values = []
        total_price_values = []
        shop_price_values = []
        orders_price_values = []
        for lst in code_price_list[:10]:
            code_values.append(lst[0])
            total_price_values.append(lst[1])
            shop_price_values.append(lst[2])
            orders_price_values.append(lst[3])
        
        # Bar chart
        legend_list = ["Shop", "Orders"]
        fig, ax = plt.subplots(figsize=(16, 8), facecolor="#232b2b")

        ax.set_facecolor("#414a4c")
        ax.spines["bottom"].set_color("khaki")
        ax.spines["top"].set_color("khaki")
        ax.spines["left"].set_color("khaki")
        ax.spines["right"].set_color("khaki")

        plt.xticks(color="khaki")
        plt.yticks(color="khaki")
        ax.tick_params(axis="x", colors="khaki")
        ax.tick_params(axis="y", colors="khaki")

        ax.bar(code_values, shop_price_values, 0.75, color="#21421e")
        ax.bar(code_values, orders_price_values, 0.75, color="#568203",
               bottom=shop_price_values)
        plt.title("PRODUCTS WITH THE HIGHEST INCOME",
            fontdict={"family": "Calibri", "color": "khaki", "size": 22,
                      "weight": "bold"}, pad=30)
        plt.xlabel("Product codes",
            fontdict={"family": "Calibri", "color": "khaki", "size": 16,
                      "weight": "bold"}, labelpad=20)
        plt.ylabel("Income",
            fontdict={"family": "Calibri", "color": "khaki", "size": 16,
                      "weight": "bold"}, labelpad=20)
        add_value_label(code_values, total_price_values, "khaki", "center")
        plt.legend(legend_list)
        plt.subplots_adjust(left=0.08, right=0.95, top=0.85, bottom=0.13)
        plt.grid()

        plt.show()

    def group_selling():
        """Chart of sales per product groups."""
        
        code_type_group_amount = []
        for index, rows in products.products_df.iterrows():
            row_list = [rows.product_code, rows.type]
            code_type_group_amount.append(row_list)
        
        for code_type in code_type_group_amount:
            for key, value in ITEMS.items():
                if code_type[1] in value:
                    code_type.append(key)

        for lst in code_type_group_amount:
            # Number of products sold in the store
            shop_product = sale.sale_df.amount[sale.sale_df.product_code ==
                                               lst[0]]
            shop_product_sum = shop_product.sum()

            # Number of products sold through orders
            orders_product = order_items.order_items_df.amount[
                order_items.order_items_df.product_code == lst[0]]
            orders_product_sum = orders_product.sum()

            total_sold = shop_product_sum + orders_product_sum
            lst.append(total_sold)

        # List of product groups
        group_list = list(ITEMS.keys())
        
        # Percentages of products sold per group
        amount_per_groups = []
        for group in group_list:
            total_group = 0
            for lst in code_type_group_amount:
                if group == lst[2]:
                    total_group += lst[3]
            amount_per_groups.append(total_group)
        
        # Pie chart
        fig, ax = plt.subplots(figsize=(8, 8), facecolor="#c19a6b")
        
        ax.set_facecolor("#c19a6b")
        matplotlib.rcParams["text.color"] = "#062a78"
        
        ax.pie(
            amount_per_groups,
            labels=group_list,
            colors=sns.color_palette(palette="YlOrBr", n_colors=7),
            autopct="%.2f%%",
            explode = [0, 0.12, 0, 0, 0, 0, 0]
        )
        plt.title(
            label="Percentages of products sold per group".upper(),
            fontdict={"family": "Calibri", "color": "#062a78", "size": 22,
                      "weight": "bold"},
            pad=30
        )
        
        plt.show()

    def group_income():
        """Chart of incomes per product groups."""

        code_type_group_income = []
        for index, rows in products.products_df.iterrows():
            row_list = [rows.product_code, rows.type]
            code_type_group_income.append(row_list)
        
        for code_type in code_type_group_income:
            for key, value in ITEMS.items():
                if code_type[1] in value:
                    code_type.append(key)
        
        for lst in code_type_group_income:
            # Income of products sold in the store
            shop_product = sale.sale_df.price[sale.sale_df.product_code ==
                                              lst[0]]
            shop_income_sum = shop_product.sum()

            # Income of products sold through orders
            orders_product = order_items.order_items_df.price[
                order_items.order_items_df.product_code == lst[0]]
            orders_income_sum = orders_product.sum()

            total_income = shop_income_sum + orders_income_sum

            lst.append(total_income)

        # List of product groups
        group_list = list(ITEMS.keys())

        # Income of products sold per group
        income_per_groups = []
        for group in group_list:
            total_group = 0
            for lst in code_type_group_income:
                if group == lst[2]:
                    total_group += lst[3]
            income_per_groups.append(total_group)
        
        # Pie chart
        fig, ax = plt.subplots(figsize=(8, 8), facecolor="#87ceeb")

        ax.set_facecolor("#87ceeb")
        matplotlib.rcParams["text.color"] = "#7a0003"

        ax.pie(
            income_per_groups,
            labels=group_list,
            colors=sns.color_palette(palette="vlag", n_colors=7),
            autopct="%.2f%%",
            explode=[0.12, 0, 0, 0, 0.24, 0.12, 0]
        )
        plt.title(
            label="Product income percentages per group".upper(),
            fontdict={"family": "Calibri", "color": "#7a0003", "size": 22,
                      "weight": "bold"},
            pad=30
        )

        plt.show()

    def manufacturer_selling():
        """Chart of numbers of products sold per manufacturer."""
        
        # Sorted manufacturer list
        manufacturers = list(set(products.products_df.manufacturer.to_list()))
        manufacturers.sort(key=lambda x: x.casefold())
        
        code_manufacturer_amount = []
        for index, rows in products.products_df.iterrows():
            row_list = [rows.product_code, rows.manufacturer]
            code_manufacturer_amount.append(row_list)
        
        for lst in code_manufacturer_amount:
            # Number of products sold in the store
            shop_amount = sale.sale_df.amount[sale.sale_df.product_code ==
                                              lst[0]]
            shop_amount_sum = shop_amount.sum()

            # Number of products sold through orders
            orders_amount = order_items.order_items_df.amount[
                order_items.order_items_df.product_code == lst[0]]
            orders_amount_sum = orders_amount.sum()

            total_amount = shop_amount_sum + orders_amount_sum
            lst.append(total_amount)

        # Number of products sold per manufacturer
        amount_per_manufacturer = []
        for manufacturer in manufacturers:
            total_manufacturer = 0
            for lst in code_manufacturer_amount:
                if manufacturer == lst[1]:
                    total_manufacturer += lst[2]
            amount_per_manufacturer.append(total_manufacturer)
        
        # Plot
        fig, ax = plt.subplots(figsize=(16, 9), facecolor="#1b1b1b")

        ax.set_facecolor("#242124")
        ax.spines["bottom"].set_color("lightgrey")
        ax.spines["top"].set_color("lightgrey")
        ax.spines["left"].set_color("lightgrey")
        ax.spines["right"].set_color("lightgrey")

        plt.xticks(color="lightgrey", rotation=75)
        plt.yticks(color="lightgrey")
        ax.tick_params(axis="x", colors="lightgrey")
        ax.tick_params(axis="y", colors="lightgrey")
        
        ax.plot(
            manufacturers,
            amount_per_manufacturer,
            marker="o",
            color="#ee82ee",
            markerfacecolor="#8b008b",
            linestyle="-."
        )
        plt.title(
            "Number of products sold per manufacturer".upper(),
            fontdict={"family": "Calibri", "color": "#a50b5e", "size": 22,
                      "weight": "bold"},
            pad=30
        )
        plt.xlabel(
            "Manufacturer",
            fontdict={"family": "Calibri", "color": "#a50b5e", "size": 16,
                      "weight": "bold"},
            labelpad=30
        )
        plt.ylabel(
            "Sold products",
            fontdict={"family": "Calibri", "color": "#a50b5e", "size": 16,
                      "weight": "bold"},
            labelpad=30
        )
        
        for x, y in zip(manufacturers, amount_per_manufacturer):
            label = y
            plt.annotate(
                label,
                (x, y),
                textcoords="offset points",
                xytext=(0, 10),
                ha="center",
                color="#8b008b",
                bbox=dict(boxstyle="round", fc="khaki")
            )

        plt.subplots_adjust(left=0.1, right=0.95, bottom=0.25)
        plt.grid()
        
        plt.show()

    def manufacturer_income():
        """Chart of the highest incomes per manufacturers."""

        # Sorted manufacturer list
        manufacturers = list(set(products.products_df.manufacturer.to_list()))
        manufacturers.sort(key=lambda x: x.casefold())

        code_manufacturer_income = []
        for index, rows in products.products_df.iterrows():
            row_list = [rows.product_code, rows.manufacturer]
            code_manufacturer_income.append(row_list)

        for lst in code_manufacturer_income:
            # Income of products sold in the store
            shop_income = sale.sale_df.price[
                sale.sale_df.product_code == lst[0]]
            shop_income_sum = shop_income.sum()
    
            # Income of products sold through orders
            orders_income = order_items.order_items_df.price[
                order_items.order_items_df.product_code == lst[0]]
            orders_income_sum = orders_income.sum()
    
            total_income = shop_income_sum + orders_income_sum
            lst.append(total_income)

        # Income of products sold per manufacturer
        income_per_manufacturer = []
        for manufacturer in manufacturers:
            total_manufacturer = 0
            for lst in code_manufacturer_income:
                if manufacturer == lst[1]:
                    total_manufacturer += lst[2]
            income_per_manufacturer.append(total_manufacturer)
        
        income_manufacturer_list = []
        for i in range(len(manufacturers)):
            income_manufacturer_list.append([manufacturers[i],
                                             income_per_manufacturer[i]])
        income_manufacturer_list.sort(key=lambda x: x[1])
        
        manufacturer_list = []
        income_list = []
        for lst in income_manufacturer_list[-15:]:
            manufacturer_list.append(lst[0])
            income_list.append(lst[1])
        
        # Plot
        fig, ax = plt.subplots(figsize=(16, 9), facecolor="#1b1b1b")

        ax.set_facecolor("#242124")
        ax.spines["bottom"].set_color("lightgrey")
        ax.spines["top"].set_color("lightgrey")
        ax.spines["left"].set_color("lightgrey")
        ax.spines["right"].set_color("lightgrey")

        plt.xticks(color="lightgrey", rotation=75)
        plt.yticks(color="lightgrey")
        ax.tick_params(axis="x", colors="lightgrey")
        ax.tick_params(axis="y", colors="lightgrey")
        
        ax.plot(
            manufacturer_list,
            income_list,
            marker="o",
            color="#9bddff",
            markerfacecolor="#008b8b",
            linestyle=":"
        )

        plt.title(
            "Income per manufacturer (top 15)".upper(),
            fontdict={"family": "Calibri", "color": "#004f98", "size": 22,
                      "weight": "bold"},
            pad=30
        )
        plt.xlabel(
            "Manufacturer",
            fontdict={"family": "Calibri", "color": "#004f98", "size": 16,
                      "weight": "bold"},
            labelpad=30
        )
        plt.ylabel(
            "Income",
            fontdict={"family": "Calibri", "color": "#004f98", "size": 16,
                      "weight": "bold"},
            labelpad=30
        )

        for x, y in zip(manufacturer_list, income_list):
            label = y
            plt.annotate(
                label,
                (x, y),
                textcoords="offset points",
                xytext=(0, 10),
                ha="center",
                color="#008b8b",
                bbox=dict(boxstyle="round", fc="khaki")
            )

        plt.subplots_adjust(left=0.1, right=0.95, bottom=0.25)
        plt.grid()

        plt.show()

    def daily_income():
        """Chart of daily incomes - total, from the store and from orders."""
        
        # List of dates
        sale_dates = sale.sale_df.sale_date.to_list()
        order_dates = orders.orders_df.order_date.to_list()
        all_dates = list(set(sale_dates + order_dates))
        
        # Only income from delivered orders is counted.
        delivered_orders_df = orders.orders_df[orders.orders_df.status ==
                                               "Delivered"]
        
        # Calculation of income from the shop and from orders
        date_sale_orders_list = []
        for day in all_dates:
            shop_sales = sale.sale_df.price[sale.sale_df.sale_date == day]
            shop_daily_total = shop_sales.sum()
            
            order_codes = delivered_orders_df.order_code[
                delivered_orders_df.order_date == day].to_list()
            
            order_daily_total = 0
            for code in order_codes:
                incomes = order_items.order_items_df.price[
                    order_items.order_items_df.order_code == code].to_list()
                order_code_income = sum(incomes)
                order_daily_total += order_code_income
            
            daily_total = shop_daily_total + order_daily_total
            
            date_sale_orders_list.append([day, shop_daily_total,
                                          order_daily_total, daily_total])
        date_sale_orders_list.sort(key=lambda x: x[3], reverse=True)
        
        # Value lists
        date_list = []
        shop_income_list = []
        order_income_list = []
        total_income_list = []
        for lst in date_sale_orders_list[:10]:
            date_list.append(lst[0].strftime("%d. %m. %Y."))
            shop_income_list.append(round(lst[1] / 1000, 2))
            order_income_list.append(round(lst[2] / 1000, 2))
            total_income_list.append(round(lst[3] / 1000, 2))
        
        # Bar chart
        legend_list = ["Total Income", "Shop Income", "Order Income"]
        fig, ax = plt.subplots(figsize=(16, 8), facecolor="#ffe5b4")

        ax.set_facecolor("#fdf5e6")
        ax.spines["bottom"].set_color("navy")
        ax.spines["top"].set_color("navy")
        ax.spines["left"].set_color("navy")
        ax.spines["right"].set_color("navy")

        plt.xticks(color="navy")
        plt.yticks(color="navy")
        ax.tick_params(axis="x", colors="navy")
        ax.tick_params(axis="y", colors="navy")
        
        dates_array = np.arange(len(date_list))
        bar_1 = ax.bar(dates_array-0.25, total_income_list, width=0.25,
                       color="#ff4500", align="center")
        ax.bar_label(bar_1, padding=7, color="navy")
        bar_2 = ax.bar(dates_array, shop_income_list, width=0.25,
                       color="#4682b4", align="center")
        ax.bar_label(bar_2, color="navy")
        bar_3 = ax.bar(dates_array+0.25, order_income_list, width=0.25,
                       color="#8db600", align="center")
        ax.bar_label(bar_3, color="navy")
        ax.set_xticks(dates_array, date_list)
        ax.set_ylim(0, 1500)
        
        plt.title(
            "DAILY INCOME",
            fontdict={"family": "Calibri", "color": "navy", "size": 22,
                      "weight": "bold"},
            pad=30
        )
        plt.xlabel(
            "Date",
            fontdict={"family": "Calibri", "color": "navy", "size": 16,
                      "weight": "bold"},
            labelpad=20
        )
        plt.ylabel(
            "Income (1000 DIN)",
            fontdict={"family": "Calibri", "color": "navy", "size": 16,
                      "weight": "bold"},
            labelpad=20
        )
        plt.legend(legend_list)
        plt.subplots_adjust(left=0.08, right=0.95, top=0.85, bottom=0.13)

        plt.show()
    
    # Main Toplevel title
    reports_title_lbl = ctk.CTkLabel(
        reports_tl,
        text="REPORTS",
        text_color="#7a0003",
        font=("Calibri", 48, "bold")
    )
    reports_title_lbl.pack(fill="x", ipady=40)
    
    # Info label
    reports_info_lbl = ctk.CTkLabel(
        reports_tl,
        text="Graphic display of certain statistical data.",
        text_color="#eee8aa",
        font=("Calibri", 16)
    )
    reports_info_lbl.pack(fill="x", pady=(0, 20))
    
    # Selection frame
    report_selection_frm = ctk.CTkFrame(reports_tl, corner_radius=1,
                                        fg_color="transparent")
    report_selection_frm.pack(expand=True, fill="x", padx=50, pady=10)
    
    report_selection_frm.grid_columnconfigure((0, 1), weight=1)
    
    # Selection Buttons
    best_selling_btn = ctk.CTkButton(
        report_selection_frm,
        width=250,
        fg_color="#1a1110",
        text_color="#eee8aa",
        hover_color="#4e1609",
        text="Best Selling",
        border_width=1,
        border_color="#eee8aa",
        font=("Calibri", 24, "bold"),
        corner_radius=10,
        command=best_selling
    )
    best_selling_btn.grid(column=0, row=0, padx=50, pady=10, ipady=3)
    
    best_selling_lbl = ctk.CTkLabel(
        report_selection_frm,
        text="Best selling products.",
        text_color="white",
        font=("Calibri", 20)
    )
    best_selling_lbl.grid(column=1, row=0, pady=10, sticky="w")
    
    highest_price_btn = ctk.CTkButton(
        report_selection_frm,
        width=250,
        fg_color="#1a1110",
        text_color="#eee8aa",
        hover_color="#4e1609",
        text="Highest Price",
        border_width=1,
        border_color="#eee8aa",
        font=("Calibri", 24, "bold"),
        corner_radius=10,
        command=highest_price
    )
    highest_price_btn.grid(column=0, row=1, padx=50, pady=10, ipady=3)
    
    highest_price_lbl = ctk.CTkLabel(
        report_selection_frm,
        text="Products with the highest prices.",
        text_color="white",
        font=("Calibri", 20)
    )
    highest_price_lbl.grid(column=1, row=1, pady=10, sticky="w")
    
    lowest_price_btn = ctk.CTkButton(
        report_selection_frm,
        width=250,
        fg_color="#1a1110",
        text_color="#eee8aa",
        hover_color="#4e1609",
        text="Lowest Price",
        border_width=1,
        border_color="#eee8aa",
        font=("Calibri", 24, "bold"),
        corner_radius=10,
        command=lowest_price
    )
    lowest_price_btn.grid(column=0, row=2, padx=50, pady=10, ipady=3)
    
    lowest_price_lbl = ctk.CTkLabel(
        report_selection_frm,
        text="Products with the lowest prices.",
        text_color="white",
        font=("Calibri", 20)
    )
    lowest_price_lbl.grid(column=1, row=2, pady=10, sticky="w")
    
    highest_income_btn = ctk.CTkButton(
        report_selection_frm,
        width=250,
        fg_color="#1a1110",
        text_color="#eee8aa",
        hover_color="#4e1609",
        text="Highest Income",
        border_width=1,
        border_color="#eee8aa",
        font=("Calibri", 24, "bold"),
        corner_radius=10,
        command=highest_income
    )
    highest_income_btn.grid(column=0, row=3, padx=50, pady=10, ipady=3)
    
    highest_income_lbl = ctk.CTkLabel(
        report_selection_frm,
        text="Products with the highest income.",
        text_color="white",
        font=("Calibri", 20)
    )
    highest_income_lbl.grid(column=1, row=3, pady=10, sticky="w")
    
    group_selling_btn = ctk.CTkButton(
        report_selection_frm,
        width=250,
        fg_color="#1a1110",
        text_color="#eee8aa",
        hover_color="#4e1609",
        text="Group Selling",
        border_width=1,
        border_color="#eee8aa",
        font=("Calibri", 24, "bold"),
        corner_radius=10,
        command=group_selling
    )
    group_selling_btn.grid(column=0, row=4, padx=50, pady=10, ipady=3)
    
    group_selling_lbl = ctk.CTkLabel(
        report_selection_frm,
        text="Total sales per product groups.",
        text_color="white",
        font=("Calibri", 20)
    )
    group_selling_lbl.grid(column=1, row=4, pady=10, sticky="w")
    
    group_income_btn = ctk.CTkButton(
        report_selection_frm,
        width=250,
        fg_color="#1a1110",
        text_color="#eee8aa",
        hover_color="#4e1609",
        text="Group Income",
        border_width=1,
        border_color="#eee8aa",
        font=("Calibri", 24, "bold"),
        corner_radius=10,
        command=group_income
    )
    group_income_btn.grid(column=0, row=5, padx=50, pady=10, ipady=3)
    
    group_income_lbl = ctk.CTkLabel(
        report_selection_frm,
        text="Product income percentages per group",
        text_color="white",
        font=("Calibri", 20)
    )
    group_income_lbl.grid(column=1, row=5, pady=10, sticky="w")
    
    manufacturer_selling_btn = ctk.CTkButton(
        report_selection_frm,
        width=250,
        fg_color="#1a1110",
        text_color="#eee8aa",
        hover_color="#4e1609",
        text="Manufacturer Selling",
        border_width=1,
        border_color="#eee8aa",
        font=("Calibri", 24, "bold"),
        corner_radius=10,
        command=manufacturer_selling
    )
    manufacturer_selling_btn.grid(column=0, row=6, padx=50, pady=10, ipady=3)
    
    manufacturer_selling_lbl = ctk.CTkLabel(
        report_selection_frm,
        text="Number of products sold per manufacturer.",
        text_color="white",
        font=("Calibri", 20)
    )
    manufacturer_selling_lbl.grid(column=1, row=6, pady=10, sticky="w")
    
    manufacturer_income_btn = ctk.CTkButton(
        report_selection_frm,
        width=250,
        fg_color="#1a1110",
        text_color="#eee8aa",
        hover_color="#4e1609",
        text="Manufacturer Income",
        border_width=1,
        border_color="#eee8aa",
        font=("Calibri", 24, "bold"),
        corner_radius=10,
        command=manufacturer_income
    )
    manufacturer_income_btn.grid(column=0, row=7, padx=50, pady=10, ipady=3)
    
    manufacturer_income_lbl = ctk.CTkLabel(
        report_selection_frm,
        text="Incomes per manufacturers.",
        text_color="white",
        font=("Calibri", 20)
    )
    manufacturer_income_lbl.grid(column=1, row=7, pady=10, sticky="w")
    
    daily_income_btn = ctk.CTkButton(
        report_selection_frm,
        width=250,
        fg_color="#1a1110",
        text_color="#eee8aa",
        hover_color="#4e1609",
        text="Daily Income",
        border_width=1,
        border_color="#eee8aa",
        font=("Calibri", 24, "bold"),
        corner_radius=10,
        command=daily_income
    )
    daily_income_btn.grid(column=0, row=8, padx=50, pady=10, ipady=3)
    
    daily_income_lbl = ctk.CTkLabel(
        report_selection_frm,
        text="Daily income - total, from the store and from orders.",
        text_color="white",
        font=("Calibri", 20)
    )
    daily_income_lbl.grid(column=1, row=8, pady=10, sticky="w")

    reports_quit_btn = ctk.CTkButton(
        reports_tl,
        width=120,
        fg_color="#1a1110",
        text_color="#eee8aa",
        hover_color="#4e1609",
        text="Quit",
        border_width=1,
        border_color="#eee8aa",
        font=("Calibri", 24, "bold"),
        corner_radius=10,
        command=reports_tl.destroy
    )
    reports_quit_btn.pack(padx=50, pady=40, ipady=3, side="right")


# Setting the logo image
logo_frm = ctk.CTkFrame(root, fg_color="black")
logo_frm.pack(fill="x")
logo = image_resize("pics/abstract_shop.jpg", 1200, 188)
logo_lbl = ctk.CTkLabel(logo_frm, image=logo, text="")
logo_lbl.pack(side="left")

# Setting left side menu
menu_frm = ctk.CTkFrame(root, fg_color="#100c08", corner_radius=0)
menu_frm.pack(fill="y", side="left")

# Buttons
discount_btn = ctk.CTkButton(
    menu_frm,
    width=200,
    fg_color="#1a1110",
    text_color="#eee8aa",
    hover_color="#4e1609",
    text="Discount",
    border_width=1,
    border_color="#eee8aa",
    font=("Calibri", 24, "bold"),
    corner_radius=10,
    command=discounts_pressed
)
discount_btn.pack(padx=50, pady=(150, 10), ipady=3)

sale_btn = ctk.CTkButton(
    menu_frm,
    width=200,
    fg_color="#1a1110",
    text_color="#eee8aa",
    hover_color="#4e1609",
    text="Sale",
    border_width=1,
    border_color="#eee8aa",
    font=("Calibri", 24, "bold"),
    corner_radius=10,
    command=sale_pressed
)
sale_btn.pack(padx=50, pady=(10, 10), ipady=3)

items_btn = ctk.CTkButton(
    menu_frm,
    width=200,
    fg_color="#1a1110",
    text_color="#eee8aa",
    hover_color="#4e1609",
    text="Products",
    border_width=1,
    border_color="#eee8aa",
    font=("Calibri", 24, "bold"),
    corner_radius=10,
    command=items_pressed
)
items_btn.pack(padx=50, pady=(10, 10), ipady=3)

order_btn = ctk.CTkButton(
    menu_frm,
    width=200,
    fg_color="#1a1110",
    text_color="#eee8aa",
    hover_color="#4e1609",
    text="Orders",
    border_width=1,
    border_color="#eee8aa",
    font=("Calibri", 24, "bold"),
    corner_radius=10,
    command=order_pressed
)
order_btn.pack(padx=50, pady=(10, 10), ipady=3)

stock_btn = ctk.CTkButton(
    menu_frm,
    width=200,
    fg_color="#1a1110",
    text_color="#eee8aa",
    hover_color="#4e1609",
    text="Stock",
    border_width=1,
    border_color="#eee8aa",
    font=("Calibri", 24, "bold"),
    corner_radius=10,
    command=stock_pressed
)
stock_btn.pack(padx=50, pady=(10, 10), ipady=3)

reports_btn = ctk.CTkButton(
    menu_frm,
    width=200,
    fg_color="#1a1110",
    text_color="#eee8aa",
    hover_color="#4e1609",
    text="Reports",
    border_width=1,
    border_color="#eee8aa",
    font=("Calibri", 24, "bold"),
    corner_radius=10,
    command=reports_pressed
)
reports_btn.pack(padx=50, pady=(10, 10), ipady=3)

# Main frame
main_frm = ctk.CTkScrollableFrame(
    root,
    fg_color="#100c08",
    corner_radius=0
)
main_frm.pack(expand=True, fill="both")

# Exit button and its frame
exit_frm = ctk.CTkFrame(root, fg_color="#100c08", corner_radius=0)
exit_frm.pack(fill="x", side="bottom")

exit_btn = ctk.CTkButton(
    exit_frm,
    width=120,
    fg_color="#1a1110",
    text_color="#eee8aa",
    hover_color="#4e1609",
    text="Exit",
    border_width=1,
    border_color="#eee8aa",
    font=("Calibri", 24, "bold"),
    corner_radius=10,
    command=lambda: [products.con.close(), sale.con.close(),
                     orders.con.close(), order_items.con.close(),
                     exit_application()]
)
exit_btn.pack(padx=50, pady=30, ipady=3, side="right")

discounts_pressed()

root.mainloop()
