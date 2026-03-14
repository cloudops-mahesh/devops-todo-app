import { useState, useEffect } from 'react';

const API = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [todos,   setTodos]   = useState([]);
  const [task,    setTask]    = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => { fetchTodos(); }, []);

  const fetchTodos = async () => {
    try {
      const res  = await fetch(`${API}/api/todos`);
      const data = await res.json();
      setTodos(data);
    } catch (err) {
      console.error('Error fetching todos:', err);
    } finally {
      setLoading(false);
    }
  };

  const addTodo = async (e) => {
    e.preventDefault();
    if (!task.trim()) return;
    await fetch(`${API}/api/todos`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ task })
    });
    setTask('');
    fetchTodos();
  };

  const toggleTodo = async (id) => {
    await fetch(`${API}/api/todos/${id}`, { method: 'PATCH' });
    fetchTodos();
  };

  const deleteTodo = async (id) => {
    await fetch(`${API}/api/todos/${id}`, { method: 'DELETE' });
    fetchTodos();
  };

  return (
    <div style={{
      maxWidth: 600,
      margin: '40px auto',
      fontFamily: 'sans-serif',
      padding: '0 20px'
    }}>

      {/* Header */}
      <div style={{
        background: '#1a6b3c',
        color: 'white',
        padding: '24px',
        borderRadius: '8px',
        marginBottom: '24px',
        textAlign: 'center'
      }}>
        <h1 style={{ margin: 0 }}>🚀 DevOps Todo App</h1>
        <p style={{ margin: '8px 0 0', opacity: 0.8 }}>
          Python FastAPI + React + Docker + AWS
        </p>
      </div>

      {/* Add Todo Form */}
      <form onSubmit={addTodo} style={{
        display: 'flex',
        gap: '8px',
        marginBottom: '24px'
      }}>
        <input
          value={task}
          onChange={e => setTask(e.target.value)}
          placeholder="Add a new task..."
          style={{
            flex: 1,
            padding: '12px 16px',
            fontSize: '15px',
            borderRadius: '6px',
            border: '2px solid #ddd',
            outline: 'none'
          }}
        />
        <button
          type="submit"
          style={{
            padding: '12px 24px',
            background: '#1a6b3c',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: 'pointer',
            fontSize: '15px',
            fontWeight: 'bold'
          }}
        >
          Add
        </button>
      </form>

      {/* Todo List */}
      {loading ? (
        <p style={{ textAlign: 'center', color: '#666' }}>Loading...</p>
      ) : todos.length === 0 ? (
        <p style={{ textAlign: 'center', color: '#666' }}>
          No todos yet! Add one above ☝️
        </p>
      ) : (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {todos.map(todo => (
            <li key={todo.id} style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              padding: '14px 16px',
              marginBottom: '8px',
              background: todo.completed ? '#f0faf4' : '#fff',
              borderRadius: '6px',
              border: `2px solid ${todo.completed ? '#1a6b3c' : '#eee'}`,
              transition: 'all 0.2s'
            }}>
              <span
                onClick={() => toggleTodo(todo.id)}
                style={{
                  cursor: 'pointer',
                  textDecoration: todo.completed ? 'line-through' : 'none',
                  color: todo.completed ? '#999' : '#111',
                  fontSize: '15px',
                  flex: 1
                }}
              >
                {todo.completed ? '✅' : '⬜'} {todo.task}
              </span>
              <button
                onClick={() => deleteTodo(todo.id)}
                style={{
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  color: '#c0392b',
                  fontSize: '20px',
                  padding: '0 4px'
                }}
              >
                ✕
              </button>
            </li>
          ))}
        </ul>
      )}

      {/* Footer */}
      <p style={{
        textAlign: 'center',
        color: '#999',
        fontSize: '13px',
        marginTop: '32px'
      }}>
        {todos.length} task{todos.length !== 1 ? 's' : ''} total
      </p>

    </div>
  );
}

export default App;