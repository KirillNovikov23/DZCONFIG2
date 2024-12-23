import subprocess

def build_commit_graph(repo_path):
    """
    Строит граф зависимостей коммитов из git-репозитория.
    Возвращает граф в виде словаря: {commit: [parent1, parent2, ...]}.
    """
    try:
        # Выполняем git log для получения коммитов и их родителей
        cmd = ["git", "-C", repo_path, "log", "--pretty=%H %P"]
        result = subprocess.check_output(cmd, text=True).strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Failed to execute git command") from e

    graph = {}
    for line in result.splitlines():
        parts = line.split()
        commit = parts[0]
        parents = parts[1:]
        graph[commit] = parents
    return graph
