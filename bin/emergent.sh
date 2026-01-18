#!/bin/bash

# UX Shell для системы Emergent (SPEC v1.7 draft)
# Данный скрипт обеспечивает интерфейс взаимодействия пользователя с ядром системы.
# Все команды транслируются напрямую в app.py без предварительной обработки или валидации на уровне shell.

# Функция для отображения статуса и фазы (UX-визуализация)
show_status() {
    echo "[Emergent Shell] Status: Active"
    # Фаза будет выведена самим приложением app.py при получении команды
}

# Основной цикл обработки команд
case "$1" in
    init|open|list|status|analyze|design|propose|execute|diff|apply|rollback)
        # Формирование строки команды из аргументов
        COMMAND_STRING="$*"
        
        # Передача команды в app.py через stdin и вывод результата
        # Скрипт ожидает, что app.py находится в родительской директории относительно bin/
        echo "$COMMAND_STRING" | python3 "$(dirname "$0")/../app.py"
        ;;
    *)
        echo "Usage: emergent <command> [args]"
        echo "Supported commands: init, open, list, status, analyze, design, propose, execute, diff, apply, rollback"
        exit 1
        ;;
esac
