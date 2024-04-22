from typing import List, Optional
from pydantic import BaseModel
from flask import Flask, jsonify, request

app = Flask(__name__)

# Модель данных для задачи
class Task(BaseModel):
    id: int
    title: str
    description: str
    status: bool

# Пример списка задач
tasks = [
    Task(id=1, title="Task 1", description="Description 1", status=False),
    Task(id=2, title="Task 2", description="Description 2", status=True),
]

# Конечная точка для получения списка всех задач
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# Конечная точка для получения задачи по ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task.id == task_id), None)
    if task:
        return jsonify(task)
    else:
        return jsonify({"error": "Task not found"}), 404

# Конечная точка для создания новой задачи
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    try:
        task = Task(**data)
        tasks.append(task)
        return jsonify(task), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Конечная точка для обновления задачи по ID
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    try:
        task_index = next((index for index, task in enumerate(tasks) if task.id == task_id), None)
        if task_index is not None:
            tasks[task_index] = Task(**data)
            return jsonify(tasks[task_index])
        else:
            return jsonify({"error": "Task not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Конечная точка для удаления задачи по ID
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    return jsonify({"message": "Task deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
