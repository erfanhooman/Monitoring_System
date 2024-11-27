import {useEffect, useState} from "react";
import {DashboardApi, RamApi, RefreshAccessToken} from "../../api.js";

export default function Ram() {
    const [data, setData] = useState([])

    const getData = () => {
        RefreshAccessToken().then(() => {
            RamApi()
                .then(res => {
                    setData(res.data.data);
                })
        })
    }

    useEffect(() => {
        getData();
    },[])

    return (
        <div>Ram</div>
    );
}