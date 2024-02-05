import timeit

import psycopg2


def execute_vacuum_commands():
    connection = psycopg2.connect(
        dbname="dbativo",
        user="postgres",
        password="postgres",
        host="satelite.ativo247.com.br",
        port="5432"
    )

    cursor = connection.cursor()

    try:
        # Desativa o modo autocommit para permitir a execução de comandos fora de transações
        connection.autocommit = True

        # Loop sobre as tabelas e execute o VACUUM para cada uma
        for table_name in get_table_names(cursor):
            vacuum_command = f"VACUUM FULL VERBOSE {table_name}"
            cursor.execute(vacuum_command)
            print(f"Executed VACUUM FULL VERBOSE IN {table_name}")
    except Exception as e:
        print(f"Erro durante a execução do VACUUM: {e}")
    finally:
        # Restaura o modo autocommit para seu estado original
        connection.autocommit = False
        cursor.close()
        connection.close()


def get_table_names(cursor):
    # Consulta para obter os nomes das tabelas no esquema 'public'
    query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]


def time_function(function):
    duration_minute_function = timeit.timeit(function, number=1)
    elapsed_time = duration_minute_function / 60.0
    print(f"Tempo decorrido: {elapsed_time:.2f} minutos")


if __name__ == "__main__":
    execute_vacuum_commands()
    time_function(execute_vacuum_commands)
