import axios from 'axios';
import { StatusCodes } from 'http-status-codes';

const baseURL = process.env.BACKEND_URL || 'http://localhost:8000';

const axiosInstance = axios.create({
    baseURL: baseURL + '/v1',
});

export const fetchData = async () => {
    try {
        const response = await axiosInstance.get('/data');
        return response.data;
    } catch (error) {
        console.error('Error fetching data:');
        //uncomment if you want to debug
        //throw error; 
    }
};

export const refreshData = async () => {
    try {
        const response = await axiosInstance.post('/refresh-data');
        if (response.status === StatusCodes.NO_CONTENT) {
            console.log('Database refreshed successfully');
        } else {
            console.error('Failed to refresh database');
        }
    } catch (error) {
        console.error('Error refreshing database:');
        //throw error;
    }
};
