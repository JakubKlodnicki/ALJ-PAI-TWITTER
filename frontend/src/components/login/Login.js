import React from 'react'
import './Login.scss'
const Login = () => {
    return (
        <div>
            <div className="login">
                <h1>Login</h1>
                <div className="links">
                    <a href="{{ url_for('login') }}" className="active">Login</a>
                    <a href="{{ url_for('register') }}">Register</a>
                </div>
                <form action="{{ url_for('login') }}" method="post">
                    <label htmlFor="username">
                        <i className="fas fa-user"></i>
                    </label>
                    <input type="text" name="username" placeholder="Username" id="username" required/>
                    <label htmlFor="password">
                        <i className="fas fa-lock"></i>
                    </label>
                    <input type="password" name="password" placeholder="Password" id="password" required/>
                    <div className="msg"></div>
                    <a href="">Reset Password</a>
                    <input type="submit" value="Login"/>
                </form>
            </div>
        </div>
    )
}
export default Login
