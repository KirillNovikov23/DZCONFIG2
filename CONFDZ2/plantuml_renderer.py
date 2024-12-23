def generate_plantuml(graph):
    """
    Генерирует PlantUML код из графа зависимостей.
    """
    lines = ["@startuml", "title Dependency Graph"]

    for commit, parents in graph.items():
        for parent in parents:
            lines.append(f'  "{parent}" --> "{commit}"')

    lines.append("@enduml")
    return "\n".join(lines)
