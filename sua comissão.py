comissão = int(input("Quantos reais você vendeu hoje?"))
var="Sua comissão é: "

if comissão >= 1600 and comissão <= 3000:
    print(var, 1500)
    
elif comissão > 3000 and comissão<=5000:
    print(var, 3500)
    
elif comissão < 1599 and comissão >= 1000:
    print(var, 900)
    
else:
    print("Fale com o gerente por favor")
        