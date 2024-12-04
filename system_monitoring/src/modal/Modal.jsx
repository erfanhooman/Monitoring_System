"use client"
import {useState} from "react";

export default function Modal({isOpen, data}) {
    const [open, setOpen] = useState(isOpen);

    return (
        open
            &&
        <div
            className="fixed top-0 left-0 w-screen h-screen flex justify-center items-center bg-[rgba(200,200,200,.7)]">
            <div className="flex flex-col p-24 bg-slate-100 rounded-lg shadow-lg w-1/2 h-1/2 justify-center items-center">
                <button onClick={() => setOpen(false)} className="px-4 py-2 bg-red-600 hover:bg-red-800 w-fit rounded-lg text-white">Close</button>
            </div>
        </div>
    );
}