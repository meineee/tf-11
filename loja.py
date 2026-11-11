# CODIGO FEIO DE PROPOSITO (TF 11). Funciona, mas viola quase todas as regras do
# Object Calisthenics. A missao e consertar SEM mudar o que ele imprime.
# Rodar no terminal: python3 loja_feia.py

from decimal import Decimal, ROUND_HALF_UP


class Cpf:
    def __init__(self, valor):
        if len(valor) != 11:
            raise ValueError("cpf invalido")
        self.valor = valor


class Email:
    def __init__(self, valor):
        if len(valor) == 0:
            raise ValueError("email vazio")
        if "@" not in valor:
            raise ValueError("email invalido")
        self.valor = valor


class Cep:
    def __init__(self, valor):
        if len(valor) != 8:
            raise ValueError("cep invalido")
        self.valor = valor


class Dinheiro:
    def __init__(self, centavos):
        if not isinstance(centavos, int):
            raise TypeError("centavos deve ser um numero inteiro")
        self.centavos = centavos

    def somar(self, outro_valor):
        return Dinheiro(self.centavos + outro_valor.centavos)

    def subtrair(self, outro_valor):
        return Dinheiro(self.centavos - outro_valor.centavos)

    def multiplicar(self, quantidade):
        return Dinheiro(self.centavos * quantidade)

    def calcular_percentual(self, percentual):
        valor_calculado = (
            Decimal(self.centavos) * Decimal(str(percentual)) / Decimal(100)
        )
        return Dinheiro(
            int(
                valor_calculado.quantize(
                    Decimal("1"), rounding=ROUND_HALF_UP
                )
            )
        )

    def __str__(self):
        sinal = "-" if self.centavos < 0 else ""
        valor_absoluto = abs(self.centavos)
        return "R$ %s%d.%02d" % (
            sinal,
            valor_absoluto // 100,
            valor_absoluto % 100,
        )


class Status:
    def __init__(self, codigo):
        if codigo not in ("A", "P", "C"):
            raise ValueError("status invalido")
        self.codigo = codigo

    def descrever(self):
        if self.codigo == "A":
            return "aberto"
        elif self.codigo == "P":
            return "pago"
        return "cancelado"

    def esta_aberto(self):
        return self.codigo == "A"


class Pedido:
    def __init__(self, cliente):
        self.cliente = cliente
        self.itens = ItensDoPedido()
        self.status = Status("A")

    def obter_status(self):
        return self.status

    def definir_status(self, novo_status):
        self.status = novo_status


class Cliente:
    def __init__(
        self,
        nome_do_cliente,
        email_do_cliente,
        cpf_do_cliente,
        rua_do_cliente,
        cidade_do_cliente,
        codigo_postal,
        tipo_de_cliente,
    ):
        self.nome_do_cliente = nome_do_cliente
        self.email_do_cliente = Email(email_do_cliente)
        self.cpf_do_cliente = Cpf(cpf_do_cliente)
        self.rua_do_cliente = rua_do_cliente
        self.cidade_do_cliente = cidade_do_cliente
        self.codigo_postal = Cep(codigo_postal)
        self.tipo_de_cliente = tipo_de_cliente


class Produto:
    def __init__(self, nome_do_produto, preco_unitario):
        self.nome_do_produto = nome_do_produto
        self.preco_unitario = preco_unitario


class ItemDoPedido:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade


class ItensDoPedido:
    def __init__(self):
        self._itens = []

    def adicionar(self, produto, quantidade):
        self._itens.append(ItemDoPedido(produto, quantidade))

    def esta_vazia(self):
        return len(self._itens) == 0

    def calcular_total(self):
        valor_total = Dinheiro(0)
        for item in self._itens:
            valor_total = valor_total.somar(
                item.produto.preco_unitario.multiplicar(item.quantidade)
            )
        return valor_total

    def imprimir_itens(self):
        for item in self._itens:
            print(
                "  ",
                item.quantidade,
                "x",
                item.produto.nome_do_produto,
                "=",
                item.produto.preco_unitario.multiplicar(item.quantidade),
            )


class Pedidos:
    def __init__(self):
        self._pedidos = {}

    def criar_pedido(self, numero_do_pedido, cliente):
        pedido = Pedido(cliente)
        self._pedidos[numero_do_pedido] = pedido
        return pedido

    def imprimir_relatorio(self):
        for numero_do_pedido, pedido in self._pedidos.items():
            print(
                "Pedido",
                numero_do_pedido,
                "-",
                pedido.cliente.nome_do_cliente,
                "-",
                pedido.cliente.cidade_do_cliente,
            )
            print("  status:", pedido.obter_status().descrever())
            pedido.itens.imprimir_itens()
            if not pedido.itens.esta_vazia():
                print(
                    "  total: %s | desconto: %s | a pagar: %s"
                    % (
                        pedido.itens.calcular_total(),
                        calcular_desconto(
                            pedido.cliente.tipo_de_cliente,
                            pedido.itens.calcular_total(),
                        ),
                        calcular_valor_a_pagar(pedido),
                    )
                )

    def calcular_total_arrecadado(self):
        valor_total_arrecadado = Dinheiro(0)
        for pedido in self._pedidos.values():
            if pedido.obter_status().codigo == "P":
                valor_total_arrecadado = valor_total_arrecadado.somar(
                    calcular_valor_a_pagar(pedido)
                )
        return valor_total_arrecadado

    def contar_pedidos_abertos(self):
        quantidade_de_pedidos_abertos = 0
        for pedido in self._pedidos.values():
            if pedido.obter_status().esta_aberto():
                quantidade_de_pedidos_abertos = (
                    quantidade_de_pedidos_abertos + 1
                )
        return quantidade_de_pedidos_abertos


def calcular_desconto(tipo_de_cliente, valor_total):
    if tipo_de_cliente == "V":
        percentual_do_desconto = 10
    elif tipo_de_cliente == "F":
        percentual_do_desconto = 20
    else:
        percentual_do_desconto = 0
    return valor_total.calcular_percentual(percentual_do_desconto)


def calcular_valor_a_pagar(pedido):
    return pedido.itens.calcular_total().subtrair(
        calcular_desconto(
            pedido.cliente.tipo_de_cliente, pedido.itens.calcular_total()
        )
    )


def pagar_pedido(pedido):
    if pedido.obter_status().esta_aberto():
        if not pedido.itens.esta_vazia():
            pedido.definir_status(Status("P"))
            return True
        else:
            return False
    else:
        return False


def cancelar_pedido(pedido):
    if pedido.obter_status().esta_aberto():
        pedido.definir_status(Status("C"))
        return True
    else:
        return False


# --- o roteiro da loja (o TF mantem esta saida identica) -----------------------
cliente_ana = Cliente(
    "Ana Souza",
    "ana@mail.com",
    "12345678901",
    "Rua das Flores, 10",
    "Sorocaba",
    "18010000",
    "V",
)
try:
    cliente_bruno = Cliente(
        "Bruno Lima",
        "bruno@mail.com",
        "123",
        "Av. Central, 200",
        "Votorantim",
        "18110000",
        "N",
    )
except ValueError as erro:
    print("pedido 2 recusado: %s" % erro)
try:
    cliente_carla = Cliente(
        "Carla Dias",
        "carla.mail.com",
        "98765432100",
        "Rua do Sol, 55",
        "Sorocaba",
        "18020000",
        "F",
    )
except ValueError as erro:
    print("pedido 4 recusado: %s" % erro)
cliente_diego = Cliente(
    "Diego Rocha",
    "diego@mail.com",
    "11122233344",
    "Rua Nova, 7",
    "Itu",
    "13300000",
    "N",
)
cliente_eva = Cliente(
    "Eva Nunes",
    "eva@mail.com",
    "55566677788",
    "Alameda Azul, 1",
    "Itu",
    "13300001",
    "F",
)
try:
    cliente_fabio = Cliente(
        "Fabio Costa",
        "fabio@mail.com",
        "99988877766",
        "Rua Velha, 3",
        "Itu",
        "123",
        "N",
    )
except ValueError as erro:
    print("pedido 7 recusado: %s" % erro)
cliente_gil = Cliente(
    "Gil Alves",
    "gil@mail.com",
    "44455566677",
    "Rua do Meio, 9",
    "Sorocaba",
    "18030000",
    "N",
)

produto_caderno = Produto("Caderno", Dinheiro(1550))
produto_caneta = Produto("Caneta", Dinheiro(250))
produto_livro = Produto("Livro", Dinheiro(8950))
produto_fone = Produto("Fone", Dinheiro(6000))

pedidos_da_loja = Pedidos()

pedido_da_ana = pedidos_da_loja.criar_pedido(1, cliente_ana)
pedido_da_ana.itens.adicionar(produto_caderno, 2)
pedido_da_ana.itens.adicionar(produto_caneta, 5)

pedido_da_ana_segundo = pedidos_da_loja.criar_pedido(3, cliente_ana)
pedido_da_ana_segundo.itens.adicionar(produto_livro, 1)

pedido_do_diego = pedidos_da_loja.criar_pedido(5, cliente_diego)

pedido_da_eva = pedidos_da_loja.criar_pedido(6, cliente_eva)
pedido_da_eva.itens.adicionar(produto_fone, 1)

pedido_do_gil = pedidos_da_loja.criar_pedido(8, cliente_gil)
pedido_do_gil.itens.adicionar(produto_fone, 2)

print("pagar 1:", pagar_pedido(pedido_da_ana))
print("pagar 3:", pagar_pedido(pedido_da_ana_segundo))
print("pagar 5:", pagar_pedido(pedido_do_diego))
print("pagar 6:", pagar_pedido(pedido_da_eva))
print("cancelar 5:", cancelar_pedido(pedido_do_diego))
print("cancelar 1:", cancelar_pedido(pedido_da_ana))

pedidos_da_loja.imprimir_relatorio()
print("arrecadado:", pedidos_da_loja.calcular_total_arrecadado())
print("abertos:", pedidos_da_loja.contar_pedidos_abertos())