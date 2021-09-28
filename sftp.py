import paramiko
import pymssql
import pandas as pd
import time


def consultaAzure(query):
	conn = pymssql.connect(server='127.0.0.1', user='user', password='pass', database='banco')
	dados = pd.read_sql(query, conn)
	conn.close()
	return dados


data = consultaAzure('select max(id_data) dt from TB_FAT_VENDAS_AGR where ID_OPERACAO_VENDA = 16')
datas = consultaAzure(f'select ID_DATA from tb_dim_data where id_data > {data.dt[0]} and ID_DATA < convert(varchar,GETDATE(),112)')
listaDatas = datas['ID_DATA'].values.tolist()

host 	= 'sftp.dominio.com.br'
user 	= 'user'
pwd 	= 'pass'
port 	= 22
caminhoFtp = '/home/pasta/'
caminhoLocal = '\\\\127.0.0.1\\pasta\\pasta2\\'


def dowFtp(remoto, local):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(host, port, user, pwd)
	sftp = ssh.open_sftp()
	try:
		sftp.get(remoto, local)
	except:
		pass	
	ssh.close()


arquivos = ['arquivo_', 'arquivo2_']
tempIni = time.time()
for name in arquivos:
	for dt in listaDatas:
		print(f'Extraindo arquivo ' + name + str(dt) + '.txt')
		dowFtp(caminhoFtp + name + str(dt) + '.txt', caminhoLocal + name + str(dt) + '.txt')
		print('--------------------------------')

tempTotal = time.strftime("%H:%M:%S", time.gmtime(time.time() - tempIni))
print(f'Finalizado em: ' + str(tempTotal))

