import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import './App.css';
import Login from './components/Login';
import Register from './components/Register';
import MapComponent from './components/MapComponent';
import LandingPage from './components/LandingPage';

const PrivateRoute = ({ component: Component }) => {
  return (
    localStorage.getItem('token') ? (
      <Component />
    ) : (
      <Navigate to="/login" />
    )
  );
};

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Geo Notes POIs</h1>
        </header>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/map" element={<PrivateRoute component={MapComponent} />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
