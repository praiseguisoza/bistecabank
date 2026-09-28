import os
import customtkinter as ctk

# Garante que o arquivo banco.txt fique sempre na mesma pasta deste script
DIRETORIO_SCRIPT = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_BANCO = os.path.join(DIRETORIO_SCRIPT, "banco.txt")

# --- FUNÇÕES PARA O ARQUIVO TXT ---
def carregar_dados():
    dados = {}
    if not os.path.exists(ARQUIVO_BANCO):
        dados_iniciais = [
            "101;Bisteca Silva;15420.50\n",
            "102;Ana Souza;3250.00\n",
            "103;Carlos Eduardo;890.75\n"
        ]
        with open(ARQUIVO_BANCO, "w", encoding="utf-8") as f:
            f.writelines(dados_iniciais)
            
    with open(ARQUIVO_BANCO, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if linha:
                partes = linha.split(";")
                if len(partes) == 3:
                    codigo, nome, saldo = partes
                    dados[codigo] = {"nome": nome, "saldo": float(saldo)}
    return dados

def salvar_todos_no_txt():
    """Reescreve o arquivo banco.txt com todos os dados e saldos atualizados."""
    with open(ARQUIVO_BANCO, "w", encoding="utf-8") as f:
        for codigo, info in banco_dados.items():
            f.write(f"{codigo};{info['nome']};{info['saldo']:.2f}\n")

banco_dados = carregar_dados()

# --- CONFIGURAÇÃO VISUAL (COMPATÍVEL COM QUALQUER VERSÃO) ---
try:
    if hasattr(ctk, "set_appearance_mode"):
        ctk.set_appearance_mode("light")
    elif hasattr(ctk, "AppearanceModeTracker"):
        ctk.AppearanceModeTracker.set_appearance_mode("light")
except Exception:
    pass

try:
    if hasattr(ctk, "set_default_color_theme"):
        ctk.set_default_color_theme("blue")
except Exception:
    pass

janela = ctk.CTk()
janela.title("Bisteca Bank")
janela.geometry("460x600")
janela.resizable(False, False)

# Abas de navegação
abas = ctk.CTkTabview(
    janela,
    width=420,
    height=560,
    segmented_button_selected_color="#0F2B5C",
    segmented_button_fg_color="#E2E8F0"
)
abas.pack(padx=20, pady=15)

aba_cadastro = abas.add("Cadastrar")
aba_consulta = abas.add("Consultar")
aba_operacoes = abas.add("Operações")

# =========================================================================
# 1. ABA: CADASTRAR USUÁRIO
# =========================================================================
titulo_cad = ctk.CTkLabel(aba_cadastro, text="Novo Cadastro", font=("Segoe UI", 24, "bold"), text_color="#1E293B")
titulo_cad.pack(pady=(12, 15))

lbl_codigo = ctk.CTkLabel(aba_cadastro, text="Código do Usuário", font=("Segoe UI", 11), text_color="#64748B")
lbl_codigo.pack(anchor="w", padx=50, pady=(4, 0))
campo_cad_codigo = ctk.CTkEntry(aba_cadastro, placeholder_text="Ex: 104", width=310, height=36, border_color="#CBD5E1")
campo_cad_codigo.pack(pady=(2, 8))

lbl_nome = ctk.CTkLabel(aba_cadastro, text="Nome Completo", font=("Segoe UI", 11), text_color="#64748B")
lbl_nome.pack(anchor="w", padx=50, pady=(4, 0))
campo_cad_nome = ctk.CTkEntry(aba_cadastro, placeholder_text="Ex: Maria Santos", width=310, height=36, border_color="#CBD5E1")
campo_cad_nome.pack(pady=(2, 8))

lbl_saldo = ctk.CTkLabel(aba_cadastro, text="Saldo Inicial (R$)", font=("Segoe UI", 11), text_color="#64748B")
lbl_saldo.pack(anchor="w", padx=50, pady=(4, 0))
campo_cad_saldo = ctk.CTkEntry(aba_cadastro, placeholder_text="Ex: 2500.00", width=310, height=36, border_color="#CBD5E1")
campo_cad_saldo.pack(pady=(2, 10))

resultado_cadastro = ctk.CTkLabel(aba_cadastro, text="", font=("Segoe UI", 12))
resultado_cadastro.pack(pady=4)

def cadastrar_usuario():
    codigo = campo_cad_codigo.get().strip()
    nome = campo_cad_nome.get().strip()
    saldo_str = campo_cad_saldo.get().strip().replace(",", ".")

    if not codigo or not nome or not saldo_str:
        resultado_cadastro.configure(text="Preencha todos os campos!", text_color="#DC2626")
        return

    if codigo in banco_dados:
        resultado_cadastro.configure(text=f"Código '{codigo}' já existe!", text_color="#DC2626")
        return

    try:
        saldo = float(saldo_str)
        if saldo < 0:
            resultado_cadastro.configure(text="Saldo inicial não pode ser negativo.", text_color="#DC2626")
            return
    except ValueError:
        resultado_cadastro.configure(text="Digite um número válido para o saldo.", text_color="#DC2626")
        return

    banco_dados[codigo] = {"nome": nome, "saldo": saldo}
    salvar_todos_no_txt()

    campo_cad_codigo.delete(0, "end")
    campo_cad_nome.delete(0, "end")
    campo_cad_saldo.delete(0, "end")
    resultado_cadastro.configure(text=f"'{nome}' cadastrado com sucesso!", text_color="#16A34A")

btn_cadastrar = ctk.CTkButton(
    aba_cadastro, text="Cadastrar", command=cadastrar_usuario,
    width=310, height=42, font=("Segoe UI", 13, "bold"),
    fg_color="#0F2B5C", hover_color="#091D3E", corner_radius=6
)
btn_cadastrar.pack(pady=10)

# =========================================================================
# 2. ABA: CONSULTAR SALDO
# =========================================================================
titulo_cons = ctk.CTkLabel(aba_consulta, text="Consultar Conta", font=("Segoe UI", 24, "bold"), text_color="#1E293B")
titulo_cons.pack(pady=(25, 15))

lbl_cons_codigo = ctk.CTkLabel(aba_consulta, text="Código do Cliente", font=("Segoe UI", 11), text_color="#64748B")
lbl_cons_codigo.pack(anchor="w", padx=50, pady=(5, 0))

campo_consulta = ctk.CTkEntry(aba_consulta, placeholder_text="Digite o código (ex: 101)", width=310, height=36, border_color="#CBD5E1")
campo_consulta.pack(pady=(2, 10))

resultado_consulta = ctk.CTkLabel(aba_consulta, text="", font=("Segoe UI", 14), justify="center")
resultado_consulta.pack(pady=15)

def buscar_saldo():
    codigo = campo_consulta.get().strip()
    if not codigo:
        resultado_consulta.configure(text="Informe um código.", text_color="#D97706")
        return

    if codigo in banco_dados:
        cliente = banco_dados[codigo]
        saldo_fmt = f"{cliente['saldo']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        resultado_consulta.configure(text=f"Titular: {cliente['nome']}\nSaldo: R$ {saldo_fmt}", text_color="#16A34A")
    else:
        resultado_consulta.configure(text="Cliente não encontrado!", text_color="#DC2626")

btn_consultar = ctk.CTkButton(
    aba_consulta, text="Consultar", command=buscar_saldo,
    width=310, height=42, font=("Segoe UI", 13, "bold"),
    fg_color="#0F2B5C", hover_color="#091D3E", corner_radius=6
)
btn_consultar.pack(pady=10)
campo_consulta.bind("<Return>", lambda event: buscar_saldo())

# =========================================================================
# 3. ABA: OPERAÇÕES BANCÁRIAS (Depósito, Saque, Transferência)
# =========================================================================
titulo_op = ctk.CTkLabel(aba_operacoes, text="Operações", font=("Segoe UI", 24, "bold"), text_color="#1E293B")
titulo_op.pack(pady=(10, 10))

def ao_mudar_operacao(valor):
    if valor == "Transferência":
        lbl_op_destino.pack(anchor="w", padx=50, pady=(4, 0), before=resultado_operacao)
        campo_op_destino.pack(pady=(2, 6), before=resultado_operacao)
    else:
        lbl_op_destino.pack_forget()
        campo_op_destino.pack_forget()

seletor_op = ctk.CTkSegmentedButton(
    aba_operacoes,
    values=["Depósito", "Saque", "Transferência"],
    command=ao_mudar_operacao,
    selected_color="#0F2B5C",
    width=310
)
seletor_op.set("Depósito")
seletor_op.pack(pady=10)

lbl_op_origem = ctk.CTkLabel(aba_operacoes, text="Código da Conta (Origem)", font=("Segoe UI", 11), text_color="#64748B")
lbl_op_origem.pack(anchor="w", padx=50, pady=(4, 0))
campo_op_origem = ctk.CTkEntry(aba_operacoes, placeholder_text="Ex: 101", width=310, height=34, border_color="#CBD5E1")
campo_op_origem.pack(pady=(2, 6))

lbl_op_valor = ctk.CTkLabel(aba_operacoes, text="Valor da Operação (R$)", font=("Segoe UI", 11), text_color="#64748B")
lbl_op_valor.pack(anchor="w", padx=50, pady=(4, 0))
campo_op_valor = ctk.CTkEntry(aba_operacoes, placeholder_text="Ex: 250.00", width=310, height=34, border_color="#CBD5E1")
campo_op_valor.pack(pady=(2, 6))

# Elementos que só aparecem quando selecionado "Transferência"
lbl_op_destino = ctk.CTkLabel(aba_operacoes, text="Código da Conta Destino", font=("Segoe UI", 11), text_color="#64748B")
campo_op_destino = ctk.CTkEntry(aba_operacoes, placeholder_text="Ex: 102", width=310, height=34, border_color="#CBD5E1")

resultado_operacao = ctk.CTkLabel(aba_operacoes, text="", font=("Segoe UI", 12))
resultado_operacao.pack(pady=6)

def realizar_operacao():
    tipo = seletor_op.get()
    origem = campo_op_origem.get().strip()
    valor_str = campo_op_valor.get().strip().replace(",", ".")

    if not origem or not valor_str:
        resultado_operacao.configure(text="Preencha os campos obrigatórios!", text_color="#DC2626")
        return

    if origem not in banco_dados:
        resultado_operacao.configure(text=f"Conta '{origem}' não encontrada!", text_color="#DC2626")
        return

    try:
        valor = float(valor_str)
        if valor <= 0:
            resultado_operacao.configure(text="O valor deve ser maior que zero.", text_color="#DC2626")
            return
    except ValueError:
        resultado_operacao.configure(text="Valor inválido!", text_color="#DC2626")
        return

    if tipo == "Depósito":
        banco_dados[origem]["saldo"] += valor
        salvar_todos_no_txt()
        novo_saldo = banco_dados[origem]["saldo"]
        resultado_operacao.configure(
            text=f"Depósito de R$ {valor:,.2f} realizado!\nNovo saldo: R$ {novo_saldo:,.2f}",
            text_color="#16A34A"
        )

    elif tipo == "Saque":
        if banco_dados[origem]["saldo"] < valor:
            resultado_operacao.configure(text="Saldo insuficiente para saque!", text_color="#DC2626")
            return
        banco_dados[origem]["saldo"] -= valor
        salvar_todos_no_txt()
        novo_saldo = banco_dados[origem]["saldo"]
        resultado_operacao.configure(
            text=f"Saque de R$ {valor:,.2f} realizado!\nNovo saldo: R$ {novo_saldo:,.2f}",
            text_color="#16A34A"
        )

    elif tipo == "Transferência":
        destino = campo_op_destino.get().strip()
        if not destino:
            resultado_operacao.configure(text="Informe a conta destino!", text_color="#DC2626")
            return
        if destino not in banco_dados:
            resultado_operacao.configure(text=f"Conta destino '{destino}' não existe!", text_color="#DC2626")
            return
        if origem == destino:
            resultado_operacao.configure(text="Origem e destino não podem ser iguais!", text_color="#DC2626")
            return
        if banco_dados[origem]["saldo"] < valor:
            resultado_operacao.configure(text="Saldo insuficiente para transferir!", text_color="#DC2626")
            return

        banco_dados[origem]["saldo"] -= valor
        banco_dados[destino]["saldo"] += valor
        salvar_todos_no_txt()

        novo_saldo = banco_dados[origem]["saldo"]
        destinatario = banco_dados[destino]["nome"]
        resultado_operacao.configure(
            text=f"Transferido R$ {valor:,.2f} para {destinatario}!\nSeu saldo atual: R$ {novo_saldo:,.2f}",
            text_color="#16A34A"
        )

    campo_op_valor.delete(0, "end")

btn_operar = ctk.CTkButton(
    aba_operacoes, text="Confirmar Operação", command=realizar_operacao,
    width=310, height=42, font=("Segoe UI", 13, "bold"),
    fg_color="#0F2B5C", hover_color="#091D3E", corner_radius=6
)
btn_operar.pack(pady=10)

janela.mainloop()