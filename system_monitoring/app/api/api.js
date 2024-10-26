import axios from "axios";

const route = process.env.NEXT_PUBLIC_API_URL;

const url = axios.create({
    baseURL: route,
})
//
// url.interceptors.response.use((response) => {
//     return response;
// }, (res) => {
//     if (res.response.status === 401) {
//         const origin = new URL(location.href).origin;
//
//         if (origin + '/' === window.location.href)
//             return;
//
//         localStorage.removeItem("token");
//         window.location.href = origin + '/';
//     }
//
//     return Promise.reject(res);
// })
// if (localStorage.getItem("token")) {
//
//     url.defaults.headers.common['Authorization'] = "Bearer " + localStorage.getItem("token");
//
// }

export function Login(value) {
    return url.post('/auth/login/', value)

}

export function DashboardApi() {
    return url.get('/dashboard/');
}

export function RamApi() {
    return url.get('/dashboard/ram/');
}

export function CpuApi() {
    return url.get('/dashboard/cpu');
}

export function DiskApi() {
    return url.get('/dashboard/disk/');
}

export function NetworkApi() {
    return url.get('/dashboard/network/');
}

export function GeneralApi() {
    return url.get('/dashboard/general/');
}

export function FsApi() {
    return url.get('/dashboard/fs/');
}