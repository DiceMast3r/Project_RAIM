import React, { useState } from 'react';
import './Navbar.css'; // นำเข้าไฟล์ CSS
import './OutputBox.css';
import './SkyPlot.css';
import skyplotImage from '../splot.png'; // Import the image
import './TopRightBox.css';
import OutputBox from './OutputBox'; // Import the new OutputBox component
import Skyplot from './SkyPlot'; // Import the Skyplot component
import TopRightBox from './TopRightBox'; // Import the TopRightBox component

const Navbar = () => {
    
    const [activeComponents, setActiveComponents] = useState([]);

    const handleClick = (event, target) => {
        event.preventDefault();
        console.log(`Navigating to ${target}`);
        setActiveComponents(prev => 
            prev.includes(target) ? prev.filter(comp => comp !== target) : [...prev, target]
        );
    };

    return (
       <header className="header">
            <div className="logo-and-nav">
                <a href="/" className="logo">RAIM Prediction System | KMITL</a>
                <nav className="navbar">
                    <a href="/" onClick={(e) => handleClick(e, 'Position&PDOP')}>Position&PDOP</a>
                    <a href="/" onClick={(e) => handleClick(e, 'Skyplot')}>Skyplot</a>
                    <a href="/" onClick={(e) => handleClick(e, 'Destination')}>Destination</a>
                </nav>
            </div>

            {activeComponents.includes('Position&PDOP') && <OutputBox />}
            {activeComponents.includes('Skyplot') && <Skyplot />}
            {activeComponents.includes('Destination') && <TopRightBox />}
       </header>
    )
};

export default Navbar;