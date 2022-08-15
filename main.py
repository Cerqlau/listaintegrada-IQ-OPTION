from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
from dateutil import tz
from colorama import Fore
from bs4 import BeautifulSoup
import threading, json, sys, requests, configparser, csv, time, os, colorama,logging
import pandas as pd



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

colorama.init(autoreset=True) # Garante reinício de cor no próximo comando print
logging.disable(level=(logging.DEBUG)) #Desabilita logs de erro para execução via arquivo.exe

def Explicense(datet):
	ExpirationDate = str(time.strftime("%Y-%m-%d"))
	if ExpirationDate > datet:
		print(f'\n{Fore.LIGHTYELLOW_EX}>>>>>RENOVE A LICENÇA - TEMPO DE TESTE ACABOU!<<<<<\n')
		print(f'\n{Fore.LIGHTYELLOW_EX}Para renovação entre em contato @laurorcerqueira\n')
		time.sleep(60)
		sys.exit()
	elif ExpirationDate == datet:
		print(f'\n{Fore.LIGHTYELLOW_EX}>>>>>LICENÇA EXPIRA HOJE!<<<<<\n')



def capturar_pares():
    global API, capturapares
    pares = {'digital': {}, 'binary': {}, 'turbo': {}}
    print('\n')
    print('Iniciando captura de pares...', end='\r')
    P = ''
    for i in range(3):
        try:
            P = API.get_all_open_time()
        except:
            pass
        if P == None:
            API.connect()
            if API.check_connect():
                continue
            else:
                print(' Erro ao conectar')
                input('\n\n Aperte enter para sair')
                sys.exit()
        elif type(P) == dict:
            capturapares=P
            break
    if P != None and P != '':
        for p in P['digital']:
            if P['digital'][ p ]['open']:
                c=API.get_digital_payout(p)
                if ( c != None):
                    pares['digital'].update({p: round( int(c) / 100 , 2)  })
                   # print(' [ DIGITAL ]:', p,'-',Fore.LIGHTYELLOW_EX+pares['digital'][p], '      ')
                else:
                    pares['digital'].update({p: 0.0  })
                  #  print(' [ DIGITAL ]:', p, '-',Fore.LIGHTYELLOW_EX+pares['digital'][p], '      ')


        d = API.get_all_profit()
        for tipo in ['turbo', 'binary']:
            for p in P[ tipo ]:
                if P[ tipo ][ p ]['open']:
                    e=d[ p ][ tipo ]
                    if e != None :
                        pares[ tipo ].update({p: d[ p ][ tipo ]  })
                       # print(' [', tipo.upper(),']:', p, '-',Fore.LIGHTYELLOW_EX + pares[ tipo ][p], '      ')
                    else:
                        pares[ tipo ].update({p: 0.0 })
                      #  print(' [', tipo.upper(),']:', p, '-',Fore.LIGHTYELLOW_EX + pares[ tipo ][p], '      ')

       #print(json.dumps(pares, indent=1))
        print(' \nCaptura de paridades finalizada!')
    return pares


def capturar_pares2():
    global API, capturapares
    pares = {'digital': {}, 'binary': {}, 'turbo': {}}

    P = ''
    for i in range(3):
        try:
            P = API.get_all_open_time()
        except:
            pass
        if P == None:
            API.connect()
            if API.check_connect():
                continue
            else:
                print(' Erro ao conectar')
                input('\n\n Aperte enter para sair')
                sys.exit()
        elif type(P) == dict:
            capturapares=P
            break
    if P != None and P != '':
        for p in P['digital']:
            if P['digital'][ p ]['open']:
                c=API.get_digital_payout(p)
                if ( c != None):
                    pares['digital'].update({p: round( int(c) / 100 , 2)  })
                    #print(' [ DIGITAL ]:', p, '-', pares['digital'][p], '      ')
                else:
                    pares['digital'].update({p: 0.0  })
                    #print(' [ DIGITAL ]:', p, '-', pares['digital'][p], '      ')


        d = API.get_all_profit()
        for tipo in ['turbo', 'binary']:
            for p in P[ tipo ]:
                if P[ tipo ][ p ]['open']:
                    e=d[ p ][ tipo ]
                    if e != None :
                        pares[ tipo ].update({p: d[ p ][ tipo ]  })
                       # print(' [', tipo.upper(),']:', p, '-', pares[ tipo ][p], '      ')
                    else:
                        pares[ tipo ].update({p: 0.0 })
                        #print(' [', tipo.upper(),']:', p, '-', pares[ tipo ][p], '      ')
        #print(f'\n{Fore.LIGHTGREEN_EX}PAYOUT ATUALIZADO!')
    return pares

def horaAtual():
    data = datetime.now()
    tm = tz.gettz('America/Sao Paulo')
    tempoAtual = data.astimezone(tm)
    horaAgora = tempoAtual.strftime('%H:%M:%S')
    return horaAgora


def timerzone(timeframe):
    if traderTimerZone == 'S':
        if timeframe < 5:
            soup = BeautifulSoup(timerzoner60_300.text, 'html.parser') #faz um parser para trabalharmos a página
        else:
            soup = BeautifulSoup(timerzoner5_15.text, 'html.parser')

        table = soup.find('table', attrs={'id': 'map-responsive'})
        rows = table.findAll('th', {"class": "th-map"})
        horariosECores = {}
        for x in rows:
            bg = x.attrs['style'].replace(";background:", "")
            if bg == "#ED3237":
                cor = "Vermelho"
            else:
                cor = ""
            hora = x.text
            hora = hora.replace("\n                                ", "").replace(
                "              ", "")
            hc = {hora: cor}
            horariosECores.update(hc)

        for x in horariosECores:
            if horaAtual()[0:5] == x and horariosECores[x] == 'Vermelho':
                return True
        return False
    else:
        return False


def Total_Operacoes(lucro):
	global total_operacoes, vitorias, derrotas, total_porcentagem
	if int(lucro) > 0:
		vitorias += 1
	else:
		derrotas += 1
	total_operacoes = vitorias + derrotas
	total_porcentagem = int(vitorias / total_operacoes * 100)
	if trailing_stop == 'S':
		Trailing_Stop(lucro)


def verifica_conexao(status,erro):
	if status == True:
		print('Conta conectada com sucesso')
	else: 
		print(f'Erro ao conectar: {erro}')
		input("")
		sys.exit()
	
	
def banca():
	global account_type, account_balance, valor_da_banca
	account_type = config['conta']
	valor_da_banca = API.get_balance()
	account_balance = '${:,.2f}'.format(valor_da_banca) if API.get_currency(
	) == 'USD' else 'R${:,.2f}'.format(valor_da_banca)


def configuracao():
	global vitorias, derrotas, total_operacoes, total_porcentagem
	arquivo = configparser.RawConfigParser()
	thisfolder = os.path.dirname(os.path.abspath(__file__))
	initfile = os.path.join(thisfolder, 'config.txt')
	arquivo.read(initfile)
	vitorias = 0
	derrotas = 0
	total_operacoes = 0
	total_porcentagem = 0

	return {'listacsv': arquivo.get('GERAL', 'listacsv'),'delay_entrada': arquivo.get('GERAL', 'delay_entrada'),'entrada': arquivo.get('GERAL', 'entrada'), 'entrada_percentual': arquivo.get('GERAL', 'entrada_percentual'), 'conta': arquivo.get('GERAL', 'conta'), 'stop_win': arquivo.get('GERAL', 'stop_win'), 'stop_loss': arquivo.get('GERAL', 'stop_loss'), 'payout': 0, 'banca_inicial': 0, 'martingale': arquivo.get('GERAL', 'martingale'), 'mgProxSinal': arquivo.get('GERAL', 'mgProxSinal'), 'valorGale': arquivo.get('GERAL', 'valorGale'), 'niveis': arquivo.get('GERAL', 'niveis'), 'analisarTendencia': arquivo.get('GERAL', 'analisarTendencia'), 'noticias': arquivo.get('GERAL', 'noticias'), 'timerzone': arquivo.get('GERAL', 'timerzone'), 'hitVela': arquivo.get('GERAL', 'hitVela'), 'telegram_token': arquivo.get('telegram', 'telegram_token'), 'telegram_id': arquivo.get('telegram', 'telegram_id'), 'usar_bot': arquivo.get('telegram', 'usar_bot'), 'email': arquivo.get('CONTA', 'email'), 'senha': arquivo.get('CONTA', 'senha'), 'trailing_stop': arquivo.get('GERAL', 'trailing_stop'), 'trailing_stop_valor': arquivo.get('GERAL', 'trailing_stop_valor'), 'payout_minimo': arquivo.get('GERAL', 'payout'), 'usar_ciclos': arquivo.get('CICLOS', 'usar_ciclos'), 'ciclos_nivel': arquivo.get('CICLOS', 'nivel_ciclos'),'soros': arquivo.get('GERAL', 'soros'),'niveis_soros': arquivo.get('GERAL', 'niveis_soros'),'travasoros':arquivo.get('GERAL','finalizar_em_soros'),'tipoopcao': arquivo.get('GERAL', 'opcao'),'mgPayout': arquivo.get('GERAL','mgPayout') }


def Clear_Screen():
	sistema = os.name
	if sistema == 'nt':
		os.system('cls')
	else:
		os.system('clear')



#inicialização variáveis globais

vitorias = 0
derrotas = 0
timerzoner60_300 = ''
timerzoner5_15 = ''

config = configuracao()
email = config['email']
senha = config['senha']

global galeRepete, lucroTotal,capturaopcao, parAntigo, direcaoAntigo, timeframeAntigo,capturaid_binaria, valor_entrada,soros,niveis_soros,quantidadesoros,galeSinalRepete,proxSinal,capturaid
datet = str('2022-10-01')
galeRepete = False
entrou_gale = False
estavanogale=False
estavanosoro=False
deuempatenogale=False
estavanogalesignal=False
perdeunosoros=False
ns=1
nv=1
parAntigo = ''
direcaoAntigo = ''
timeframeAntigo = ''
galeantigo=0.0
lucroTotal = 0.0
with open('swapresultadolista.txt','w') as arquivo:
    arquivo.write(str(lucroTotal))
arquivo.close()
lucroTotal=float(lucroTotal)
lucro=0.0
perdas = 0.0
novo_stop_loss = 0
loop=0
cont_gale_sinal=0
trailing_ativo = False
tipoOpcao = str(config['tipoopcao'])
valorGaleProxSinal = float(config['entrada'])
valor_entrada = float(config['entrada'])
analisarTendencia = config['analisarTendencia']
galeVela = config['mgProxSinal']
galeSinal = config['martingale']
galepayout = config['mgPayout']
noticias = config['noticias']
traderTimerZone = config['timerzone']
hitdeVela = config['hitVela']
trailing_stop = config['trailing_stop']
trailing_stop_valor = float(config['trailing_stop_valor'])
payout_minimo = int(config['payout_minimo'])
ciclos_ativos = 0
valor_entrada_ciclo = float(config['entrada'])
entrada_percentual = config['entrada_percentual']
delay_entrada = int(abs((int(config['delay_entrada'])))*-1)
periodo = 20
soros= str(config['soros'])
niveis_soros=int(config['niveis_soros'])
quantidadesoros =0
lucro_dig=0.0
lucro_bin=0.0
capturaid_digtal = 0
capturaid_binaria =0
capturaopcao=False
capturapares=False
capturapayout =0.0
travasoros=str(config['travasoros'])
verificastop=False

global VERIFICA_BOT, TELEGRAM_ID
VERIFICA_BOT = config['usar_bot']
TELEGRAM_ID = config['telegram_id']
Clear_Screen()

def banner2():
	os.system('cls' if os.name == 'nt' else 'clear')
	print ("")
	print ("")
	print (Fore.GREEN+"██╗     █████╗██╗   ██╗██████╗ ███████╗")
	print (Fore.GREEN+"██║   ██╔══██╗██║   ██║██╔══██╗██╔══██║")
	print (Fore.GREEN+"██║   ███████║██║   ██║██████╔╝██║  ██║")
	print (Fore.GREEN+"██╚══╗██╔══██║██║   ██║██╔══██╗██║  ██║")
	print (Fore.GREEN+"█████║██║  ██║████████║██║  ██║███████║")
	print (Fore.GREEN+"╚════╝╚═╝  ╚═╝╚═══════╝╚═╝  ╚═╝╚══════╝")
	print (Fore.GREEN+"██████╗ ███████╗████████╗███████╗")
	print (Fore.GREEN+"██╔══██╗██╔══██║╚══██╔══╝██╔════╝")
	print (Fore.GREEN+"██████╔╝██║  ██║   ██║   ███████╗")
	print (Fore.GREEN+"██╔══██╗██║  ██║   ██║   ╚════██║")
	print (Fore.GREEN+"██████╔╝███████║   ██║   ███████║")
	print (Fore.GREEN+"╚═════╝ ╚══════╝   ╚═╝   ╚══════╝v0.7")
	print (Fore.GREEN+"=======================================")
	print (Fore.LIGHTRED_EX+"Written by @laurocerqueira")
	print ("")
	print (Fore.LIGHTBLUE_EX+"Este Bot tem como objetivo realizar operações a partir de uma lista CSV")
	print (Fore.LIGHTBLUE_EX+"#vamosdominaromercado #tradermilionário")
	print (Fore.LIGHTBLUE_EX+"Este BOT é FREE se você comprou DENUNCIE !"+Fore.RESET)
	print ("")

#==============================================#
#Função para animação de loading               #
#==============================================#
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()
#==============================================#
#Função para carregamento da lista de sinais   #
#==============================================#
def carregar_sinais():
	global filecsv__
	arquivo = open(filecsv__, encoding='UTF-8')
	lista = arquivo.read()
	arquivo.close
	lista = lista.split('\n')

	for index,a in enumerate(lista):
		if a == '':
			del lista[index]
	time.sleep(1)
	return lista

#==============================================#
#Função para captura do Perfil do usuário      #
#==============================================#
def perfil():
  perfil = json.loads(json.dumps(API.get_profile_ansyc()))

  return perfil

  '''
		name
		first_name
		last_name
		email
		city
		nickname
		currency
		currency_char
		address
		created
		postal_index
		gender
		birthdate
		balance
	'''
########################### INÍCIO DO BOT ###############################

banner2()

Explicense(datet)

if noticias == 'S':
	try:
		response = requests.get("http://botpro.com.br/calendario-economico/")
		texto = response.content
	except:
		print('Erro ao carregar json de notícias!!')
		noticias = 'N'
if traderTimerZone == 'S':
	try:
		timerzoner60_300 = requests.get('https://tradertimerzone.com/web/index.php?r=operation/maps&model=60-300', headers=headers)
		timerzoner5_15 = requests.get('https://tradertimerzone.com/web/index.php?r=operation%2Fmaps&model=5-15', headers=headers)
	except:
		print('Erro ao carregar json do Trader Timer Zone!!')
		traderTimerZone = 'N'

API = IQ_Option(email, senha)
checkstatus,reason = API.connect()
verifica_conexao(chekstatus,reason)
API.change_balance(config['conta'])
#Chamada do perfil do usuário
dados=perfil()   # a variável dados recebe todas as informações da função perfil
print("")

# Definição de variáveis para animação
items = list(range(0, 57))
l = len(items)

#Impressão de dados do usuário
print('\n#:===============================================================:#')
print(f"   Esta é sua versão da API {IQ_Option.__version__}")
print('#:===============================================================:#')
print(f"Bem vindo: {dados['name']}")
#print(f"Apelido: {dados['nickname']}")
#print(f"Cidade: {dados['city']}")
#print(f"Endereço: {dados['address']}")
#print(f"Data de criação da conta: {timestamp_converter(dados['created'])}")
account_balance = '$ {:,.2f}'.format(API.get_balance()) if API.get_currency() == 'USD' else 'R$ {:,.2f}'.format(API.get_balance())
print(f"{'Saldo da conta de Treinamento' if API.get_balance_mode() == 'PRACTICE' else 'Saldo da conta REAL'}: {account_balance}")
print('#:===============================================================:#')
mensagmperfil= '#:===============================================================:#\n'+f"Bem vindo: {dados['name']}\n"+f"Cidade: {dados['city']}\n"
mensagmperfil+=f"Endereço: {dados['address']}\n"+f"{'Saldo da conta de Treinamento' if API.get_balance_mode() == 'PRACTICE' else 'Saldo da conta REAL'}: {account_balance}\n"+'#:===============================================================:#'

mensagemconfig=f'   CONFIGURAÇÕES DO BOT\n'+'#:===============================================================:#\n'
mensagemconfig+=f"Lista de Sinais: "+f"{str(config['listacsv'])}\n"
mensagemconfig+=f"Valor de Entrada: R${config['entrada']}\n"+f"Valor Entrada percentual: "+f"{'Ativada' if config['entrada_percentual'] == 'S' else 'Desativada'}\n"
mensagemconfig+=f"Delay de Entrada: "+f"-{str(config['delay_entrada'])}s\n"
mensagemconfig+=f"Tipo de Conta: "+f"{'Treinamento' if config['conta'] == 'PRACTICE' else 'Real'}\n"
mensagemconfig+=f"Stop Win: R$"+f"{str(config['stop_win'])}\n"
mensagemconfig+=f"Stop Loss: R$"+f"{str(config['stop_loss'])}\n"
mensagemconfig+=f"Trailing Stop: "+f"{'Ativado' if config['trailing_stop'] == 'S' else 'Desativado'}\n"
mensagemconfig+=f"Trailing Stop Valor: R$"+f"{str(config['trailing_stop_valor'])}\n"
mensagemconfig+=f"Payout Mínimo: "+f"{str(config['payout_minimo'])}%\n"
mensagemconfig+=f"Opção escolhida: "+f" {str(config['tipoopcao'])}\n"
mensagemconfig+=f"Martingale Próxima Vela: "+f"{'Ativado' if config['martingale'] == 'S' else 'Desativado'}\n"
mensagemconfig+=f"Martingale Próximo Sinal: "+f"{'Ativado' if config['mgProxSinal'] == 'S' else 'Desativado'}\n"
mensagemconfig+=f"Martingale Tipo: "+f"{'Recuperação' if config['mgPayout'] == 'S' else 'Cobertura'}\n"
mensagemconfig+=f"Fator martingale de cobertura: x"+f"{str(config['valorGale'])}\n"
mensagemconfig+=f"Niveis martingale: "+f"{str(config['niveis'])}\n"
mensagemconfig+=f"Soros: "+f"{'Ativado' if config['soros'] == 'S' else 'Desativado'}\n"
mensagemconfig+=f"Niveis Soros: "+f"{str(config['niveis_soros'])}\n"
mensagemconfig+=f"Finalizar em Soros: "+f"{'Ativado' if str(travasoros) == 'S' else 'Desativado'}\n"
mensagemconfig+=f"Usar Ciclos: "+f"{'Ativado' if config['usar_ciclos'] == 'S' else 'Desativado'}\n"
mensagemconfig+=f"Niveis Ciclos: "+f"{str(config['ciclos_nivel'])}\n"
mensagemconfig+='#:===============================================================:#\n'+'   FITLTROS DO BOT\n'+'#:===============================================================:#\n'
mensagemconfig+=f"Analisar Tendência EMA10: "+f"{'Ativado' if config['analisarTendencia'] == 'S' else 'Desativado'}\n"
mensagemconfig+=f"Analisar Notícias Infomoney: "+f"{'Ativado' if config['noticias'] == 'S' else 'Desativado'}\n"
mensagemconfig+=f"Analisar Timerzone Infomoney: "+f"{'Ativado' if config['timerzone'] == 'S' else 'Desativado'}\n"
mensagemconfig+=f"Analisar HIT de VELA no PAR: "+f"{'Ativado' if config['hitVela'] == 'S' else 'Desativado'}\n"
mensagemconfig+='#:===============================================================:#\n'+'   CONFIGURAÇÃO TELEGRAM\n'+'#:===============================================================:#\n'
mensagemconfig+=f"Envio de mensagns Telegram: "+f"{'Ativado' if config['usar_bot'] == 'S' else 'Desativado'}\n"
mensagemconfig+=f"Telegram Token: "+f"{str(config['telegram_token'])}\n"
mensagemconfig+=f"Telegram ID: "+f"{str(config['telegram_id'])}\n"+'#:===============================================================:#'
print(mensagemconfig)

#verfirica se o arquivo foi digitado corretamente
while True:
	print('\nA configuração está correta?(y/n): ', end='')
	verifica_lista=str(input())
	if verifica_lista == 'y' or verifica_lista=='Y':
		print('\nOk então vamos prosseguir')
		time.sleep(0.3)
		break
	elif verifica_lista == 'n' or verifica_lista=='N':
		input('\nFaz o seguinte localize o arquivo config.txt existente na pasta preencha, salve e execute o bot novamente')
		os.system('exit' if os.name == 'nt' else 'exit')
		sys.exit()
	else:
		input('\nResposta inválida estou desligando')
		os.system('exit' if os.name == 'nt' else 'exit')
		sys.exit()



while True:
	arquivofile = str(config['listacsv'])
	thisfolder = os.path.dirname(os.path.abspath(__file__))
	initfile = os.path.join(thisfolder, arquivofile)
	filecsv__ = str(initfile)

	if len(filecsv__) > 0 and filecsv__.count('.csv') > 0:
		break
	else:
		print('Fala sério!!! O arquivo está escrito algo assim *sinais_YYYY-MM-DD_TM.csv* tenta de novo')
		arquivofile= str(input())
		time.sleep(1)



# Chama da função para carregamento da lista de sinais e impressão dos dados catalogados na lista
lista=carregar_sinais()
print("\nOk estou carregando a lista")

# Chamada para animação início em 0%
printProgressBar(0, l, prefix = 'Uploading de lista:', suffix = 'Complete', length = 50)
for i, item in enumerate(items):
    # Do stuff...
    time.sleep(0.1)
    # Update Progress Bar
    printProgressBar(i + 1, l, prefix = 'Uploading de lista:', suffix = 'Complete', length = 50)

mensagemlista=f'   LISTA DE SINAIS: {arquivofile} CARREGADA\n'+f'#:===============================================================:#\n'
print("")
for sinal in lista:
	dados = sinal.split(';')
	#mensagemlista += f"{str(dados[1])} - {str(dados[2])} - {str(dados[3])}\n"
	a =Fore.LIGHTRED_EX if dados[3] == 'PUT' else Fore.LIGHTGREEN_EX
	print(f'{Fore.LIGHTYELLOW_EX}{dados[1]}{Fore.RESET} - {dados[2]} - {a}{dados[3]}{Fore.RESET}')
print(f'\nTotal de {len(lista)} sinais carregados')




print('\nA lista esta correta?(y/n): ', end='')
verifica_lista=str(input())
if verifica_lista == 'y' or verifica_lista=='Y':
   print('\n Ok então vamos prosseguir, estou carregando os sinais')
   time.sleep(0.5)
elif verifica_lista == 'n' or verifica_lista=='N':
	input('\nFaz o seguinte localize e apague os arquivos .csv existentes na pasta, execute novamente o bot e gere outra lista...')
	os.system('exit' if os.name == 'nt' else 'exit')
	sys.exit()
else:
	input('\nResposta inválida estou desligando')
	os.system('exit' if os.name == 'nt' else 'exit')
	sys.exit()

# Chamada para animação início em 0%
printProgressBar(0, l, prefix = 'Carregando sinais:', suffix = 'Complete', length = 50)
for i, item in enumerate(items):
    # Do stuff...
    time.sleep(0.1)
    # Update Progress Bar
    printProgressBar(i + 1, l, prefix = 'Carregando sinais:', suffix = 'Complete', length = 50)


parescapturados=capturar_pares()


def Mensagem(mensagem):
	if VERIFICA_BOT == 'S':
		token = config['telegram_token']
		url = f'https://api.telegram.org/bot{token}/'
		try:
			return requests.post(url + 'sendMessage', {'chat_id': TELEGRAM_ID, 'text': str(mensagem)})
		except:
			print(f'{Fore.RED}ERRO AO ENVIAR MENSAGEM AO TELEGRAM!!')



def timestamp_converter():
	hora = datetime.now()
	tm = tz.gettz('America/Sao Paulo')
	hora_atual = hora.astimezone(tm)
	return hora_atual.strftime('%H:%M:%S')


def timeFrame(timeframe):

	if timeframe == 'M1':
		return 1

	elif timeframe == 'M5':
		return 5

	elif timeframe == 'M15':
		return 15

	elif timeframe == 'M30':
		return 30

	elif timeframe == 'H1':
		return 60
	else:
		return 'erro'


def verificarStop():
	global stop_win,stop_loss,lucroTotal
	a=''
	try:
		if float(lucroTotal) >= float(stop_win):
			deustop = 'WIN'
			a=Fore.LIGHTBLUE_EX
		elif float(lucroTotal) <= float(stop_loss):
			deustop = 'LOSS'
			a=Fore.LIGHTRED_EX
		else:
			deustop = False
		if deustop:
			verificastop = True
			while True:
				thread_ativas = threading.active_count()
				if thread_ativas == 3:
					banca()
					mensagem = f'{a}STOP {deustop} BATIDO!!! - RESULTADO: {float(round(lucroTotal, 2))}\n'
					mensagem += f'{Fore.RESET}Operações: {total_operacoes} | Vencedoras: {vitorias} | Perdedoras: {derrotas}\nAssertividade: {total_porcentagem}%\n'
					mensagem += f"Saldo da conta {'demo' if account_type == 'PRACTICE' else 'real'}: {account_balance}"
					print(f'{mensagem}')
					Mensagem(mensagem)
					sys.exit()
				else:
					print(
						f'{Fore.RED}AGUARDANDO FINALIZAÇÃO DE {Fore.GREEN}{thread_ativas - 3} THREADS', end='\x1b[K\r')
					time.sleep(5)
	except:
		pass
     


def Trailing_Stop(lucro):
	global stop_loss, novo_stop_loss
	if lucroTotal >= trailing_stop_valor and lucro > 0:
		novo_stop_loss += int(lucro)
		stop_loss = novo_stop_loss
		print(f'{Fore.GREEN}Trailing STOP ajustado! Novo STOP LOSS: {stop_loss}')
		Mensagem(f'Trailing STOP ajustado! Novo STOP LOSS: {stop_loss}')



def buscarMenor():

	global em_espera, get_profit,filecsv__
	get_profit = True
	arquivo = open(filecsv__ )
	leitor = csv.reader(arquivo, delimiter=';')
	timeNow = timestamp_converter()
	f = '%H:%M:%S'
	em_espera = []
	for row in leitor:
		if len(row[2]) == 5:
			horario = row[2] + ":00"
		else:
			horario = row[2]
		dif = int((datetime.strptime(timeNow, f) - datetime.strptime(horario, f)).total_seconds())
		# Filtro para excluir os sinais que ja se passaram os horarios
		if dif < -40:
			# Adiciona a diferença de tempo em segundos para posterior sorteio de menor valor
			row.append(dif)
			# Coloca os dados da paridade juntamente com o tempo restante para entrada em uma lista
			em_espera.append(row)

	# Verifica se a lista tem sinais pendentes para operar, caso contrario verifica se ainda tem posicoes abertas e aguarda o encerramento pra finalizar o bot
	if len(em_espera) == 0:
		while True:
			thread_ativas = threading.active_count()
			if thread_ativas == 3:
				em_espera = False
				banca()
				mensagem = f'Lista de sinais finalizada..\nLucro: R${str(round(lucroTotal, 2))}\n'
				mensagem += f'Operações: {total_operacoes} | Vencedoras: {vitorias} | Perdedoras: {derrotas}\n Assertividade: {total_porcentagem}%\n'
				mensagem += f"Saldo da conta {'demo' if account_type == 'PRACTICE' else 'real'}: {account_balance}"
				print(f'{Fore.GREEN}{mensagem}')
				Mensagem(mensagem)
				sys.exit()
			else:
				print(
				    f'{Fore.RED}AGUARDANDO FINALIZAÇÃO DE {Fore.GREEN}{thread_ativas - 3} THREADS', end='\x1b[K\r')
				time.sleep(60)
	else:
		# Ordena a lista pela entrada mais proxima
		em_espera.sort(key=lambda x: x[4], reverse=True)
		# Informa quantos sinais restam para serem executados
		print(f'SINAIS PENDENTES: {len(em_espera)}')
		# Informa o próximo sinal a ser executado
		print(f'{Fore.GREEN}PROXIMO: {em_espera[0][1]} | TEMPO: {em_espera[0][0]} | HORA: {em_espera[0][2]} | DIREÇÃO: {em_espera[0][3]}')
		Mensagem(f'SINAIS PENDENTES: {len(em_espera)}\nPROXIMO: {em_espera[0][1]} | TEMPO: {em_espera[0][0]} | HORA: {em_espera[0][2]} | DIREÇÃO: {em_espera[0][3]}')


def noticas(paridade):
	global noticas

	if noticias == 'S':
		try:
			objeto = json.loads(texto)

			# Verifica se o status code é 200 de sucesso
			if response.status_code != 200 or objeto['success'] != True:
				print('Erro ao contatar notícias')

			# Pega a data atual
			data = datetime.now()
			tm = tz.gettz('America/Sao Paulo')
			data_atual = data.astimezone(tm)
			data_atual = data_atual.strftime('%Y-%m-%d')
			tempoAtual = data.astimezone(tm)
			minutos_lista = tempoAtual.strftime('%H:%M:%S')

			# Varre todos o result do JSON
			for noticia in objeto['result']:
				# Separa a paridade em duas Ex: AUDUSD separa AUD e USD para comparar os dois
				paridade1 = paridade[0:3]
				paridade2 = paridade[3:6]

				# Pega a paridade, impacto e separa a data da hora da API
				moeda = noticia['economy']
				impacto = noticia['impact']
				atual = noticia['data']
				data = atual.split(' ')[0]
				hora = atual.split(' ')[1]

				# Verifica se a paridade existe da noticia e se está na data atual
				if moeda == paridade1 or moeda == paridade2 and data == data_atual:
					formato = '%H:%M:%S'
					d1 = datetime.strptime(hora, formato)
					d2 = datetime.strptime(minutos_lista, formato)
					dif = (d1 - d2).total_seconds()
					# Verifica a diferença entre a hora da noticia e a hora da operação
					minutesDiff = dif / 60

					# Verifica se a noticia irá acontencer 30 min antes ou depois da operação
					if minutesDiff >= -30 and minutesDiff <= 0 or minutesDiff <= 30 and minutesDiff >= 0:
						if impacto >= 1:
							return impacto, moeda, hora, True
					else:
						pass
				else:
					pass
			return 0, 0, 0, False
		except:
			print('Erro ao verificar notícias!! Filtro não funcionará')
			return 0, 0, 0, False
	else:
		return 0, 0, 0, False





all_asset =''
profit=''

def Get_All_Profit(par):
	global all_asset, profit,API
	digital=None

	profit = API.get_all_profit()

	for i in range(5):
		try:
			all_asset = API.get_all_open_time()
		except:
			pass

		if all_asset == None:
			API.connect()
			if API.check_connect():
				continue
			else:
				print(' Erro ao conectar')
				input('\n\n Aperte enter para sair')
				sys.exit()
		elif type(all_asset) == dict:
			break

	if all_asset != None and all_asset != '':
		print(Fore.RED+'SOU DIFERENTE DE NONE')
		for p in all_asset['digital']:
			if all_asset['digital'][ p ]['open']:
				check = API.get_digital_payout(p)
				if check !=None and check !='':
					print ('check: ',check)
					break

		if all_asset['digital'][par]['open']:
			digital = API.get_digital_payout(par)

		if digital == None or digital =='':
			return check
		else:
			print ('digital:', digital)
			return int(digital)




def checkProfit(par, timeframe,parescapturados):
	binaria = False
	turbo = False
	digital=False

	if timeframe > 15:
		try:
			if parescapturados["turbo"][par]:
				turbo = parescapturados["turbo"][par] * 100
				print(f'\n{par} - TURBO: {str(turbo)}')
				return "binaria", binaria
		except:
			pass

	try:
		if parescapturados["turbo"][par]:
			turbo = parescapturados["turbo"][par] * 100
			print(f'\n{par} -TURBO: {str(turbo)}')
	except:
		pass
	try:
		if parescapturados["digital"][par]:
			digital = parescapturados["digital"][par]*100
			print(f'{par} -DIGITAL: {str(digital)}')
	except:
		pass
	try:
		if parescapturados["binary"][par]:
			binaria = parescapturados["binary"][par] * 100
			print(f'{par} -BINARIA: {str(turbo)}')
	except:
		pass

	digital = 0.0 if digital == False else digital
	binaria = 0.0 if binaria == False else binaria
	turbo   = 0.0 if turbo   == False else turbo

	if timeframe>5 and timeframe <=15:
		if digital == 0.0 and binaria == 0.0:
			return False,0
		if binaria > digital:
			return "binaria", binaria
		if digital >= binaria:
			return "digital", digital



	if timeframe <=5:
		if digital == 0.0 and turbo == 0.0:
			return False,0
		if digital >= turbo:
			return "digital", digital
		if turbo >  digital:
			return "binaria", turbo





def Calcula_Valor_Ciclo(lucro):
	global valor_entrada_ciclo, ciclos_ativos
	ciclos_ativos += 1
	if lucro < 0 and ciclos_ativos <= int(config['ciclos_nivel']):
		valor_entrada_ciclo = round(float(config['entrada']) * (float(config['valorGale']) ** int(ciclos_ativos)))
	else:
		valor_entrada_ciclo = float(config['entrada'])
		ciclos_ativos = 0


def entradas(status, id, par, dir, timeframe, opcao, valorGaleSinal):
	global parescapturados,galeRepete,perdeunosoros, deuempatenogale,estavanogalesignal, estavanogale,estavanosoro,galepayout, lucroTotal,lucro_bin,lucro_dig,lucro,galeantigo,capturaopcao, parAntigo, direcaoAntigo,capturaid_digtal,capturaid_binaria, timeframeAntigo, valor_entrada, proxSinal, valorGaleProxSinal,quantidadesoros, niveis_soros,entrou_gale,perdas,ns,nv
	capturaopcao=status
	taxa = 0.0
	try:
		if opcao == 'digital':
			while True:
				resultado, taxa = API.check_win_digital_v2(id)
				if resultado:
					break
			if taxa !=None:
				lucro=taxa
				time.sleep(1)
				with open('swapresultadolista.txt','r') as arquivo:
					lucroTotal= arquivo.readline()
					lucroTotal=round(float(lucroTotal),2)
				arquivo.close()
				lucroTotal += lucro
				lucroTotal = round(lucroTotal,2)
				with open('swapresultadolista.txt','w') as arquivo:
					arquivo.write(str(lucroTotal))
				arquivo.close()
				lucroTotal = float(lucroTotal)
				galeRepete = False
				entrou_gale = False
				if lucro > 0:
					nv = 1
					ns =1
					perdeunosoros=False
					deuempatenogale=False #Reinicia a trava de repetição de valor em caso de empate no gale de sinal
					perdas=0.0 #Reinicia a variável de acúmulo de perdas do gale de sinal
					try:
						print(f'\n{id} | {par} -> win | R${str(round(lucro, 2))}\nResultado parcial: R${str(round(lucroTotal, 2))}\n')
						Mensagem(f'{id} | {par} -> win | R${str(round(lucro, 2))}\nResultado parcial: R${str(round(lucroTotal, 2))}')
					except:
						pass
					if soros == 'S':
							if quantidadesoros< niveis_soros:
								if estavanogale == True:
									valor_entrada = float(config['entrada'])
									print( f'\n\n{Fore.LIGHTYELLOW_EX}REAJUSTANDO ENTRADA PARA R${valor_entrada} ESTAVA NO GALE DE VELA\n')
									Mensagem( f'REAJUSTANDO ENTRADA PARA R${valor_entrada} ESTAVA NO GALE DE VELA')
									estavanogale=False
								elif estavanogalesignal == True:
									valor_entrada = float(config['entrada'])
									print( f'\n\n{Fore.LIGHTYELLOW_EX}REAJUSTANDO ENTRADA PARA R${valor_entrada} ESTAVA NO GALE DE SINAL\n')
									Mensagem( f'REAJUSTANDO ENTRADA PARA R${valor_entrada} ESTAVA NO GALE DE SINAL')
									estavanogalesignal=False
								else:
									valor_entrada = round(float(config['entrada']) + float(round(lucro,2)),2)
									quantidadesoros+=1
									print(f'\n\n{Fore.LIGHTBLUE_EX}SOROS NIVEL {quantidadesoros} NO PRÓXIMO SINAL |R${valor_entrada}\n')
									Mensagem(f'\n\nSOROS NIVEL{quantidadesoros} NO PRÓXIMO SINAL |R${valor_entrada}\n')

							else:
								print(f'\n\n{Fore.LIGHTBLUE_EX}LOOP DE SOROS NIVEL {quantidadesoros} ATINGIDO REINICIANDO ENTRADAS...\n')
								Mensagem(f'LOOP DE SOROS NIVEL {quantidadesoros} ATNGIDO REINICIANDO...')
								estavanosoro=True
								quantidadesoros=0
								valor_entrada = float(config['entrada'])
					else:
						valor_entrada=float(config['entrada'])
						if estavanogale == True:
							print( f'\n\n{Fore.LIGHTYELLOW_EX}REAJUSTANDO ENTRADA PARA R${valor_entrada} ESTAVA NO GALE DE VELA\n')
							Mensagem( f'REAJUSTANDO ENTRADA PARA R${valor_entrada} ESTAVA NO GALE DE VELA')
							estavanogale=False
						elif estavanogalesignal == True:
							print( f'\n\n{Fore.LIGHTYELLOW_EX}REAJUSTANDO ENTRADA PARA R${valor_entrada} ESTAVA NO GALE DE SIANL\n')
							Mensagem( f'REAJUSTANDO ENTRADA PARA R${valor_entrada} ESTAVA NO GALE DE SINAL')
							estavanogalesignal=False
						else:
							print(f'\n\n{Fore.LIGHTYELLOW_EX}VALOR DE ENTRADA AJUSTADO PARA R${valor_entrada}\n')
							Mensagem(f'VALOR DE ENTRADA AJUSTADO PARA R${valor_entrada}')
				elif lucro == 0.0:
					try:
						print(f'\n{id} | {par} -> doji | R$0\nResultado parcial: R${str(round(lucroTotal, 2))}\n')
						Mensagem(f'{id} | {par} -> doji | R$0\nResultado parcial: R${str(round(lucroTotal, 2))}')
					except:
						pass
					entrou_gale=False #Libera a trava do gale de vela em caso de empate
					if soros == 'S':
						if estavanosoro == True:
							print( f'\n\n{Fore.LIGHTYELLOW_EX}RETORNANDO ENTRADA PARA R${valor_entrada} DEU EMPATE NO SOROS')
							Mensagem( f'RETORNANDO ENTRADA DEU EMPATE NO SOROS')
					else:
						valor_entrada=float(config['entrada'])

					if 	deuempatenogale ==True:
						valor_entrada = float(round(galeantigo,2))
						print( f'\n\n{Fore.LIGHTYELLOW_EX} EMPATE NO GALE REAJUSTADO PARA R${valor_entrada}')
						Mensagem(f'EMPATE NO GALE REAJUSTADO PARA R${valor_entrada}')
				else:
					try:
						print(f'\n{id} | {par} -> loss | R${str(round(lucro, 2))}\nResultado parcial: R${str(round(lucroTotal, 2))}\n')
						Mensagem(f'{id} | {par} -> loss | R${str(round(lucro, 2))}\nResultado parcial: R${str(round(lucroTotal, 2))}')
					except:
						pass
					quantidadesoros=0
					if galeVela == 'S': #Martingale no próximo sinal
						if ns <= int(config['niveis']):
							if galepayout == 'S': #ativa calculo do gale através do payout
								if  ns > 1:
									perdas+=lucro
									valor_entrada = round(float(abs(perdas)) * (100/capturapayout),2)+1.0
									ns+=1
								else:
									perdas+=lucro
									valor_entrada = round((float(config['entrada'])*(100/capturapayout)),2)+1.0
									ns+=1
							else:
								valor_entrada = round((float(valor_entrada) * float(config['valorGale'])), 2) #calculo do gale através de multiplicador
								ns+=1

							galeantigo = valor_entrada #captura valor do ultimo gale de sinal para função de empate
							deuempatenogale=True #trava que repete o valor do gale no laço de empate
							estavanogalesignal=True #trava que repete retorna valor inicial  no laço do soros saindo so gale
							print(f'{Fore.LIGHTRED_EX} \n\nMARTINGALE NO PRÓXIMO SINAL|{str(dir).upper()}|NIVEL {ns-1}|{valor_entrada}\n')
							Mensagem(f'MARTINGALE NO PRÓXIMO SINAL|{str(dir).upper()}|NIVEL {ns-1}|{valor_entrada}')
						else:
							valor_entrada = float(config['entrada']) # retorna uma entrada normal caso atinja os níveis de gale
							perdas=0.0
							ns=1
							print(f'{Fore.LIGHTYELLOW_EX} ATINGIDO NÍVEIS DE GALE DE SINAL\n')
							Mensagem('ATINGIDO NÍVEIS DE GALE DE SINAL')


					elif galeSinal == 'S': #martingale na próxima vela
							if nv <= int(config['niveis']):

								if galepayout == 'S': #ativa calculo do gale através do payout
									if  nv > 1:
										perdas+=lucro
										valorGaleSinal = round((float(abs(perdas)) * (100/capturapayout)),2)+1.0
										nv+=1
									else:
										perdas+=lucro
										valorGaleSinal = round((float(config['entrada'])*(100/capturapayout)),2)+1.0
										nv+=1
								else:
									valorGaleSinal = round((float(valorGaleSinal) * float(config['valorGale'])), 2) #calculo do gale através de multiplicador
									nv+=1

								entrou_gale = True
								galeantigo = valorGaleSinal #captura valor do ultimo gale de sinal para função de empate
								estavanogale=True #trava que repete retorna valor inicial  no laço do soros saindo so gale
								deuempatenogale=True #trava que repete o valor do gale no laço de empate
								status, id = API.buy_digital_spot_v2(par,valorGaleSinal, dir, timeframe) #operação de gale na proxima vela
								threading.Thread(target=entradas, args=(
								status, id, par, dir, timeframe, opcao,valorGaleSinal), daemon=True).start()
								print(f'{Fore.LIGHTRED_EX} \n\nMARTINGALE PRÓXIMA VELA NIVEL {nv-1} NO PAR {par}| VALOR: R${valorGaleSinal}')
								Mensagem(f'MARTINGALE PRÓXIMA VELA NIVEL {nv-1} NO PAR {par}| VALOR: R${valorGaleSinal}')
							else:
								valor_entrada = float(config['entrada'])
								perdas=0.0
								nv=1
								print(f'{Fore.LIGHTYELLOW_EX}ATINGIDO NÍVEIS DE GALE DE VELA\n')
								Mensagem('ATINGIDO NÍVEIS DE GALE DE VELA')
				if not entrou_gale:
					Total_Operacoes(lucro)
					if config['usar_ciclos'] == 'S':
						Calcula_Valor_Ciclo(lucro)
			time.sleep(0.5)
	
		elif opcao == 'binaria':	
			if status:
				while True:
					resultado,taxa = API.check_win_v4(id)
					if resultado:
						break
					capturaid_binaria = id
				if taxa != None:
					lucro = taxa
					time.sleep(0.5)
					with open('swapresultadolista.txt','r') as arquivo:
						lucroTotal= arquivo.readline()
						lucroTotal=round(float(lucroTotal),2)
					arquivo.close()
					lucroTotal += lucro
					lucroTotal=round(lucroTotal,2)
					with open('swapresultadolista.txt','w') as arquivo:
						arquivo.write(str(lucroTotal))
					arquivo.close()
					lucroTotal = float(lucroTotal)
					galeRepete = False
					entrou_gale = False
					if resultado=='win':
						n = 1
						ns =1
						perdeunosoros=False
						deuempatenogale=False #Reinicia a trava de repetição de valor em caso de empate no gale de sinal
						perdas=0.0 #Reinicia a variável de acúmulo de perdas do gale de sinal
						try:
							print(f'\n\n{id} | {par} -> win | R${str(round(lucro, 2))}\nResultado parcial: R${str(round(lucroTotal, 2))}\n')
							Mensagem(f'{id} | {par} -> win | R${str(round(lucro, 2))}\nResultado parcial: R${str(round(lucroTotal, 2))}')
						except:
							pass
						if soros == 'S':
							if quantidadesoros< niveis_soros:
								if estavanogale == True:
									valor_entrada = float(config['entrada'])
									print( f'\n\n{Fore.LIGHTYELLOW_EX}REAJUSTANDO ENTRADA PARA R${valor_entrada} ESTAVA NO GALE DE VELA\n')
									Mensagem( f'REAJUSTANDO ENTRADA PARA R${valor_entrada} ESTAVA NO GALE DE VELA')
									estavanogale=False
								elif estavanogalesignal == True:
									valor_entrada = float(config['entrada'])
									print( f'\n\n{Fore.LIGHTYELLOW_EX}REAJUSTANDO ENTRADA PARA R${valor_entrada} ESTAVA NO GALE DE SINAL\n')
									Mensagem( f'REAJUSTANDO ENTRADA PARA R${valor_entrada} ESTAVA NO GALE DE SINAL')
									estavanogalesignal=False
								else:
									valor_entrada = round(float(config['entrada']) + float(round(lucro,2)),2)
									quantidadesoros+=1
									print(f'{Fore.LIGHTBLUE_EX}\n\nSOROS NIVEL {quantidadesoros} NO PRÓXIMO SINAL |R${valor_entrada}\n')
									Mensagem(f'\n\nSOROS NIVEL{quantidadesoros} NO PRÓXIMO SINAL |R${valor_entrada}\n')


							else:
								print(f'\n\n{Fore.LIGHTBLUE_EX}LOOP DE SOROS NIVEL {quantidadesoros} ATINGIDO REINICIANDO ENTRADAS...\n')
								Mensagem(f'LOOP DE SOROS NIVEL {quantidadesoros} ATNGIDO REINICIANDO...')
								estavanosoro=True
								quantidadesoros=0
								valor_entrada = float(config['entrada'])
						else:
							valor_entrada=float(config['entrada'])
							if estavanogale == True:
								print( f'\n\n{Fore.LIGHTYELLOW_EX}REAJUSTANDO ENTRADA PARA R${valor_entrada} ESTAVA NO GALE DE VELA\n')
								Mensagem( f'REAJUSTANDO ENTRADA PARA R${valor_entrada} ESTAVA NO GALE DE VELA')
								estavanogale=False
							elif estavanogalesignal == True:
								print( f'\n\n{Fore.LIGHTYELLOW_EX}REAJUSTANDO ENTRADA PARA R${valor_entrada} ESTAVA NO GALE DE SIANL\n')
								Mensagem( f'REAJUSTANDO ENTRADA PARA R${valor_entrada} ESTAVA NO GALE DE SINAL')
								estavanogalesignal=False
							else:
								print(f'\n\n{Fore.LIGHTYELLOW_EX}VALOR DE ENTRADA AJUSTADO PARA R${valor_entrada}\n')
								Mensagem(f'VALOR DE ENTRADA AJUSTADO PARA R${valor_entrada}')



					elif resultado == 'equal':
						try:
							print(f'\n\n{id} | {par} -> doji | R$0\nResultado parcial: R${str(round(lucroTotal, 2))}\n')
							Mensagem(f'{id} | {par} -> doji | R$0\nResultado parcial: R${str(round(lucroTotal, 2))}')
						except:
							pass
						entrou_gale=False #Libera a trava do gale de vela em caso de empate
						if soros == 'S':
							if estavanosoro == True:
								print( f'\n\n{Fore.LIGHTYELLOW_EX}RETORNANDO ENTRADA PARA R${valor_entrada} DEU EMPATE NO SOROS')
								Mensagem( f'RETORNANDO ENTRADA DEU EMPATE NO SOROS')
						else:
							valor_entrada=float(config['entrada'])

						if 	deuempatenogale ==True:
							valor_entrada = float(round(galeantigo,2))
							print( f'\n\n{Fore.LIGHTYELLOW_EX} EMPATE NO GALE REAJUSTADO PARA R${valor_entrada}')
							Mensagem(f'EMPATE NO GALE REAJUSTADO PARA R${valor_entrada}')
					elif resultado == 'loose':
						try:
							print(f'\n\n{id} | {par} -> loss | R${str(round(lucro, 2))}\nResultado parcial: R${str(round(lucroTotal, 2))}\n')
							Mensagem(f'{id} | {par} -> loss | R${str(round(lucro, 2))}\nResultado parcial: R${str(round(lucroTotal, 2))}')
						except:
							pass
						quantidadesoros=0
						if galeVela == 'S': #Martingale no próximo sinal
							if ns <= int(config['niveis']):
								if galepayout == 'S': #ativa calculo do gale através do payout
									if  ns > 1:
										perdas+=lucro
										valor_entrada = round((float(abs(perdas)) * (100/capturapayout)),2)+1.0
										ns+=1
									else:
										perdas+=lucro
										valor_entrada = round((float(config['entrada'])*(100/capturapayout)),2)+1.0
										ns+=1
								else:
									valor_entrada = round((float(valor_entrada) * float(config['valorGale'])), 2) #calculo do gale através de multiplicador
									ns+=1

								galeantigo = valor_entrada #captura valor do ultimo gale de sinal para função de empate
								deuempatenogale=True #trava que repete o valor do gale no laço de empate
								estavanogalesignal=True #trava que repete retorna valor inicial  no laço do soros saindo so gale
								print(f'{Fore.LIGHTRED_EX} \n\nMARTINGALE NO PRÓXIMO SINAL|{str(dir).upper()}|NIVEL {ns-1}|{valor_entrada}\n')
								Mensagem(f'MARTINGALE NO PRÓXIMO SINAL|{str(dir).upper()}|NIVEL {ns-1}|{valor_entrada}')
							else:
								valor_entrada = float(config['entrada']) # retorna uma entrada normal caso atinja os níveis de gale
								perdas=0.0
								ns=1
								print(f'{Fore.LIGHTYELLOW_EX} ATINGIDO NÍVEIS DE GALE DE SINAL\n')
								Mensagem('ATINGIDO NÍVEIS DE GALE DE SINAL')


						elif galeSinal == 'S': #martingale na próxima vela
								if nv <= int(config['niveis']):

									if galepayout == 'S': #ativa calculo do gale através do payout
										if  nv > 1:
											perdas+=lucro
											valorGaleSinal = round((float(abs(perdas)) * (100/capturapayout)),2)+1.0
											nv+=1
										else:
											perdas+=lucro
											valorGaleSinal = round((float(config['entrada'])*(100/capturapayout)),2)+1.0
											nv+=1
									else:
										valorGaleSinal = round((float(valorGaleSinal) * float(config['valorGale'])), 2) #calculo do gale através de multiplicador
										nv+=1

									entrou_gale = True
									galeantigo = valorGaleSinal #captura valor do ultimo gale de sinal para função de empate
									estavanogale=True #trava que repete retorna valor inicial  no laço do soros saindo so gale
									deuempatenogale=True #trava que repete o valor do gale no laço de empate
									status, id = API.buy(valorGaleSinal, par, dir, timeframe) #operação de gale na proxima vela
									threading.Thread(target=entradas, args=(
									status, id, par, dir, timeframe, opcao,valorGaleSinal), daemon=True).start()
									
									print(f'{Fore.LIGHTRED_EX} \n\nMARTINGALE PRÓXIMA VELA NIVEL {nv-1} NO PAR {par}| VALOR: R${valorGaleSinal}')
									Mensagem(f'MARTINGALE PRÓXIMA VELA NIVEL {nv-1} NO PAR {par}| VALOR: R${valorGaleSinal}')
								else:
									valor_entrada = float(config['entrada'])
									perdas=0.0
									nv=1
									print(f'{Fore.LIGHTYELLOW_EX}ATINGIDO NÍVEIS DE GALE DE VELA\n')
									Mensagem('ATINGIDO NÍVEIS DE GALE DE VELA')
					if not entrou_gale:
						Total_Operacoes(lucro)
						if config['usar_ciclos'] == 'S':
							Calcula_Valor_Ciclo(lucro)

		else:
			print(f'{Fore.RED}\n\nERRO AO REALIZAR OPERAÇÃO!!\n')
	except:
		pass


def Verificar_Tendencia(par, timeframe):
	velas = API.get_candles(par, (timeframe * 60), periodo, time.time())
	fechamento = round(velas[-1]['close'], 4)
	df = pd.DataFrame(velas)
	EMA = df['close'].ewm(span=periodo, adjust=False).mean()
	for data in EMA:
		EMA10 = data

	if EMA10 > fechamento:
		dir = 'put'
	elif fechamento > EMA10:
		dir = 'call'
	else:
		dir = False

	return dir


def Filtro_Hit_Vela(par, timeframe):
	velas = API.get_candles(par, (60 * timeframe), 5, time.time())
	velas[0] = 'r' if velas[0]['open'] > velas[0]['close'] else 'g'
	velas[1] = 'r' if velas[1]['open'] > velas[1]['close'] else 'g'
	velas[2] = 'r' if velas[2]['open'] > velas[2]['close'] else 'g'
	velas[3] = 'r' if velas[3]['open'] > velas[3]['close'] else 'g'
	hit = velas[0] + velas[1] + velas[2] + velas[3]
	if hit == 'rrrr' or hit == 'gggg':
		return True
	else:
		return False


def operar(valor_entrada, par, direcao, timeframe, horario, opcao, payout):
	global capturaopcao, estavanogale,estavanosoro, estavanogalesignal
	status = False

	try:
		if opcao == 'digital':
			status, id = API.buy_digital_spot_v2(par, valor_entrada, direcao, timeframe)
			threading.Thread(target=entradas, args=(status, id, par, direcao, timeframe, opcao,valor_entrada), daemon=True).start()

		elif opcao == 'binaria':
			status, id = API.buy(valor_entrada, par, direcao, timeframe)
			threading.Thread(target=entradas, args=(status, id, par, direcao, timeframe, opcao,valor_entrada), daemon=True).start()

		else:
			print(Fore.LIGHTRED_EX+' ERRO AO REALIZAR ENTRADA!!')
			Mensagem('ERRO AO REALIZAR ENTRADA!!')
			time.sleep(1)
	except:
		print(Fore.LIGHTRED_EX+' ERRO AO REALIZAR ENTRADA!!')
		Mensagem('ERRO AO REALIZAR ENTRADA!!')
		time.sleep(1)

	if status:
		print(f'\n\nINICIANDO OPERAÇÃO {str(id)}..\n {str(horario)} | {par} | OPÇÃO: {opcao.upper()} | DIREÇÃO: {direcao.upper()} | M{timeframe} | PAYOUT: {payout}% | VALOR: R${valor_entrada}\n\n')
		Mensagem(f'INICIANDO OPERAÇÃO {str(id)}..\n {str(horario)} | {par} | OPÇÃO: {opcao.upper()} | DIREÇÃO: {direcao.upper()} | M{timeframe} | PAYOUT: {payout}% | VALOR: R${valor_entrada}' )


while True:
	if API.check_connect() == False:
		print('>> Erro ao se conectar!\n')
		input('   Aperte enter para sair')
		sys.exit()
	else:
		print(f'\n{Fore.LIGHTBLUE_EX}   >>>CONECTADO COM SUCESSO!<<<\n')
		Mensagem(f'   >>>CONECTADO COM SUCESSO!<<<\n')
		banca()
		config['banca_inicial'] = valor_da_banca
		Mensagem(mensagmperfil) #envia mensagem sobre os dados inicias da conta do usuário
		Mensagem(mensagemconfig)
		break

def main():
	global loop,stop_win,stop_loss,capturapayout,get_profit,par,direcao,timeframe,valor_entrada,percentual_gain,percentual_loss,quantidadesoros,niveis_soros,payout,delay_entrada,analisarTendencia,hitdeVela,payout_minimo,entrou_gale,total_operacoes,total_porcentagem,vitorias,derrotas,account_type,account_balance,opcao,paridades_fechadas
	try:
		buscarMenor()

		while True:
			timeNow = timestamp_converter()
			data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
			print(data_hora, end='\x1b[K\r')


			for row in em_espera:
				horario = row[2]
				if galeRepete:
					par = parAntigo
					direcao = direcaoAntigo
					timeframe = timeframeAntigo
					valor_entrada = valorGaleProxSinal
				else:
					par = row[1].upper()
					direcao = row[3].lower()
					timeframe_retorno = timeFrame(row[0])
					timeframe = 0 if (timeframe_retorno == 'error') else timeframe_retorno
					if config['usar_ciclos'] == 'S':
						valor_entrada = valor_entrada_ciclo
						stop_win = abs(float(config['stop_win']))
						stop_loss = float(config['stop_loss']) * -1.0
					elif entrada_percentual == 'S':
						valor_entrada = int((float(config['entrada']) / 100) * (valor_da_banca + lucroTotal))
						percentual_loss = float(config['stop_loss'])
						percentual_gain = float(config['stop_win'])
						stop_loss = int((percentual_loss / 100) * valor_da_banca) * -1
						stop_win = int((percentual_gain / 100) * valor_da_banca)
					else:

						stop_win = abs(float(config['stop_win']))
						stop_loss = float(config['stop_loss']) * -1.0

						if loop == 0:
							valor_entrada = float(config['entrada'])
							loop+=1


						# Termina a operação caso atinja o número de Soros
						if quantidadesoros>niveis_soros and travasoros == 'S':
							print(f'{Fore.LIGHTBLUE_EX}\nFINALIZANDO OPERAÇÕES NIVEL {niveis_soros} DE SOROS ATINGIDO')
							banca()
							mensagem = f'Operações: {total_operacoes} | Vencedoras: {vitorias} | Perdedoras: {derrotas}\nAssertividade: {total_porcentagem}%\n'
							mensagem += f"Resultado total: {round(lucroTotal,2)}\n"
							mensagem += f"Saldo da conta {'demo' if account_type == 'PRACTICE' else 'real'}: {account_balance}"
							print(f'{Fore.GREEN}{mensagem}')
							Mensagem(f'FINALIZANDO OPERAÇÕES NIVEL {niveis_soros} DE SOROS ATINGIDO')
							Mensagem(mensagem)
							sys.exit()

				if len(horario) == 5:
					s = horario + ":00"
				else:
					s = horario
				f = '%H:%M:%S'
				dif = (datetime.strptime(timeNow, f) - datetime.strptime(s, f)).total_seconds()

				if (dif ==-40) and get_profit == True:
					get_profit = False
					paridades_fechadas = []

				if dif==-20:

					if tipoOpcao == 'BINARIA':
						opcao='binaria'
						all_asset_ = API.get_all_open_time()
						profit_ = API.get_all_profit()
						if all_asset_['turbo'][par]['open']:
							payout = int(profit_[par]["turbo"] * 100)
							capturapayout=payout
							print(f'{Fore.LIGHTYELLOW_EX}TIPO DE OPÇÃO: {str(opcao).upper()}| PAYOUT {payout}%\n')
							Mensagem(f'TIPO DE OPÇÃO: {str(opcao).upper()}| PAYOUT {payout}%')

					if tipoOpcao == 'DIGITAL':
						opcao='digital'
						try:
							payout = int(API.get_digital_payout(par))
							capturapayout=payout
						except:
							pass
						print(f'{Fore.LIGHTYELLOW_EX}TIPO DE OPÇÃO: {str(opcao).upper()}|PAYOUT {payout}%\n')
						Mensagem(f'TIPO DE OPÇÃO: {str(opcao).upper()}| PAYOUT {payout}%')


					if tipoOpcao == 'AUTO':
						opcao, payout = checkProfit(par, timeframe,parescapturados)
						capturapayout=payout
						print(f'{Fore.LIGHTYELLOW_EX}TIPO DE OPÇÃO AUTO: {str(opcao).upper()}| PAYOUT {payout}%\n')
						Mensagem( f'TIPO DE OPÇÃO AUTO: {str(opcao).upper()}| PAYOUT {payout}%')

					if payout == None or payout== '':
						payout=0
						print (f'{Fore.LIGHTRED_EX} ERRO AO CAPTURAR PAYOUT NO {par}\n')


					if not opcao:
						paridades_fechadas.append(par)


				if dif == delay_entrada:
					impacto, moeda, hora, stts = noticas(par)
					if stts:
						print(f' {Fore.LIGHTRED_EX}NOTÍCIA COM IMPACTO DE {impacto} TOUROS NA MOEDA {moeda} ÀS {hora}!\n')
						Mensagem(f' NOTÍCIA COM IMPACTO DE {impacto} TOUROS NA MOEDA {moeda} ÀS {hora}!\n')
						time.sleep(1)
					else:
						if timerzone(int(timeframe)):
							print(f' {Fore.LIGHTRED_EX}HORÁRIO NÃO RECOMENDADO PELO TIMERZONE!')
							Mensagem(' HORÁRIO NÃO RECOMENDADO PELO TIMERZONE!')
							time.sleep(1)
						else:
							if analisarTendencia == 'S':
								tend = Verificar_Tendencia(par, timeframe)
							else:
								tend = direcao

							if hitdeVela == 'S':
								hit = Filtro_Hit_Vela(par, timeframe)
							else:
								hit = False

							if tend != direcao:
								print(f' {Fore.LIGHTRED_EX}SINAL NA PARIDADE {par} CONTRA TENDÊNCIA!\n')
								Mensagem(f'SINAL NA PARIDADE {par} CONTRA TENDÊNCIA!\n')
								time.sleep(1)

							else:
								if hit:
									print(f' {Fore.LIGHTRED_EX}HIT DE VELA NA PARIDADE {par}!\n')
									Mensagem(f' HIT DE VELA NA PARIDADE {par}!\n')
									time.sleep(1)

								elif par not in paridades_fechadas:
									if payout >= payout_minimo:
										thread_ativas = threading.active_count()
										if config['usar_ciclos'] == 'S' and thread_ativas > 2:
											print(f' {Fore.LIGHTRED_EX}OPERAÇÃO EM ANDAMENTO. ABORTANDO ENTRADA!')
											Mensagem(' OPERAÇÃO EM ANDAMENTO. ABORTANDO ENTRADA!')
											time.sleep(5)
											break
										else:
											if entrou_gale ==False: # bloqueia entrada de demais sinais caso o martingale seja ativado
												operar(valor_entrada, par, direcao, timeframe, horario, opcao, payout)

										if config['usar_ciclos'] == 'S':
											break
								else:
									if par in paridades_fechadas:
										print(f' {Fore.LIGHTRED_EX}PARIDADE {par} FECHADA!\n')
										Mensagem(f' PARIDADE {par} FECHADA!\n')
									else:
										print(f' {Fore.LIGHTRED_EX}PAYOUT ABAIXO DO MINIMO ESTABELECIDO!\n')
										Mensagem(' PAYOUT ABAIXO DO MINIMO ESTABELECIDO!\n')
										time.sleep(0.5)

				if dif > 0:
					buscarMenor()
					break
			verificarStop()
			if verificastop:
				break
			time.sleep(0.5)
	except KeyboardInterrupt:
		banca()
		mensagem = f'Operações: {total_operacoes} | Vencedoras: {vitorias} | Perdedoras: {derrotas}\nAssertividade: {total_porcentagem}%\n'
		mensagem += f"Resultado total: {round(lucroTotal,2)}\n"
		mensagem += f"Saldo da conta {'demo' if account_type == 'PRACTICE' else 'real'}: {account_balance}"
		print(f'{Fore.GREEN}{mensagem}')
		Mensagem(mensagem)
		exit()

### Inicialização em Threading #####
threading.Thread(target=main,args=(),daemon=True).start()
timer = int(time.time())
while True :
    if (int(time.time())-timer)==60:
        parescapturados=capturar_pares2()
        timer = int(time.time())



