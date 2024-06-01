import LineChart from './components/LineChart';
import RefreshButton from './components/RefreshButton';
import { fetchDataAndSetData } from './utils';
import React, { useState, useEffect } from 'react';

const App = () => {
    const [data, setData] = useState({ labels: [], values: [] });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchDataAndSetData(setData, setLoading, setError);
    }, []);

    const refreshGraph = async () => {
        fetchDataAndSetData(setData, setLoading, setError);
    };

    return (
        <div className="Chart">
            <h2> Cost of borrowing for households for house purchase - Monthly</h2>
            <LineChart data={data} />
            <RefreshButton onClick={refreshGraph} />
        </div>
    );
};

export default App;

