"use client"
import {useForm} from "react-hook-form";
import * as yup from "yup";
import {yupResolver} from "@hookform/resolvers/yup";
import {Login} from "@/app/api/api";
import {log} from "next/dist/server/typescript/utils";


export const LoginYup = yup.object().shape({
    username: yup.string()
        .required("Username is required."),
    password: yup.string()
        .required("Password is required."),
});

export default function LoginForm() {
    const {register, handleSubmit, formState: {errors}} = useForm({resolver: yupResolver(LoginYup)});

    const loginHandler = (value) => {
        Login(value)
    }

    return (
        <form onSubmit={handleSubmit(loginHandler)}
              className="flex flex-col p-[8rem] bg-gray-200 rounded-lg gap-5 justify-center items-center">
            <div className="flex flex-col gap-2">
                <label htmlFor="">Username</label>
                <input
                    {...register("username")}
                    className="rounded-lg p-2 px-10"
                    type="text"
                />
                <small className="text-red-700">{errors.username?.message}</small>
            </div>
            <div className="flex flex-col gap-2">
                <label htmlFor="">password</label>
                <input
                    {...register("password")}
                    className="rounded-lg p-2 px-10"
                    type="password"
                />
                <small className="text-red-700">{errors.username?.message}</small>
            </div>

            <button className="px-6 py-2 bg-green-500 hover:bg-green-700 w-fit rounded-lg mt-2">Login</button>
        </form>
    );
}