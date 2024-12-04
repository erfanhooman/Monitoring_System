"use client"

import { useState } from "react";
import Modal from "./Modal.jsx";

export function ActivationModal({ data }) {
    const [isActive, setActive] = useState(false);

    if (!data?.history?.length) {
        return null;
    }

    return (
        <>
            <button
                onClick={() => setActive(true)}
                className="bg-gray-300 px-2 py-1 rounded-xl self-center transition-all duration-300 ease-in-out hover:bg-gray-400 hover:text-white hover:scale-105"
            >
                Show more
            </button>
            <Modal isOpen={isActive} onClose={() => setActive(false)} data={data} />
        </>
    );
}
