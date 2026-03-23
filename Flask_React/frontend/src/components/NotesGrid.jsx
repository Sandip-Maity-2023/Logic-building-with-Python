import { motion } from "framer-motion";

function NotesGrid({ notes }) {

  return (

    <div className="grid grid-cols-3 gap-6 mt-8">

      {notes.map(note => (

        <motion.div
          key={note.id}
          whileHover={{ y: -5 }}
          className="bg-white shadow-md rounded-xl p-5"
        >

          <h2 className="text-xl font-bold">
            {note.title}
          </h2>

          <p className="text-gray-600 mt-2">
            {note.content}
          </p>

        </motion.div>

      ))}

    </div>

  );
}

export default NotesGrid;