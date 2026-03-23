import { useState } from "react";
import { addNote } from "../Api";

function Noteform({ refresh }) {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    await addNote({ title, content });

    setTitle("");
    setContent("");
  };

  return (
    <div className="bg-white shadow-lg rounded-xl p-6 max-w-lg mx-auto mt-6">
      <h2 className="text-2xl font-bold text-gray-700 mb-4">
        Create New Note
      </h2>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">

        <input
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="border border-gray-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <textarea
          placeholder="Write your note..."
          value={content}
          onChange={(e) => setContent(e.target.value)}
          rows="4"
          className="border border-gray-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <button
          type="submit"
          className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 rounded-lg transition duration-200"
        >
          Add Note
        </button>

      </form>
    </div>
  );
}

export default Noteform;