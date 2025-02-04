import React from 'react';
import './OutputBox.css'; // Use a separate CSS file

const OutputBox = () => {
  return (
    <div className="output-box-container">
      <div className="output-box">
        <div className="label">Latitude Longitude:</div>
        <div>13.7563° N, 100.5018° E</div>
        <div className="label">Sat In View:</div>
        <div>12</div>
        <div className="label">PDOP:</div>
        <div>1.5</div>
        <div className="label">RAIM Avaliable Mode:</div>
        <div>Mode1</div>
        <div>Mode2</div>
        <div>Mode3</div>
      </div>
    </div>
  );
};

export default OutputBox;