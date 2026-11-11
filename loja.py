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
        valor_absoluto = abs(self.centavos)
        texto_do_valor = "R$ %d.%02d" % (
            valor_absoluto // 100,
            valor_absoluto % 100,
        )
        if self.centavos >= 0:
            return texto_do_valor
        return "R$ -" + texto_do_valor[3:]


class Status:
    def __init__(self, codigo):
        if codigo not in ("A", "P", "C"):
            raise ValueError("status invalido")
        self._codigo = codigo

    def descrever(self):
        descricoes = {
            "A": "aberto",
            "P": "pago",
            "C": "cancelado",
        }
        return descricoes[self._codigo]

    def esta_aberto(self):
        return self._codigo == "A"

    def esta_pago(self):
        return self._codigo == "P"


class Pedido:
    def __init__(self, cliente):
        self._cliente = cliente
        self._itens = ItensDoPedido()
        self._status = Status("A")

    def adicionar_item(self, produto, quantidade):
        self._itens.adicionar(produto, quantidade)

    def pagar(self):
        if not self.pode_ser_pago():
            return False
        self._status = Status("P")
        return True

    def pode_ser_pago(self):
        return self.esta_aberto() and not self._itens.esta_vazia()

    def cancelar(self):
        if not self.esta_aberto():
            return False
        self._status = Status("C")
        return True

    def esta_aberto(self):
        return self._status.esta_aberto()

    def esta_pago(self):
        return self._status.esta_pago()

    def calcular_valor_a_pagar(self):
        valor_total = self._itens.calcular_total()
        valor_do_desconto = self._cliente.desconto_sobre(valor_total)
        return valor_total.subtrair(valor_do_desconto)

    def imprimir_relatorio(self, numero_do_pedido):
        self._cliente.imprimir_identificacao(numero_do_pedido)
        print("  status:", self._status.descrever())
        self._itens.imprimir_itens()
        if self._itens.esta_vazia():
            return
        self.imprimir_totais()

    def imprimir_totais(self):
        valor_total = self._itens.calcular_total()
        valor_do_desconto = self._cliente.desconto_sobre(valor_total)
        valor_a_pagar = valor_total.subtrair(valor_do_desconto)
        print(
            "  total: %s | desconto: %s | a pagar: %s"
            % (valor_total, valor_do_desconto, valor_a_pagar)
        )


class Pessoa:
    def __init__(self, nome, cpf, email):
        self.nome = nome
        self.cpf = cpf
        self.email = email

    def imprimir_nome(self):
        print(self.nome, "-", end=" ")


class Endereco:
    def __init__(self, rua, cidade, cep):
        self.rua = rua
        self.cidade = cidade
        self.cep = cep

    def imprimir_cidade(self):
        print(self.cidade)


class Cliente:
    def __init__(self, pessoa, endereco, tipo_de_cliente):
        self.pessoa = pessoa
        self.endereco = endereco
        self.tipo_de_cliente = tipo_de_cliente

    def imprimir_identificacao(self, numero_do_pedido):
        print("Pedido", numero_do_pedido, "-", end=" ")
        self.pessoa.imprimir_nome()
        self.endereco.imprimir_cidade()

    def desconto_sobre(self, valor):
        return self.tipo_de_cliente.desconto_sobre(valor)


class Produto:
    def __init__(self, nome_do_produto, preco_unitario):
        self.nome_do_produto = nome_do_produto
        self.preco_unitario = preco_unitario

    def calcular_total(self, quantidade):
        return self.preco_unitario.multiplicar(quantidade)

    def imprimir_item(self, quantidade):
        valor_do_item = self.calcular_total(quantidade)
        print(
            "  ",
            quantidade,
            "x",
            self.nome_do_produto,
            "=",
            valor_do_item,
        )


class ItemDoPedido:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade

    def calcular_total(self):
        return self.produto.calcular_total(self.quantidade)

    def imprimir(self):
        self.produto.imprimir_item(self.quantidade)


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
            valor_do_item = item.calcular_total()
            valor_total = valor_total.somar(valor_do_item)
        return valor_total

    def imprimir_itens(self):
        for item in self._itens:
            item.imprimir()


class Pedidos:
    def __init__(self):
        self._pedidos = {}

    def criar_pedido(self, numero_do_pedido, cliente):
        pedido = Pedido(cliente)
        self._pedidos[numero_do_pedido] = pedido
        return pedido

    def imprimir_relatorio(self):
        for numero_do_pedido, pedido in self._pedidos.items():
            pedido.imprimir_relatorio(numero_do_pedido)

    def calcular_total_arrecadado(self):
        valor_total_arrecadado = Dinheiro(0)
        pedidos_pagos = [
            pedido for pedido in self._pedidos.values() if pedido.esta_pago()
        ]
        for pedido in pedidos_pagos:
            valor_a_pagar = pedido.calcular_valor_a_pagar()
            valor_total_arrecadado = valor_total_arrecadado.somar(
                valor_a_pagar
            )
        return valor_total_arrecadado

    def contar_pedidos_abertos(self):
        return sum(
            1
            for pedido in self._pedidos.values()
            if pedido.esta_aberto()
        )


class TipoNormal:
    def desconto_sobre(self, valor):
        return valor.calcular_percentual(0)


class TipoVip:
    def desconto_sobre(self, valor):
        return valor.calcular_percentual(10)


class TipoFuncionario:
    def desconto_sobre(self, valor):
        return valor.calcular_percentual(20)


# --- o roteiro da loja (o TF mantem esta saida identica) -----------------------
cliente_ana = Cliente(
    Pessoa("Ana Souza", Cpf("12345678901"), Email("ana@mail.com")),
    Endereco("Rua das Flores, 10", "Sorocaba", Cep("18010000")),
    TipoVip(),
)
try:
    cliente_bruno = Cliente(
        Pessoa("Bruno Lima", Cpf("123"), Email("bruno@mail.com")),
        Endereco("Av. Central, 200", "Votorantim", Cep("18110000")),
        TipoNormal(),
    )
except ValueError as erro:
    print("pedido 2 recusado: %s" % erro)
try:
    cliente_carla = Cliente(
        Pessoa("Carla Dias", Cpf("98765432100"), Email("carla.mail.com")),
        Endereco("Rua do Sol, 55", "Sorocaba", Cep("18020000")),
        TipoFuncionario(),
    )
except ValueError as erro:
    print("pedido 4 recusado: %s" % erro)
cliente_diego = Cliente(
    Pessoa("Diego Rocha", Cpf("11122233344"), Email("diego@mail.com")),
    Endereco("Rua Nova, 7", "Itu", Cep("13300000")),
    TipoNormal(),
)
cliente_eva = Cliente(
    Pessoa("Eva Nunes", Cpf("55566677788"), Email("eva@mail.com")),
    Endereco("Alameda Azul, 1", "Itu", Cep("13300001")),
    TipoFuncionario(),
)
try:
    cliente_fabio = Cliente(
        Pessoa("Fabio Costa", Cpf("99988877766"), Email("fabio@mail.com")),
        Endereco("Rua Velha, 3", "Itu", Cep("123")),
        TipoNormal(),
    )
except ValueError as erro:
    print("pedido 7 recusado: %s" % erro)
cliente_gil = Cliente(
    Pessoa("Gil Alves", Cpf("44455566677"), Email("gil@mail.com")),
    Endereco("Rua do Meio, 9", "Sorocaba", Cep("18030000")),
    TipoNormal(),
)

produto_caderno = Produto("Caderno", Dinheiro(1550))
produto_caneta = Produto("Caneta", Dinheiro(250))
produto_livro = Produto("Livro", Dinheiro(8950))
produto_fone = Produto("Fone", Dinheiro(6000))

pedidos_da_loja = Pedidos()

pedido_da_ana = pedidos_da_loja.criar_pedido(1, cliente_ana)
pedido_da_ana.adicionar_item(produto_caderno, 2)
pedido_da_ana.adicionar_item(produto_caneta, 5)

pedido_da_ana_segundo = pedidos_da_loja.criar_pedido(3, cliente_ana)
pedido_da_ana_segundo.adicionar_item(produto_livro, 1)

pedido_do_diego = pedidos_da_loja.criar_pedido(5, cliente_diego)

pedido_da_eva = pedidos_da_loja.criar_pedido(6, cliente_eva)
pedido_da_eva.adicionar_item(produto_fone, 1)

pedido_do_gil = pedidos_da_loja.criar_pedido(8, cliente_gil)
pedido_do_gil.adicionar_item(produto_fone, 2)

print("pagar 1:", pedido_da_ana.pagar())
print("pagar 3:", pedido_da_ana_segundo.pagar())
print("pagar 5:", pedido_do_diego.pagar())
print("pagar 6:", pedido_da_eva.pagar())
print("cancelar 5:", pedido_do_diego.cancelar())
print("cancelar 1:", pedido_da_ana.cancelar())

pedidos_da_loja.imprimir_relatorio()
print("arrecadado:", pedidos_da_loja.calcular_total_arrecadado())
print("abertos:", pedidos_da_loja.contar_pedidos_abertos())