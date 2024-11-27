import {useEffect, useState} from "react";
import {DashboardApi, FsApi, RefreshAccessToken} from "../../api.js";

export default function FS() {
    const [data, setData] = useState([])

    const getData = () => {
        RefreshAccessToken().then(() => {
            FsApi()
                .then(res => {
                    setData(res.data.data);
                })
        })
    }

    useEffect(() => {
        getData();
    },[])

    return(<div>FS</div>)
}