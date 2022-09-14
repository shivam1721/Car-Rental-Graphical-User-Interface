from cProfile import label
from datetime import date
import os
import sys
import sqlite3
from tkinter import *
from tkinter import ttk
from tabs import *
from datetime import datetime

payDate = StringVar()

vehicle3 =StringVar()
  
total = IntVar()

dateOfPay = StringVar()

turnIn = StringVar()

value = StringVar()

submitComplete_label = Label(root)


def bookRental():
  global dateOfPay
  global turnIn
  global total
  global vehicle3
  global payDate
  ################### calculate total for rental ##################
  def calcTotal(event):
    global dateOfPay
    global turnIn
    global total
    global vehicle3
    global payDate
    carType = type3.get()
    category = category3.get()
    rentalType = rentalType4.get()
    if carType == 'Compact': 
      carType = "1" 
  
    elif carType == "Medium": 
      carType = "2"
  
    elif carType == "Large": 
      carType = "3" 
      
    elif carType == "SUV": 
      carType = "4"
       
    elif carType == "Truck": 
      carType = "5"
  
    elif carType == "VAN": 
      carType = "6"  
  
    if category == 'Basic': 
      category = "0" 
  
    elif category == "Luxury": 
      category = "1"
  
    iq_conn = sqlite3.connect('rental.db')
    iq_cur = iq_conn.cursor()
    if rentalType == "Weekly":
      iq_cur.execute("SELECT Weekly FROM RATE WHERE Type = ? AND Category = ?",
                    (carType, category,))
    elif rentalType == "Daily":
      iq_cur.execute("SELECT Daily FROM RATE WHERE Type = ? AND Category = ?",
                    (carType, category,))  
    #executes search query when list vehicles button is clicked 
    rates = iq_cur.fetchall()
    arr = rates[0]
    #commit changes
    iq_conn.commit()
  	#close the DB connection
    iq_conn.close()
    
    #calculate total amount for rental and place it in label
    total = int(arr[0]) * int(quantity.get())
  
    #set total here  
    value = "$" + str(total)
       
    
    total_value = Label(tab5, text = value)
    total_value.grid(row = 12,  column =  1)

  ###################### reserve  vehicle ###########################
  def reserve_query():
  
    global dateOfPay
    global turnIn
    global total
    global vehicle3
    global payDate
    global submitComplete_label
    submitComplete_label.destroy()
    arr = vehicle3.get().split(',')
    VIN = arr[0].split('(')
    VIN = VIN[1].replace("'", "")
    print(VIN)
      
    print("Total", total)
    #weekly or daily rental, convert to numeric representation
    rentalType = rentalType4.get()
    
    if rentalType == "Daily":
      rentalType = "1"
    elif rentalType == "Weekly": 
      rentalType = "7"
    dateOfPay = payDateChoice.get()
    if dateOfPay == "Pay Today":
      turnIn = "NULL"
    elif dateOfPay == "Pay On Return":
      turnIn = orderDate.get()
    #answer to whether cusomter wants to pay today or on return of vehicle
    checkOut = 1
    
    submit_conn = sqlite3.connect('rental.db')
    submit_cur = submit_conn.cursor()
    submit_cur.execute("INSERT INTO RENTAL VALUES (:CustID, :VehicleID, :StartDate, :OrderDate, :RentalType, :Qty, :ReturnDate, :TotalAmount, :PaymentDate, :Returned) ",
  		{
  			'CustID': customerId.get(),
  			'VehicleID': VIN,
  			'StartDate': startDate.get(),
  			'OrderDate': orderDate.get(),
  			'RentalType': rentalType,
        'Qty': quantity.get(),
        'ReturnDate': endDate.get(),
        'TotalAmount': total,
        'PaymentDate': turnIn,
        'Returned' : checkOut,
  		})
    #commit changes
    submit_conn.commit()
  	#close the DB connection
    submit_conn.close()

  
    submitComplete_label = Label(tab5, text = 'Vehicle Booking Complete!')
    submitComplete_label.grid(row =16, column = 0, columnspan = 2 )
    
  #list query for vehicles
  carType = StringVar()
  category = StringVar()

  ######## search for avilable vehicles #################
  def input_query():
    global dateOfPay
    global turnIn
    global total
    global vehicle3
    global payDate
    global submitComplete_label
    submitComplete_label.destroy()
  
    carType = type3.get()
    category = category3.get()
    start = startDate.get()
    end = endDate.get()
    print(start)
    print(end)
    if carType == 'Compact': 
      carType = "1" 
  
    elif carType == "Medium": 
      carType = "2"
  
    elif carType == "Large": 
      carType = "3" 
      
    elif carType == "SUV": 
      carType = "4"
       
    elif carType == "Truck": 
      carType = "5"
  
    elif carType == "VAN": 
      carType = "6"  
  
    if category == 'Basic': 
      category = "0" 
  
    elif category == "Luxury": 
      category = "1"  
    Returned = 0
    iq_conn = sqlite3.connect('rental.db')
    iq_cur = iq_conn.cursor()
    iq_cur.execute("SELECT v.VehicleID, v.Description, v.Year, v.Type, v.Category FROM VEHICLE v, RENTAL r WHERE v.Type = ? AND v.Category = ? AND r.Returned = ? AND r.StartDate < ? AND r.ReturnDate < ? GROUP BY v.VehicleID",
                  (carType, category, Returned, start, end,))
    
    #executes search query when list vehicles button is clicked 
    output_records3 = iq_cur.fetchall()
   
    #commit changes
    iq_conn.commit()
  	#close the DB connection
    iq_conn.close()
    submitComplete_label = Label()
    if (len(output_records3) == 0):
      print(len(output_records3))
      submitComplete_label = Label(tab5, text = 'No matching results...')
      submitComplete_label.grid(row =16, column = 0, columnspan = 2 )
    else:
      vehicle3.set("Select from results")
      drop3 = OptionMenu(tab5, vehicle3, *output_records3, command = calcTotal)
      drop3.grid(row = 11, column =1, columnspan = 2, pady = 5, padx = 10, ipadx = 100)
      reserve_qry_btn = Button(tab5, text = 'Reserve Vehicle', command = reserve_query)
      reserve_qry_btn.grid(row = 13, column =1, columnspan = 1, pady = 10, padx = 5, ipadx = 100)
  
    # #calculate total here and place in a label
    # payOptions = ["Pay Today", "Pay On Return"]
    # payDate.set("Ca")
    # payDrop = OptionMenu(tab5, payDate, *payOptions, command = calcTotal)
    # payDrop.grid(row = 10, column =1, columnspan = 2, pady = 5, padx = 10, ipadx = 100)
    
  

 

    
    
  
  
  # input fields
  customerId = Entry(tab5, width = 30)
  customerId.grid(row = 0, column = 1)
  
  startDate = Entry(tab5, width = 30)
  startDate.grid(row = 1, column = 1)
  
  endDate = Entry(tab5, width = 30)
  endDate.grid(row = 2, column = 1)
  
  orderDate = Entry(tab5, width = 30)
  orderDate.grid(row = 3, column = 1)
  
  #vehicle type drop down menu	
  vehicleTypes = ["Compact", "Medium", "Large", "SUV", "Truck", "VAN"]
  type3 = StringVar()
  type3.set("Vehicle Type")
  drop = OptionMenu(tab5, type3, *vehicleTypes)
  drop.grid(column = 1, row=4 )
  
  #vehicle category dropdown menu
  vehicleCategories = ['Basic', 'Luxury']
  category3 = StringVar()
  category3.set("Vehicle Category")
  drop2 = OptionMenu(tab5, category3, *vehicleCategories)
  drop2.grid(column = 1, row= 5)
  
  #vehicle rental type dropdown menu
  vehicleRentalType = ["Daily", "Weekly"]
  rentalType4 = StringVar()
  rentalType4.set("Rental Type")
  drop3 = OptionMenu(tab5, rentalType4, *vehicleRentalType)
  drop3.grid(column = 1, row= 6)

  #pay date choice
  rentalPayChoice = ["Pay Today", "Pay On Return"]
  payDateChoice = StringVar()
  payDateChoice.set("When To Pay")
  drop4 = OptionMenu(tab5, payDateChoice, *rentalPayChoice)
  drop4.grid(column = 1, row= 7)
  
  quantity = Entry(tab5, width = 30)
  quantity.grid(row = 8, column = 1)
  
  #create labels
  customerId_label = Label(tab5, text = 'Customer ID: ')
  customerId_label.grid(row =0, column = 0)
  
  startDate_label = Label(tab5, text = 'Start Date**: ')
  startDate_label.grid(row =1, column = 0)
  
  endDate_label = Label(tab5, text = 'End Date**: ')
  endDate_label.grid(row =2, column = 0)
  
  orderDate_label = Label(tab5, text = 'Order Date: ')
  orderDate_label.grid(row = 3, column = 0)
  
  type_label3 = Label(tab5, text = 'Type**: ')
  type_label3.grid(row =4, column = 0)
  
  category_label3 = Label(tab5, text = 'Category**: ')
  category_label3.grid(row =5, column = 0)
  
  vehicle_rental_label = Label(tab5, text = 'Rental Type: ')
  vehicle_rental_label.grid(row =6, column = 0)
  
  quantity_label = Label(tab5, text = 'Quantity')
  quantity_label.grid(row = 8,  column =  0)

  total_label = Label(tab5, text = 'Total')
  total_label.grid(row = 12,  column =  0)
  
  #create another dropdown that displays results in a select menu rather than print them
  input_qry_btn = Button(tab5, text = 'Search available vehicles', command = input_query)
  input_qry_btn.grid(row = 10, column =1, columnspan = 1, pady = 10, padx = 10, ipadx = 100)
  #results dropdown menu
