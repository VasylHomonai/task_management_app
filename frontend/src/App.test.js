import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';
import axios from 'axios';


// Мокаємо axios
jest.mock('axios');

describe('App component', () => {

  test('renders TaskList heading', async () => {
    axios.get.mockResolvedValue({ data: [] });

    render(<App />);
    const headingElement = await screen.findByText(/Список задач/i);
    expect(headingElement).toBeInTheDocument();
  });

  test('renders tasks from API', async () => {
    const tasks = [
      { id: 1, title: 'Перша задача', status: 'невиконана' },
      { id: 2, title: 'Друга задача', status: 'виконана' }
    ];
    axios.get.mockResolvedValueOnce({ data: tasks });

    render(<App />);

    for (const task of tasks) {
      await waitFor(() => {
        expect(screen.getByText(`${task.title} - ${task.status}`)).toBeInTheDocument();
      });
    }
  });

});
