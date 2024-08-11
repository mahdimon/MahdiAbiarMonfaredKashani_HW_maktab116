#!/bin/bash
FILE="todo_list.csv"

if [ ! -f "$FILE" ]; then
    echo "status,priority,name,date" >"$FILE"
fi

while true; do
    read -rp "

1 for adding new task
2 for marking a task as done
3 for deleting a task
4 for showing task list
5 for search
exit for exiting program: " command
    case "${command}" in
    1)
        read -rp "enter task name: " name
        name="${name//,/;}"
        read -rp "enter due date: " date
        date="${date//,/;}"
        read -rp "enter priority level from 1 to 3: " priority

        if [[ ! $priority =~ ^[1-3]$ ]]; then
            echo "priority must be an int form 1 to 3"
        else
            echo "todo,$priority,$name,$date" >>$FILE
        fi
        ;;
    2)
        read -rp "enter the task name: " name
        name="${name//,/;}"
        awk -F, -v target="$name" 'BEGIN {OFS=","} $3 == target {$1 = "done"} {print}' "$FILE" | sponge "$FILE"
        ;;
    3)
        read -rp "enter the task name: " name
        name="${name//,/;}"
        awk -F, -v target="$name" 'BEGIN {OFS=","} $3 == target {$1 = "deleted"} {print}' "$FILE" | sponge "$FILE"
        ;;
    4)
        read -rp "1 for showing todo list
2 for showing done list
3 for showing deleted list: " command
        case "${command}" in
        1)
            status="todo"
            ;;
        2)
            status="done"
            ;;
        3)
            status="deleted"
            ;;
        *)
            echo not a valid input
            ;;
        esac
        awk -F, -v status="$status" '$1 == status ' "$FILE"
        ;;
    5)
        read -rp "1 for searching in todo list
2 for searching in done list
3 for searching in deleted list: " command
        read -rp 'enter task name: ' name
        name="${name//,/;}"
        case "${command}" in
        1)
            status="todo"
            ;;
        2)
            status="done"
            ;;
        3)
            status="deleted"
            ;;
        *)
            echo not a valid input
            ;;
        esac
        awk -F, -v status="$status" -v name="$name" '$1 == status && $3 == name' "$FILE"
        ;;
    'exit')
        exit
        ;;
    *)
        echo "not a valid input"
        ;;
    esac

done
