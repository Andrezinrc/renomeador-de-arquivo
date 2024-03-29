from flask import Flask, render_template, request, redirect, url_for
import os
import logging

app = Flask(__name__)

logging.basicConfig(filename='renomeador.log', level=logging.INFO)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/renomear', methods=['POST'])
def renomear():
    try:
        diretorio = request.form.get('diretorio')
        escolha_tipo = request.form.get('escolha_tipo')
        padrao_nome = request.form.get('padrao_nome')

        os.chdir(diretorio)

        logging.info(f'Diretório: {os.getcwd()}')

        renomeacoes = []

        for contador, arq in enumerate(os.listdir()):
            if os.path.isfile(arq):
                _, extensao = os.path.splitext(arq)
                extensao = extensao.lower().strip()

                if escolha_tipo.lower().strip() == 'todos' or extensao in escolha_tipo.split(','):
                    nome_arq, exten_arq = os.path.splitext(arq)
                    nome_arq = padrao_nome + ' ' + str(contador + 1)
                    nome_novo = f'{nome_arq}{exten_arq}'

                    renomeacoes.append((arq, nome_novo))
                    os.rename(arq, nome_novo)

        logging.info(f'Renomeações realizadas em {diretorio}: {renomeacoes}')

        return render_template('index.html', renomeacoes=renomeacoes, success_message='Arquivos renomeados com sucesso.')

    except Exception as e:
        error_message = f'Diretório: {diretorio} não encontrado.'
        print(e)
        print(error_message)
        logging.error(error_message)
        return render_template('index.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
