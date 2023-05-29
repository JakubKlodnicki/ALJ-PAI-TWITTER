import logo from './logo.svg';
import './App.css';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import Login from "./components/login/Login";
import Register from "./components/register/Register";
import Home from "./components/home/Home";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
            <Route path="*" element={<Login/>}/>
            <Route path="/register" element={<Register/>}/>
            <Route path="/home" element={<Home/>}/>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
