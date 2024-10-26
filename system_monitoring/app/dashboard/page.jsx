import SideBar from "@/app/Components/sideBar/SideBar";

export default function DashboardPage() {
    return (
        <html lang="en">
        <body className="flex relative">
        <SideBar />
        <main className="basis-4/5 p-5 relative">{children}</main>
        </body>
        </html>
    );

}