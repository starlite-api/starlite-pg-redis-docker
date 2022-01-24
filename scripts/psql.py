import subprocess

if __name__ == "__main__":
    print("Running PSQL in the postgres docker container")

    # Get credentials from the postgres container
    raw_env_vars = subprocess.check_output("docker compose exec postgres env", shell=True).decode().strip()
    env_vars = {i.split("=")[0]: i.split("=")[1] for i in raw_env_vars.split("\n")}

    # The example below *does not* require a postgres/psql installation
    # on the Client. However, if you're going to have that installed anyway,
    # you might consider replacing this with simply: PGPASSWORD={pw} psql -h localhost -p 5433 -U {user} {db}

    subprocess.check_call(
        [
            "docker",
            "compose",
            "run",
            "--env",
            f'PGPASSWORD={env_vars["POSTGRES_PASSWORD"]}',
            "postgres",
            "psql",
            "--host=postgres",
            f'--username={env_vars["POSTGRES_USER"]}',
            f'{env_vars["POSTGRES_DB"]}',
        ]
    )
