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
    valuesRangeEnd: 20,
    categoriesN: 2,
    massRangeStart: 1,
    massRangeEnd: 10,
    annealing: {
      cycles: 100,
    },
    tabu: {
      iterations: 100,
      size: 15,
    },
    genetic: {
      mutationChance: 20,
    },
  };

  let data = [];
  let count = 0;
  let normalize = false;

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

  socket.on("stop", (res) => {
    working = false;
    console.log("event: stop");
    res = JSON.parse(res);
    console.log(res.message);
  });

  function start() {
    if (ioConnected) {
      working = true;
      socket.emit("start", { type: algorithm, settings: settings });
    }
  }
  function stop() {
    if (ioConnected) {
      socket.emit("stop", {});
    }
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
        Algorytm<br />
        <select bind:value={algorithm}>
          <option value="annealing">Wyżarzanie</option>
          <option value="tabu">Tabu</option>
          <option value="genetic">Genetyczny</option>
        </select>
      </label>

      <label class="inline">
        Normalizuj<br />
        <input type="checkbox" bind:checked={normalize} />
      </label>

      <button on:click={start}>Start</button>
      <button on:click={stop}>Stop</button>
      {#if working}
        <span transition:fade><Loader type={"clock"} /></span>
      {/if}
      {#if count > 0}
        <p>{count}</p>
      {/if}
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
