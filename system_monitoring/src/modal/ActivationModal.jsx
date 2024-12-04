"use client"

import {useState} from "react";
import Modal from "@/app/Components/modal/Modal";

export function ActivationModal({data}) {
    const [isActive, setActive] = useState(false);

    return (
        <>
            <button onClick={() =>setActive(true)} className="bg-blue-700 px-4 py-2 rounded-lg self-center">Show more</button>
            <Modal setModal={isActive} data={data}/>
        </>
    );
}