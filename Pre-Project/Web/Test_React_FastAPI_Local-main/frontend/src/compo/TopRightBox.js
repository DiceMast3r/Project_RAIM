import React, { useState } from 'react';
import './TopRightBox.css';
import OutputBox from './OutputBox'; // Import the new OutputBox component

const TopRightBox = () => {
  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');
  const [departureTime, setDepartureTime] = useState(new Date().toISOString().slice(0, 16));

  const handleRequestRoute = () => {
    // Add your request route logic here
    console.log('Requesting route from', origin, 'to', destination, 'at', departureTime);
  };

  const handleClearRoute = () => {
    setOrigin('');
    setDestination('');
    setDepartureTime(new Date().toISOString().slice(0, 16));
  };

  const handleFas = () => {
    console.log('Fas button clicked');
  };

  const handleFf = () => {
    console.log('Ff button clicked');
  };

  return (
    <div className="container">
      <div className="top-right-box">
        <div className="label">Departure Airport (ICAO CODE):</div>
        <input
          type="text"
          placeholder="Enter your Origin"
          className="input-box"
          value={origin}
          onChange={(e) => setOrigin(e.target.value)}
        />
        <div className="label">Destination Airport (ICAO CODE):</div>
        <input
          type="text"
          placeholder="Enter your Destination"
          className="input-box"
          value={destination}
          onChange={(e) => setDestination(e.target.value)}
        />
        <div className="label">Departure Date and Time:</div>
        <input
          type="datetime-local"
          className="input-box"
          value={departureTime}
          onChange={(e) => setDepartureTime(e.target.value)}
        />
        <button className="request-route-button" onClick={handleRequestRoute}>Request Route</button>
        <button className="clear-route-button" onClick={handleClearRoute}>Clear Route and Waypoint</button>
        <button className="fas-button" onClick={handleFas}>Fetch Route from Database</button>
        <button className="ff-button" onClick={handleFf}>Fetch GPS TLE Data</button>
      </div>
    </div>
  );
};

export default TopRightBox;