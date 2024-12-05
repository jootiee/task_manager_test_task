import os
from typing import Optional, List

from task_manager import Task, TaskManager
from task_manager.utils import *
from messages import *


def select_task(manager: TaskManager) -> Task:
    tasks = manager.get_tasks()
    task_numbers = set()
    for task in tasks:
        title = task.to_dict()['title']
        id = task.to_dict()['id']
        task_numbers.add(id)
        print("Название задачи:", title)
        print("Номер задачи:", id)
        print()
    while True:
        choice = input(EDIT_TASK_MESSAGE)
        if choice.isdigit():
            if int(choice) in task_numbers:
                break
        print(EDIT_TASK_ERROR_MESSAGE)
        input()

    return tasks[int(choice) - 1]


def prompt_features(features: Optional[dict] = dict()) -> dict:
    for feature in FEATURES.keys():
            if feature in ('id', 'status'):
                continue

            while True:
                print(ADD_TASK_MESSAGES[feature])
                choice = input()
                match feature:
                    case 'due_date':
                        try:
                            features[feature] = validate_date(choice)
                            break
                        except ValueError:
                            print(DATE_WRONG_INPUT_MESSAGE)
                            continue

                    case 'priority':
                        if not choice.isdigit():
                            print(PRIORITY_WRONG_INPUT_MESSAGE)
                            continue
                        if int(choice) < 1 | 3 < int(choice):
                            print(PRIORITY_WRONG_INPUT_MESSAGE)
                            continue
                        else:
                            features[feature] = list(Priority)[int(choice) - 1]
                            break

                    case _:
                        if choice == '':
                            print(FEATURE_EMPTY_MESSAGE.format(feature.lower()))
                            continue
                        else:
                            features[feature] = choice
                            break
    return features


def create_task(manager: TaskManager) -> Task:
    features = {'status': Status.UNCOMPLETED}
    features = prompt_features(features)
    task = manager.add_task(**features)
    return task


def edit_task(manager: TaskManager, task: Task) -> Task:
        features = prompt_features(task.to_dict())
        manager.edit_task(task, features)
        return manager.get_task_by_id(task.id)


def print_tasks(tasks: List[Task]) -> None:
    for task in tasks:
        print('-' * 30)
        print(VIEW_TASK_MESSAGE.format(*task.to_dict(pretty=True).values()))


def main():
    manager = TaskManager()
    while True:
        os.system('cls' if os.name=='nt' else 'clear')
        print(MAIN_MENU_MESSAGE)

        choice = input("Ваш выбор: ")
        match choice:
            case "1":
                tasks = manager.get_tasks()
                print_tasks(tasks)
            case "2":
                create_task(manager)
                manager.save_tasks()
            case "3":
                task = select_task(manager)
                print(EDIT_TASK_CHOICE_MESSAGE)
                while True:
                    choice = input("Ваш выбор: ")
                    if choice.isdigit():
                        if int(choice) in (1, 2):
                            choice = int(choice)
                            break
                    print(EDIT_TASK_WRONG_CHOICE_MESSAGE)
                match choice:
                    case 1:
                        res = manager.mark_task_as_completed(task)
                        if res is False:
                            print(EDIT_COMPLETED_TASK_ERROR_MESSAGE)
                        else:
                            print(TASK_COMPLETION_MESSAGE.format(choice))
                    case 2:
                        manager.edit_task(task)
                manager.save_tasks()
            case "4":
                task = select_task(manager)
                manager.delete_task(task)
                manager.save_tasks()
            case "5":
                while True:
                    choice = input("Поиск по названию и описанию задач: ")
                    if choice:
                        break
                    print(ERROR_EMPTY_MESSAGE)
                tasks = manager.search_tasks(choice)
                print_tasks(tasks)
            case "6":
                print("Выход.")
                break
            case _:
                print(MENU_WRONG_INPUT_MESSAGE)
        input(MENU_PROCEED_MESSAGE)


if __name__ == "__main__":
    main()
