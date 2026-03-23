import { FaStickyNote, FaChartPie, FaCog } from "react-icons/fa";

function Sidebar() {

  return (
    <div className="h-screen w-64 bg-gray-900 text-white p-6">

      <h1 className="text-2xl font-bold mb-8">
        SmartNotes
      </h1>

      <ul className="space-y-6">

        <li className="flex items-center gap-3 cursor-pointer">
          <FaStickyNote />
          Notes
        </li>

        <li className="flex items-center gap-3 cursor-pointer">
          <FaChartPie />
          Dashboard
        </li>

        <li className="flex items-center gap-3 cursor-pointer">
          <FaCog />
          Settings
        </li>

      </ul>

    </div>
  );
}

export default Sidebar;