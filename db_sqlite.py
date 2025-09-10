import sqlite3
import os

class Database:
    """
    Uma classe para encapsular as operações do banco de dados SQLite.
    Fornece uma interface simples para conectar, executar queries e gerenciar
    transações de forma segura.
    """

    def __init__(self, db_name: str = "database.db"):
        """
        Inicializa a classe Database e conecta-se ao banco de dados.

        Args:
            db_name (str): O nome do arquivo do banco de dados SQLite.
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Estabelece a conexão com o banco de dados e cria um cursor."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            # print(f"Conexão com o banco de dados '{self.db_name}' estabelecida.")
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def close(self):
        """Fecha a conexão com o banco de dados se ela estiver aberta."""
        if self.conn:
            self.conn.commit()  # Garante que todas as transações pendentes sejam salvas
            self.conn.close()
            # print(f"Conexão com o banco de dados '{self.db_name}' fechada.")

    def execute_query(self, query: str, params: tuple = ()) -> int:
        """
        Executa uma query genérica.

        Args:
            query (str): A string da query SQL.
            params (tuple): Uma tupla de parâmetros para a query, para evitar injeção de SQL.

        Returns:
            int: O número de linhas afetadas pela query, ou None em caso de erro.
        """
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            print(f"Erro ao executar a query: {e}")
            return None

    def create_table(self, table_name: str, columns: dict) -> None:
        """
        Cria uma nova tabela no banco de dados se ela não existir.

        Args:
            table_name (str): O nome da tabela a ser criada.
            columns (dict): Um dicionário onde as chaves são os nomes das colunas
                            e os valores são os tipos de dados e restrições (ex: 'TEXT NOT NULL').
        """
        column_definitions = ", ".join([f"{name} {definition}" for name, definition in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions});"
        self.execute_query(query)
        # print(f"Tabela '{table_name}' verificada/criada com sucesso.")

    def insert_data(self, table_name: str, data: dict) -> int:
        """
        Insere uma nova linha de dados em uma tabela.

        Args:
            table_name (str): O nome da tabela.
            data (dict): Um dicionário onde as chaves são os nomes das colunas
                         e os valores são os dados a serem inseridos.

        Returns:
            int: O ID da última linha inserida.
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        values = tuple(data.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
        
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erro ao inserir dados: {e}")
            return None

    def fetch_data(self, table_name: str, columns: str = "*", condition: dict = None, order_by: str = None) -> list:
        """
        Busca dados de uma tabela.

        Args:
            table_name (str): O nome da tabela.
            columns (str): As colunas a serem selecionadas (padrão: '*').
            condition (dict, optional): Condições para a cláusula WHERE.
                                        Ex: {'id': 1, 'status': 'ativo'}
            order_by (str, optional): Coluna para ordenar os resultados.

        Returns:
            list: Uma lista de tuplas representando as linhas encontradas.
        """
        query = f"SELECT {columns} FROM {table_name}"
        params = []

        if condition:
            where_clauses = " AND ".join([f"{key} = ?" for key in condition.keys()])
            query += f" WHERE {where_clauses}"
            params.extend(condition.values())

        if order_by:
            query += f" ORDER BY {order_by}"

        try:
            self.cursor.execute(query, tuple(params))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao buscar dados: {e}")
            return []

    def update_data(self, table_name: str, data: dict, condition: dict) -> int:
        """
        Atualiza dados existentes em uma tabela.

        Args:
            table_name (str): O nome da tabela.
            data (dict): Os novos dados a serem atualizados.
            condition (dict): A condição para a cláusula WHERE.

        Returns:
            int: O número de linhas atualizadas.
        """
        set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
        where_clause = " AND ".join([f"{key} = ?" for key in condition.keys()])
        
        values = tuple(data.values()) + tuple(condition.values())
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause};"
        
        return self.execute_query(query, values)

    def delete_data(self, table_name: str, condition: dict) -> int:
        """
        Deleta dados de uma tabela.

        Args:
            table_name (str): O nome da tabela.
            condition (dict): A condição para a cláusula WHERE.

        Returns:
            int: O número de linhas deletadas.
        """
        where_clause = " AND ".join([f"{key} = ?" for key in condition.keys()])
        values = tuple(condition.values())
        query = f"DELETE FROM {table_name} WHERE {where_clause};"
        
        return self.execute_query(query, values)
    
    def __del__(self):
        """Garante que a conexão com o banco de dados seja fechada ao destruir a instância."""
        self.close()