# -*- coding: utf-8 -*-
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson.objectid import ObjectId

class MongoDatabase:
    """
    Uma classe para encapsular as operações do MongoDB.
    Fornece uma interface simples para conectar, e realizar operações
    CRUD (Create, Read, Update, Delete) em coleções e documentos.
    """

    def __init__(self, db_name="meu_banco_mongo", uri="mongodb://localhost:27017/"):
        """
        Inicializa a classe MongoDatabase, conecta-se ao servidor e seleciona o banco de dados.

        Args:
            db_name (str): O nome do banco de dados a ser usado.
            uri (str): A string de conexão do MongoDB.
        """
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None
        self.connect()

    def connect(self):
        """Estabelece a conexão com o servidor MongoDB."""
        try:
            self.client = MongoClient(self.uri)
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            # print(f"Conexão com MongoDB estabelecida com sucesso. Usando o banco '{self.db_name}'.")
        except ConnectionFailure as e:
            print(f"Erro ao conectar ao MongoDB: {e}")
            self.client = None
            self.db = None

    def close(self):
        """Fecha a conexão com o servidor MongoDB."""
        if self.client:
            self.client.close()
            # print("Conexão com o MongoDB fechada.")

    def insert_document(self, collection_name, document):
        """
        Insere um novo documento em uma coleção.

        Args:
            collection_name (str): O nome da coleção.
            document (dict): O documento a ser inserido.

        Returns:
            ObjectId: O ID do documento inserido, ou None em caso de erro.
        """
        if not self.db:
            return None
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(document)
            return result.inserted_id
        except Exception as e:
            print(f"Erro ao inserir documento: {e}")
            return None

    def find_documents(self, collection_name, query={}):
        """
        Busca documentos em uma coleção com base em uma query.

        Args:
            collection_name (str): O nome da coleção.
            query (dict): O filtro da busca (padrão: {}, que retorna todos os documentos).

        Returns:
            list: Uma lista de documentos que correspondem à query.
        """
        if not self.db:
            return []
        try:
            collection = self.db[collection_name]
            # O retorno de find() é um cursor, então convertemos para uma lista
            return list(collection.find(query))
        except Exception as e:
            print(f"Erro ao buscar documentos: {e}")
            return []

    def find_one_document(self, collection_name, query={}):
        """
        Busca um único documento em uma coleção.

        Args:
            collection_name (str): O nome da coleção.
            query (dict): O filtro da busca.

        Returns:
            dict: O primeiro documento encontrado, ou None.
        """
        if not self.db:
            return None
        try:
            collection = self.db[collection_name]
            return collection.find_one(query)
        except Exception as e:
            print(f"Erro ao buscar um documento: {e}")
            return None

    def update_one_document(self, collection_name, query, new_values):
        """
        Atualiza um único documento que corresponde à query.

        Args:
            collection_name (str): O nome da coleção.
            query (dict): O filtro para encontrar o documento a ser atualizado.
            new_values (dict): Os campos e valores a serem atualizados,
                               geralmente dentro de um operador como '$set'.
                               Ex: {"$set": {"idade": 31}}

        Returns:
            int: O número de documentos modificados.
        """
        if not self.db:
            return 0
        try:
            collection = self.db[collection_name]
            result = collection.update_one(query, new_values)
            return result.modified_count
        except Exception as e:
            print(f"Erro ao atualizar documento: {e}")
            return 0

    def delete_one_document(self, collection_name, query):
        """
        Deleta um único documento que corresponde à query.

        Args:
            collection_name (str): O nome da coleção.
            query (dict): O filtro para encontrar o documento a ser deletado.

        Returns:
            int: O número de documentos deletados.
        """
        if not self.db:
            return 0
        try:
            collection = self.db[collection_name]
            result = collection.delete_one(query)
            return result.deleted_count
        except Exception as e:
            print(f"Erro ao deletar documento: {e}")
            return 0

    def delete_many_documents(self, collection_name, query):
        """
        Deleta múltiplos documentos que correspondem à query.

        Args:
            collection_name (str): O nome da coleção.
            query (dict): O filtro para encontrar os documentos a serem deletados.

        Returns:
            int: O número de documentos deletados.
        """
        if not self.db:
            return 0
        try:
            collection = self.db[collection_name]
            result = collection.delete_many(query)
            return result.deleted_count
        except Exception as e:
            print(f"Erro ao deletar múltiplos documentos: {e}")
            return 0

