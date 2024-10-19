"use client"
import Link from "next/link";
import Home from "@/app/components/svg/HomeSvg";
import CpuSvg from "@/app/components/svg/CpuSvg";
import {useState} from "react";

const urls = []

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
            isActive: false,
        },
        {
            address: '/cpu',
            name: 'Cpu',
            svg: <CpuSvg />,
            isActive: false,
        },
        {
            address: '/fs',
            name: 'FS',
            isActive: false,
        },
        {
            address: '/disk',
            name: 'Disk',
            isActive: false,
        },
        {
            address: '/network',
            name: 'Network',
            isActive: false,
        },
        {
            address: '/general',
            name: 'General',
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
        <aside className="basis-1/5 p-5">
            <ul className="flex flex-col gap-5">
                {
                    urls.map((url, index) => (
                        <li className={`flex w-full gap-5 items-center bg-blue-100 p-3 px-5 rounded-3xl 
                        ${url.isActive ? "bg-sky-300" : "bg-sky-100"}`}
                            onClick={() => activeUrlHandler(index)}
                            key={index}>
                            {url.svg}
                            <Link href={url.address} className="text-xl">{url.name}</Link>
                        </li>
                    ))
                }
            </ul>
        </aside>
    );
}