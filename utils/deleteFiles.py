import os

from logs.logs import Logs


def deleteFiles(directoryPath):
    try:
        files = os.listdir(directoryPath)
        if len(files) > 0:
            for file in files:
                file_path = os.path.join(directoryPath, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            Logs.log_sucess("Todos os arquivos foram deletados com sucesso")
    except OSError as e:
        Logs.log_fail("Erro ao deletar arquivos, verifique a pasta de destino")
        raise Exception('localStorage', 'Erro ao deletar arquivos, verifique a pasta de destino', e)