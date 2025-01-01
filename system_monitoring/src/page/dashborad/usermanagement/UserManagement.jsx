import {useEffect, useState} from "react";
import {
    AddNewSubUsers,
    GetUserPermissionsApi,
    ModifyPermissionsApi,
    ModifyUserManagementDetailApi,
    RefreshAccessToken,
    UserManagementApi,
} from "../../../api.js";

export default function UserManagement() {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [formErrors, setFormErrors] = useState({});
    const [showModal, setShowModal] = useState(false);
    const [permissionsModal, setPermissionsModal] = useState({show: false, userId: null, permissions: []});
    const [newUser, setNewUser] = useState({
        username: "",
        password: "",
        confirmPassword: "",
    });
    const [successMessage, setSuccessMessage] = useState("");

    const availablePermissions = [
        "DASHBOARD",
        "CPU",
        "RAM",
        "DISK",
        "NETWORK",
        "GENERAL",
        "FS",
        "SETTINGS",
        "USER",
    ];

    // Get user list
    const getUsers = () => {
        setLoading(true);
        setError(null);

    RefreshAccessToken()
        .then(() => {
            UserManagementApi()
                .then((res) => {
                    console.log(res);

                    if (res.status === 403) {
                        setError("You do not have permission");
                    } else if (!res.data.success) {
                        setError(res.data.message);
                    } else {
                        setUsers(res.data.data.users);
                    }
                })
                .catch(() => {
                    console.log(res);
                    setError("Failed to fetch users. Please try again.");
                })
                .finally(() => {
                    setLoading(false);
                });
        })
    };

    // Handle activating/deactivating users
    const handleToggleActive = (user_id, currentStatus) => {
        const newStatus = !currentStatus;
        setLoading(true);

        RefreshAccessToken().then(() => {
            ModifyUserManagementDetailApi(user_id, newStatus)
                .then((res) => {
                    if (!res.data.success) {
                        setError(res.data.message);
                    } else {
                        setUsers((prevUsers) =>
                            prevUsers.map((user) =>
                                user.id === user_id ? {...user, active: newStatus} : user
                            )
                        );
                    }
                })
                .catch(() => {
                    setError("Failed to update user status. Please try again.");
                })
                .finally(() => {
                    setLoading(false);
                });
        });
    };

    // Add new user
    const handleAddNewUser = () => {
        if (newUser.password !== newUser.confirmPassword) {
            setError("Passwords do not match.");
            return;
        }

        if (!/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/.test(newUser.password)) {
            setError("Password must be at least 8 characters long and contain at least one letter and one number.");
            return;
        }

        setLoading(true);
        setError(null);

        AddNewSubUsers(newUser)
            .then((res) => {
                if (res.data.success) {
                    setSuccessMessage("User created successfully!");
                    setShowModal(false);
                    setNewUser({username: "", password: "", confirmPassword: ""}); // Reset form fields
                    getUsers();
                } else {
                    setFormErrors(res.data.data);
                }
            })
            .catch(() => {
                setError("Failed to add user. Please try again.");
            })
            .finally(() => {
                setLoading(false);
            });
    };

    const handleManagePermissions = (userId) => {
        setLoading(true);
        RefreshAccessToken().then(() => {
            GetUserPermissionsApi(userId)
                .then((res) => {
                    if (res.data.success) {
                        const userPermissions = res.data.data.permissions.map(
                            (permission) => permission.codename
                        );
                        setPermissionsModal({
                            show: true,
                            userId,
                            permissions: userPermissions,
                        });
                    } else {
                        setError(res.data.message);
                    }
                })
                .catch(() => {
                    setError("Failed to fetch user permissions. Please try again.");
                })
                .finally(() => {
                    setLoading(false);
                });
        });
    };

    const handlePermissionChange = (permission) => {
        setPermissionsModal((prev) => {
            const newPermissions = prev.permissions.includes(permission)
                ? prev.permissions.filter((perm) => perm !== permission)
                : [...prev.permissions, permission];
            return {...prev, permissions: newPermissions};
        });
    };

    const handleSavePermissions = () => {
        const {userId, permissions} = permissionsModal;
        setLoading(true);
        ModifyPermissionsApi({user_id: userId, permissions})
            .then((res) => {
                if (res.data.success) {
                    setSuccessMessage("Permissions updated successfully!");
                    setPermissionsModal({show: false, userId: null, permissions: []});
                } else {
                    setError(res.data.message);
                }
            })
            .catch(() => {
                setError("Failed to update permissions. Please try again.");
            })
            .finally(() => {
                setLoading(false);
            });
    };

    useEffect(() => {
        getUsers();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return (
            <div className="text-red-600 text-center">
                <p>{error}</p>
            </div>
        );
    }

    return (
        <div className="p-6 bg-gray-50 h-full">
            <h1 className="text-2xl font-semibold mb-6">User Management</h1>

            {/* Add New User Button */}
            <button
                onClick={() => setShowModal(true)}
                className="bg-blue-500 text-white px-4 py-2 rounded mb-6"
            >
                Add New User
            </button>

            {/* Success Message */}
            {successMessage && (
                <div className="bg-green-500 text-white p-4 mb-6 rounded">
                    <p>{successMessage}</p>
                </div>
            )}

            {/* User Table */}
            <div className="overflow-x-auto">
                <table className="min-w-full bg-white border border-gray-300">
                    <thead>
                    <tr>
                        <th className="py-3 px-4 border-b text-left">Username</th>
                        <th className="py-3 px-4 border-b text-left">Status</th>
                        <th className="py-3 px-4 border-b text-left">Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    {users.length === 0 ? (
                        <tr>
                            <td colSpan="3" className="text-center py-4">No users available.</td>
                        </tr>
                    ) : (
                        users.map((user) => (
                            <tr key={user.id}>
                                <td className="py-3 px-4 border-b">{user.user.username}</td>
                                <td className="py-3 px-4 border-b">
                                        <span
                                            className={`px-4 py-2 rounded ${user.active ? "bg-green-500" : "bg-red-600"} text-white`}
                                        >
                                            {user.active ? "Active" : "Inactive"}
                                        </span>
                                </td>
                                <td className="py-3 px-4 border-b">
                                    <button
                                        onClick={() => handleToggleActive(user.id, user.active)}
                                        className={`px-4 py-2 rounded ${user.active ? "bg-green-500" : "bg-red-600"} text-white`}
                                    >
                                        {user.active ? "Deactivate" : "Activate"}
                                    </button>
                                    <button
                                        onClick={() => handleManagePermissions(user.id)}
                                        className="ml-2 bg-blue-500 text-white px-4 py-2 rounded"
                                    >
                                        Manage Permissions
                                    </button>
                                </td>
                            </tr>
                        ))
                    )}
                    </tbody>
                </table>
            </div>

            {/* Modal for Adding New User */}
            {showModal && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
                    <div className="bg-white p-6 rounded-lg shadow-lg w-96">
                        <h2 className="text-xl font-semibold mb-4">Add New User</h2>

                        {/* Form for Adding User */}
                        <div className="mb-4">
                            <label htmlFor="username" className="block">Username</label>
                            <input
                                type="text"
                                id="username"
                                className="w-full px-4 py-2 border rounded"
                                value={newUser.username}
                                onChange={(e) => setNewUser({...newUser, username: e.target.value})}
                            />
                            {formErrors.username && (
                                <span className="text-red-500 text-sm">{formErrors.username[0]}</span>
                            )}
                        </div>

                        <div className="mb-4">
                            <label htmlFor="password" className="block">Password</label>
                            <input
                                type="password"
                                id="password"
                                className="w-full px-4 py-2 border rounded"
                                value={newUser.password}
                                onChange={(e) => setNewUser({...newUser, password: e.target.value})}
                            />
                            {formErrors.password && (
                                <span className="text-red-500 text-sm">{formErrors.password[0]}</span>
                            )}
                        </div>

                        <div className="mb-4">
                            <label htmlFor="confirmPassword" className="block">Confirm Password</label>
                            <input
                                type="password"
                                id="confirmPassword"
                                className="w-full px-4 py-2 border rounded"
                                value={newUser.confirmPassword}
                                onChange={(e) => setNewUser({...newUser, confirmPassword: e.target.value})}
                            />
                            {newUser.password !== newUser.confirmPassword && (
                                <span className="text-red-500 text-sm">Passwords do not match.</span>
                            )}
                        </div>

                        <div className="flex justify-between mt-4">
                            <button
                                onClick={() => setShowModal(false)}
                                className="bg-gray-500 text-white px-4 py-2 rounded"
                            >
                                Cancel
                            </button>
                            <button
                                onClick={handleAddNewUser}
                                className="bg-blue-500 text-white px-4 py-2 rounded"
                            >
                                Add User
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Permissions Modal */}
            {permissionsModal.show && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
                    <div className="bg-white p-6 rounded-lg shadow-lg w-96">
                        <h2 className="text-xl font-semibold mb-4">Manage Permissions</h2>

                        <div>
                            {availablePermissions.map((permission) => (
                                <div key={permission} className="mb-4">
                                    <label className="flex items-center">
                                        <input
                                            type="checkbox"
                                            checked={permissionsModal.permissions.includes(permission)}
                                            onChange={() => handlePermissionChange(permission)}
                                            className="mr-2"
                                        />
                                        {permission}
                                    </label>
                                </div>
                            ))}
                        </div>

                        <div className="flex justify-between mt-4">
                            <button
                                onClick={() => setPermissionsModal({show: false, userId: null, permissions: []})}
                                className="bg-gray-500 text-white px-4 py-2 rounded"
                            >
                                Cancel
                            </button>
                            <button
                                onClick={handleSavePermissions}
                                className="bg-blue-500 text-white px-4 py-2 rounded"
                            >
                                Save
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
