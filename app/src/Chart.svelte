<script>
  import { onMount } from "svelte";
  import Chart from "chart.js/auto";

  export let data;
  export let normalize;
  let labels;

  let canvas;
  let chart;

  $: if (chart && data.length) {
    let displayData = [];
    if (normalize) {
      data.forEach((el) => {
        displayData.push(normalizeArray(el));
      });
    } else {
      displayData = data;
    }
    labels = [];
    displayData[0].forEach((_, i) => {
      labels.push(i);
    });
    for (let i = 0; i < chart.data.datasets.length; i++) {
      chart.data.labels = labels;
      chart.data.datasets[i].data = displayData[i];
    }
    chart.update();
  }

  function normalizeArray(array) {
    let max = Math.max(...array);
    let min = Math.min(...array);
    return array
      .map((el) => {
        return el - min;
      })
      .map((el) => {
        if (el == 0) return el;
        return el / (max - min);
      });
  }

  function newChart(canvas) {
    return new Chart(canvas, {
      type: "line",
      data: {
        datasets: [
          { label: "Funkcja celu", borderColor: "rgb(255, 33, 33)" },
          { label: "Masa", borderColor: "rgb(33, 255, 155)" },
          { label: "Dystans", borderColor: "rgb(33, 151, 255)" },
        ],
      },
      options: {
        fill: false,
        interaction: { intersect: false },
        radius: 0,
        tension: 0,
        plugins: { legend: { position: "bottom" } },
        color: "rgb(255,255,255)",
        scales: {
          x: {
            grid: {
              borderColor: "rgb(150,150,150)",
              color: "rgb(150,150,150)",
            },
            ticks: { color: "rgb(255,255,255)" },
          },
          y: {
            grid: {
              borderColor: "rgb(150,150,150)",
              color: "rgb(150,150,150)",
            },
            ticks: { color: "rgb(255,255,255)" },
          },
        },
      },
    });
  }

  onMount(() => {
    chart = newChart(canvas);
  });

</script>

<canvas width="100" height="50" bind:this={canvas} />
