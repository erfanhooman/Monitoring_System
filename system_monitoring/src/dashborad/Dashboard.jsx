import {jwtDecode} from 'jwt-decode';
import Sidebar from "../components/sidebar/Sidebar.jsx";
import {Outlet} from "react-router-dom";

export default function Dashboard() {
    const token = localStorage.getItem('accessToken');
    const decoded = jwtDecode(token);
    const userType = decoded['user_type'];

    return (
        <div className="flex justify-center items-center h-dvh">
            <Sidebar type={userType}/>
            <main className="basis-4/5 p-5 mb-[1%] mt-[2%]">
                <Outlet/>
            </main>
        </div>);
}
