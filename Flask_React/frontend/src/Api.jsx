import axios from "axios"

const API=axios.create({
    baseURL:"http://127.0.0.1:5000"
});

export const getNotes=()=>API.get("/notes");
export const addNote=(note)=>API.post("/notes",note);
export const deleteNote=(id)=>API.delete(`/notes/${id}`);