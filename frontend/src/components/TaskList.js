import React, { useEffect, useState } from 'react';
import axios from 'axios';

const TaskList = () => {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    // Використовуємо ім'я контейнера бекенду для Docker network
    //axios.get('http://localhost:5000/api/tasks/public')
    axios.get('/api/tasks/public')
      .then(response => {
        setTasks(response.data);
      })
      .catch(error => {
        console.error('Сталася помилка під час отримання задач!', error);
      });
  }, []);

  return (
    <div>
      <h1>Список задач</h1>
      <ul>
        {tasks.map(task => (
          <li key={task.id}>{task.title} - {task.status}</li>
        ))}
      </ul>
    </div>
  );
};

export default TaskList;
