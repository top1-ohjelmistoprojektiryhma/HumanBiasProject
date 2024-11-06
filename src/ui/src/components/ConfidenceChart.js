import React, { useEffect, useRef } from 'react';
import { Line } from 'react-chartjs-2';
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
      data: data[agent].map(([summary, score], i) => ({ x: i + 1, y: score, summary })), // Include summary in data points
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

  const splitLongText = (text, maxLength) => {
    const words = text.split(' ');
    const lines = [];
    let currentLine = '';

    words.forEach(word => {
      if ((currentLine + word).length <= maxLength) {
        currentLine += `${word} `;
      } else {
        lines.push(currentLine.trim());
        currentLine = `${word} `;
      }
    });

    if (currentLine.length > 0) {
      lines.push(currentLine.trim());
    }

    return lines;
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
            position: 'nearest', // Adjust tooltip position to stay within the chart area
            callbacks: {
              label: function(context) {
                const role = context.dataset.label;
                const score = context.raw.y;
                const summary = context.raw.summary;
                // Split the summary into multiple lines without breaking words
                const summaryLines = splitLongText(summary, 50); // Adjust the number to control line length
                return [`Agent: ${role}`, `Confidence score: ${score}%`, '', ...summaryLines, ''];
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