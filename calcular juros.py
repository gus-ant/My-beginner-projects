

#eu nomeei a como os juros sobre o investimento durante um mês
def juros(a):
    result= a*int(input("quanto você quer aplicar em Selic(5% de juros ao mês)?"))
    return result
#a é igual ao juros
result=juros(1.05)
print("no próximo mês você terá: ", round(result))
result=juros(1.05**12)
print("daqui a 12 meses você terá", round(result*12))