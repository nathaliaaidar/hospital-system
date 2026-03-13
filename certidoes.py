import pandas as pd
import webbrowser
import os

# --- Bloco de código para encontrar a planilha ---
# 1. Descobre o caminho absoluto para a pasta onde este script está salvo.
#    Isso funciona não importa de onde você execute (VSCode, terminal, etc).
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Junta o caminho da pasta com o nome do arquivo da planilha.
file_path = os.path.join(script_dir, "CertidoesRTCON.xlsx")


# --- Validação e Execução Principal ---
if not os.path.exists(file_path):
    print(f"ERRO: A planilha 'CertidoesRTCON.xlsx' não foi encontrada.")
    print(f"O programa procurou por ela em: {file_path}")
    print("Certifique-se de que a planilha está na mesma pasta que o script 'certidoes.py'.")
    input("\nPressione Enter para fechar.")
else:
    try:
        df = pd.read_excel(file_path)

        # --- Função para abrir o link ---
        def open_link(choice):
            try:
                index = int(choice) - 1
                if 0 <= index < len(df):
                    url = df.loc[index, 'LINK ACESSO']
                    certidao_nome = df.loc[index, 'CERTIDÕES']
                    print(f"\nAbrindo: {certidao_nome}...")
                    print(f"URL: {url}")
                    webbrowser.open(url)
                else:
                    print("Opção inválida. Por favor, escolha um número da lista.")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")
            except KeyError as e:
                print(f"Erro: A coluna {e} não foi encontrada na planilha.")
                print("Verifique se os nomes das colunas no arquivo Excel estão corretos.")

        # --- Loop Principal do Programa ---
        while True:
            print("\n--- Escolha a certidão para abrir o link ---")
            for i, certidao in enumerate(df['CERTIDÕES']):
                print(f"{i+1}: {certidao}")

            user_choice = input("\nDigite o número da certidão (ou 'sair' para fechar): ")

            if user_choice.lower() == 'sair':
                break
            
            open_link(user_choice)

    except Exception as e:
        print("Ocorreu um erro inesperado ao processar a planilha.")
        print(f"Detalhes: {e}")
        input("\nPressione Enter para fechar.")