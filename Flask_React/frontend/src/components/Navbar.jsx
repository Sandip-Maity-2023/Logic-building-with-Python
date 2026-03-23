function Navbar() {

  return (
    <div className="bg-black text-white p-4 flex justify-between">

      <h1 className="text-xl font-bold">
        Smart Notes Dashboard
      </h1>

      <input
        placeholder="Search notes..."
        className="text-black px-3 py-1 rounded"
      />

    </div>
  );
}

export default Navbar;