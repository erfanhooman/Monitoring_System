import {useEffect, useState} from "react";
import {DashboardApi, GeneralApi, RefreshAccessToken} from "../../api.js";

export default function General() {
    const [data, setData] = useState([])

    const getData = () => {
        RefreshAccessToken().then(() => {
            GeneralApi()
                .then(res => {
                    setData(res.data.data);
                })
        })
    }

    useEffect(() => {
        getData();
    },[])

    return (<div>General</div>);
}