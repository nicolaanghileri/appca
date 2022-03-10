import React from 'react';

import "./login.css";

const Login = () => {
    return (
        
        <div class="login">
            
            <h1 class="title">Login</h1> 
            <br></br>
            <br></br>
            <br></br>
            <br></br>   
            <div class="login-inputs">
                 
                <input type="text" placeholder="Username"/>
                <br></br>
                <br></br>
                <input type="password" placeholder="Password"/>
                <br></br>
                <br></br>
                <button class="btn">Let's go!</button>
            </div>
        </div>

    );
};

export default Login;