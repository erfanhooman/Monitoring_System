import "./globals.css";
import SideBar from "@/app/components/sideBar/SideBar";

export default function RootLayout({children}) {

    return (
        <html lang="en">
            <body className="flex">
                <SideBar />
                <main className="basis-4/5 p-5">{children}</main>
            </body>
        </html>
    );
}
