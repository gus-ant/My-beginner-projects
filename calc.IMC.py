# 1st input: enter height in meters e.g: 1.65
height = input("Altura? (m) ")
# 2nd input: enter weight in kilograms e.g: 72
weight = input("Peso? (em kg) ")
# 🚨 Don't change the code above 👆

# Write your code below this line 👇
imc = (float(weight) / (float(height) * float(height)))

print("seu IMC é: ", round(imc, 2))

#>>>Aqui será dito o estado da pessoa:

vc = "Você está: "
if imc <= 19:
    print(vc + "magro")
elif imc > 19 and imc <= 25:
    print(vc + "normal")
elif imc > 25 and imc <= 30:
    print(vc + "acima do peso")
else:
    print(vc + "obeso")
