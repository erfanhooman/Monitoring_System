import {useForm} from "react-hook-form";
import {yupResolver} from "@hookform/resolvers/yup";
import * as yup from "yup";
import {useEffect} from "react";
import {AddAlert, EditUserApi, RefreshAccessToken} from "../../api.js";
import swal from "sweetalert2";

export const AddAlertYup = yup.object().shape({
    item_key: yup.string().required('item key is required.'),
    alert_level: yup.string(),
    enabled: yup.boolean(),
});

export default function AlertForm({ onClose, getData }) {
    const { handleSubmit, register, formState: { errors }} = useForm({resolver: yupResolver(AddAlertYup)})

    const onsubmit = (value) => {
        RefreshAccessToken().then(() => {
            AddAlert(value).then(() => {
                getData();
                onClose();
                swal.fire({
                    icon: "success",
                    title: "Alert Added",
                    timer: 2500,
                    position: "bottom-start",
                    toast: true,
                    timerProgressBar: true,
                    showConfirmButton: false,
                })
            })
        })
    }

    return (
        <form className='flex flex-col p-[8rem] bg-gray-200 rounded-lg gap-5 justify-center items-center h-dvh'
              onSubmit={handleSubmit(onsubmit)}>
            <div className='flex gap-2'>
                <div className="flex flex-col gap-2 w-1/2">
                    <label htmlFor="">Item key</label>
                    <input
                        {...register("item_key")}
                        className="rounded-md p-2 px-10 bg-white"
                        type="text"
                        placeholder='Username'
                    />
                    <small className="text-red-700">{errors.item_key?.message}</small>
                </div>
                <div className="flex flex-col gap-2">
                    <label htmlFor="">Is Enabled</label>
                    <select name="" id=""
                            {...register("enabled")}
                            className="rounded-md p-2 px-24 bg-white" defaultValue={true}>
                        <option value={true}>Enabled</option>
                        <option value={false}>disabled</option>
                    </select>
                    <small className="text-red-700">{errors.enabled?.message}</small>
                </div>
            </div>

            <div className='flex gap-2'>
                <div className="flex flex-col gap-2">
                    <label htmlFor="">Alert Level</label>
                    <input
                        {...register("alert_level")}
                        className="rounded-md p-2 px-10 bg-white"
                        type="text"
                    />
                    <small className="text-red-700">{errors.zabbix_server_url?.message}</small>
                </div>
            </div>

            <div className='flex gap-2'>
                <button className="px-6 py-2 bg-rose-500 hover:bg-rose-700 w-fit rounded-lg mt-2"
                        onClick={onClose}>Back
                </button>
                <button className="px-6 py-2 bg-green-500 hover:bg-green-700 w-fit rounded-lg mt-2">Add</button>
            </div>
        </form>
    )
}