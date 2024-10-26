import "./globals.css";
import LoginForm from "@/app/Components/form/LoginForm";

export default function RootLayout() {
    return (
        <html lang="en">
            <body className="flex justify-center items-center h-dvh">
                <LoginForm />
            </body>
        </html>
    );
}
