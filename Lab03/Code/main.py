import re


class Node:
    def __init__(self, token_value, index):
        self.token_value = token_value
        self.index = index
        self.left = None
        self.right = None


class SymbolTableBST:
    def __init__(self):
        self.root = None
        self.current_index = 0
        self.in_order_list = []

    def insert(self, token_value):
        if self.root is None:
            self.root = Node(token_value, self.current_index)
            idx = self.current_index
            self.current_index += 1
            return idx
        else:
            return self._insert_recursive(self.root, token_value)

    def _insert_recursive(self, node, token_value):
        if token_value == node.token_value:
            return node.index
        elif token_value < node.token_value:
            if node.left is None:
                node.left = Node(token_value, self.current_index)
                self.current_index += 1
                return node.left.index
            else:
                return self._insert_recursive(node.left, token_value)
        else:
            if node.right is None:
                node.right = Node(token_value, self.current_index)
                self.current_index += 1
                return node.right.index
            else:
                return self._insert_recursive(node.right, token_value)

    def _in_order_traversal(self, node):
        if node is not None:
            self._in_order_traversal(node.left)
            self.in_order_list.append((node.index, node.token_value))
            self._in_order_traversal(node.right)

    def __str__(self):
        self.in_order_list = []
        self._in_order_traversal(self.root)
        res = "Symbol Table (BST In-Order):\n"
        res += "-" * 35 + "\n"
        for idx, val in self.in_order_list:
            res += f" Poz: {idx:<3} | Valoare: {val}\n"
        res += "-" * 35
        return res


class Scanner:
    def __init__(self):
        self.st = SymbolTableBST()
        self.pif = []
        self.errors = []

        self.rules = [
             ('RESERVED_MULTI', r'trimite ordin de executie|pentru fiecare|raportat la|elaboreaza:'),
            ('RESERVED', r'\b(daca|musai|atata|Da|Ba|si|sau|nu-i|citesteSenzor)\b'),
            ('OPERATOR', r'==|!=|<=|>=|<|>|\+|-|\*|/|%|='),
            ('SEPARATOR', r'\(|\)|\[|\]|,'),
            ('STRING', r'"[^"]*"'),
            ('NUMBER', r'\b0|[1-9][0-9]*\b'),
            ('IDENTIFIER', r'[a-zA-Z][a-zA-Z0-9]*'),
            ('WHITESPACE', r'[ \t\n]+'),
            ('MISMATCH', r'.')
        ]

        self.regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.rules)

    def scan(self, source_code):
        line_num = 1
        for match in re.finditer(self.regex, source_code):
            kind = match.lastgroup
            value = match.group()

            if kind == 'WHITESPACE':
                line_num += value.count('\n')
                continue
            elif kind == 'MISMATCH':
                self.errors.append(f"Eroare Lexicala linia {line_num}: token invalid '{value}'")
            elif kind in ['RESERVED_MULTI', 'RESERVED', 'OPERATOR', 'SEPARATOR']:
                self.pif.append((value, -1))
            elif kind in ['IDENTIFIER', 'NUMBER', 'STRING']:
                st_index = self.st.insert(value)
                token_type = "ID" if kind == 'IDENTIFIER' else "CONST"
                self.pif.append((token_type, st_index))

    def print_pif(self):
        print("Program Internal Form (PIF):")
        print("-" * 35)
        for token, st_pos in self.pif:
            print(f" {token:<25} | {st_pos}")
        print("-" * 35 + "\n")


if __name__ == "__main__":
    cod_mock_1 = """
    temp = citesteSenzor(1)
    
    daca temp > 25 musai
        trimite ordin de executie (1, "AC", "porneste")
    atata
    
    temp = citesteSenzor(2)
    
    daca temp < 19 musai
        trimite ordin de executie (2, "AC", "opreste")
    atata
    """

    cod_mock_2 = """
    totiSenzorii = [ 1, 2, 3, 4, 5]

    medieTemp = 0

    pentru fiecare senzor raportat la totiSenzorii elaboreaza:
        temp = citesteSenzor(senzor)
        medieTemp = medieTemp + temp
    atata
    
    medieTemp = medieTemp / 5
    
    daca medieTemp > 27 musai
        trimite ordin de executie (totiSenzorii, "all", "in")
    atata
    
    daca medieTemp < 19 musai
        trimite ordin de executie (totiSenzorii, "all", "out")
    atata
    
    pentru fiecare senzor raportat la totiSenzorii elaboreaza:
        temp = citesteSenzor(senzor)
        daca temp > 25 musai
            trimite ordin de executie (senzor, "AC", "pornit")
        atata
        daca temp < 19 musai
            trimite ordin de executie (senzor, "AC", "oprit")
        atata
    atata
    
    temp5 = citesteSenzor(5)
    temp3 = citesteSenzor(3)
    
    daca temp3 < temp5 musai
        trimite ordin de executie (5, "AC", "pornit")
    atata
    
    daca temp3 > temp5 musai
        trimite ordin de executie (3, "AC", "oprit")
    atata
    """

    scanner = Scanner()
    scanner.scan(cod_mock_1)

    print("mock 1")
    scanner.print_pif()
    print(scanner.st)

    scanner = Scanner()
    scanner.scan(cod_mock_2)
    print("mock 2")
    scanner.print_pif()
    print(scanner.st)