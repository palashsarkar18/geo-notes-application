import React from 'react';
import './App.css';
import MapComponent from './components/MapComponent';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Geo Notes POIs</h1>
      </header>
      <MapComponent />
    </div>
  );
}

export default App;
