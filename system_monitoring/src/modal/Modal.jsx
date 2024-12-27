import {Line} from 'react-chartjs-2'; // Make sure to import Line from react-chartjs-2
import {
    CategoryScale,
    Chart as ChartJS,
    Legend,
    LinearScale,
    LineElement,
    PointElement,
    Title,
    Tooltip
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

export default function Modal({ isOpen, onClose, data }) {
    if (!isOpen) return null;

    const chartData = {
        labels: data.history.map((item) => item.clock),
        datasets: [
            {
                label: "Value Over Time",
                data: data.history.map((item) => item.value),
                borderColor: "rgba(75, 192, 192, 1)",
                backgroundColor: "rgba(75, 192, 192, 0.2)",
                fill: true,
                tension: 0.2,
            },
        ],
    };

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                type: "category",
                title: {
                    display: true,
                    text: "Time",
                },
            },
            y: {
                title: {
                    display: true,
                    text: "Value",
                },
                ticks: {
                    callback: function (value) {
                        return value.toFixed(2);
                    },
                    stepSize: 0.1,
                },
            },
        },
        plugins: {
            legend: {
                position: "top",
            },
        },
    };


    return (
        <div
            className="fixed z-50 top-0 left-0 w-screen h-screen flex justify-center items-center bg-[rgba(200,200,200,.7)]">
            <div className="flex flex-col p-6 bg-white rounded-lg shadow-lg w-3/4 h-3/4">
                <div className="mb-4">
                    <h2 className="text-lg font-bold">{data.name}</h2>
                    <p className="text-gray-600 mb-2">
                        <strong>Description: </strong>
                        {data.description}
                    </p>
                    {data.recommendation && (
                        <p className="text-gray-600">
                            <strong>Recommendation: </strong>
                            <p className="text-red-700">
                                {data.recommendation}
                            </p>

                        </p>
                    )}
                </div>

                <div className="mb-4 h-64">
                    <Line data={chartData} options={chartOptions}/>
                </div>

                <div className="overflow-y-auto flex-grow">
                    <h3 className="text-md font-bold mb-4">History</h3>
                    <table className="table-auto w-full border-collapse border border-gray-300">
                        <thead>
                        <tr className="bg-gray-200">
                            <th className="border border-gray-300 px-4 py-2">Clock</th>
                            <th className="border border-gray-300 px-4 py-2">Value</th>
                            <th className="border border-gray-300 px-4 py-2">Status</th>
                        </tr>
                        </thead>
                        <tbody>
                        {data.history.map((item, index) => (
                            <tr key={index} className="hover:bg-gray-100">
                                <td className="border border-gray-300 px-4 py-2">{item.clock}</td>
                                <td className="border border-gray-300 px-4 py-2">{item.value}</td>
                                <td className="border border-gray-300 px-4 py-2">{item.status}</td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>

                <button
                    onClick={onClose}
                    className="mt-4 px-4 py-2 bg-red-600 hover:bg-red-800 text-white rounded-lg self-end"
                >
                    Close
                </button>
            </div>
        </div>
    );
}