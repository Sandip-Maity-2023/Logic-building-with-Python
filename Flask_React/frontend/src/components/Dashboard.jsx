import { FaStickyNote } from "react-icons/fa";

function Dashboard({ notes }) {

  return (
    <div className="grid grid-cols-3 gap-6">

      <div className="bg-white shadow-lg p-6 rounded-xl">
        <h2 className="text-gray-500">Total Notes</h2>
        <p className="text-3xl font-bold">{notes.length}</p>
      </div>

      <div className="bg-blue shadow-lg p-6 rounded-xl">
        <h2 className="text-gray-500">Last Activity</h2>
        <p className="text-xl">Today</p>
      </div>

      <div className="bg-blue shadow-lg p-6 rounded-xl flex items-center">
        <FaStickyNote size={40}/>
        <span className="ml-5 font-italic">Smart Notes</span>
      </div>

    </div>
  );
}

export default Dashboard;