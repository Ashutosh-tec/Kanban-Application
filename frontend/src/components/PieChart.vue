<template>
  <div class="root-pie">

    
    <div class="pieText" >
      
      <h5>Please refer to the below pie chart to see a short lookup at your dashboard.</h5>
      <p>Three type of tasks are in dashboard:</p>
      <p>
        <ul>
          <li>Complete Tasks: {{ this.data[0] }}</li>
          <li>Pending Task: {{ this.data[1] }} </li>
          <li>Expired Task: {{ this.data[2] }} </li>
        </ul>
      </p>
  </div>
  <br/>
  <div id="pie-wrapper">
    <canvas id="myPieChart" width="400" height="400"></canvas>
    <label>Task Classification</label>
  </div>
  
  
</div>
</template>

<script>
import Chart from "chart.js/auto";
export default {
  name: "App",

  data() {
    return {
      label: ["Completed", "Pending", "Crossed Deadline"],
      data: [],

    };
  },
  async mounted() {
    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/summary_images/1/${localStorage.getItem(
          "user_id"
        )}`,
        {
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": localStorage.getItem("auth-token"),
          },
        }
      );
      if (res.ok) {
        const data = await res.json();
        this.data = data;
      }
    } catch (e) {
      if (localStorage.getItem("user_id") == null) {
        if (
          confirm("Looks like your account is not detected. Please log in.")
        ) {
          console.log(e);
          this.$router.push("/login");
        }
      }
      console.log(e);
    }

    const ctx = document.getElementById("myPieChart");

    const data = {
      labels: this.label,
      datasets: [
        {
          label: "Number of task",
          data: this.data,
          backgroundColor: [
            "rgb(153, 255, 204)",
            "rgb(255, 255, 153)",
            "rgb(255, 179, 179)",
          ],
          hoverOffset: 4,
        },
      ],
    };

    const myChart = new Chart(ctx, {
      type: "pie",
      data: data,
    });
    myChart;
  },
  methods: {
    async getData() {},
  },
  created() {
    this.getData();
  },
};
</script>

<style>
#pie-wrapper {
  width: 20%;
  height: 20%;
  margin-top: 4rem;
  /*max-width: 100%;*/
}
.root-pie{
  text-align: center;
}
ul {
  display: inline-block;
  margin: 0;
  padding: 0;
  /* For IE, the outcast */
  zoom:1;
  *display: inline;
}
.pieText{
  font-family: cursive;
  margin-left: 2rem;
  float: left;
  padding-top: 9rem;
}

@media screen and (max-width: 900px) {
  #pie-wrapper {
    width: 65%;
    height: 65%;
    float:none;
  }
  .pieText{
    margin-bottom: auto;
    margin-left: 0rem;
  float: none;
  padding-top: 0rem;
  }
}
</style>
