"use client"
import {CpuApi} from "@/app/api/api";
import Modal from "@/app/Components/modal/Modal";
import {ActivationModal} from "@/app/Components/modal/ActivationModal";

export default async function CpuPage() {
    const request = await CpuApi();
    const data = request.data.data;

    return (
        <div className="relative grid grid-cols-3 gap-4">
            {
                data.map((item, index) => (
                    <div className="relative p-5 bg-gray-100 rounded-lg flex flex-col justify-between gap-5 shadow-sm
                                    hover:bg-gray-300 transition-colors duration-1000 items-stretch"
                                    key={index}>
                        <h1 className="hover-title">{item.name}</h1>

                        <p className="hidden-description">{item.description}</p>

                        <div className="flex items-center justify-between">
                            <p>{item.value}</p>
                            {
                                item.status
                                    &&
                                <p className={`${item.status === "normal" ? "bg-green-400" : "bg-red-700"}
                                    p-2 w-fit text-white rounded-lg`}>{item.status}</p>
                            }
                        </div>

                        <ActivationModal data={item?.history}/>
                    </div>
                ))
            }
        </div>
    );
}