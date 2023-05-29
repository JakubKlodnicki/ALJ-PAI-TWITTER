import React, { useState } from 'react';

const Register = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [msg, setMsg] = useState('');

    const handleRegister = async (e) => {
        e.preventDefault();

        if (!username || !password || !email) {
            setMsg('Please fill out the form!');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:5000/register/', {
                username,
                password,
                email,
            });

            setMsg(response.data);
        } catch (error) {
            console.log(error);
            setMsg('Registration failed.');
        }
    };

    return (
        <div>
            <h1>Register</h1>
            <form onSubmit={handleRegister}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <button type="submit">Register</button>
            </form>
            {msg && <p>{msg}</p>}
        </div>
    );
};

export default Register;
