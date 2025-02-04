import React from 'react';
import './SkyPlot.css';
import skyplotImage from '../splot.png'; // Import the image

const SkyPlot = () => {
  return (
    <div className="skyplot-container">
      <div className="new-box">
        <div className="label">Sky plot:</div>
        <img src={skyplotImage} alt="Sky plot" className="skyplot-image" />
      </div>
    </div>
  );
};

export default SkyPlot;