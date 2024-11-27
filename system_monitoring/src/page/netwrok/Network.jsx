import {useEffect, useState} from "react";
import {NetworkApi, RefreshAccessToken} from "../../api.js";

export default function Network() {
    const [data, setData] = useState()

    const getData = () => {
        RefreshAccessToken()
            .then(() => {
                NetworkApi()
                    .then(res => {
                        setData(res.data.data);
                    })
            })
    }

    useEffect(() => {
        getData();
    }, [])
    return (<div>network</div>);
}