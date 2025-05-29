from flask import Flask, render_template, request, send_file
import os
import pandas as pd
from werkzeug.utils import secure_filename
from verificador import verificar_link
from prisma import gerar_relatorio_prisma, gerar_fluxograma_prisma
from busca import buscar_em_fontes

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        termos_raw = request.form['termos']
        termos = [t.strip() for t in termos_raw.split(',') if t.strip()]
        origem_dados = request.form.get('origem')
        df = pd.DataFrame()

        if origem_dados == 'arquivo':
            if 'arquivo' not in request.files:
                return "Arquivo não enviado"
            file = request.files['arquivo']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)
                df = pd.read_excel(path)

        elif origem_dados == 'busca':
            df = buscar_em_fontes(termos)
            if not df.empty:
                path = os.path.join(app.config['UPLOAD_FOLDER'], 'resultado_busca.xlsx')
                df.to_excel(path, index=False)

        else:
            return "Erro: Origem dos dados não reconhecida."

        if df.empty or 'link' not in df.columns:
            return "Nenhum link encontrado nas fontes ou o arquivo não contém coluna 'link'."

        df = df.dropna(subset=['link']).reset_index(drop=True)

        resultados_origem, resultados_encontrados, temas_correlatos, tempos = [], [], [], []

        for link in df['link']:
            origem, encontrados, duracao = verificar_link(link, termos)
            resultados_origem.append(origem)
            resultados_encontrados.append(", ".join(encontrados))
            temas_correlatos.append("TEM" if len(encontrados) == len(termos) else "NÃO TEM")
            tempos.append(round(duracao, 2))

        df['origem_conteudo'] = resultados_origem
        df['temas_correlatos'] = temas_correlatos
        df['termos_encontrados'] = resultados_encontrados
        df['tempo_execucao_s'] = tempos

        output_excel = os.path.join(UPLOAD_FOLDER, 'resultado_formatado.xlsx')
        df.to_excel(output_excel, index=False)

        # Gerar e salvar relatórios PRISMA corretamente
        resumo = gerar_relatorio_prisma(df)

        json_path = os.path.join(UPLOAD_FOLDER, 'relatorio_prisma.json')
        csv_path = os.path.join(UPLOAD_FOLDER, 'relatorio_prisma.csv')
        fluxograma_path = os.path.join(UPLOAD_FOLDER, 'fluxograma_prisma.png')

        with open(json_path, 'w', encoding='utf-8') as f_json:
            import json
            json.dump(resumo, f_json, indent=4, ensure_ascii=False)

        pd.DataFrame([resumo]).to_csv(csv_path, index=False)

        gerar_fluxograma_prisma(resumo, fluxograma_path)

        return render_template('index.html', pronto=True, arquivos=[
            ('Resultado Formatado', output_excel),
            ('Relatório JSON', json_path),
            ('Relatório CSV', csv_path),
            ('Fluxograma PRISMA', fluxograma_path)
        ])

    return render_template('index.html', pronto=False)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

def iniciar_flask():
    import webbrowser
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=False)
