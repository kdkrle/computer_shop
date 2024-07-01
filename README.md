# 1. Project title
    COMPUTER SHOP MANAGEMENT

# 2. Brief description of the project
The project was done as an integral part of the practice course "Python 
Developer - Advanced" in the company **ITOiP** (IT Training and Practice - 
https://itoip.rs).

"Computer Shop Management" is an application that would be used by a shop 
employee to record successful sales, update inventory, manipulate orders, 
and as the insight into certain sales and pricing statistics.

The application was made in Python, with the help of the PostgreSQL 
database management system. The 'Custom Tkinter' library was used to create 
the user interface. In cases where certain elements of the 'Custom Tkinter' 
library were not considered appropriate, there were used those from the 
'ttk' library (Combobox, Spinbox and Treeview).

Tables made as an example are in the archive 'tables.zip'.

# 3. The README.md file contents
#### 1. Project title
#### 2. Brief description of the project
#### 3. The README.md file contents
#### 4. Database and table structure
#### 5. Application description and usage

# 4. Database and table structure
Database name: "computer_shop"

Tables:

    products
        product_code        (varchar (6), primary key, not null)
                                                        # product code
        name                (varchar (60), not null)    # product name
        manufacturer        (varchar (25), not null)    # manufacturer name
        type                (varchar (25), not null)    # product type
        quantity            (integer, not null)         # product amount
        price               (float, not null)           # product price
        discount            (integer, not null)         # percentage discount

    sale
        sold_item_code  (serial, primary key, not null) # sales number
        bill_number     (varchar (10), not null)        # bill number
        product_code    (varchar (6), not null)         # product code
        amount          (integer, not null)             # amount sold
        price           (float, not null)               # sale price
        sale_date       (date, not null)                # date of sale

    orders
        order_code          (varchar (10), primary key, not null)
                                                        # order code
        customer_name       (varchar (40), not null)    # customer name
        customer_address    (varchar (40), not null)    # customer address
        customer_phone      (varchar (40), not null)    # customer phone
        order_date          (date, not null)            # order date
        status              (varchar (10), not null)    # order status

    order_items
        item_code       (serial, primary key, not null) # ordered prod. number
        order_code      (varchar (10), not null)        # order code
        product_code    (varchar (6), not null)         # product code
        price           (float, not null)               # sale price
        amount          (integer, not null)             # sale amount


# 5. Application description and usage

## 5.1 Main screen - opening

![1 - Main Screen](https://github.com/kdkrle/computer_shop/assets/59825527/98d91862-8192-4b85-8c47-14c622139f42)

_Picture 1: Main Screen - Opening_

At the top of the main screen there is an image with the name of the store. 
Below that there are two parts.

On the left there is a menu with buttons, with which we can select the area 
of operation of the store that we need.

At the right part, the necessary changes are made, or we get an insight into 
some information for the selected area. By launching the application,
this section contains what we would get by pressing the 'Discount' button.

At the very bottom, in the right corner, there is an 'Exit' button to exit 
the application.

## 5.2.1 Discount

![2 1 - Discount](https://github.com/kdkrle/computer_shop/assets/59825527/0c331e7b-e6c2-452a-a027-7680e47c8bcc)

_Picture 2: Discount_

By pressing the 'Discount' button or while opening the application itself, a 
list of products that are currently on discount is displayed on the main 
screen. Each of those items has an icon of the group the product belongs to,
next to which is the name of the product itself. Below that is the 
information about the product type, regular price as well as discount price,
which is highlighted.

Below the list is the 'Update' button. When we press it, it opens a new 
screen, which serves to update the discount.

### 5.2.2 Discount update

![2 2 - Discount Update](https://github.com/kdkrle/computer_shop/assets/59825527/85c16c23-3d1c-442b-b2b6-bef235d54897)

_Picture 3: Discount Update_


At the top of the new screen we have a title, below which is a short 
explanation about the way to select and sort the data to be selected.

Next to it there is the frame in which you can choose the way of displaying 
the product list. In it, you can select to sort products by their code, 
name, manufacturer or type, and the list can also be shortened to only 
those products that are already on discount.

By selecting a product from the drop-down menu, information about that 
product is displayed: its code, manufacturer, type, current discount, 
regular price and discount price. If we want to change the discount for the 
selected product, we enter the change in the 'Set discount' field and press 
the 'Update' button at the bottom of the screen.

If we press the 'Update' button without selecting a product or without 
changing the discount, we will receive a notification about it.

The 'Quit' button is used to close this window.

### 5.3 Sale

Pressing the 'Sale' button opens the sales section, which serves as the 
store's chash register.

The product is selected from the drop-down menu, and then the quantity is 
selected. By pressing the 'Add' button, the selected product and quantity 
are added to the list for sale, and at the same time the total amount is 
updated.

Apart from the 'Add' button, which adds the product and quantity to the 
list for sale, there are three other buttons.

The 'Delete' button deletes the selected item from the list, the 'Clear 
All' button deletes all items from the list, and the 'Realize' button 
releases the sale/bill.

### 5.4 Product review

Selecting 'Products' from the main menu opens a section for reviewing all 
products.

Below the title there are two frames and two buttons. In the left frame, you 
can choose different ways of sorting the displayed products.

The right frame shortens the list of displayed products to a certain 
manufacturer, a certain type or a certain group of products. It is possible 
to choose only one of these three criteria.

On the right there are the 'Apply' and 'Reset' buttons. Pressing the first 
button applies the selected display mode and the selected filter. The second 
button cancels these selections and sets them to their original values, but 
does not reset the list itself. To do that you need to press the first button.

### 5.5.1 Orders - review and status

By pressing the button 'Orders' from the main menu, we get the possibility 
to review previous orders, create a new order and change the status of one 
of the existing orders.

An insight into the details of an order can be obtained by selecting its 
code from the drop-down menu. After selection, the status of the order, the 
customer's name, his address, his phone number and the details of the order 
with the total price are displayed. Each individual item in the product 
details contains the quantity of the ordered item, its name and the total 
price (quantity times price of the individual item).

Below the order details there are two buttons. The first one is for changing 
the status of the order, and the second one is for creating a new one. There 
are five order statuses, and they can be selected from the drop-down menu.

When creating an order, regardless of whether it was created online or an 
employee made it in the store, it has the status 'Received'. The order has 
only been recorded. When the employee prepares the products for shipment, 
he should also change the status of the order to 'Ready'. The status 
changes again when the delivery service picks up the order and the status 
then changes to 'Sent'. Finally, depending on whether the order was 
successfully delivered or returned, the status changes to 'Delivered' or 
'Returned'. Changing the order status in the database is done by selecting 
the option from the drop-down menu and pressing the 'Change status' button.

## 5.5.2 Orders - creating new

Pressing the 'Create New' button opens a new window where we can create a 
new order. In that window there are two frames and five buttons.

The first box is for entering customer data and the order code, which is 
automatically generated. Customer data is his name, address and phone number.

The second frame is the basket into which we insert the products to be 
ordered. The name of the product is selected from the drop-down menu, and 
next to it is a field for entering the quantity of that product. The item 
is placed in the basket (put on the order list) by pressing the 'Add' 
button. By selecting the item we don't want and pressing the 'Delete' 
button, we delete the item from the list.Deleting all items from the basket 
is done by pressing the 'Clear All' button. If we are satisfied with the 
items and their quantity, we can press the 'Create' button, with which we 
realize the order, which gets the status 'Received'. The 'Exit' button 
closes this window.

### 5.6 Stock update

The 'Stock' button takes us to the section where we can update the stock. 
Stocks are updated when replenished or in order to correct errors in stock.

Below the title there are two frames. The first frame is intended for sorting 
products by code, name, type or current quantity in stock.

In the second frame, we choose whether to add or subtract from the stock. 
Depending on the selection for addition or subtraction, the name of the 
button ('Add'/'Subtract') that confirms the changes is also changed. Below 
the add or subtract selection is a drop-down menu of products. When 
selecting a product, the icon of the product group and the name of the 
selected product are displayed in the lower part, and below that is the 
information about the type of product, its price and the current quantity 
in stock.

At the very bottom, in the right corner, there is a field for entering the 
quantity of the product that we want to add or subtract from the stock 
and a button that performs the addition or subtraction operation and 
updates it in the database.

### 5.7 Reports

Pressing the 'Reports' button opens a new window with the same title. 
Below the title is a short notice that from here you can get a graphic 
display of some statistical data about the products or about the operation 
of the store.

Then there are nine buttons on the left and brief explanations of what they 
do by pressing them on the right. At the bottom there is the 'Quit' button 
to close this window.

The nine buttons have the following function. The first opens a bar chart 
with the top 15 best-selling products (in-store and through orders), with 
the total number of sales in the middle of the column.

The second button takes us to the display of 10 products with the highest 
prices, and the third one to the display of 10 products with the lowest prices.

The fourth chart shows which 10 products generated the most income 
(in-store and through orders), with total sales in the middle of the column.

The fifth and sixth graphs are percentages of products sold per group and 
percentages of product income, also per group.

The seventh and eighth charts represent the number of products sold and the 
amount of income per manufacturer, with the fact that for the sake of 
clear view, only the first 15 manufacturers were selected for this second 
chart.

The last chart shows the top daily income, along with the store income 
and order income for that day.

NOTE: In some charts, product codes are used instead of their names, as 
it would be awkward to use the names, because some of them are very long.
