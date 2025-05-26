import pandas as pd
import json
import graphviz

def gerar_relatorio_prisma(df, caminho_base="relatorio_prisma"):
    resumo = {
        "identificados": int(df.attrs.get("identificados", len(df))),
        "avaliados_por_palavras_chave": int(len(df)),
        "com_todos_os_termos": int(df["temas_correlatos"].eq("TEM").sum()),
        "excluidos": int(df["temas_correlatos"].eq("NÃO TEM").sum())
    }

    # Salvar JSON
    with open(f"{caminho_base}.json", "w", encoding="utf-8") as fjson:
        json.dump(resumo, fjson, indent=4, ensure_ascii=False)

    # Salvar CSV
    pd.DataFrame([resumo]).to_csv(f"{caminho_base}.csv", index=False)

    print(f"✅ Relatórios PRISMA exportados como {caminho_base}.json e .csv")
    return resumo

def gerar_fluxograma_prisma(resumo, nome_arquivo="fluxograma_prisma"):
    dot = graphviz.Digraph(format="png")
    dot.attr(rankdir='TB')

    dot.node("A", f"Identificados: {resumo['identificados']}")
    dot.node("B", f"Avaliados por palavras-chave: {resumo['avaliados_por_palavras_chave']}")
    dot.node("C", f"Com todos os termos: {resumo['com_todos_os_termos']}")
    dot.node("D", f"Excluídos: {resumo['excluidos']}")
    dot.node("E", "Incluídos na análise final")

    dot.edges([("A", "B"), ("B", "C"), ("B", "D"), ("C", "E")])

    output_path = dot.render(filename=nome_arquivo, cleanup=True)
    print(f"✅ Fluxograma PRISMA salvo como {output_path}")
    return output_path
