import subprocess

if __name__ == "__main__":
    print("Running redis-cli in the redis docker container")

    # The example below *does not* require a redis/redis-cli installation
    # on the Client. However, if you're going to have that installed anyway,
    # you might consider replacing this with simply: redis-cli -h localhost -p 6380

    subprocess.check_call(
        [
            "docker",
            "compose",
            "run",
            "redis",
            "redis-cli",
            "-h",
            "redis",
        ]
    )
