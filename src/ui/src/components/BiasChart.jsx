import React, { useState } from "react";
import { Doughnut } from "react-chartjs-2";
import { Chart as ChartJS, Tooltip, Legend, ArcElement } from "chart.js";

ChartJS.register(Tooltip, Legend, ArcElement);

const BiasChart = ({ data }) => {
  data = JSON.parse(data);
  const biases = data.biases;
  const [hoveredIndex, setHoveredIndex] = useState(null);

  const chartData = {
    labels: biases.map((item) => item.bias_name),
    datasets: [
      {
        data: biases.map((item) => item.bias_severity),
        backgroundColor: [
          "#2F99DA",
          "#F25757",
          "#FFE156",
          "#03B5AA",
          "#87DD62",
          "#7FDEFF",
          "#FB62F6",
          "#FF6A2A",
          "#BF4ABD",
          "#00F58B",
        ],
        hoverBackgroundColor: [
          "#52AAE0",
          "#F68D8D",
          "#FFE985",
          "#03DDCF",
          "#A5E58A",
          "#ADEBFF",
          "#FC9CF9",
          "#FF9B70",
          "#CF77CE",
          "#70FFC1",
        ],
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      tooltip: {
        callbacks: {
          label: function (tooltipItem) {
            const index = tooltipItem.dataIndex;
            return ` severity: ${biases[index].bias_severity}`;
          },
        },
      },
      legend: {
        position: "top",
      },
    },
    onHover: (event, chartElement) => {
      if (chartElement.length > 0) {
        const index = chartElement[0].index;
        if (hoveredIndex !== index) {
          setHoveredIndex(index);
          console.log(biases[index]);
        }
      } else if (hoveredIndex !== null) {
        setHoveredIndex(null);
      }
    },
  };

  return (
    <div>
      <div style={{ width: "400px", margin: "auto" }}>
        <Doughnut data={chartData} options={options} />
      </div>
      <div style={{ marginTop: "20px", height: "140px" }}>
        {hoveredIndex !== null && (
          <div>
            <h3>{biases[hoveredIndex].bias_name}</h3>
            <p>{biases[hoveredIndex].reasoning}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default BiasChart;
