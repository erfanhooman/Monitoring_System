import {useEffect, useState} from "react";
import {CpuApi, DashboardApi, RefreshAccessToken} from "../../api.js";

export default function Cpu() {
    const [data, setData] = useState([])

    const getData = () => {
        RefreshAccessToken().then(() => {
            CpuApi()
                .then(res => {
                    console.log(res)
                    setData(res.data.data);
                })
        })
    }

    useEffect(() => {
        getData();
    },[])


    return (
        <div className="relative grid grid-cols-3 gap-4 h-dvh overflow-auto">
            {
                data.map((item, index) => (
                    <div className="relative p-5 bg-gray-100 rounded-lg flex flex-col justify-between gap-5 shadow-sm
                                    hover:bg-gray-300 transition-colors duration-1000 items-stretch"
                         key={index}>
                        <h1 className="hover-title">{item.name}</h1>


                        <div className="flex items-center justify-between">
                            <p>{item.value}</p>
                            {
                                item.status
                                &&
                                <p className={`${item.status === "normal" ? "bg-green-400" : "bg-red-700"}
                                    p-2 w-fit text-white rounded-lg`}>{item.status}</p>
                            }
                        </div>

                        {/*<ActivationModal data={item?.history}/>*/}
                    </div>
                ))
            }
        </div>
    );
}