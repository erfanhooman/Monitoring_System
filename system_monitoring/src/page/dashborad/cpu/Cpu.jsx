import {useEffect, useState} from "react";
import {CpuApi, RefreshAccessToken} from "../../../api.js";
import {ActivationModal} from '../../../modal/ActivationModal.jsx';

export default function Cpu() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const getData = () => {
        setLoading(true);
        setError(null);

        RefreshAccessToken().then(() => {
            CpuApi()
                .then((res) => {
                    if (res.status === 403) {
                        setError("You do not have permission");
                    } else if (res.data.success !== true) {
                        setError(res.data.message);
                    } else {
                        setData(res.data.data);
                    }
                })
                .catch((err) => {
                    console.error("Error fetching CPU data:", err);
                    setError("Server is down. Please wait and try again.");
                })
                .finally(() => {
                    setLoading(false);
                });
        });
    };

    useEffect(() => {
        getData();
    }, []);

    const LoadingSpinner = () => (
        <div className="flex justify-center items-center h-full">
            <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-blue-500"></div>
        </div>
    );

    if (loading) {
        return <LoadingSpinner/>;
    }

    if (error) {
        return (
            <div className="text-center text-lg text-red-600 mt-8">
                <p>{error}</p>
            </div>
        );
    }

    return (
        <div className="relative h-screen">
            <div
                className="relative grid grid-cols-3 gap-6 p-4 bg-gray-50 h-screen overflow-auto cursor-default select-none">
                {data.map((item, index) => (
                    <div
                        className="relative p-6 bg-white rounded-lg flex flex-col justify-between gap-4 shadow-md hover:shadow-lg transition-shadow duration-300 border border-gray-200"
                        key={index}
                    >
                        <h1 className="text-xl font-semibold text-gray-800 cursor-default">{item.name}</h1>

                        <div className="flex items-center justify-between">
                            <p className="text-gray-700 text-lg">{item.value}</p>
                            {item.status && (
                                <p
                                    className={`${
                                        item.status === "normal" ? "bg-green-500" : "bg-red-600"
                                    } text-sm px-3 py-1 text-white rounded-full`}
                                >
                                    {item.status}
                                </p>
                            )}
                        </div>
                        <div className="flex justify-center items-center">
                            <ActivationModal data={item}/>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
