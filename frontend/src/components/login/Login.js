import React, { useState } from 'react';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();

        // Wysyłanie żądania logowania do backendu
        const response = await fetch('http://127.0.0.1:5000/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        setMessage(data.message);

        if (data.success) {
            // Przekierowanie na inną stronę po zalogowaniu
            window.location.href = 'http://127.0.0.1:5000/home/';
        }
    };

    return (
        <div>
            <h1>Panel logowania</h1>
            {message && <p>{message}</p>}
            {/*<div className="links">*/}
            {/*    <a onDoubleClick={window.location.href = 'http://127.0.0.1:3000/login/'} className="active">Login</a>*/}
            {/*    <a onClick={window.location.href = 'http://127.0.0.1:3000/register/'}>Register</a>*/}
            {/*</div>*/}
            <form onSubmit={handleSubmit}>
                <label htmlFor="username">Nazwa użytkownika:</label>
                <input
                    type="text"
                    id="username"
                    name="username"
                    value={username}
                    onChange={(event) => setUsername(event.target.value)}
                    required
                /><br /><br />
                <label htmlFor="password">Hasło:</label>
                <input
                    type="password"
                    id="password"
                    name="password"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    required
                /><br /><br />
                <input type="submit" value="Zaloguj się" />
            </form>
        </div>
    );
};

export default Login;