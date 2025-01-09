import {useForm} from "react-hook-form";
import {yupResolver} from "@hookform/resolvers/yup";
import * as yup from "yup";
import {useEffect} from "react";
import {EditUserApi, RefreshAccessToken} from "../../api.js";
import swal from "sweetalert2";

export const EditUserYup = yup.object().shape({
    user_id: yup.number().required(),
    username: yup.string()
        .required("Username is required."),
    active: yup.boolean(),
    zabbix_server_url: yup.string(),
    zabbix_username: yup.string(),
    zabbix_password: yup.string(),
    zabbix_host_name: yup.string()
});

export default function UserForm({ onClose, data, getData }) {
    const { handleSubmit, register, reset, formState: { errors }} = useForm({resolver: yupResolver(EditUserYup)})

    if (!data) {
        onClose();
    }

    const onsubmit = (value) => {
        value['user'] = {
            username: value.username,
        }
        RefreshAccessToken().then(() => {
            EditUserApi(value).then(() => {
                getData();
                onClose();
                swal.fire({
                    icon: "success",
                    title: "User edited",
                    timer: 2500,
                    position: "bottom-start",
                    toast: true,
                    timerProgressBar: true,
                    showConfirmButton: false,
                })
            })
        })
    }

    useEffect(() => {
        reset({
            user_id: data.id,
            username: data.user.username,
            active: data.active,
            zabbix_server_url: data.zabbix_server_url,
            zabbix_username: data.zabbix_username,
            zabbix_password: data.zabbix_password,
            zabbix_host_name: data.zabbix_host_name,
        })
    },[])

    return (
        <form className='flex flex-col p-[8rem] bg-gray-200 rounded-lg gap-5 justify-center items-center h-dvh'
              onSubmit={handleSubmit(onsubmit)}>
            <div className='flex gap-2'>
                <div className="flex flex-col gap-2 w-1/2">
                    <label htmlFor="">Username</label>
                    <input
                        {...register("username")}
                        className="rounded-md p-2 px-10 bg-white"
                        type="text"
                        placeholder='Username'
                    />
                    <small className="text-red-700">{errors.username?.message}</small>
                </div>
                <div className="flex flex-col gap-2">
                    <label htmlFor="">Is Active</label>
                    <select name="" id=""
                            {...register("active")}
                            className="rounded-md p-2 px-24 bg-white" defaultValue={true}>
                        <option value={true}>Active</option>
                        <option value={false}>Not Active</option>
                    </select>
                    <small className="text-red-700">{errors.active?.message}</small>
                </div>
            </div>

            <div className='flex gap-2'>
                <div className="flex flex-col gap-2">
                    <label htmlFor="">Zabbix Server Url</label>
                    <input
                        {...register("zabbix_server_url")}
                        className="rounded-md p-2 px-10 bg-white"
                        type="text"
                    />
                    <small className="text-red-700">{errors.zabbix_server_url?.message}</small>
                </div>
                <div className="flex flex-col gap-2">
                    <label htmlFor="">Zabbix Username</label>
                    <input
                        {...register("zabbix_username")}
                        className="rounded-md p-2 px-10 bg-white"
                        type="text"
                    />
                    <small className="text-red-700">{errors.zabbix_username?.message}</small>
                </div>
            </div>

            <div className="flex gap-2">
                <div className="flex flex-col gap-2">
                    <label htmlFor="">Zabbix Password</label>
                    <input
                        {...register("zabbix_password")}
                        className="rounded-md p-2 px-10 bg-white"
                        type="text"
                    />
                    <small className="text-red-700">{errors.zabbix_password?.message}</small>
                </div>
                <div className="flex flex-col gap-2">
                    <label htmlFor="">Zabbix Host Name</label>
                    <input
                        {...register("zabbix_host_name")}
                        className="rounded-md p-2 px-10 bg-white"
                        type="text"
                    />
                    <small className="text-red-700">{errors.zabbix_host_name?.message}</small>
                </div>
            </div>

            <div className="hidden">
                <input
                    {...register("user_id")}
                    className="rounded-md p-2 px-10 bg-white"
                    type="number"
                />
            </div>

            <div className='flex gap-2'>
                <button className="px-6 py-2 bg-rose-500 hover:bg-rose-700 w-fit rounded-lg mt-2"
                        onClick={onClose}>Back
                </button>
                <button className="px-6 py-2 bg-green-500 hover:bg-green-700 w-fit rounded-lg mt-2">Edit</button>
            </div>
        </form>
    )
}