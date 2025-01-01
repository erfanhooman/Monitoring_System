import {useEffect, useState} from "react";
import {RefreshAccessToken, SettingsApi, UpdateSettingsApi} from "../../../api.js";

export default function Settings() {
    const [data, setData] = useState({
        zabbix_server_url: "",
        zabbix_username: "",
        zabbix_host_name: "",
        bundle_download: "", // URL for bundle download
    });
    const [loading, setLoading] = useState(true); // Track loading state
    const [error, setError] = useState(null); // Track general errors
    const [editing, setEditing] = useState(false); // Toggle edit mode
    const [formErrors, setFormErrors] = useState({}); // Validation errors

    const getData = () => {
        setLoading(true);
        setError(null);

        RefreshAccessToken().then(() => {
            SettingsApi()
                .then((res) => {
                    if (res.status === 403) {
                        setError("You do not have permission");
                    } else if (!res.data.success) {
                        setError(res.data.message);
                    } else {
                        setData(res.data.data);
                    }
                })
                .catch(() => {
                    setError("Failed to fetch settings. Please try again.");
                })
                .finally(() => {
                    setLoading(false);
                });
        });
    };

    const handleEditToggle = () => {
        setEditing(!editing);
        setFormErrors({});
    };

    const handleChange = (e) => {
        const {name, value} = e.target;
        setData((prevData) => ({...prevData, [name]: value}));
    };

    const handleSave = () => {
        setLoading(true);
        setError(null);

        RefreshAccessToken()
            .then(() => {
                UpdateSettingsApi(data)
                    .then((res) => {
                        if (res.data.success) {
                            setEditing(false);
                            setFormErrors({});
                            alert("Settings updated successfully!");
                        } else {
                            if (res.data.data) {
                                setFormErrors(res.data.data); // Field-specific errors
                            } else {
                                setError(res.data.message || "An error occurred.");
                            }
                        }
                    })
                    .catch(() => {
                        setError("Failed to save settings. Please try again.");
                    })
                    .finally(() => {
                        setLoading(false);
                    });
            })
            .catch(() => {
                setError("Failed to refresh access token. Please try again.");
                setLoading(false);
            });
    };

    useEffect(() => {
        getData();
    }, []); // Fetch data on component mount

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return (
            <div className="text-center text-lg text-red-600 mt-8">
                <p>{error}</p>
            </div>
        );
    }

    return (
        <div className="p-6 bg-gray-50 h-full">
            <h1 className="text-2xl font-semibold mb-6">Zabbix Settings</h1>

            {/* General Error Display */}
            {error && (
                <div className="text-red-600 text-center mb-4">
                    <p>{error}</p>
                </div>
            )}

            <div className="space-y-4">
                {Object.keys(data).map((key) => (
                    <div key={key} className="flex flex-col">
                        <label className="text-gray-700 font-medium">
                            {key.replace(/_/g, " ").toUpperCase()}
                        </label>
                        {key === "bundle_download" ? (
                            <a
                                href={data[key]}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-blue-500 underline"
                            >
                                Download the bundle
                            </a>
                        ) : editing ? (
                            <input
                                type="text"
                                name={key}
                                value={data[key]}
                                onChange={handleChange}
                                className="p-2 border rounded"
                            />
                        ) : (
                            <p className="text-gray-600">{data[key]}</p>
                        )}
                        {formErrors[key] && (
                            <p className="text-red-600 text-sm">{formErrors[key].join(", ")}</p>
                        )}
                    </div>
                ))}
            </div>

            <div className="mt-6 flex space-x-4">
                {editing ? (
                    <>
                        <button
                            onClick={handleSave}
                            className="px-4 py-2 bg-blue-500 text-white rounded"
                        >
                            Save
                        </button>
                        <button
                            onClick={handleEditToggle}
                            className="px-4 py-2 bg-gray-300 text-gray-700 rounded"
                        >
                            Cancel
                        </button>
                    </>
                ) : (
                    <button
                        onClick={handleEditToggle}
                        className="px-4 py-2 bg-blue-500 text-white rounded"
                    >
                        Edit
                    </button>
                )}
            </div>
        </div>
    );
}
