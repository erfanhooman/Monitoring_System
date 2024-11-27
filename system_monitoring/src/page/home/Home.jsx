import {useEffect, useState} from "react";
import {DashboardApi, RefreshAccessToken} from "../../api.js";

export default function Home() {
    const [data, setData] = useState([])

    const getData = () => {
        RefreshAccessToken().then(() => {
            DashboardApi()
                .then(res => {
                    setData(res.data.data);
                })
        })
    }

    useEffect(() => {
        getData();
    },[])

    return (<div>home</div>);
}