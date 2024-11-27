import {useEffect, useState} from "react";
import {DiskApi, NetworkApi, RefreshAccessToken} from "../../api.js";

export default function Disk() {
    const [data, setData] = useState()

    const getData = () => {
        RefreshAccessToken()
            .then(() => {
                DiskApi()
                    .then(res => {
                        setData(res.data.data);
                    })
            })
    }

    useEffect(() => {
        getData();
    }, [])
    return (<div>Disk</div>);
}