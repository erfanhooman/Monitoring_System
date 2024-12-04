"use client"

import {useState} from "react";
import Modal from "./Modal.jsx";

export function ActivationModal({data}) {
    const [isActive, setActive] = useState(false);
    return (
        <>
            <button onClick={() => setActive(true)}
                    className="bg-green-700 px-4 py-2 rounded-lg self-center"
            >
                Show more
            </button>
            <Modal isOpen={isActive} onClose={()=>setActive(false)} data={data}/>
        </>
    );
}