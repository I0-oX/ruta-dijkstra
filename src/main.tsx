import React from 'react';
import ReactDOM from 'react-dom/client';

function App() {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Dijkstra Algorithm Visualizer</h1>
      <p className="text-gray-600">Enter your graph data to visualize the shortest path.</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
