import { useEffect, useState } from "react";
import { getNotes, deleteNote } from "./Api";

import Navbar from "./components/Navbar";
import Dashboard from "./components/Dashboard";
import NoteList from "./components/Notelist";
import Noteform from "./components/Noteform";

function App() {
  const [notes, setNotes] = useState([]);

  const fetchNotes = async () => {
    const res = await getNotes();
    setNotes(res.data);
  };

  const removeNote = async (id) => {
    await deleteNote(id);
    fetchNotes();
  };

  useEffect(() => {
    fetchNotes();
  }, []);

  return (
    <div className="bg-gray-100 min-h-screen">
      <Navbar />

      <div className="p-8">
        <Dashboard notes={notes} />
        
        <NoteList notes={notes} deleteNote={removeNote} />
        <Noteform />
      </div>
    </div>
  );
}

export default App;
