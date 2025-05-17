from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# Carrega as credenciais do .env
load_dotenv()
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

# Classe para gerenciar o banco
class MovieCRUD:
    def __init__(self):
        self.driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    def close(self):
        self.driver.close()

    def create(self, title, year):
        with self.driver.session() as session:
            session.run("CREATE (:Movie {title: $title, year: $year})", title=title, year=year)
            print(f"Filme '{title}' criado!")

    def read(self):
        with self.driver.session() as session:
            result = session.run("MATCH (m:Movie) RETURN m.title, m.year")
            return [(record["m.title"], record["m.year"]) for record in result]

    def update(self, title, new_title, year):
        with self.driver.session() as session:
            session.run(
                "MATCH (m:Movie {title: $title}) SET m.title = $new_title, m.year = $year",
                title=title, new_title=new_title, year=year
            )
            print(f"Filme '{title}' atualizado!")

    def delete(self, title):
        with self.driver.session() as session:
            session.run("MATCH (m:Movie {title: $title}) DELETE m", title=title)
            print(f"Filme '{title}' deletado!")

# Menu interativo
def main():
    crud = MovieCRUD()
    while True:
        print("\n=== Menu de Filmes ===")
        print("1. Criar filme")
        print("2. Listar filmes")
        print("3. Atualizar filme")
        print("4. Deletar filme")
        print("5. Sair")
        choice = input("Escolha (1-5): ")

        if choice == "1":
            title = input("Título: ")
            year = input("Ano: ")
            crud.create(title, year)

        elif choice == "2":
            movies = crud.read()
            if movies:
                for title, year in movies:
                    print(f"Título: {title}, Ano: {year}")
            else:
                print("Nenhum filme encontrado.")

        elif choice == "3":
            title = input("Título atual: ")
            new_title = input("Novo título: ")
            year = input("Novo ano: ")
            crud.update(title, new_title, year)

        elif choice == "4":
            title = input("Título para deletar: ")
            crud.delete(title)

        elif choice == "5":
            print("Saindo...")
            crud.close()
            break

        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()