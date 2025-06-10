tam=input("qual o tamanho da pizza?(S,M,L)")

bill=0

if tam=="S":
    bill+=15
elif tam=="M":
    bill+=20
else:
    bill+=25

add=input("recheio adicional?(Y,N)")

if add=="Y":
    bill+=5.99

queijo=input("queijo adicional?(Y,N)")

if queijo=="Y":
    bill+=6.50
    
print(f"Por favor, pague {bill} reais")