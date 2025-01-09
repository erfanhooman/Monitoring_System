import Swal from "sweetalert2";
import swal from "sweetalert2";
import {useForm} from "react-hook-form";
import {yupResolver} from "@hookform/resolvers/yup";
import {useNavigate} from "react-router-dom";
import {LoginApi} from "../../../api.js";
import * as yup from "yup";
import {jwtDecode} from "jwt-decode";

export const LoginYup = yup.object().shape({
    username: yup.string()
        .required("Username is required."),
    password: yup.string()
        .required("Password is required."),
});


export default function Login() {
    const navigate = useNavigate();
    const {register, handleSubmit, formState: {errors}} = useForm({resolver: yupResolver(LoginYup)});

    const token = localStorage.getItem('accessToken');
    const decoded = jwtDecode(token);
    const userType = decoded['usertype'];

    const loginHandler = (value) => {
        LoginApi(value).then(res => {
            if (res.status === 401) {
                Swal.fire({
                    icon: 'error',
                    text: 'Incorrect username or password',
                    showConfirmButton: false,
                    timer: 2000,
                    position: "bottom-start",
                    timerProgressBar: true,
                    toast: true,
                });
            } else if (res.status === 500) {
                Swal.fire({
                    icon: 'error',
                    text: 'Server error',
                    showConfirmButton: false,
                    timer: 2000,
                    position: "bottom-start",
                    timerProgressBar: true,
                    toast: true,
                });
            } else {
                Swal.fire({
                    icon: 'success',
                    text: 'Login successfully',
                    showConfirmButton: false,
                    timer: 2000,
                    position: "bottom-start",
                    timerProgressBar: true,
                    toast: true,
                }).then(() => {
                    userType === 'admin' ? navigate('/admin') :navigate('/dashboard')
                });
            }
        }).catch((error) => {
            swal.fire({
                icon: 'error',
                text: error,
                showConfirmButton: false,
                timer: 2000,
                position: "bottom-start",
                timerProgressBar: true,
                toast: true,
            })
        })
    }


    return (
        <form onSubmit={handleSubmit(loginHandler)}
              className="flex flex-col p-[8rem] bg-gray-200 rounded-lg gap-5 justify-center items-center h-dvh">
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