import { useEffect, useState } from "react";
import { NetworkApi, RefreshAccessToken } from "../../api.js";
import { ActivationModal } from '../../modal/ActivationModal.jsx';

export default function Network() {
    const [data, setData] = useState({}); // Initialize as an empty object
    const [loading, setLoading] = useState(true); // Track loading state

    const getData = () => {
        setLoading(true); // Start loading when fetching data
        RefreshAccessToken().then(() => {
            NetworkApi()
                .then((res) => {
                    console.log(res);
                    if (res.data.success && res.data.data) {
                        setData(res.data.data); // Set the data (object with disks)
                    } else {
                        console.error('Error: Invalid data structure');
                    }
                })
                .catch((err) => {
                    console.error('Error fetching disk data:', err);
                })
                .finally(() => {
                    setLoading(false); // Set loading to false when data is fetched
                });
        });
    };

    useEffect(() => {
        getData();
    }, []); // Fetch data on component mount

    // Loading spinner component
    const LoadingSpinner = () => (
        <div className="flex justify-center items-center h-full">
            <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-blue-500"></div>
        </div>
    );

    // JSX rendering
    if (loading) {
        return <LoadingSpinner/>; // Show the spinner when loading
    }

    return (
        <div className="relative h-screen p-4 bg-gray-50 overflow-auto">
            {/* Check if data is available */}
            {Object.keys(data).length > 0 ? (
                Object.keys(data).map((diskKey) => (
                    <div key={diskKey} className="mb-8">
                        {/* Display Disk Name as a Header */}
                        <h1 className="text-2xl font-semibold text-gray-800 mb-4">{diskKey}</h1>

                        {/* Create a grid for the metrics, 3 columns layout */}
                        <div className="grid grid-cols-3 gap-6">
                            {data[diskKey].map((metric, index) => (
                                <div key={index} className="p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 border border-gray-200">
                                    <h2 className="text-lg font-semibold text-gray-700">{metric.name}</h2>
                                    <p className="text-gray-600">{metric.description}</p>
                                    <div className="flex items-center justify-between mt-4">
                                        <p className="text-gray-700 text-lg">{metric.value}</p>
                                        {metric.status && (
                                            <p
                                                className={`${
                                                    metric.status === "normal" ? "bg-green-500" : "bg-red-600"
                                                } text-sm px-3 py-1 text-white rounded-full`}
                                            >
                                                {metric.status}
                                            </p>
                                        )}
                                    </div>

                                    {/* Activation Modal or additional content */}
                                    <div className="flex justify-center items-center mt-4">
                                        <ActivationModal data={metric} />
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                ))
            ) : (
                <p className="text-center text-lg text-gray-500">No disk data available</p>
            )}
        </div>
    );
}
