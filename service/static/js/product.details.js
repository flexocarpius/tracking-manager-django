let initChart;

const chartColors = {
  red: "rgb(255, 99, 132)",
  orange: "rgb(255, 159, 64)",
  yellow: "rgb(255, 205, 86)",
  green: "rgb(75, 192, 192)",
  blue: "rgb(54, 162, 235)",
  purple: "rgb(153, 102, 255)",
  grey: "rgb(231,233,237)",
};

$(document).ready(() => {
  initChart = async (id) => {
    response = await fetch(`http://localhost:8000/products/details/data/${id}`);
    data = await response.json();
    const config = {
      type: "line",
      data: {
        labels: data.trackings,
        datasets: [
          {
            label: "Totals",
            backgroundColor: chartColors.red,
            borderColor: chartColors.red,
            data: data.totals,
            fill: false,
          },
        ],
      },
      options: {
        responsive: true,
        title: {
          display: true,
          text: "Totals by tracking",
        },
        tooltips: {
          mode: "label",
        },
        hover: {
          mode: "nearest",
          intersect: true,
        },
        scales: {
          xAxes: [
            {
              display: true,
              scaleLabel: {
                display: true,
                labelString: "Tracking name",
              },
            },
          ],
          yAxes: [
            {
              display: true,
              scaleLabel: {
                display: true,
                labelString: "Total",
              },
            },
          ],
        },
      },
    };

    var ctx = document.getElementById("canvas").getContext("2d");
    window.myLine = new Chart(ctx, config);
  };
});
