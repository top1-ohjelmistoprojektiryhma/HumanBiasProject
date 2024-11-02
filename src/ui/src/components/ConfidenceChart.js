import React from "react";
import { Line } from "react-chartjs-2";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const ConfidenceChart = ({ data, agents }) => {
    const labels = data[0].map((_, index) => `Score ${index + 1}`);
    const colors = [
        { background: "rgba(255, 99, 132, 0.2)", border: "rgba(255, 99, 132, 1)" },
        { background: "rgba(54, 162, 235, 0.2)", border: "rgba(54, 162, 235, 1)" },
        { background: "rgba(255, 159, 64, 0.2)", border: "rgba(255, 159, 64, 1)" },
        { background: "rgba(75, 192, 192, 0.2)", border: "rgba(75, 192, 192, 1)" },
        { background: "rgba(153, 102, 255, 0.2)", border: "rgba(153, 102, 255, 1)" },
        { background: "rgba(255, 206, 86, 0.2)", border: "rgba(255, 206, 86, 1)" },
    ];

    const chartData = {
        labels: labels,
        datasets: data.map((dataset, index) => ({
            label: `${agents[index]}`,
            data: dataset,
            backgroundColor: colors[index % colors.length].background,
            borderColor: colors[index % colors.length].border,
            borderWidth: 3,
            pointBackgroundColor: colors[index % colors.length].border,
            pointBorderColor: "#fff",
            pointHoverBackgroundColor: "#fff",
            pointHoverBorderColor: colors[index % colors.length].border,
        })),
    };

    return <Line data={chartData} />;
};

export default ConfidenceChart;
