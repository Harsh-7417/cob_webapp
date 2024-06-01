import React, { useRef } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const LineChart = ({ data }) => {
    const chartRef = useRef(null);

    const chartData = {
        labels: data.labels,
        datasets: [
            {
                label: 'Percent per annum',
                data: data.values,
                fill: false,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                tension: 0.1,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,  // Ensures the chart resizes to fit its container
    };

    return (
        <div style={{ position: 'relative', height: '400px', width: '100%' }}>
            <Line ref={chartRef} data={chartData} options={options} />
        </div>
    );
};

export default LineChart;
