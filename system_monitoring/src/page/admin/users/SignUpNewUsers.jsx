import { useState } from "react";
import { SignUpUserApi, RefreshAccessToken } from "../../../api.js";

export default function SignUpNewUsers() {
    const [formData, setFormData] = useState({
        username: "",
        password: "",
        confirmPassword: "",
    });
    const [errors, setErrors] = useState({});
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");

    const passwordValidation = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
        setErrors({ ...errors, [name]: "" }); // Clear error when typing
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        setMessage("");
        setErrors({});
        setLoading(true);

        // Validate password
        if (!passwordValidation.test(formData.password)) {
            setErrors((prevErrors) => ({
                ...prevErrors,
                password: "Password must be at least 8 characters long and include both letters and numbers.",
            }));
            setLoading(false);
            return;
        }

        // Check if passwords match
        if (formData.password !== formData.confirmPassword) {
            setErrors((prevErrors) => ({
                ...prevErrors,
                confirmPassword: "Passwords do not match.",
            }));
            setLoading(false);
            return;
        }

        // Proceed with the sign-up API call if validation passes
        RefreshAccessToken().then(() => {
            SignUpUserApi(formData)
                .then((res) => {
                    const { success, message, data } = res.data;

                    if (success) {
                        setMessage("User signed up successfully!");
                        setFormData({ username: "", password: "", confirmPassword: "" }); // Reset form
                    } else {
                        setErrors(data || {});
                        setMessage(message || "Sign-up failed.");
                    }
                })
                .catch((err) => {
                    console.error("Error signing up user:", err);
                    setMessage("Server error. Please try again later.");
                })
                .finally(() => {
                    setLoading(false);
                });
        });
    };

    const LoadingSpinner = () => (
        <div className="flex justify-center items-center h-full">
            <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-blue-500"></div>
        </div>
    );

    return (
        <div className="flex justify-center items-center min-h-screen">
            <div className="w-full max-w-sm p-6 bg-white rounded-xl shadow-xl">
                <h2 className="text-2xl font-semibold text-center mb-4">Sign Up New User</h2>

                {message && (
                    <p className={`mb-4 ${message.includes("success") ? "text-green-500" : "text-red-500"}`}>
                        {message}
                    </p>
                )}

                {loading && <LoadingSpinner />}

                <form onSubmit={handleSubmit} className="space-y-4">
                    {/* Username */}
                    <div>
                        <label className="block text-sm font-medium mb-1">Username</label>
                        <input
                            type="text"
                            name="username"
                            value={formData.username}
                            onChange={handleChange}
                            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                        {errors.username && (
                            <p className="text-red-500 text-sm mt-1">{errors.username[0]}</p>
                        )}
                    </div>

                    {/* Password */}
                    <div>
                        <label className="block text-sm font-medium mb-1">Password</label>
                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                        {errors.password && (
                            <p className="text-red-500 text-sm mt-1">{errors.password}</p>
                        )}
                    </div>

                    {/* Confirm Password */}
                    <div>
                        <label className="block text-sm font-medium mb-1">Confirm Password</label>
                        <input
                            type="password"
                            name="confirmPassword"
                            value={formData.confirmPassword}
                            onChange={handleChange}
                            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                        {errors.confirmPassword && (
                            <p className="text-red-500 text-sm mt-1">{errors.confirmPassword}</p>
                        )}
                    </div>

                    <button
                        type="submit"
                        className="w-full py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        disabled={loading}
                    >
                        Sign Up
                    </button>
                </form>
            </div>
        </div>
    );
}
