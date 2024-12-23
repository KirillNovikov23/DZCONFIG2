import os
import sys
import toml
import subprocess
from collections import defaultdict


def load_config(config_path):
    """
    Загружает конфигурацию из TOML-файла.
    """
    with open(config_path, 'r', encoding='utf-8') as file:
        return toml.load(file)


def get_commit_dependencies(repo_path):
    """
    Собирает зависимости между коммитами из git-истории.
    Возвращает словарь, где ключ — коммит, а значение — его родительские коммиты и сообщение.
    """
    os.chdir(repo_path)
    result = subprocess.run(
        ["git", "log", "--pretty=format:%H %P %s"],
        capture_output=True,
        text=True
    )

    if not result.stdout.strip():  # Проверка на пустой результат
        print("Ошибка: История коммитов пуста или git не настроен в указанном репозитории.")
        sys.exit(1)

    print("Git log output:")
    print(result.stdout)  # Вывод для отладки

    dependencies = defaultdict(list)
    for line in result.stdout.split('\n'):
        if not line.strip():  # Пропускаем пустые строки
            continue
        parts = line.split()
        if len(parts) < 2:  # Пропускаем строки с недостаточным количеством данных
            continue
        commit = parts[0]
        parents = parts[1:-1]  # Родительские коммиты
        message = ' '.join(parts[len(parents) + 1:])
        dependencies[commit] = {"parents": parents, "message": message}
    return dependencies


def generate_plantuml_code(dependencies):
    """
    Генерирует PlantUML-код на основе зависимостей коммитов.
    """
    plantuml_code = ["@startuml", "!define RECTANGLE #lightblue"]
    plantuml_code.append("title Git Commit Dependencies\n")

    for commit, data in dependencies.items():
        plantuml_code.append(f"{commit} : {data['message']}")
        for parent in data['parents']:
            plantuml_code.append(f"{parent} --> {commit}")

    plantuml_code.append("@enduml")
    return '\n'.join(plantuml_code)


def save_to_file(output_path, content):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(content)


def main():
    if len(sys.argv) != 2:
        print("Usage: python visualizer.py <path_to_config.toml>")
        sys.exit(1)

    config_path = sys.argv[1]
    config = load_config(config_path)

    repo_path = config.get("repo_path")
    output_path = config.get("output_path")

    if not repo_path:
        print("Error: 'repo_path' is missing in the config.toml file.")
        sys.exit(1)

    if not output_path:
        print("Error: 'output_path' is missing in the config.toml file.")
        sys.exit(1)

    dependencies = get_commit_dependencies(repo_path)
    plantuml_code = generate_plantuml_code(dependencies)
    save_to_file(output_path, plantuml_code)

    print("Generated PlantUML code:")
    print(plantuml_code)


if __name__ == "__main__":
    main()