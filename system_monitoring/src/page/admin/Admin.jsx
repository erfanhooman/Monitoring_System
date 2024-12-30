import {jwtDecode} from 'jwt-decode';
import Sidebar from "../../components/sidebar/Sidebar.jsx";
import {Outlet} from "react-router-dom";

export default function Admin() {
    const token = localStorage.getItem('accessToken');
    const decoded = jwtDecode(token);
    const userType = decoded['usertype'];

    return (
        <div className="flex justify-center items-center h-dvh">
            <Sidebar type={userType}/>
            <main className="basis-4/5 p-5 mb-[1%] mt-[2%]">
                <Outlet context={userType}/>
            </main>
        </div>);
}
