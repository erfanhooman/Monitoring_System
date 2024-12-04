"use client"

export default function Modal({ isOpen, onClose, data }) {
    if (!isOpen) return null;

    return (
        <div className="fixed top-0 left-0 w-screen h-screen flex justify-center items-center bg-[rgba(200,200,200,.7)]">
            <div className="flex flex-col p-6 bg-white rounded-lg shadow-lg w-3/4 h-3/4">
                <div className="overflow-y-auto flex-grow">
                    <h2 className="text-lg font-bold mb-4">History</h2>
                    <table className="table-auto w-full border-collapse border border-gray-300">
                        <thead>
                            <tr className="bg-gray-200">
                                <th className="border border-gray-300 px-4 py-2">Clock</th>
                                <th className="border border-gray-300 px-4 py-2">Value</th>
                                <th className="border border-gray-300 px-4 py-2">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {data.map((item, index) => (
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
