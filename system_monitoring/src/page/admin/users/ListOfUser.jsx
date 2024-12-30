import {useEffect, useState} from "react";
import {GetUserApi, ListOfUsersApi, RefreshAccessToken} from "../../../api.js";
import DetailsSvg from "../../../components/svg/DetailsSvg.jsx";
import Modal from "../../../modal/Modal.jsx";
import UserEditModal from "../../../modal/UserEditModal.jsx";

export default function ListOfUser() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [user, setUser] = useState({});
    const [openModal, setOpenModal] = useState(false);

    const getData = () => {
        setLoading(true);
        setError(null);

        RefreshAccessToken().then(() => {
            ListOfUsersApi()
                .then((res) => {
                    if (res.status === 403) {
                        setError("You do not have permission");
                    } else if (res.data.success !== true) {
                        setError(res.data.message);
                    } else {
                        setData(res.data.data.users);
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

    const userHandler = (userId) => {
        RefreshAccessToken().then(() => {
            GetUserApi(userId).then((res) => {
                setUser(res.data.data);
                setOpenModal(true);
            })
        })
    }

    const setModalClose = () => {
        setOpenModal(false);
    }

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
        <>
            { openModal && <UserEditModal data={user} isOpen={openModal} onClose={setModalClose} />}
            <div className="h-dvh flex items-center px-20">
                <table className="w-full border-8 p-8 rounded-4xl">
                    <thead className='rounded-4xl'>
                    <tr className="w-full p-4 border-2">
                        <th className="py-4">UserName</th>
                        <th className="py-4">Zabbix Hostname</th>
                        <th className="py-4">Zabbix Password</th>
                        <th className="py-4">Zabbix Server Url</th>
                        <th className="py-4">Zabbix Username</th>
                        <th className="py-4">Show Details</th>
                    </tr>
                    </thead>
                    <tbody>
                    {
                        data.map((user, index) => (
                            <tr key={index} className="w-full p-4 border-2 hover:bg-gray-100">
                                <td className="text-center py-4 select-none">{user.user.username}</td>
                                <td className="text-center py-4 select-none">{user?.zabbix_host_name}</td>
                                <td className="text-center py-4 select-none">{user?.zabbix_password}</td>
                                <td className="text-center py-4 select-none">{user?.zabbix_server_url}</td>
                                <td className="text-center py-4 select-none">{user?.zabbix_username}</td>
                                <td className="text-center py-4 select-none hover:cursor-pointer flex justify-center"
                                    onClick={() => userHandler(user.id)}><DetailsSvg/></td>
                            </tr>
                        ))
                    }
                    </tbody>
                </table>
            </div>
        </>

    );
}