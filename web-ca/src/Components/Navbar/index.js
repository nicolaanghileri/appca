import React from 'react';
import "./index.css";
import {NavLink as Link} from 'react-router-dom';
const Navbar = () => {
    return (
        <header>
            <h1 class="logo">Controllo Ambientale</h1>
            <nav>
                <ul class = "nav_links">
                    <li><Link to='/'>Home</Link></li>
                    <li><Link to='/fishino'></Link>Fishino</li>
                    <li><Link to='/contact'></Link>Contact</li>
                </ul>
            </nav>
            <Link to="login"class="cta"><button>Login</button></Link>
        </header>
    );
};

export default Navbar;