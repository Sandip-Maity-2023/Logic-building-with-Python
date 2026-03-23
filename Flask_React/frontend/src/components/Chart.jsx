import { Bar } from "react-chartjs-2";

function Charts() {

  const data = {
    labels: ["Mon","Tue","Wed","Thu","Fri"],
    datasets: [
      {
        label: "Notes Created",
        data: [2,4,3,6,5]
      }
    ]
  };

  return (
    <div className="bg-white p-6 shadow rounded-xl mt-8">
      <Bar data={data}/>
    </div>
  );
}

export default Charts;