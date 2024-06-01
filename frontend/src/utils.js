import { fetchData } from './backendServices';

export const fetchDataAndSetData = async (setData, setLoading, setError) => {
    setLoading(true);
    setError(null);
    try {
        const backendData = await fetchData();
        const chartData = {
            labels: backendData?.map(item => item.id),
            values: backendData?.map(item => item.value)
        };
        setData(chartData);
        setLoading(false);
    } catch (error) {
        setError("Failed to fetch data");
        setLoading(false);
    }
};
