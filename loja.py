# CODIGO FEIO DE PROPOSITO (TF 11). Funciona, mas viola quase todas as regras do
# Object Calisthenics. A missao e consertar SEM mudar o que ele imprime.
# Rodar no terminal: python3 loja_feia.py

pedidos = []                   # todos os pedidos da loja: lista solta, global


class Pedido:
    def __init__(self, numero_do_pedido, nome_do_cliente, cpf_do_cliente, email_do_cliente, rua_do_cliente, cidade_do_cliente, codigo_postal, tipo_de_cliente):
        self.numero_do_pedido = numero_do_pedido
        self.nome_do_cliente = nome_do_cliente
        self.cpf_do_cliente = cpf_do_cliente
        self.email_do_cliente = email_do_cliente
        self.rua_do_cliente = rua_do_cliente
        self.cidade_do_cliente = cidade_do_cliente
        self.codigo_postal = codigo_postal
        self.tipo_de_cliente = tipo_de_cliente
        self.itens = []       # cada item e uma lista: [produto, quantidade, preco]
        self.status = "A"     # A = aberto, P = pago, C = cancelado

    def obter_status(self):
        return self.status

    def definir_status(self, novo_status):
        self.status = novo_status


def validar_dados_do_cliente(email_do_cliente, cpf_do_cliente, codigo_postal):
    if len(email_do_cliente) > 0:
        if "@" in email_do_cliente:
            if len(cpf_do_cliente) == 11:
                if len(codigo_postal) == 8:
                    return "ok"
                else:
                    return "cep invalido"
            else:
                return "cpf invalido"
        else:
            return "email invalido"
    else:
        return "email vazio"


def criar_pedido(numero_do_pedido, nome_do_cliente, cpf_do_cliente, email_do_cliente, rua_do_cliente, cidade_do_cliente, codigo_postal, tipo_de_cliente):
    resultado_da_validacao = validar_dados_do_cliente(
        email_do_cliente, cpf_do_cliente, codigo_postal
    )
    if resultado_da_validacao != "ok":
        print("pedido", numero_do_pedido, "recusado:", resultado_da_validacao)
        return None
    else:
        pedido = Pedido(numero_do_pedido, nome_do_cliente, cpf_do_cliente, email_do_cliente, rua_do_cliente, cidade_do_cliente, codigo_postal, tipo_de_cliente)
        pedidos.append(pedido)
        return pedido


def adicionar_item(pedido, nome_do_produto, quantidade, preco_unitario):
    pedido.itens.append([nome_do_produto, quantidade, preco_unitario])


def calcular_total(pedido):
    valor_total = 0
    for item in pedido.itens:
        valor_total = valor_total + item[1] * item[2]
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
        pedido.tipo_de_cliente, calcular_total(pedido)
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
            pedido.nome_do_cliente,
            "-",
            pedido.cidade_do_cliente,
        )
        print("  status:", descrever_status(pedido.obter_status()))
        for item in pedido.itens:
            print(
                "  ",
                item[1],
                "x",
                item[0],
                "= R$ %.2f" % (item[1] * item[2]),
            )
        if len(pedido.itens) > 0:
            print(
                "  total: R$ %.2f | desconto: R$ %.2f | a pagar: R$ %.2f"
                % (
                    calcular_total(pedido),
                    calcular_desconto(
                        pedido.tipo_de_cliente, calcular_total(pedido)
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
pedido_da_ana = criar_pedido(1, "Ana Souza", "12345678901", "ana@mail.com", "Rua das Flores, 10", "Sorocaba", "18010000", "V")
adicionar_item(pedido_da_ana, "Caderno", 2, 15.5)
adicionar_item(pedido_da_ana, "Caneta", 5, 2.5)

criar_pedido(2, "Bruno Lima", "123", "bruno@mail.com", "Av. Central, 200", "Votorantim", "18110000", "N")

pedido_da_ana_segundo = criar_pedido(3, "Ana Souza", "12345678901", "ana@mail.com", "Rua das Flores, 10", "Sorocaba", "18010000", "V")
adicionar_item(pedido_da_ana_segundo, "Livro", 1, 89.5)

criar_pedido(4, "Carla Dias", "98765432100", "carla.mail.com", "Rua do Sol, 55", "Sorocaba", "18020000", "F")

pedido_do_diego = criar_pedido(5, "Diego Rocha", "11122233344", "diego@mail.com", "Rua Nova, 7", "Itu", "13300000", "N")

pedido_da_eva = criar_pedido(6, "Eva Nunes", "55566677788", "eva@mail.com", "Alameda Azul, 1", "Itu", "13300001", "F")
adicionar_item(pedido_da_eva, "Fone", 1, 60.0)

criar_pedido(7, "Fabio Costa", "99988877766", "fabio@mail.com", "Rua Velha, 3", "Itu", "123", "N")

pedido_do_gil = criar_pedido(8, "Gil Alves", "44455566677", "gil@mail.com", "Rua do Meio, 9", "Sorocaba", "18030000", "N")
adicionar_item(pedido_do_gil, "Fone", 2, 60.0)

print("pagar 1:", pagar_pedido(pedido_da_ana))
print("pagar 3:", pagar_pedido(pedido_da_ana_segundo))
print("pagar 5:", pagar_pedido(pedido_do_diego))
print("pagar 6:", pagar_pedido(pedido_da_eva))
print("cancelar 5:", cancelar_pedido(pedido_do_diego))
print("cancelar 1:", cancelar_pedido(pedido_da_ana))

gerar_relatorio()
print("arrecadado: R$ %.2f" % calcular_total_arrecadado())
print("abertos:", contar_pedidos_abertos())