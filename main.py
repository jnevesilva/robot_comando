##Código para o comando
#######################
from microbit import *
import radio
import utime
import music

radio.on()
robot_id=1
em_corrida=False
tempo_inicio = 0
tempo_final = 0

radio.config(group=robot_id)

def calcular_forca(inclinacao):
    if abs(inclinacao) < 200:
        return 0
    sinal = 1 if inclinacao > 0 else -1
    forca = (abs(inclinacao) - 200) * (255 / 800)
    return int(min(forca, 255) * sinal)

dist_str = "--"

while True:
    if button_b.is_pressed():
        if not em_corrida:
            # INICIAR CORRIDA
            em_corrida = True
            tempo_inicio = utime.ticks_ms()
            radio.send("M:0,0,0,0") # O '1' no fim faz reset às penalizações do carro
            music.pitch(1000, 200, wait=True) # Som de partida
            display.show(Image.YES)
            sleep(1000) # Esperar que o jogador largue os botões
        else:
            # TERMINAR CORRIDA
            em_corrida = False
            radio.send("M:0,0,0,0") # Travar o carro
            tempo_final = utime.ticks_diff(utime.ticks_ms(), tempo_inicio) / 1000 # Tempo em segundos
            music.play(music.ENTERTAINER, wait=False) # Som de vitória
            
            # Espera que tires o dedo do botão B antes de avançar
            while button_b.is_pressed():
                sleep(50)
            # Mostra os resultados no ecrã repetidamente
            while not (button_b.is_pressed()):
                display.scroll("T:" + str(int(tempo_final)))
            sleep(1000) # Previne duplo clique ao tentar sair do ecrã de pontuação
            display.show(Image.TARGET)
            
    if em_corrida:
        x = accelerometer.get_x()
        y = accelerometer.get_y()
    
        acelerador = calcular_forca(-y)
        volante = calcular_forca(x)
    
        m_esq = max(-255, min(255, acelerador + volante))
        m_dir = max(-255, min(255, acelerador - volante))

        # 1. Lê o botão B: se estiver premido é 1, senão é 0
        buzina = 1 if pin_logo.is_touched() else 0
    
        # 2. Envia a nova mensagem tripla (Ex: "M:200,150,1")
        radio.send("M:" + str(m_esq) + "," + str(m_dir) + "," + str(buzina))
    
        px = max(0, min(4, int((x + 1024) / 2048 * 5)))
        py = max(0, min(4, int((y + 1024) / 2048 * 5)))
        display.clear()
        display.set_pixel(px, py, 9)
    
    # selecionar o robot a comandar
    if button_a.is_pressed():
        # Incrementa o contador
        robot_id += 1
        if robot_id > 9:
            robot_id  = 1
        display.show(robot_id)
        radio.config(group=robot_id)
        # Pausa para evitar que os números saltem muito rápido
        while button_a.is_pressed():
           sleep(50)
