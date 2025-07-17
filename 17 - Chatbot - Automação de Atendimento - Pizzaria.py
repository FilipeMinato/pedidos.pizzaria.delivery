# Projeto 21 - Bot de Atendimento para Compra em Pizzaria
# Interface gráfica com Tkinter para simular um atendimento de pizzaria
# Cliente escolhe tamanho, sabores, adicionais, entrega e forma de pagamento
# Pagamento pode ser via PIX (com desconto) ou cartão (link fictício)
# Usa mensagens amigáveis e uma experiência passo a passo

import tkinter as tk
from tkinter import messagebox
import time  # usado no comentário, mas não está sendo usado diretamente no código

# ========================
# DADOS INICIAIS DO SISTEMA
# ========================

# Dicionário com tamanhos de pizza: chave -> (nome, diâmetro cm, preço base, quantidade de sabores)
tamanhos = {
    1: ("Pequena Mimo", 40, 59.90, 2),
    2: ("Média Saborosa", 50, 79.90, 3),
    3: ("Grande Tentação", 60, 99.90, 4),
    4: ("Gigante Supremo", 70, 129.90, 4)
}

# Lista de sabores disponíveis para o cliente escolher
sabores = {
    1: "Margherita Clássica", 2: "Pepperoni Picante", 3: "Frango com Catupiry",
    4: "Quatro Queijos", 5: "Portuguesa Tradicional", 6: "Calabresa Apimentada",
    7: "Vegetariana Garden", 8: "Chocolate com Morango", 9: "Atum Especial",
    10: "Bacon Crocante", 11: "Camarão Deluxe", 12: "Cheddar com Cebola",
    13: "Brócolis com Alho", 14: "Marguerita Vegana", 15: "Carne Seca com Catupiry"
}

# Preços fixos para adicionais
PRECO_REFRI = 15.00
PRECO_BORDA = 10.00
PRECO_ENTREGA = 10.00


# ========================
# CLASSE PRINCIPAL DO APP
# ========================
class PizzariaApp:
    def __init__(self, master):
        """Inicializa o app, define janela e configurações iniciais."""
        self.master = master
        master.title("Pizzaria Super Delícias")
        self.pedidos = []             # Lista de todas as pizzas do pedido
        self.total_geral = 0          # Soma total do pedido
        self.tem_entrega = False      # Indica se o cliente escolheu entrega
        self.setup_inicio()           # Começa na tela inicial

    def limpar_janela(self):
        """Remove todos os widgets da janela (útil para trocar de tela)."""
        for widget in self.master.winfo_children():
            widget.destroy()

    def setup_inicio(self):
        """Exibe a tela inicial com botão para iniciar novo pedido."""
        self.limpar_janela()
        tk.Label(self.master, text="🍕 Bem-vindo à Pizzaria Super Delícias! 🍕", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self.master, text="Fazer um pedido", command=self.novo_pedido, width=30).pack(pady=20)

    def novo_pedido(self):
        """Inicia um novo dicionário para representar uma pizza e chama seleção de tamanho."""
        self.pizza = {
            'tamanho': None,
            'sabores': [],
            'preco': 0.0,
            'borda': 0,
            'refri': 0
        }
        self.selecionar_tamanho()

    def selecionar_tamanho(self):
        """Exibe botões para escolher o tamanho da pizza."""
        self.limpar_janela()
        tk.Label(self.master, text="Escolha o tamanho da pizza:", font=("Helvetica", 14)).pack(pady=10)
        for k, v in tamanhos.items():
            texto = f"{k} - {v[0]} ({v[1]}cm) - R${v[2]:.2f} ({v[3]} sabores)"
            tk.Button(self.master, text=texto, width=45, command=lambda k=k: self.definir_tamanho(k)).pack(pady=4)

    def definir_tamanho(self, k):
        """Registra o tamanho escolhido e avança para a seleção de sabores."""
        self.pizza['tamanho'] = tamanhos[k]
        self.pizza['preco'] = tamanhos[k][2]
        self.max_sabores = tamanhos[k][3]
        self.selecionar_sabor()

    def selecionar_sabor(self):
        """Permite escolher os sabores da pizza, respeitando o limite de sabores."""
        self.limpar_janela()
        tk.Label(self.master, text=f"Escolha {len(self.pizza['sabores'])+1}º sabor de até {self.max_sabores}:", font=("Helvetica", 13)).pack(pady=10)
        for num, sabor in sabores.items():
            tk.Button(self.master, text=f"{num} - {sabor}", width=45, command=lambda num=num: self.adicionar_sabor(num)).pack(pady=3)

    def adicionar_sabor(self, sabor_id):
        """Adiciona o sabor escolhido à pizza e verifica se precisa escolher mais sabores."""
        self.pizza['sabores'].append(sabor_id)
        if len(self.pizza['sabores']) < self.max_sabores:
            self.selecionar_sabor()
        else:
            self.adicionais()

    def adicionais(self):
        """Exibe a tela com opções de adicionais para a pizza."""
        self.limpar_janela()
        tk.Label(self.master, text="Adicionais para esta pizza:", font=("Helvetica", 14)).pack(pady=10)

        self.resumo_texto = tk.StringVar()
        self.atualizar_resumo()

        tk.Button(self.master, text="Adicionar Refrigerante 2L", command=self.add_refri).pack(pady=5)
        tk.Button(self.master, text="Adicionar Borda Recheada", command=self.add_borda).pack(pady=5)
        tk.Label(self.master, textvariable=self.resumo_texto, justify="left", font=("Helvetica", 11)).pack(pady=10)
        tk.Button(self.master, text="Concluir esta pizza", command=self.confirmar_pizza).pack(pady=10)

    def add_refri(self):
        """Adiciona refrigerante, com limite de 2 por pizza."""
        if self.pizza['refri'] < 2:
            self.pizza['refri'] += 1
            self.pizza['preco'] += PRECO_REFRI
            self.atualizar_resumo()
        else:
            messagebox.showinfo("Limite atingido", "Você só pode adicionar até 2 refrigerantes por pizza.")

    def add_borda(self):
        """Adiciona borda, com limite de 1 por pizza."""
        if self.pizza['borda'] == 0:
            self.pizza['borda'] = 1
            self.pizza['preco'] += PRECO_BORDA
            self.atualizar_resumo()
        else:
            messagebox.showinfo("Limite atingido", "Você só pode adicionar 1 borda por pizza.")

    def atualizar_resumo(self):
        """Atualiza o resumo da pizza atual com tamanhos, sabores e adicionais."""
        r = f"🍕 {self.pizza['tamanho'][0]} - R${self.pizza['tamanho'][2]:.2f}\n"
        r += "Sabores:\n" + "\n".join([f"- {sabores[s]}" for s in self.pizza['sabores']])
        if self.pizza['refri']:
            r += f"\n🥤 Refrigerante(s): {self.pizza['refri']} x R${PRECO_REFRI:.2f}"
        if self.pizza['borda']:
            r += f"\n🧀 Borda Recheada: R${PRECO_BORDA:.2f}"
        r += f"\nTotal desta pizza: R${self.pizza['preco']:.2f}"
        self.resumo_texto.set(r)

    def confirmar_pizza(self):
        """Adiciona a pizza ao pedido e pergunta se deseja adicionar outra."""
        self.pedidos.append(self.pizza)
        self.total_geral += self.pizza['preco']
        if messagebox.askyesno("Adicionar mais uma pizza?", "Deseja adicionar mais uma pizza ao pedido?"):
            self.novo_pedido()
        else:
            self.perguntar_entrega()

    def perguntar_entrega(self):
        """Mostra o resumo parcial e pergunta se deseja incluir entrega."""
        self.limpar_janela()
        resumo = "\n".join([f"{p['tamanho'][0]} - R${p['preco']:.2f}" for p in self.pedidos])
        resumo += f"\n\nSubtotal: R${self.total_geral:.2f}"
        tk.Label(self.master, text="Resumo do pedido:", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(self.master, text=resumo, justify="left", font=("Helvetica", 11)).pack()

        if messagebox.askyesno("Entrega", "Deseja entrega por R$10,00?"):
            self.tem_entrega = True
            self.total_geral += PRECO_ENTREGA

        self.pagamento()

    def pagamento(self):
        """Exibe o resumo final e opções de pagamento."""
        self.limpar_janela()
        resumo = "\n".join([f"{p['tamanho'][0]} - R${p['preco']:.2f}" for p in self.pedidos])
        if self.tem_entrega:
            resumo += f"\nEntrega - R${PRECO_ENTREGA:.2f}"
        resumo += f"\n\nTOTAL GERAL: R${self.total_geral:.2f}"
        tk.Label(self.master, text="Resumo Final:", font=("Helvetica", 14)).pack(pady=10)
        tk.Label(self.master, text=resumo, justify="left", font=("Helvetica", 11)).pack()

        tk.Label(self.master, text="Escolha a forma de pagamento:", font=("Helvetica", 13)).pack(pady=10)
        tk.Button(self.master, text="PIX (10% de desconto)", command=self.pagamento_pix).pack(pady=5)
        tk.Button(self.master, text="Cartão de Crédito", command=self.pagamento_cartao).pack(pady=5)

    def pagamento_pix(self):
        """Apresenta chave PIX e aplica desconto de 10%."""
        total_pix = self.total_geral * 0.9
        messagebox.showinfo("PIX", f"Chave PIX: 123e4567-e89b-12d3-a456-426614174000\nValor com desconto: R${total_pix:.2f}")
        if messagebox.askyesno("Confirmação", "Você realizou o pagamento via PIX?"):
            self.finalizar()

    def pagamento_cartao(self):
        """Simula link de pagamento via cartão."""
        messagebox.showinfo("Cartão", "Link de pagamento:\nhttps://mercadopago.com.br/checkout/fake123")
        if messagebox.askyesno("Confirmação", "Você realizou o pagamento com cartão?"):
            self.finalizar()

    def finalizar(self):
        """Mostra mensagem de agradecimento e reinicia o app para novo pedido."""
        self.limpar_janela()
        if self.tem_entrega:
            msg = "🍕 Obrigado pelo pedido! Sua entrega chegará em aproximadamente 50 minutos."
        else:
            msg = "🍕 Obrigado pelo pedido! Sua pizza estará pronta para retirada em até 35 minutos."
        tk.Label(self.master, text=msg, wraplength=400, font=("Helvetica", 13)).pack(pady=20)
        tk.Button(self.master, text="Novo Pedido", command=self.setup_inicio).pack(pady=20)
        # Resetando tudo para um novo pedido
        self.pedidos = []
        self.total_geral = 0
        self.tem_entrega = False


# ========================
# EXECUÇÃO DO APLICATIVO
# ========================
root = tk.Tk()
root.geometry("520x620")  # Define o tamanho da janela
app = PizzariaApp(root)   # Cria uma instância do app
root.mainloop()           # Inicia o loop principal do Tkinter
