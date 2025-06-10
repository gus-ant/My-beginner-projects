import random
import time

# Dimensões da tela
LARGURA = 40
ALTURA = 20

# Posição inicial do pinguim
pinguim_x = LARGURA // 2
pinguim_y = ALTURA // 2

# Velocidade do pinguim
velocidade_y = 0

# Posição do cano superior
cano_superior_x = LARGURA - 10
cano_superior_y_min = 5
cano_superior_y_max = ALTURA - 8

# Posição do cano inferior
cano_inferior_x = LARGURA - 10
cano_inferior_y_min = 8
cano_inferior_y_max = ALTURA

# Pontuação
pontuacao = 0

# Função para desenhar a tela
def desenhar_tela():
    print("+" + "-" * LARGURA + "+")
    for y in range(ALTURA):
        print("|", end="")
        for x in range(LARGURA):
            if x == pinguim_x and y == pinguim_y:
                print("@", end="")
            elif x == cano_superior_x and (cano_superior_y_min <= y <= cano_superior_y_max):
                print("#", end="")
            elif x == cano_inferior_x and (cano_inferior_y_min <= y <= cano_inferior_y_max):
                print("#", end="")
            else:
                print(" ", end="")
        print("|")
    print("+" + "-" * LARGURA + "+")

# Função para atualizar a posição do pinguim
def atualizar_pinguim(pinguim_y):
    global velocidade_y
    velocidade_y += 0.25
    if velocidade_y > 5:
        velocidade_y = 5
    pinguim_y += velocidade_y

# Função para atualizar a posição dos canos
def atualizar_canos():
    global cano_superior_y_min, cano_superior_y_max, cano_inferior_y_min, cano_inferior_y_max
    cano_superior_y_min = random.randint(5, ALTURA - 8)
    cano_superior_y_max = cano_superior_y_min + 8
    cano_inferior_y_min = cano_superior_y_max + 10
    cano_inferior_y_max = ALTURA

# Função para verificar colisão
def verificar_colisao():
    global pontuacao
    if (pinguim_x == cano_superior_x and
        (cano_superior_y_min <= pinguim_y <= cano_superior_y_max)) or \
       (pinguim_x == cano_inferior_x and
        (cano_inferior_y_min <= pinguim_y <= cano_inferior_y_max)):
        return True
    else:
        if pinguim_y <= 0 or pinguim_y >= ALTURA - 1:
            return True
        else:
            return False

# Loop principal do jogo
while True:
    # Desenhar a tela
    desenhar_tela()

    # Atualizar a posição do pinguim
    atualizar_pinguim(pinguim_y)

    # Atualizar a posição dos canos
    atualizar_canos()

    # Verificar colisão
    if verificar_colisao():
        print("Você perdeu!")
        break

    # Pontuação
    pontuacao += 1
    print(f"Pontuação: {pontuacao}")

    # Controle do pinguim (teclas)
    if input().lower() == " ":
        velocidade_y = -5

    # Tempo de espera entre as atualizações
    time.sleep(0.1)
