import argparse
import json
import os
import datetime

def main():
    parser = argparse.ArgumentParser(
        prog='tasktracer',
        formatter_class=argparse.RawTextHelpFormatter,
        description="""
                            🚀 TASK TRACER CLI                      
        ------------------------------------------------------------          
        A simple command-line tool to manage your tasks efficiently.""")

    subparsers = parser.add_subparsers(dest='command')

    # Subparser for the "add" command
    parser_add = subparsers.add_parser('add', help='Add a new task')
    parser_add.add_argument('description', type=str, help='Description of the task')

    # Subparser for the "list" command
    parser_list = subparsers.add_parser('list', help='List all tasks')
    parser_list.add_argument('-c', '--completed', action='store_true', help='Show only completed tasks')
    parser_list.add_argument('-p', '--progress', action='store_true', help='Show tasks in progress')
    parser_list.add_argument('-t', '--todo', action='store_true', help='Show tasks to do')

    # Subparser for the "delete" command
    parser_delete = subparsers.add_parser('delete', help='Delete a task')
    parser_delete.add_argument('task_id', type=int, help='ID of the task to delete')

    # Subparser for the "update" command
    parser_update = subparsers.add_parser('update', help='Update a task')
    parser_update.add_argument('task_id', type=int, help='ID of the task to update')
    parser_update.add_argument('-d', '--description', type=str, help='New description for the task')
    parser_update.add_argument('-s', '--status', type=str, choices=['todo', 'in-progress', 'done'], help='New status (todo, in-progress, done)')

    args = parser.parse_args()

    if args.command == 'add':

        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current date and time
        tasks = json.load(open('list.json', 'r'))  # Load existing tasks from the JSON file
        new_id = max([t['id'] for t in tasks], default=0) + 1
        new_task = {
            "id": new_id,
            "description": args.description,
            "Status": "todo",
            "Created_at": date_time,
            "Updated_at": date_time
        }
        tasks.append(new_task)  # Add the new task to the list of tasks
        with open('list.json', 'w') as f:
            json.dump(tasks, f, indent=4)  # Save the updated tasks to the JSON file
        print(f"Task added: {args.description}")

    elif args.command == 'list':
        try:
            with open('list.json', 'r') as f:
                tasks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            tasks = []

        if not tasks:
            print("No tasks found.")
        else:
            # Filtered tasks based on the provided flags
            filtered_tasks = []
            for task in tasks:
                # If no specific filter is provided, include all tasks
                if not (args.completed or args.progress or args.todo):
                    filtered_tasks.append(task)
                elif args.completed and task['Status'] == 'done':
                    filtered_tasks.append(task)
                elif args.progress and task['Status'] == 'in-progress':
                    filtered_tasks.append(task)
                elif args.todo and task['Status'] == 'todo':
                    filtered_tasks.append(task)

            # Display the filtered tasks
            if not filtered_tasks:
                print("No tasks found for this filter.")
            else:
                print(f"{'ID':<5} {'Description':<25} {'Status':<15} {'Updated at'}")
                print("-" * 75)
                for task in filtered_tasks:
                    print(f"{task['id']:<5} {task['description']:<25} {task['Status']:<15} {task['Updated_at']}")
                    print("-" * 75)

    elif args.command == 'delete':
        tasks = json.load(open('list.json', 'r')) # Load existing tasks from the JSON file
        task_to_delete = next((task for task in tasks if task['id'] == args.task_id), None)
        if task_to_delete:
            tasks.remove(task_to_delete)
            with open('list.json', 'w') as f:
                json.dump(tasks, f, indent=4) # Save the updated tasks to the JSON file
            print("Task deleted.")
        else:
            print("Task not found.")

    elif args.command == "update":
        task_to_update = None
        with open('list.json', 'r') as f:
            tasks = json.load(f) # Load existing tasks from the JSON file
            for task in tasks:
                if task['id'] == args.task_id:
                    task_to_update = task
                    break

        if task_to_update:
            changed = False
            if args.description:
                task_to_update['description'] = args.description
                changed = True
            if args.status:
                task_to_update['Status'] = args.status
                changed = True
            if changed:
                task_to_update['Updated_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Update the "Updated_at" field with the current date and time
                with open('list.json', 'w') as f:
                    json.dump(tasks, f, indent=4) # Save the updated tasks to the JSON file
                print(f"Task {args.task_id} updated.")
            else:
                print("No changes to update. Use --description or --status to specify what to update.")
        else:
            print("Task not found.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()