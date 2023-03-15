import configparser
from zapv2 import ZAPv2

# Configuración del archivo de configuración
config = configparser.ConfigParser()
config.read('config.ini')

# Cargar la sesión de ZAP
zap = ZAPv2(apikey='myapikey')
session_name = config.get('zap', 'session_name')
if session_name not in zap.sessions:
    zap.core.new_session(name=session_name)
zap.core.load_session(name=session_name)

# Leer las credenciales de autenticación desde el archivo de configuración
auth_method = config.get('authentication', 'method')
username = config.get('authentication', 'username')
password = config.get('authentication', 'password')

# Configurar el contexto de autenticación
context_name = config.get('context', 'name')
context_id = zap.context.new_context(context_name)
zap.context.set_context(context_id)
zap.authentication.set_authentication_method(contextid=context_id, authmethodname=auth_method)
zap.authentication.set_authentication_credentials(contextid=context_id, authcredentialsconfigparams=[{'name': 'username', 'value': username}, {'name': 'password', 'value': password}])

# Iniciar el escaneo
target_url = config.get('target', 'url')
zap.urlopen(target_url)
zap.spider.scan(target_url)
zap.ascan.scan(target_url)

# Esperar a que finalice el escaneo y guardar los resultados
while int(zap.ascan.status()) < 100:
    print('Escaneando...')
    time.sleep(5)
zap.core.save_session(session_name)
