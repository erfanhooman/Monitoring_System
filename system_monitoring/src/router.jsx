import {createBrowserRouter} from "react-router-dom";
import Login from "./page/login/Login.jsx";
import Dashboard from "./dashborad/Dashboard.jsx";
import Ram from "./page/ram/Ram.jsx";
import React from "react";
import Home from "./page/home/Home.jsx";
import FS from "./page/fs/FS.jsx";
import Cpu from "./page/cpu/Cpu.jsx";
import Disk from "./page/disk/Disk.jsx";
import Network from "./page/netwrok/Network.jsx";
import Setting from "./page/setting/Setting.jsx";
import General from "./page/general/General.jsx";

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
    }
]);

export default router;