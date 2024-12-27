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
                path: '/dashboard',
                element: <Home/>
            },
            {
                path: '/dashboard/ram',
                element: <Ram/>
            },
            {
                path: '/dashboard/cpu',
                element: <Cpu/>
            },
            {
                path: '/dashboard/fs',
                element: <FS/>
            },
            {
                path: '/dashboard/disk',
                element: <Disk/>
            },
            {
                path: '/dashboard/network',
                element: <Network/>
            },
            {
                path: '/dashboard/general',
                element: <General/>
            },
            {
                path: '/dashboard/setting',
                element: <Setting/>
            }
        ]
    },
    {
        path: '/admin',
        element: <Admin />,
        children: [
            {
                path: '/admin',
                element: <ListOfUser/>,
            },
        ]
    }
]);

export default router;