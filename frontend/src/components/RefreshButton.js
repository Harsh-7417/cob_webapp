import React from 'react';
import { refreshData } from '../backendServices';

const RefreshButton = ({ onClick }) => {

    const refreshDataSteps = async () => {
        await refreshData();
        onClick();
    };
    return (
        <button className="refresh-button" onClick={refreshDataSteps}>Refresh Data</button>
    );
};

export default RefreshButton;
