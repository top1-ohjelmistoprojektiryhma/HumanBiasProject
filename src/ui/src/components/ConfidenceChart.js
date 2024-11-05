import React, { useEffect, useRef } from 'react';
import { Chart, registerables } from 'chart.js';

// Register all necessary components
Chart.register(...registerables);

const ConfidenceChart = ({ data }) => {
  const chartRef = useRef(null);
  console.log(data);
  // Extract agent roles and their corresponding scores
  const agents = Object.keys(data);

  const colors = [
    { background: "rgba(255, 99, 132, 0.2)", border: "rgba(255, 99, 132, 1)" },
    { background: "rgba(54, 162, 235, 0.2)", border: "rgba(54, 162, 235, 1)" },
    { background: "rgba(255, 159, 64, 0.2)", border: "rgba(255, 159, 64, 1)" },
    { background: "rgba(75, 192, 192, 0.2)", border: "rgba(75, 192, 192, 1)" },
    { background: "rgba(153, 102, 255, 0.2)", border: "rgba(153, 102, 255, 1)" },
    { background: "rgba(255, 206, 86, 0.2)", border: "rgba(255, 206, 86, 1)" },
  ];

  const chartData = {
    labels: Array.from({ length: Math.max(...Object.values(data).map(scores => scores.length)) }, (_, i) => i + 1),
    datasets: agents.map((agent, index) => ({
      label: agent,
      data: data[agent].map(([_, score]) => score), // Extract scores
      backgroundColor: colors[index % colors.length].background,
      borderColor: colors[index % colors.length].border,
      borderWidth: 3,
      pointBackgroundColor: colors[index % colors.length].border,
      pointBorderColor: "#fff",
      pointHoverBackgroundColor: "#fff",
      pointHoverBorderColor: colors[index % colors.length].border,
      fill: false, // Ensure the area under the line is not filled
    })),
  };

  useEffect(() => {
    if (chartRef.current) {
      chartRef.current.destroy();
    }
    chartRef.current = new Chart(document.getElementById('confidenceChart'), {
      type: 'line',
      data: chartData,
      options: {
        scales: {
          x: {
            title: {
              display: true,
              text: 'Response Number'
            }
          },
          y: {
            min: 0,
            max: 100,
            title: {
              display: true,
              text: 'Confidence Score (%)'
            },
            ticks: {
              callback: function(value) {
                return value + '%'; // Add '%' to the y-axis labels
              }
            }
          }
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: function(context) {
                const role = context.dataset.label;
                const score = context.raw;
                return [`Agent: ${role}`, `Confidence score: ${score}%`];
              }
            }
          }
        }
      }
    });

    return () => {
      if (chartRef.current) {
        chartRef.current.destroy();
      }
    };
  }, [data]);

  return <canvas id="confidenceChart" />;
};

export default ConfidenceChart;