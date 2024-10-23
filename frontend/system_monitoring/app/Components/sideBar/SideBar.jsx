"use client"
import Link from "next/link";
import Home from "@/app/Components/svg/HomeSvg";
import CpuSvg from "@/app/Components/svg/CpuSvg";
import {useState} from "react";
import RamSvg from "@/app/Components/svg/RamSvg";
import FsSvg from "@/app/Components/svg/FsSvg";
import DiskSvg from "@/app/Components/svg/DiskSvg";
import NetworkSvg from "@/app/Components/svg/NetworkSvg";
import GeneralSvg from "@/app/Components/svg/GeneralSvg";
import SettingSvg from "@/app/Components/svg/SettingSvg";

export default function SideBar() {
    const address = window.location.href.split('/')
    const [urls, setUrls] = useState([

        {
            address: '/',
            name: 'Home',
            svg: <Home/>,
            isActive: address[address.length - 1] === ' ',

        },
        {
            address: '/ram',
            name: 'Ram',
            svg: <RamSvg/>,
            isActive: address[address.length - 1] === 'ram',
        },
        {
            address: '/cpu',
            name: 'Cpu',
            svg: <CpuSvg/>,
            isActive: address[address.length - 1] === 'cpu',
        },
        {
            address: '/fs',
            name: 'FS',
            svg: <FsSvg/>,
            isActive: address[address.length - 1] === 'fs',
        },
        {
            address: '/disk',
            name: 'Disk',
            svg: <DiskSvg/>,
            isActive: address[address.length - 1] === 'disk',
        },
        {
            address: '/network',
            name: 'Network',
            svg: <NetworkSvg/>,
            isActive: address[address.length - 1] === 'network',
        },
        {
            address: '/general',
            name: 'General',
            svg: <GeneralSvg/>,
            isActive: address[address.length - 1] === 'general',
        },
        {
            address: '/setting',
            name: 'Setting',
            svg: <SettingSvg/>,
            isActive: address[address.length - 1] === 'setting',
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
                            <div
                                className={`${url.isActive ? 'px-1 py-4 absolute bg-sky-700 top-0 right-0 block rounded-lg' : 'hidden'}`}></div>
                            <Link href={url.address}
                                  className={`${url.isActive ? "text-sky-700" : "text-black"} text-xl flex gap-5 font-bold`}>
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