import os

def generate_env_file(source_filename='env.example', target_filename='.env'):
    """
    Gera um arquivo .env a partir de um arquivo .env.example,
    caso o arquivo .env ainda não exista.
    """
    if os.path.exists(target_filename):
        print(f'O arquivo "{target_filename}" já existe.')
    else:
        # Copia o conteúdo de .env.example para .env
        try:
            with open(source_filename, 'r') as source_file:
                content = source_file.read()
                with open(target_filename, 'w') as target_file:
                    target_file.write(content)
            print(f'Arquivo "{target_filename}" gerado com sucesso a partir de "{source_filename}".')
        except FileNotFoundError:
            print(f'Erro: O arquivo fonte "{source_filename}" não foi encontrado.')

if __name__ == '__main__':
    print(os.path)
    # Executa a função de geração do arquivo .env
    generate_env_file()