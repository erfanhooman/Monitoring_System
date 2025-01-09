import axios from "axios";

const route = import.meta.env.VITE_API_URL;

const url = axios.create({
    baseURL: route
});

export function LoginApi(value) {
    return url.post('/auth/login/', value)
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
        });
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

export function SettingsApi() {
    return url.get('/auth/settings/update/');
}

export function UpdateSettingsApi(data) {
    return url.post('/auth/settings/update/', data);
}

export function FsApi() {
    return url.get('/dashboard/fs/');
}

export function ListOfUsersApi() {
    return url.get('/auth/super-admin/admin-management/');
}

export function GetUserApi(user_id) {
    return url.post('/auth/super-admin/admin-management/', {user_id});
}

export function EditUserApi(data) {
    return url.post('/auth/super-admin/admin-management/', data);
}

export function SignUpUserApi(data) {
    return url.post('/auth/super-admin/admin-signup/', data)
}

export function UserManagementApi() {
    return url.get('/auth/admin/user-management/', );
}

export function ModifyUserManagementDetailApi(user_id, activeStatus) {
    return url.post('/auth/admin/user-management/', { user_id, active: activeStatus });
}

export function AddNewSubUsers(data){
    return url.post('/auth/admin/user-signup/', data)
}

export function GetUserPermissionsApi(user_id){
    return url.post('/auth/admin/user-management/', {user_id})
}

export function ModifyPermissionsApi(data) {
    return url.post('/auth/admin/user-management/permission/', data);
}

export function GetAlert() {
    return url.get('/prefalert/');
}

export function DeleteAlert(data) {
    return url.delete('prefalert', data);
}

export function AddAlert(data) {
    return url.post('/prefalert/', data);
}

