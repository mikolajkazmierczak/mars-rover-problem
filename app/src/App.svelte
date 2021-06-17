<script>
  import { io } from "socket.io-client";
  import { fade } from "svelte/transition";
  import Chart from "./Chart.svelte";
  import Loader from "./Loader.svelte";

  const socket = io("http://localhost:5000");

  let ioConnected = false;
  let working = false;

  let algorithm;

  let settings = {
    seed: 42,
    iterations: 50,
    capacity: 50,
    range: 150,
    x: 50,
    y: 50,
    samplesN: 20,
    valuesRangeStart: 1,
    valuesRangeEnd: 10,
    categoriesN: 2,
    massRangeStart: 1,
    massRangeEnd: 10,
    annealing: {
      cycles: 100,
      trials: 50,
      accepted: 1,
      probStart: 0.7,
      probEnd: 0.001,
    },
    tabu: {
      iterations: 100,
      size: 15,
    },
    genetic: {
      iterations: 100,
      mutationChance: 0.5,
    },
  };

  let data = [];
  let count = 0;
  let normalize = false;

  let filepathSettings = "settings.json";
  let filepathChart = "chart.json";

  socket.on("connect", () => {
    console.log("event: connect");
    ioConnected = true;
  });

  socket.on("disconnect", () => {
    console.log("event: disconnect");
    ioConnected = false;
  });

  socket.on("update", (res) => {
    console.log("event: update");
    res = JSON.parse(res);
    count = res.count;
    data = [res.objectives, res.masses, res.distances];
  });

  socket.on("stop", () => {
    console.log("event: stop");
    working = false;
  });

  socket.on("read", (res) => {
    console.log("event: read");
    console.log(res);
    if (res.name == "settings") settings = res.data;
    else if (res.name == "chart") {
      data = res.data;
    }
  });

  function start() {
    if (ioConnected) {
      working = true;
      socket.emit("start", {
        type: algorithm,
        settings: settings,
      });
    }
  }
  function stop() {
    if (ioConnected) {
      socket.emit("stop", {});
    }
  }

  function save(filepath, data) {
    socket.emit("save", {
      filepath: filepath,
      data: data,
    });
  }
  function read(filepath, name) {
    socket.emit("read", {
      filepath: filepath,
      name: name,
    });
  }

</script>

<main>
  <h1>Problem łazika marsjańskiego</h1>

  <div class="settings">
    <div>
      <h2>Ustawienia</h2>
      <label>
        Ziarno losowości<br />
        <input type="number" bind:value={settings.seed} />
      </label>
      <label>
        Ładowność robota<br />
        <input type="number" bind:value={settings.capacity} />
      </label>
      <label>
        Zasięg robota<br />
        <input type="number" bind:value={settings.range} />
      </label>
      <label>
        Wielkość mapy marsa<br />
        <input type="number" bind:value={settings.x} />
        <input type="number" bind:value={settings.y} />
      </label>
      <label>
        Ilość próbek<br />
        <input type="number" bind:value={settings.samplesN} />
      </label>
      <label>
        Ilość kategorii<br />
        <input type="number" bind:value={settings.categoriesN} />
      </label>
      <label>
        Zakres wartości kategorii<br />
        <input type="number" bind:value={settings.valuesRangeStart} />
        <input type="number" bind:value={settings.valuesRangeEnd} />
      </label>
      <label>
        Zakres wagi próbek<br />
        <input type="number" bind:value={settings.massRangeStart} />
        <input type="number" bind:value={settings.massRangeEnd} />
      </label>
    </div>

    <div>
      <h2>Wyżarzanie</h2>
      <label>
        Cykle<br />
        <input type="number" bind:value={settings.annealing.cycles} />
      </label>
      <label>
        Próby<br />
        <input type="number" bind:value={settings.annealing.trials} />
      </label>
      <label>
        Ilość rozwiązań<br />
        <input type="number" bind:value={settings.annealing.accepted} />
      </label>
      <label>
        Prawdopodobieństwo<br />
        <input type="number" bind:value={settings.annealing.probStart} />
        <input type="number" bind:value={settings.annealing.probEnd} />
      </label>

      <h2>Tabu</h2>
      <label>
        Iteracje<br />
        <input type="number" bind:value={settings.tabu.iterations} />
      </label>
      <label>
        Wielkość listy tabu<br />
        <input type="number" bind:value={settings.tabu.size} />
      </label>

      <h2>Genetyczny</h2>
      <label>
        Iteracje<br />
        <input type="number" bind:value={settings.genetic.iterations} />
      </label>
      <label>
        Współczynnik mutacji<br />
        <input type="number" bind:value={settings.genetic.mutationChance} />
      </label>
    </div>

    <div>
      <h2>Uruchamianie</h2>

      <p class="diode">
        Socket:
        <span class={ioConnected ? "success" : "error"}>
          &nbsp;&nbsp;&nbsp;&nbsp;
        </span>
      </p>

      <label>
        Ustawienia<br />
        <input type="text" bind:value={filepathSettings} />
      </label>
      <button
        on:click={() => {
          save(filepathSettings, settings);
        }}
        >Zapisz
      </button>
      <button
        on:click={() => {
          read(filepathSettings, "settings");
        }}
        >Wczytaj
      </button>

      <label>
        Wykres<br />
        <input type="text" bind:value={filepathChart} />
      </label>
      <button
        on:click={() => {
          save(filepathChart, data);
        }}
        >Zapisz
      </button>
      <button
        on:click={() => {
          read(filepathChart, "chart");
        }}
        >Wczytaj
      </button>

      <label>
        Algorytm<br />
        <select bind:value={algorithm}>
          <option value="annealing">Wyżarzanie</option>
          <option value="tabu">Tabu</option>
          <option value="genetic">Genetyczny</option>
        </select>
      </label>

      <button on:click={start}>Start</button>
      <button on:click={stop}>Stop</button>
      {#if working}
        <span transition:fade><Loader type={"clock"} /></span>
      {/if}
      {#if count > 0}
        <span transition:fade>{count}</span>
      {/if}

      <label class="inline">
        Normalizuj<br />
        <input type="checkbox" bind:checked={normalize} />
      </label>
    </div>
  </div>

  <Chart {data} {normalize} />
</main>

<style>
  main {
    margin: auto;
    padding-bottom: 10vh;
    width: 600px;
  }

  h1 {
    margin-top: 10vw;
  }
  h2 {
    margin: 20px 0 10px 0;
  }
  label {
    margin-bottom: 10px;
  }
  input,
  select {
    margin-top: 3px;
  }
  label.inline {
    display: flex;
    align-items: center;
  }

  button {
    margin-bottom: 20px;
  }

  .settings {
    margin-bottom: 40px;
    display: flex;
    justify-content: space-between;
  }
  .settings > div {
    width: 200px;
  }

  .diode {
    margin-bottom: 20px;
  }
  p {
    margin: 0;
    font-size: 0.8rem;
  }

</style>
