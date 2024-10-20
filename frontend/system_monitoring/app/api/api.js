import axios from "axios";

const route = process.env.NEXT_PUBLIC_API_URL; // Accessible on both client and server

const url = axios.create({
    baseURL: route,
})

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