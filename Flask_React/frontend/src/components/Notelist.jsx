import { motion } from "framer-motion";

function NoteList({ notes, refresh, deleteNote }) {

  return (

    <div className="grid grid-cols-3 gap-5 mt-8">

      {notes.map(note => (

        <motion.div
          whileHover={{ scale: 1.05 }}
          className="bg-white shadow-lg rounded-xl p-6"
          key={note.id}
        >

          <h3 className="text-xl font-bold">{note.title}</h3>

          <p className="text-gray-600 mt-2">
            {note.content}
          </p>

          <button
            className="mt-4 bg-red-500 text-white px-3 py-1 rounded"
            onClick={()=>deleteNote(note.id)}
          >
            Delete
          </button>

        </motion.div>

      ))}

    </div>
  );
}

export default NoteList;