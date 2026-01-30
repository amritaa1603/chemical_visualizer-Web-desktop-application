import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import { Bar } from 'react-chartjs-2';
import { Upload, Activity, Clock, FileDown, Droplets, Thermometer, Gauge } from 'lucide-react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function App() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [history, setHistory] = useState([]);

  const fetchHistory = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8000/api/history/');
      setHistory(res.data);
    } catch (err) { console.error("History error"); }
  };

  useEffect(() => { fetchHistory(); }, []);

  const handleUpload = async () => {
    if (!file) return alert("Select CSV!");
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await axios.post('http://127.0.0.1:8000/api/upload/', formData);
      setData(res.data);
      fetchHistory();
    } catch (err) { alert("Check if Django is running!"); }
  };

  return (
    <div className="full-screen-container">
      {/* Top Banner */}
      <div className="header-banner">
        <h2 style={{display: 'flex', alignItems: 'center', gap: '12px', margin: 0}}>
          <Activity color="#2563eb" size={32} /> Chemical Equipment Visualizer
        </h2>
        <div style={{display: 'flex', gap: '10px'}}>
          <input type="file" onChange={(e) => setFile(e.target.files[0])} />
          <button className="btn-primary" onClick={handleUpload}>Process Data</button>
        </div>
      </div>

      {data && (
        <div className="stats-row">
          <div className="stat-card">
            <small style={{color: '#64748b', display: 'flex', alignItems: 'center', gap: '5px'}}>
              <Gauge size={14}/> Avg Pressure
            </small>
            <h3>{data.summary.avg_pressure.toFixed(2)} PSI</h3>
          </div>
          <div className="stat-card">
            <small style={{color: '#64748b', display: 'flex', alignItems: 'center', gap: '5px'}}>
              <Thermometer size={14}/> Avg Temp
            </small>
            <h3>{data.summary.avg_temperature.toFixed(2)} °C</h3>
          </div>
          <div className="stat-card">
            <small style={{color: '#64748b', display: 'flex', alignItems: 'center', gap: '5px'}}>
              <Droplets size={14}/> Avg Flowrate
            </small>
            <h3>{data.summary.avg_flowrate ? data.summary.avg_flowrate.toFixed(2) : "0.00"} m³/h</h3>
          </div>
          <div className="stat-card">
            <small style={{color: '#64748b'}}>Total Items</small>
            <h3>{data.summary.total_count} Units</h3>
          </div>
        </div>
      )}

      <div className="main-grid">
        <div className="card">
          <h4>Type Distribution Analysis</h4>
          <div style={{height: '400px'}}>
            {data ? (
              <Bar 
                data={{
                  labels: Object.keys(data.summary.type_distribution),
                  datasets: [{ label: 'Units', data: Object.values(data.summary.type_distribution), backgroundColor: '#2563eb', borderRadius: 8 }]
                }} 
                options={{ maintainAspectRatio: false }} 
              />
            ) : (
              <div style={{display:'flex', justifyContent:'center', alignItems:'center', height:'100%', color:'#94a3b8'}}>
                Upload a file to see visualization
              </div>
            )}
          </div>
        </div>

        <div className="card">
          <h4 style={{display: 'flex', alignItems: 'center', gap: '8px', borderBottom: '1px solid #f1f5f9', paddingBottom: '10px'}}>
            <Clock size={18} /> Recent Uploads
          </h4>
          <div className="history-list">
            {history.map((item, idx) => (
              <div key={idx} className="history-item">
                <div>
                  <div style={{fontWeight: '600', fontSize: '14px'}}>{item.file}</div>
                  <small style={{color: '#94a3b8'}}>{new Date(item.date).toLocaleTimeString()}</small>
                </div>
                {/* --- CHANGE MADE HERE --- */}
                <a href={`http://127.0.0.1:8000/api/report/${item.id}/`} target="_blank" rel="noreferrer">
                  <button className="btn-download"><FileDown size={14}/> PDF</button>
                </a>
                {/* ------------------------ */}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;