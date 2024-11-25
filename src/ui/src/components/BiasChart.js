import React from "react";
import { Doughnut } from "react-chartjs-2";
import { Chart as ChartJS, Tooltip, Legend, ArcElement } from "chart.js";

ChartJS.register(Tooltip, Legend, ArcElement);

const BiasChart = ({ data }) => {
    //const data = [
    //    { bias_name: "Bias A", bias_severity: 30, reasoning: "Reasoning for Bias A" }];

    // Kaaviolle tarvittavat datat
    const chartData = {
        labels: data.map(item => item.bias_name),
        datasets: [
            {
                data: data.map(item => item.bias_severity),
                backgroundColor: ['#FF5733', '#33FF57', '#3357FF', '#F1C40F'],
                hoverBackgroundColor: ['#FF6845', '#45FF68', '#4568FF', '#F1D34F']
            }
        ]
    };

    // Asetukset (tooltips sisältävät perustelun)
    const options = {
        responsive: true,
        plugins: {
            tooltip: {
                callbacks: {
                    label: function (tooltipItem) {
                        const index = tooltipItem.dataIndex;
                        return `${data[index].bias_name}: ${data[index].bias_severity} (${data[index].reasoning})`;
                    }
                }
            },
            legend: {
                position: "top"
            }
        }
    };

    return (
        <div style={{ width: "400px", height: "400px", margin: "auto" }}>
            <Doughnut data={chartData} options={options} />
        </div>
    );
};

export default BiasChart;
