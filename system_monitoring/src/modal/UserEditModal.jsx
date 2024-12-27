import UserForm from "../components/userForm/UserForm.jsx";

export default function UserEditModal({isOpen, onClose, data}) {
    if (!isOpen) return null;


    return (
        <div className="fixed z-50 top-0 left-0 w-screen h-screen flex justify-center items-center bg-[rgba(200,200,200,.7)]">
            <div className="flex flex-col p-6 bg-white rounded-lg shadow-lg w-3/4 h-5/6">
                <UserForm onClose={onClose} data={data}/>
            </div>
        </div>
    );
}