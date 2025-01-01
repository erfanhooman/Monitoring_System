import {createBrowserRouter} from "react-router-dom";
import Login from "./page/dashborad/login/Login.jsx";
import Dashboard from "./page/dashborad/dashboard.jsx";
import Ram from "./page/dashborad/ram/Ram.jsx";
import React from "react";
import Home from "./page/dashborad/home/Home.jsx";
import FS from "./page/dashborad/fs/FS.jsx";
import Cpu from "./page/dashborad/cpu/Cpu.jsx";
import Disk from "./page/dashborad/disk/Disk.jsx";
import Network from "./page/dashborad/netwrok/Network.jsx";
import Setting from "./page/dashborad/setting/Setting.jsx";
import General from "./page/dashborad/general/General.jsx";
import ListOfUser from "./page/admin/users/ListOfUser.jsx";
import Admin from "./page/admin/Admin.jsx";
import SignUpNewUsers from "./page/admin/users/SignUpNewUsers.jsx";
import UserManagement from "./page/dashborad/usermanagement/UserManagement.jsx"


const router = createBrowserRouter([
    {
        path: '/',
        element: <Login/>
    },
    {
        path: '/dashboard',
        element: <Dashboard/>,
        children: [
            {
                path: '',
                element: <Home/>
            },
            {
                path: 'ram',
                element: <Ram/>
            },
            {
                path: 'cpu',
                element: <Cpu/>
            },
            {
                path: 'fs',
                element: <FS/>
            },
            {
                path: 'disk',
                element: <Disk/>
            },
            {
                path: 'network',
                element: <Network/>
            },
            {
                path: 'general',
                element: <General/>
            },
            {
                path: 'setting',
                element: <Setting/>
            },
            {
                path: 'users',
                element: <UserManagement/>
            }
        ]
    },
    {
        path: '/admin',
        element: <Admin/>,
        children: [
            {
                path: '',
                element: <ListOfUser/>,
            },
            {
                path: 'signup',
                element: <SignUpNewUsers/>
            }
        ]
    }
]);

export default router;