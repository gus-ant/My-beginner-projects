notas=[]
for x in range(3):
    notaal=input("nota?")
    nome=input("nome?")
    resultado=[notaal,nome]
    notas.append(resultado)
print("qtd de notas", len(notas))

for n in notas:
    notaal=n[0]
    nome=n[1]
    print("aluno:",nome,"tirou nota:",notaal)