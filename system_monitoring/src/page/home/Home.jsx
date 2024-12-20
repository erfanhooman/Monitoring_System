import { useEffect, useState } from "react";
import { DashboardApi, RefreshAccessToken } from "../../api.js";
import { Link } from "react-router-dom"; // Import Link for routing

export default function Dashboard() {
  const [data, setData] = useState(null); // Use `null` initially to check if data is loaded
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const getData = () => {
    setLoading(true);
    setError(null);

    RefreshAccessToken().then(() => {
      DashboardApi()
        .then((res) => {
          if (res.data.success) {
            setData(res.data.data); // Populate the data
          } else {
            setError(res.data.message);
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
    return <LoadingSpinner />; // Display loading spinner while fetching data
  }

  if (error) {
    return <div>{error}</div>; // Display error if there's an issue
  }

  if (!data) {
    return <div>No data available</div>; // In case of no data after loading
  }

  return (
    <div className="p-8 bg-gray-100 min-h-screen">
      {/* Apply space-y here for consistent spacing between rows */}
      <div className="space-y-12">
        {/* CPU Row */}
        {data.CPU && (
          <Link to="/dashboard/cpu">
            <div className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300 ease-in-out">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">CPU</h2>
              <p className="text-gray-600 mb-4">{data.CPU.description}</p>
              <div className="flex justify-between text-lg">
                <span className="font-medium text-gray-700">Last Value</span>
                <span className="text-gray-900">{data.CPU.last_value}</span>
              </div>
              <div className="flex justify-between text-lg mt-2">
                <span className="font-medium text-gray-700">Previous Value</span>
                <span className="text-gray-500">{data.CPU.pre_value}</span>
              </div>
            </div>
          </Link>
        )}

        {/* RAM Row */}
        {data.RAM && (
          <Link to="/dashboard/ram">
            <div className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300 ease-in-out">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">RAM</h2>
              <p className="text-gray-600 mb-4">{data.RAM.description}</p>
              <div className="flex justify-between text-lg">
                <span className="font-medium text-gray-700">Last Value</span>
                <span className="text-gray-900">{data.RAM.last_value}</span>
              </div>
              <div className="flex justify-between text-lg mt-2">
                <span className="font-medium text-gray-700">Previous Value</span>
                <span className="text-gray-500">{data.RAM.pre_value}</span>
              </div>
            </div>
          </Link>
        )}

        {/* Disk Row */}
        {data.Disk && (
          <Link to="/dashboard/disk">
            <div className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300 ease-in-out">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">Disk</h2>
              <p className="text-gray-600 mb-4">{data.Disk.description}</p>
              <div className="flex justify-between text-lg">
                <span className="font-medium text-gray-700">Last Value</span>
                <span className="text-gray-900">{data.Disk.last_value}</span>
              </div>
              <div className="flex justify-between text-lg mt-2">
                <span className="font-medium text-gray-700">Previous Value</span>
                <span className="text-gray-500">{data.Disk.pre_value}</span>
              </div>
            </div>
          </Link>
        )}
      </div>
    </div>
  );
}
