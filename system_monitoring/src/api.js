import axios from "axios";

const route = import.meta.env.VITE_API_URL;

const url = axios.create({
    baseURL: route,
})

url.interceptors.response.use((response) => {
    return response;
}, (res) => {
    if(!res) {
        if (res.response.status === 401) {
            const origin = new URL(location.href).origin;

            if (origin + '/' === window.location.href)
                return;

            localStorage.removeItem("accessToken");
            localStorage.removeItem("refreshToken");

            window.location.href = origin;
        }

        return Promise.reject(res);
    }
})

// if (localStorage.getItem("token"))
//     url.defaults.headers.common['Authorization'] = "Bearer " + localStorage.getItem("tokenAccess");

export function LoginApi(value) {
    return url.post('/auth/login/', value)  // Add return here
        .then(res => {
            const accessToken = res.data.data.access;
            const refreshToken = res.data.data.refresh;

            url.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;

            localStorage.setItem("accessToken", accessToken);
            localStorage.setItem("refreshToken", refreshToken);

            return res.status;
        })
        .catch(() => {
            throw "Connection error!";
        })
}

export function RefreshAccessToken() {
    const refreshToken = localStorage.getItem('refreshToken');

    if (!refreshToken) {
        const origin = new URL(location.href).origin;

        if (origin + '/' === window.location.href)
            return;

        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");

        window.location.href = origin;
    }

    url.defaults.headers.common['Authorization'] = `Bearer ${refreshToken}`;

    return url.post('/token/refresh/', {
        refresh: refreshToken
    })
        .then(res => {
            const accessToken = res.data.access;

            url.defaults.headers.common['Authorization'] = "Bearer " + accessToken;

            localStorage.setItem('accessToken', accessToken);
        })
        .catch(error => {
            throw error;
        });
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