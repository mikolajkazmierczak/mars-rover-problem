<script>
  import { io } from "socket.io-client";

  const socket = io("http://localhost:5000");

  let connected = false;

  let data = ["test"];

  socket.on("connect", () => {
    connected = true;
    console.log("connected");
  });

  socket.on("update", (res) => {
    const json = JSON.parse(res);
    console.log("update");
    data = json.data;
  });

  function start() {
    if (connected) {
      socket.emit("start", { type: "tabu" });
    }
  }

</script>

<main>
  <button on:click={start}>start</button>
  <p>{data}</p>
</main>
