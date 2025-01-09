import {Link, useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import HomeSvg from "../svg/HomeSvg.jsx";
import RamSvg from "../svg/RamSvg.jsx";
import CpuSvg from "../svg/CpuSvg.jsx";
import FsSvg from "../svg/FsSvg.jsx";
import DiskSvg from "../svg/DiskSvg.jsx";
import NetworkSvg from "../svg/NetworkSvg.jsx";
import GeneralSvg from "../svg/GeneralSvg.jsx";
import SettingSvg from "../svg/SettingSvg.jsx";
import UserManagmentSvg from "../svg/UserManagmentSvg.jsx";
import SignupNewUsersSvg from "../svg/SignupNewUsers.jsx";

export default function Sidebar({type}) {
    const address = window.location.href.split('/');
    const navigate = useNavigate();

    const [urls, setUrls] = useState(type === 'admin' ? [
        {
            address: '/admin',
            name: 'User Management',
            svg: <UserManagmentSvg/>,
            isActive: address[address.length - 1] === 'admin',
        },
        {
            address: '/admin/signup',
            name: 'Sign up new Users',
            svg: <UserManagmentSvg/>,
            isActive: address[address.length - 1] === 'signup',
        },
    ] : [
        {
            address: '/dashboard',
            name: 'Home',
            svg: <HomeSvg/>,
            isActive: address[address.length - 1] === 'dashboard',
        },
        {
            address: '/dashboard/ram',
            name: 'Ram',
            svg: <RamSvg/>,
            isActive: address[address.length - 1] === 'ram',
        },
        {
            address: '/dashboard/cpu',
            name: 'Cpu',
            svg: <CpuSvg/>,
            isActive: address[address.length - 1] === 'cpu',
        },
        {
            address: '/dashboard/fs',
            name: 'FS',
            svg: <FsSvg/>,
            isActive: address[address.length - 1] === 'fs',
        },
        {
            address: '/dashboard/disk',
            name: 'Disk',
            svg: <DiskSvg/>,
            isActive: address[address.length - 1] === 'disk',
        },
        {
            address: '/dashboard/network',
            name: 'Network',
            svg: <NetworkSvg/>,
            isActive: address[address.length - 1] === 'network',
        },
        {
            address: '/dashboard/general',
            name: 'General',
            svg: <GeneralSvg/>,
            isActive: address[address.length - 1] === 'general',
        },
        {
            address: '/dashboard/setting',
            name: 'Setting',
            svg: <SettingSvg/>,
            isActive: address[address.length - 1] === 'setting',
        },
        {
            address: '/dashboard/users',
            name: 'Users Management',
            svg: <UserManagmentSvg/>,
            inActive: address[address.length - 1] === 'user'
        }
    ]);

    const activeUserHandler = (selectedIndex) => {
        setUrls(urls.map((url, index) => ({
            ...url,
            isActive: selectedIndex === index,
        })));
    };

    return (
        <aside className="basis-1/5 p-5 shadow-lg h-dvh">
            <h1 className="mb-10 text-3xl font-bold text-gray-600">Monitoring System</h1>
            <ul className="flex flex-col gap-8">
                {
                    urls.map((url, index) => (
                        <li className={`flex w-full gap-5 items-center relative`}
                            onClick={() => activeUserHandler(index)}
                            key={index}>
                            <Link to={url.address} className='w-full'>
                                <div
                                    className={`${url.isActive ? 'px-1 py-4 absolute bg-sky-700 top-0 right-0 block rounded-lg' : 'hidden'}`}></div>
                                <div
                                    className={`${url.isActive ? "text-sky-700" : "text-black"} text-xl flex gap-5 font-bold`}>
                                    {url.svg}
                                    {url.name}
                                </div>
                            </Link>
                        </li>
                    ))
                }
            </ul>
            <button className="absolute bottom-10 left-64 px-4 py-2 bg-blue-600 hover:bg-blue-700 w-fit rounded-lg mt-2 text-white" onClick={() => navigate('/')}>Log out</button>
        </aside>
    );
}
