import React, { useEffect, useRef } from 'react';
import { Chart, registerables } from 'chart.js';

// Register all necessary components
Chart.register(...registerables);

const ConfidenceChart = ({ data }) => {
  const chartRef = useRef(null);
  const chartInstanceRef = useRef(null); // Ref to store the Chart.js instance

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

  // Preprocess data to replace 0 values with null
  const preprocessData = (data) => {
    const processedData = {};
    for (const agent in data) {
      processedData[agent] = data[agent].map(([summary, score], i) => [summary, score === 0 ? null : score]);
    }
    return processedData;
  };

  const processedData = preprocessData(data);

  const chartData = {
    labels: Array.from({ length: Math.max(...Object.values(processedData).map(scores => scores.length)) }, (_, i) => i + 1),
    datasets: agents.map((agent, index) => ({
      label: agent,
      data: processedData[agent].map(([summary, score], i) => ({ x: i + 1, y: score, summary })), // Include summary in data points
      backgroundColor: colors[index % colors.length].background,
      borderColor: colors[index % colors.length].border,
      borderWidth: 3,
      pointBackgroundColor: colors[index % colors.length].border,
      pointBorderColor: "#fff",
      pointHoverBackgroundColor: "#fff",
      pointHoverBorderColor: colors[index % colors.length].border,
      fill: false, // Ensure the area under the line is not filled
      categoryPercentage: 0.9, // Adjusts group width on the x-axis
      barPercentage: 0.9, // Adjusts bar width on the x-axis
      skipNull: true
    })),
  };

  const splitLongText = (text, maxLength) => {
    const sanitizedText = text.replace(/\n/g, ' '); // Replace newlines with spaces
    const words = sanitizedText.split(' ');
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

  const externalTooltipHandler = (context) => {
    // Tooltip Element
    let tooltipEl = document.getElementById('chartjs-tooltip');

    // Create element on first render
    if (!tooltipEl) {
      tooltipEl = document.createElement('div');
      tooltipEl.id = 'chartjs-tooltip';
      tooltipEl.innerHTML = '<table></table>';
      document.body.appendChild(tooltipEl);
    }

    // Hide if no tooltip
    const tooltipModel = context.tooltip;
    if (tooltipModel.opacity === 0) {
      tooltipEl.style.opacity = 0;
      return;
    }

    // Set caret Position
    tooltipEl.classList.remove('above', 'below', 'no-transform');
    if (tooltipModel.yAlign) {
      tooltipEl.classList.add(tooltipModel.yAlign);
    } else {
      tooltipEl.classList.add('no-transform');
    }

    function getBody(bodyItem) {
      return bodyItem.lines;
    }

    // Set Text
    if (tooltipModel.body) {
      const titleLines = tooltipModel.title || [];
      const bodyLines = tooltipModel.body.map(getBody);

      let innerHtml = '<thead>';

      titleLines.forEach(function (title) {
        innerHtml += '<tr><th>' + title + '</th></tr>';
      });
      innerHtml += '</thead><tbody>';

      bodyLines.forEach(function (body, i) {
        const colors = tooltipModel.labelColors[i];
        const style = 'background:' + colors.backgroundColor;
        const span = '<span style="' + style + '"></span>';
        innerHtml += '<tr><td>' + span + body + '</td></tr>';
      });
      innerHtml += '</tbody>';

      const tableRoot = tooltipEl.querySelector('table');
      tableRoot.innerHTML = innerHtml;
    }

    const position = context.chart.canvas.getBoundingClientRect();
    tooltipEl.style.opacity = 1;
    tooltipEl.style.position = 'absolute';
    tooltipEl.style.left = position.left + window.pageXOffset + tooltipModel.caretX + 'px';
    tooltipEl.style.top = position.top + window.pageYOffset + tooltipModel.caretY + 'px';
    tooltipEl.style.font = tooltipModel.options.bodyFont.string;
    tooltipEl.style.padding = tooltipModel.options.padding + 'px ' + tooltipModel.options.padding + 'px';
    tooltipEl.style.pointerEvents = 'none';
    tooltipEl.style.width = '370px'; // Set the tooltip width
    tooltipEl.style.maxWidth = 'none'; // Allow the tooltip to exceed the chart boundaries
    tooltipEl.style.whiteSpace = 'pre-line'; // Allow text to wrap
    tooltipEl.style.backgroundColor = 'rgba(0, 0, 0, 1)';
    tooltipEl.style.color = 'white'; // Set text color to white for better contrast
    tooltipEl.style.border = '1px solid #ccc'; // Add a border for better visibility
    tooltipEl.style.borderRadius = '4px'; // Add border radius for rounded corners
    tooltipEl.style.boxShadow = '0px 0px 10px rgba(0, 0, 0, 0.1)'; // Add a subtle shadow for better visibility
  };

  useEffect(() => {
    if (!chartInstanceRef.current) {
      const ctx = chartRef.current.getContext('2d');

      // Create a temporary chart to calculate the minimum bar width
      const tempChart = new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: {
          responsive: true,
          plugins: {
            tooltip: {
              enabled: false,
            },
          },
        },
      });

      // Calculate the minimum bar width
      let minBarWidth = Infinity;
      tempChart.data.datasets.forEach((dataset, datasetIndex) => {
        const bars = tempChart.getDatasetMeta(datasetIndex).data;
        bars.forEach(bar => {
          if (bar.width < minBarWidth) {
            minBarWidth = bar.width;
            // edit all datasetIndexes to have the same barThickness
            // chartData.datasets[datasetIndex].barThickness = minBarWidth;
            chartData.datasets.forEach((dataset) => {
              dataset.barThickness = minBarWidth;
            });
            console.log(minBarWidth);
          }
        });
      });

      // Destroy the temporary chart
      tempChart.destroy();

      // Create the actual chart with the calculated minBarWidth
      chartInstanceRef.current = new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: {
          responsive: true,
          plugins: {
            tooltip: {
              enabled: false, // Disable the default tooltip
              external: externalTooltipHandler, // Use the external tooltip handler
              callbacks: {
                label: function(context) {
                  const role = context.dataset.label;
                  const score = context.raw.y;
                  const summary = context.raw.summary;
                  // Split the summary into multiple lines without breaking words
                  const summaryLines = splitLongText(summary, 50); // Adjust the number to control line length
                  return [`Agent: ${role}`, `Confidence score: ${score}%`, summaryLines.join(' ')].join('\n');
                }
              }
            }
          },
          scales: {
            x: {
              title: {
                display: true,
                text: 'Round Number'
              },
              ticks: {
                display: true,
              },
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
        },
      });
    } else {
      chartInstanceRef.current.data = chartData;
      chartInstanceRef.current.update();
    }

    return () => {
      if (chartInstanceRef.current) {
        chartInstanceRef.current.destroy();
        chartInstanceRef.current = null;
      }
    };
  }, [data]); // Only update when `data` changes

  return <canvas ref={chartRef} id="confidenceChart"/>;
};

export default ConfidenceChart;