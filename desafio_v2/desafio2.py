import textwrap
from abc import ABC, abstractmethod

class PessoaFisica:
    def __init__(self, nome, data_nascimento, cpf):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Cliente(PessoaFisica):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(nome, data_nascimento, cpf)
        self.contas = []    
        self.endereco = endereco
        
    def adicionar_conta(self, conta):
        self.contas.append(conta)
        
    def listar_contas(self):
        return self.contas
    
    def realizar_transacao(self, conta, transacao):
        if transacao.registrar(conta):
            conta.historico.adicionar_transacao(transacao)
            print("Transação realizada com sucesso!")
        else:
            print("Falha na transação.")


class Conta:
    def __init__(self, numero, cliente, agencia = "0001"):
        self.saldo = 0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()
    
    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            return True
        return False
    
    def sacar(self, valor):
        if valor > 0 and valor <= self.saldo:
            self.saldo -= valor
            return True
        return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0
        
    def sacar(self, valor):
        if valor > self.limite:
            print("Operação falhou! O valor do saque excede o limite.")
            return False
        if self.numero_saques >= self.limite_saques:
            print("Operação falhou! Número máximo de saques excedido.")
            return False
        if super().sacar(valor):
            self.numero_saques += 1
            return True
        return False
        
        
class Transacao(ABC):
    
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @abstractmethod
    def registrar(self, conta):
        pass
    
class Saque(Transacao):
    
    @property
    def valor(self):
        return self._valor
    
    def __init__(self, valor):
        self._valor = valor
        
    def registrar(self, conta):
        return conta.sacar(self.valor)


class Deposito(Transacao):
    
    @property
    def valor(self):
        return self._valor
    
    def __init__(self, valor):
        self._valor = valor
        
    def registrar(self, conta):
        return conta.depositar(self.valor)


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

    def imprimir(self):
        if not self.transacoes:
            print("Não foram realizadas movimentações.")
            return

        for transacao in self.transacoes:
            print(f"{transacao.__class__.__name__}: R$ {transacao.valor:.2f}")




def menu():
    menu = """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [l] Nova conta
    [n] Novo usuário
    [num] Listar contas
    [q] Sair

    => """
    return input(textwrap.dedent(menu))

# ===== Programa principal =====
def main():
    
    clientes = []
    contas = []
    
    while True:
        opcao = menu()

        if opcao == "d":
            cpf = input("CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if not cliente or not cliente.contas:
                print("Cliente ou conta não encontrado.")
                continue

            valor = float(input("Valor do depósito: "))
            cliente.realizar_transacao(cliente.contas[0], Deposito(valor))

        elif opcao == "s":
            cpf = input("CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if not cliente or not cliente.contas:
                print("Cliente ou conta não encontrado.")
                continue

            valor = float(input("Valor do saque: "))
            cliente.realizar_transacao(cliente.contas[0], Saque(valor))

        elif opcao == "e":
            cpf = input("CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if not cliente or not cliente.contas:
                print("Cliente ou conta não encontrado.")
                continue
            
            conta = cliente.contas[0]
            print("\n===== EXTRATO =====")
            conta.historico.imprimir()
            print(f"Saldo: R$ {conta.saldo:.2f}")
            print("===================")
            
        elif opcao == "n":
            nome = input("Nome: ")
            cpf = input("CPF: ")
            data = input("Data nascimento: ")
            endereco = input("Endereço: ")

            cliente = Cliente(nome, data, cpf, endereco)
            clientes.append(cliente)
            print("Cliente criado com sucesso!")
        
        elif opcao == "l":
            cpf = input("CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if not cliente:
                print("Cliente não encontrado.")
                continue

            conta = ContaCorrente(len(contas) + 1, cliente)
            cliente.adicionar_conta(conta)
            contas.append(conta)
            print("Conta criada com sucesso!")

        elif opcao == "num":
            cpf = input("CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if not cliente:
                print("Cliente não encontrado.")
                continue

            if not cliente.contas:
                print("Cliente não possui contas.")
                continue

            print("\n===== CONTAS DO CLIENTE =====")
            for conta in cliente.listar_contas():
                print(f"Agência: {conta.agencia}")
                print(f"Número: {conta.numero}")
                print(f"Saldo: R$ {conta.saldo:.2f}")
                print("-" * 30)
                    
        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
    
main()