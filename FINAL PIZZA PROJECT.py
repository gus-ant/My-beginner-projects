print("Thank you for choosing Python Pizza Deliveries!")
size = input("Size of the pizza?(S,M,L)") # What size pizza do you want? S, M, or L
add_pepperoni = input("Pepperoni? (Y or N)") # Do you want pepperoni? Y or N
extra_cheese = input("Cheese? Y or N") # Do you want extra cheese? Y or N

# 🚨 Don't change the code above 👆
# Write your code below this line 👇
thank="Thank you for choosing Python Pizza Deliveries!"
y="Your final bill is:"
price_s=15
price_m=20
price_l=25
price_pepe=3
price_cheese=1

if size=="S":
    if add_pepperoni=="Y":
        if extra_cheese=="Y":
            print(y,f"${price_s+2+price_cheese}")
        else:
        
            print(y,f"${price_s+price_pepe}")
    else:
        if extra_cheese=="Y":
        
            print(y,f"${price_s+price_cheese}")
        else:
        
            print(y,f"${price_s}")
            
elif size=="M":
    if add_pepperoni=="Y":
        if extra_cheese=="Y":
        
            print(y,f"${price_m+price_pepe+price_cheese}")
        else:
        
            print(y,f"${price_m+price_pepe}")
    else:
        if extra_cheese=="Y":
        
            print(y,f"${price_m+price_cheese}")
        else:
        
            print(y,f"${price_m}")
            
elif size=="L":
    if add_pepperoni=="Y":
        if extra_cheese=="Y":
          
            print(y,f"${price_l+price_pepe+price_cheese}")
        else:
        
            print(y,f"${price_l+price_pepe}")
    else:
        if extra_cheese=="Y":
        
            print(y,f"${price_l+price_cheese}")
        else:
        
            print(y,f"${price_l}")

    