# CODIGO FEIO DE PROPOSITO (TF 11). Funciona, mas viola quase todas as regras do
# Object Calisthenics. A missao e consertar SEM mudar o que ele imprime.
# Rodar no terminal: python3 loja_feia.py

pedidos = []                   # todos os pedidos da loja: lista solta, global


class Pedido:
    def __init__(self, numero_do_pedido, cliente):
        self.numero_do_pedido = numero_do_pedido
        self.cliente = cliente
        self.itens = []
        self.status = "A"     # A = aberto, P = pago, C = cancelado

    def obter_status(self):
        return self.status

    def definir_status(self, novo_status):
        self.status = novo_status


class Cliente:
    def __init__(
        self,
        nome_do_cliente,
        cpf_do_cliente,
        email_do_cliente,
        rua_do_cliente,
        cidade_do_cliente,
        codigo_postal,
        tipo_de_cliente,
    ):
        self.nome_do_cliente = nome_do_cliente
        self.cpf_do_cliente = cpf_do_cliente
        self.email_do_cliente = email_do_cliente
        self.rua_do_cliente = rua_do_cliente
        self.cidade_do_cliente = cidade_do_cliente
        self.codigo_postal = codigo_postal
        self.tipo_de_cliente = tipo_de_cliente


class Produto:
    def __init__(self, nome_do_produto, preco_unitario):
        self.nome_do_produto = nome_do_produto
        self.preco_unitario = preco_unitario


class ItemDoPedido:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade


def validar_dados_do_cliente(cliente):
    if len(cliente.email_do_cliente) > 0:
        if "@" in cliente.email_do_cliente:
            if len(cliente.cpf_do_cliente) == 11:
                if len(cliente.codigo_postal) == 8:
                    return "ok"
                else:
                    return "cep invalido"
            else:
                return "cpf invalido"
        else:
            return "email invalido"
    else:
        return "email vazio"


def criar_pedido(numero_do_pedido, cliente):
    resultado_da_validacao = validar_dados_do_cliente(cliente)
    if resultado_da_validacao != "ok":
        print("pedido", numero_do_pedido, "recusado:", resultado_da_validacao)
        return None
    else:
        pedido = Pedido(numero_do_pedido, cliente)
        pedidos.append(pedido)
        return pedido


def adicionar_item(pedido, produto, quantidade):
    pedido.itens.append(ItemDoPedido(produto, quantidade))


def calcular_total(pedido):
    valor_total = 0
    for item in pedido.itens:
        valor_total = (
            valor_total + item.quantidade * item.produto.preco_unitario
        )
    return valor_total


def calcular_desconto(tipo_de_cliente, valor_total):
    if tipo_de_cliente == "V":
        valor_do_desconto = valor_total * 0.10
    elif tipo_de_cliente == "F":
        valor_do_desconto = valor_total * 0.20
    else:
        valor_do_desconto = 0
    return valor_do_desconto


def calcular_valor_a_pagar(pedido):
    return calcular_total(pedido) - calcular_desconto(
        pedido.cliente.tipo_de_cliente, calcular_total(pedido)
    )


def pagar_pedido(pedido):
    if pedido.obter_status() == "A":
        if len(pedido.itens) > 0:
            pedido.definir_status("P")
            return True
        else:
            return False
    else:
        return False


def cancelar_pedido(pedido):
    if pedido.obter_status() == "A":
        pedido.definir_status("C")
        return True
    else:
        return False


def descrever_status(status):
    if status == "A":
        return "aberto"
    elif status == "P":
        return "pago"
    else:
        return "cancelado"


def gerar_relatorio():
    for pedido in pedidos:
        print(
            "Pedido",
            pedido.numero_do_pedido,
            "-",
            pedido.cliente.nome_do_cliente,
            "-",
            pedido.cliente.cidade_do_cliente,
        )
        print("  status:", descrever_status(pedido.obter_status()))
        for item in pedido.itens:
            print(
                "  ",
                item.quantidade,
                "x",
                item.produto.nome_do_produto,
                "= R$ %.2f"
                % (item.quantidade * item.produto.preco_unitario),
            )
        if len(pedido.itens) > 0:
            print(
                "  total: R$ %.2f | desconto: R$ %.2f | a pagar: R$ %.2f"
                % (
                    calcular_total(pedido),
                    calcular_desconto(
                        pedido.cliente.tipo_de_cliente,
                        calcular_total(pedido),
                    ),
                    calcular_valor_a_pagar(pedido),
                )
            )


def calcular_total_arrecadado():
    valor_total_arrecadado = 0
    for pedido in pedidos:
        if pedido.obter_status() == "P":
            valor_total_arrecadado = (
                valor_total_arrecadado + calcular_valor_a_pagar(pedido)
            )
    return valor_total_arrecadado


def contar_pedidos_abertos():
    quantidade_de_pedidos_abertos = 0
    for pedido in pedidos:
        if pedido.obter_status() == "A":
            quantidade_de_pedidos_abertos = quantidade_de_pedidos_abertos + 1
    return quantidade_de_pedidos_abertos


# --- o roteiro da loja (o TF mantem esta saida identica) -----------------------
cliente_ana = Cliente(
    "Ana Souza",
    "12345678901",
    "ana@mail.com",
    "Rua das Flores, 10",
    "Sorocaba",
    "18010000",
    "V",
)
cliente_bruno = Cliente(
    "Bruno Lima",
    "123",
    "bruno@mail.com",
    "Av. Central, 200",
    "Votorantim",
    "18110000",
    "N",
)
cliente_carla = Cliente(
    "Carla Dias",
    "98765432100",
    "carla.mail.com",
    "Rua do Sol, 55",
    "Sorocaba",
    "18020000",
    "F",
)
cliente_diego = Cliente(
    "Diego Rocha",
    "11122233344",
    "diego@mail.com",
    "Rua Nova, 7",
    "Itu",
    "13300000",
    "N",
)
cliente_eva = Cliente(
    "Eva Nunes",
    "55566677788",
    "eva@mail.com",
    "Alameda Azul, 1",
    "Itu",
    "13300001",
    "F",
)
cliente_fabio = Cliente(
    "Fabio Costa",
    "99988877766",
    "fabio@mail.com",
    "Rua Velha, 3",
    "Itu",
    "123",
    "N",
)
cliente_gil = Cliente(
    "Gil Alves",
    "44455566677",
    "gil@mail.com",
    "Rua do Meio, 9",
    "Sorocaba",
    "18030000",
    "N",
)

produto_caderno = Produto("Caderno", 15.5)
produto_caneta = Produto("Caneta", 2.5)
produto_livro = Produto("Livro", 89.5)
produto_fone = Produto("Fone", 60.0)

pedido_da_ana = criar_pedido(1, cliente_ana)
adicionar_item(pedido_da_ana, produto_caderno, 2)
adicionar_item(pedido_da_ana, produto_caneta, 5)

criar_pedido(2, cliente_bruno)

pedido_da_ana_segundo = criar_pedido(3, cliente_ana)
adicionar_item(pedido_da_ana_segundo, produto_livro, 1)

criar_pedido(4, cliente_carla)

pedido_do_diego = criar_pedido(5, cliente_diego)

pedido_da_eva = criar_pedido(6, cliente_eva)
adicionar_item(pedido_da_eva, produto_fone, 1)

criar_pedido(7, cliente_fabio)

pedido_do_gil = criar_pedido(8, cliente_gil)
adicionar_item(pedido_do_gil, produto_fone, 2)

print("pagar 1:", pagar_pedido(pedido_da_ana))
print("pagar 3:", pagar_pedido(pedido_da_ana_segundo))
print("pagar 5:", pagar_pedido(pedido_do_diego))
print("pagar 6:", pagar_pedido(pedido_da_eva))
print("cancelar 5:", cancelar_pedido(pedido_do_diego))
print("cancelar 1:", cancelar_pedido(pedido_da_ana))

gerar_relatorio()
print("arrecadado: R$ %.2f" % calcular_total_arrecadado())
print("abertos:", contar_pedidos_abertos())