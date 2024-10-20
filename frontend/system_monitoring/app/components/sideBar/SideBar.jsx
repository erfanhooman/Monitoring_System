"use client"
import Link from "next/link";
import Home from "@/app/components/svg/HomeSvg";
import CpuSvg from "@/app/components/svg/CpuSvg";
import {useState} from "react";
import RamSvg from "@/app/components/svg/RamSvg";
import FsSvg from "@/app/components/svg/FsSvg";
import DiskSvg from "@/app/components/svg/DiskSvg";
import NetworkSvg from "@/app/components/svg/NetworkSvg";
import GeneralSvg from "@/app/components/svg/GeneralSvg";
import SettingSvg from "@/app/components/svg/SettingSvg";

export default function SideBar() {
    const [urls, setUrls] = useState([

        {
            address: '/',
            name: 'Home',
            svg: <Home/>,
            isActive: true,

        },
        {
            address: '/ram',
            name: 'Ram',
            svg: <RamSvg />,
            isActive: false,
        },
        {
            address: '/cpu',
            name: 'Cpu',
            svg: <CpuSvg/>,
            isActive: false,
        },
        {
            address: '/fs',
            name: 'FS',
            svg: <FsSvg />,
            isActive: false,
        },
        {
            address: '/disk',
            name: 'Disk',
            svg: <DiskSvg />,
            isActive: false,
        },
        {
            address: '/network',
            name: 'Network',
            svg: <NetworkSvg />,
            isActive: false,
        },
        {
            address: '/general',
            name: 'General',
            svg: <GeneralSvg />,
            isActive: false,
        },
        {
            address: '/setting',
            name: 'Setting',
            svg: <SettingSvg />,
            isActive: false,
        }

    ]);

    const activeUrlHandler = (selectedIndex) => {
        setUrls(urls.map((url, index) => ({
            ...url,
            isActive: selectedIndex === index,
        })));
    }

    return (
        <aside className="basis-1/5 p-5 shadow-lg h-dvh">
            <h1 className="mb-10 text-3xl font-bold text-gray-600">Monitoring System</h1>
            <ul className="flex flex-col gap-8">
                {
                    urls.map((url, index) => (
                        <li className={`flex w-full gap-5 items-center relative`}
                            onClick={() => activeUrlHandler(index)}
                            key={index}>
                            <div className={`${url.isActive ? 'px-1 py-4 absolute bg-sky-700 top-0 right-0 block rounded-lg' : 'hidden'}`}></div>
                            <Link href={url.address} className={`${url.isActive ? "text-sky-700" : "text-black"} text-xl flex gap-5 font-bold`}>
                                {url.svg}
                                {url.name}
                            </Link>
                        </li>
                    ))
                }
            </ul>
        </aside>
    );
}